# CONCURRENT EXECUTION 2 ASYNC POOL - Option 4 Implementation Plan

## Overview
This document outlines the implementation plan for Option 4: Remove gevent, keep Flask, use ThreadPoolExecutor for concurrent loop execution. This approach eliminates AsyncToSync conflicts while enabling true concurrent execution.

## Problem Statement
- Current: gevent + asyncio conflicts cause "AsyncToSync" and "event loop running" errors
- Current: HTTP requests block while loops run (bad UX)
- Current: No concurrent execution possible
- Current: No progress tracking or cancellation

## Solution Architecture

### Core Design Principle
**Decouple HTTP requests from loop execution**

```
HTTP Request → Immediate Response (execution_id) → Background Thread Pool Execution
     ↓                                                         ↓
Client Polls Status                                    Store Progress/Results
```

## Implementation Details

### 1. Remove gevent Dependencies

#### A. Remove from requirements.txt
```diff
- gevent==24.2.1
- gevent-websocket==0.10.1
- flask-socketio==5.3.6  # If using gevent backend
```

#### B. Remove gevent imports and monkey patching
```python
# Remove these lines from app startup:
# import gevent.monkey
# gevent.monkey.patch_all()
```

#### C. Replace SocketIO backend (if using gevent)
```python
# Change from:
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent')

# To:
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
```

### 2. Create Async Loop Manager

#### File: `web/services/async_loop_manager.py`

```python
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from enum import Enum
import threading
import time
import uuid

class ExecutionStatus(Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class ExecutionInfo:
    execution_id: str
    user_id: int
    loop_id: int
    agent_id: Optional[int]
    action_name: Optional[str]
    status: ExecutionStatus
    created_at: float
    progress_updates: List[Dict]
    result: Optional[Dict] = None
    error: Optional[str] = None

class AsyncLoopManager:
    def __init__(self, max_workers=20):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.executions = {}  # execution_id -> ExecutionInfo
        self.user_executions = {}  # user_id -> [execution_ids]

    def start_execution(self, app, user_id, loop_id, agent_id=None, action_name=None):
        execution_id = str(uuid.uuid4())

        execution_info = ExecutionInfo(
            execution_id=execution_id,
            user_id=user_id,
            loop_id=loop_id,
            agent_id=agent_id,
            action_name=action_name,
            status=ExecutionStatus.QUEUED,
            created_at=time.time(),
            progress_updates=[]
        )

        self.executions[execution_id] = execution_info
        future = self.executor.submit(self._run_loop, execution_id, app, user_id, loop_id, agent_id, action_name)

        return execution_id

    def _run_loop(self, execution_id, app, user_id, loop_id, agent_id, action_name):
        """Run loop in isolated thread with no gevent interference"""
        with app.app_context():
            try:
                self._update_status(execution_id, ExecutionStatus.RUNNING)

                # Run loop synchronously in clean thread
                result = self._execute_loop_sync(user_id, loop_id, agent_id, action_name)

                self.executions[execution_id].result = result
                self._update_status(execution_id, ExecutionStatus.COMPLETED)

            except Exception as e:
                self.executions[execution_id].error = str(e)
                self._update_status(execution_id, ExecutionStatus.FAILED)
```

### 3. Clean Route Implementation - Direct Replacement

#### Add `web/routes/loops_public.py` - Replace Existing Endpoints
```python
from web.services.async_loop_manager import get_async_loop_manager
from flask import Response, request, jsonify, current_app, g
import json
import time

# REPLACE existing blocking endpoint run_loop with async version start_loop
@loops_bp.route('/api/loops/<int:loop_id>/start', methods=['POST'])
def start_loop(loop_id):
    """Start loop execution asynchronously"""
    try:
        user_id = get_current_user_id()
        manager = get_async_loop_manager()

        execution_id = manager.start_execution(
            app=current_app,
            user_id=user_id,
            loop_id=loop_id
        )

        return jsonify({
            "success": True,
            "execution_id": execution_id,
            "message": "Loop execution started"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@loops_bp.route('/api/executions/<execution_id>/status', methods=['GET'])
def get_execution_status(execution_id):
    """Get current status and progress"""
    try:
        manager = get_async_loop_manager()
        status = manager.get_execution_status(execution_id)

        if not status:
            return jsonify({"error": "Execution not found"}), 404

        return jsonify(status)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@loops_bp.route('/api/executions/<execution_id>/cancel', methods=['POST'])
def cancel_execution(execution_id):
    """Cancel a running execution"""
    try:
        manager = get_async_loop_manager()
        success = manager.cancel_execution(execution_id)

        if success:
            return jsonify({"success": True, "message": "Execution cancelled"})
        else:
            return jsonify({"success": False, "message": "Execution not found or already completed"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@loops_bp.route('/api/executions/<execution_id>/stream', methods=['GET'])
def stream_execution_updates(execution_id):
    """Server-Sent Events stream for real-time updates"""
    def generate():
        manager = get_async_loop_manager()
        last_update = 0

        while True:
            try:
                status = manager.get_execution_status(execution_id)
                if not status:
                    break

                # Send new progress updates
                new_updates = [u for u in status['progress_updates']
                              if u['timestamp'] > last_update]

                for update in new_updates:
                    yield f"data: {json.dumps(update)}\n\n"
                    last_update = update['timestamp']

                if status['status'] in ['completed', 'failed', 'cancelled']:
                    break

                time.sleep(1)
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e), 'type': 'error'})}\n\n"
                break

    return Response(generate(), mimetype='text/event-stream')

@loops_bp.route('/api/users/<int:user_id>/executions', methods=['GET'])
def get_user_executions(user_id):
    """Get all executions for a user"""
    try:
        limit = request.args.get('limit', 50, type=int)
        manager = get_async_loop_manager()
        executions = manager.get_user_executions(user_id, limit)

        return jsonify({
            "executions": executions,
            "total": len(executions)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

#### Update `web/routes/agents.py` - Replace Existing Endpoints
```python
from web.services.async_loop_manager import get_async_loop_manager

# REPLACE existing blocking endpoint with async version
@agents_bp.route('/api/public/agent/<int:agent_id>/action/<action_name>/', methods=['POST'])
def run_agent_action(agent_id, action_name):
    """Run agent action asynchronously - returns execution_id immediately"""
    try:
        manager = get_async_loop_manager()

        execution_id = manager.start_execution(
            app=current_app,
            user_id=None,  # Public endpoint
            loop_id=None,
            agent_id=agent_id,
            action_name=action_name,
            request_data=request.get_json() if request.is_json else None
        )

        return jsonify({
            "success": True,
            "execution_id": execution_id,
            "message": f"Agent {agent_id} action {action_name} started",
            "status_url": f"/api/executions/{execution_id}/status"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ADD authenticated agent endpoint
@agents_bp.route('/api/agents/<int:agent_id>/action/<action_name>/start', methods=['POST'])
@token_required
def start_agent_action(current_user, agent_id, action_name):
    """Start authenticated agent action asynchronously"""
    try:
        user_id = current_user.user_id if hasattr(g, 'current_user') else None
        manager = get_async_loop_manager()

        execution_id = manager.start_execution(
            app=current_app,
            user_id=user_id,
            loop_id=None,  # Will be resolved from agent
            agent_id=agent_id,
            action_name=action_name,
            request_data=request.get_json() if request.is_json else None
        )

        return jsonify({
            "success": True,
            "execution_id": execution_id,
            "message": f"Agent {agent_id} action {action_name} started"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
```

### 5. Session Management in Threaded Environment

#### **Session-Dependent Components Architecture**

Instead of duplicating session access code across components, all session-dependent services will inherit from a common abstract base class:

```python
# New file: core/services/session_dependent.py
from abc import ABC
from typing import Optional
import threading
from core.services.session import session_manager, SessionContext

class SessionDependent(ABC):
    """Abstract base class for all components that depend on session context"""

    def __init__(self):
        self._session_manager = session_manager

    @property
    def current_session(self) -> Optional[SessionContext]:
        """Get current thread's session context"""
        return self._session_manager.get_current_session()

    @property
    def user_id(self) -> Optional[int]:
        """Get current user ID from session context"""
        session = self.current_session
        return session.user_id if session else None

    @property
    def loop_id(self) -> Optional[int]:
        """Get current loop ID from session context"""
        session = self.current_session
        return session.loop_id if session else None

    @property
    def execution_id(self) -> Optional[str]:
        """Get current execution ID from session context"""
        session = self.current_session
        return session.execution_id if session else None

    @property
    def agent_id(self) -> Optional[int]:
        """Get current agent ID from session context"""
        session = self.current_session
        return session.agent_id if session else None

    @property
    def session_id(self) -> Optional[str]:
        """Get current session ID"""
        session = self.current_session
        return session.session_id if session else None

    def require_session(self) -> SessionContext:
        """Get current session or raise exception if none"""
        session = self.current_session
        if not session:
            raise RuntimeError("No active session context in current thread")
        return session

    def log_with_context(self, message: str, level: str = "info"):
        """Log message with session context"""
        context_info = f"[{self.execution_id}|U:{self.user_id}|L:{self.loop_id}]"
        full_message = f"{context_info} {message}"

        # Use appropriate logging method
        if hasattr(self, '_logger'):
            getattr(self._logger, level)(full_message)
        else:
            print(f"[{level.upper()}] {full_message}")
```

#### **Updated Session Manager**

```python
# Enhanced core/services/session.py
@dataclass
class SessionContext:
    session_id: str
    execution_id: str
    user_id: int
    loop_id: int
    agent_id: Optional[int]
    action_name: Optional[str]
    request_data: Optional[Dict]
    created_at: float
    broadcast_collection: List
    broadcast_data_json: List
    thread_id: int = None

    def __post_init__(self):
        if self.thread_id is None:
            self.thread_id = threading.get_ident()

class SessionManager:
    def __init__(self):
        self._sessions = {}  # session_id -> SessionContext
        self._thread_local = threading.local()
        self._lock = threading.RLock()

    def create_isolated_session(self, execution_id, user_id, loop_id, agent_id=None, action_name=None, request_data=None):
        """Create a new session context for isolated thread execution"""
        session_id = f"exec_{execution_id}_{int(time.time())}"

        with self._lock:
            session_context = SessionContext(
                session_id=session_id,
                execution_id=execution_id,
                user_id=user_id,
                loop_id=loop_id,
                agent_id=agent_id,
                action_name=action_name,
                request_data=request_data,
                created_at=time.time(),
                broadcast_collection=[],
                broadcast_data_json=[]
            )
            self._sessions[session_id] = session_context

        return session_id

    def set_current_session(self, session_id):
        """Set the current session for this thread"""
        self._thread_local.current_session_id = session_id

    def get_current_session(self) -> Optional[SessionContext]:
        """Get the current session context for this thread"""
        session_id = getattr(self._thread_local, 'current_session_id', None)
        if session_id and session_id in self._sessions:
            return self._sessions[session_id]
        return None

    def cleanup_session(self):
        """Clean up current thread's session"""
        session_id = getattr(self._thread_local, 'current_session_id', None)
        if session_id:
            with self._lock:
                self._sessions.pop(session_id, None)
            self._thread_local.current_session_id = None

# Global session manager instance
session_manager = SessionManager()
```

#### **Component Implementations Using SessionDependent**

```python
# core/adapters/broadcast_adapter.py
from core.services.session_dependent import SessionDependent

class BroadcastAdapter(SessionDependent):
    def __init__(self):
        super().__init__()

    def broadcast(self, data, event_type="data"):
        """Broadcast data within current session context"""
        session = self.require_session()  # Will raise if no session

        broadcast_data = BroadcastData(data, event_type)
        session.broadcast_collection.append(broadcast_data)

        # Log with context
        self.log_with_context(f"Broadcasting {event_type} data: {type(data).__name__}")

        # Emit via SocketIO
        self._emit_to_socketio(broadcast_data)

    def _emit_to_socketio(self, broadcast_data):
        """Emit broadcast data via SocketIO for real-time updates"""
        try:
            from web.web_interface import socketio
            socketio.emit('execution_update', {
                'execution_id': self.execution_id,
                'timestamp': time.time(),
                'data': broadcast_data.to_serializable(),
                'type': 'broadcast'
            }, room=f"execution_{self.execution_id}")
        except Exception as e:
            self.log_with_context(f"SocketIO broadcast failed: {e}", "warning")

# core/services/logger_service.py
from core.services.session_dependent import SessionDependent

class LoggerService(SessionDependent):
    def __init__(self, component=None):
        super().__init__()
        self.component = component or "loopai"
        self._logger = self._setup_logger()

    def info(self, message):
        """Log info message with session context"""
        if self.current_session:
            context = f"[{self.execution_id}|U:{self.user_id}|L:{self.loop_id}]"
            self._logger.info(f"{context} {message}")
        else:
            self._logger.info(message)

    def error(self, message):
        """Log error message with session context"""
        if self.current_session:
            context = f"[{self.execution_id}|U:{self.user_id}|L:{self.loop_id}]"
            self._logger.error(f"{context} {message}")
        else:
            self._logger.error(message)

# core/services/file_service.py
from core.services.session_dependent import SessionDependent

class FileSystemService(SessionDependent):
    def __init__(self):
        super().__init__()

    def get_user_directory(self):
        """Get user directory path based on session context"""
        if not self.user_id:
            raise ValueError("No user context available")
        return f"/app/var/users/{self.user_id}"

    def get_loop_directory(self):
        """Get loop directory path based on session context"""
        if not self.user_id or not self.loop_id:
            raise ValueError("No user/loop context available")
        return f"/app/var/users/{self.user_id}/loops/{self.loop_id}"

    def save_execution_artifact(self, filename, content):
        """Save file in execution-specific directory"""
        execution_dir = f"{self.get_loop_directory()}/executions/{self.execution_id}"
        os.makedirs(execution_dir, exist_ok=True)

        file_path = os.path.join(execution_dir, filename)
        with open(file_path, 'w') as f:
            f.write(content)

        self.log_with_context(f"Saved execution artifact: {filename}")
        return file_path

# core/controllers/loop_controller.py
from core.services.session_dependent import SessionDependent

class LoopController(SessionDependent):
    def __init__(self, loop_file_path, user_id=None, project_id=None, loop_id=None):
        super().__init__()
        self.loop_file_path = loop_file_path
        self._logger = LoggerService()

        # Use session context if available, fallback to parameters
        session = self.current_session
        if session:
            self.user_id = session.user_id
            self.loop_id = session.loop_id
            self.project_id = project_id  # Could be derived from session
        else:
            # Fallback for backward compatibility
            self.user_id = user_id
            self.project_id = project_id
            self.loop_id = loop_id

    def run_sync(self):
        """Synchronous loop execution for thread pool"""
        self.log_with_context(f"Starting loop execution from {self.loop_file_path}")

        # All broadcast operations automatically use session context
        broadcast_adapter.broadcast({
            "message": "Loop execution started",
            "loop_file": self.loop_file_path
        }, "execution_start")

        # Rest of implementation...
        # All logging and broadcasting automatically includes session context
```

#### **AsyncLoopManager Integration**

```python
# In web/services/async_loop_manager.py
def _run_loop(self, execution_id, app, user_id, loop_id, agent_id, action_name, request_data):
    """Run loop in isolated thread with proper session management"""
    with app.app_context():
        try:
            # Create isolated session context for this thread
            thread_session_id = session_manager.create_isolated_session(
                execution_id=execution_id,
                user_id=user_id,
                loop_id=loop_id,
                agent_id=agent_id,
                action_name=action_name,
                request_data=request_data
            )

            # Set thread-local session context
            session_manager.set_current_session(thread_session_id)

            # Update execution status
            self._update_status(execution_id, ExecutionStatus.RUNNING)

            # Now all SessionDependent components automatically have access to context
            if agent_id and action_name:
                result = self._execute_agent_action(agent_id, action_name, request_data)
            else:
                result = self._execute_loop_direct(user_id, loop_id)

            # Capture broadcast data (automatically collected in session)
            session = session_manager.get_current_session()
            final_result = {
                'execution_result': result,
                'broadcast_collection': session.broadcast_collection,
                'broadcast_collection_json': session.broadcast_data_json,
                'session_id': thread_session_id
            }

            self.executions[execution_id].result = final_result
            self._update_status(execution_id, ExecutionStatus.COMPLETED)

        except Exception as e:
            self.executions[execution_id].error = str(e)
            self._update_status(execution_id, ExecutionStatus.FAILED)
        finally:
            session_manager.cleanup_session()
```

#### **Benefits of SessionDependent Architecture**

✅ **DRY Principle**: No duplicate session access code across components
✅ **Consistent Interface**: All components access session data the same way
✅ **Easy Context Logging**: Automatic context information in all logs
✅ **Type Safety**: Optional typing for all session properties
✅ **Error Handling**: `require_session()` for components that need session
✅ **Backward Compatibility**: Graceful fallback when no session available
✅ **Thread Safety**: Session manager handles all thread-local access

#### **Migration Strategy for Existing Components**

```python
# Simple migration pattern:
# OLD:
class SomeService:
    def do_something(self):
        from core.services.session import session_manager
        session = session_manager.get_current_session()
        user_id = session.user_id if session else None
        # ... rest of logic

# NEW:
class SomeService(SessionDependent):
    def do_something(self):
        # user_id automatically available as self.user_id
        # ... rest of logic unchanged
```

### 6. Convert Async Operations to Sync

#### Replace aiohttp with requests
```python
# OLD (asyncio):
async with aiohttp.ClientSession() as session:
    response = await session.post(url, json=data)
    result = await response.json()

# NEW (sync):
import requests
response = requests.post(url, json=data)
result = response.json()
```

#### Replace async OpenAI calls
```python
# OLD (asyncio):
response = await openai.ChatCompletion.acreate(...)

# NEW (sync):
response = openai.ChatCompletion.create(...)
```

#### Update LoopController
```python
class LoopController:
    def run_sync(self):  # New sync method
        """Synchronous loop execution for thread pool"""
        # Convert all async operations to sync
        # No asyncio.run() needed

    async def run(self):  # Keep for backward compatibility
        """Legacy async method - calls run_sync"""
        return self.run_sync()
```

### 6. Vue.js Frontend Architecture Analysis

#### **Current Architecture (Well-Designed):**
The existing Vue.js frontend already follows best practices:

✅ **Proper API abstraction**: Components → `ApiService` → `LoopApi` → `apiClient`
✅ **No direct HTTP calls**: All requests go through service layer
✅ **Real-time updates**: SocketIO for progress streaming
✅ **Status management**: Visual indicators and console output
✅ **Separation of concerns**: Clean component structure

#### **Current Loop Execution Flow:**
```javascript
// LoopDetails.vue (line 141)
const response = await ApiService.runLoop(loop.value.id);

// LoopApi.js (line 18-20)
static async runLoop(loopId) {
  return apiClient.get(`/runloop/${loopId}`).then(response => response.data);
}
```

**Problem**: The `runLoop` call blocks until completion (5-30 minutes)

### 6. Frontend Changes Required

#### A. Extend LoopApi.js (Non-Breaking)
```javascript
// Add these new methods to LoopApi.js
export default class LoopApi {
  // Keep existing methods for backward compatibility
  static async runLoop(loopId) {
    return apiClient.get(`/runloop/${loopId}`).then(response => response.data);
  }

  // NEW: Async execution methods
  static async startLoop(loopId) {
    return apiClient.post(`/loops/${loopId}/start`).then(response => response.data);
  }

  static async getExecutionStatus(executionId) {
    return apiClient.get(`/executions/${executionId}/status`).then(response => response.data);
  }

  static async cancelExecution(executionId) {
    return apiClient.post(`/executions/${executionId}/cancel`).then(response => response.data);
  }

  static async getUserExecutions(userId, limit = 50) {
    return apiClient.get(`/users/${userId}/executions?limit=${limit}`).then(response => response.data);
  }

  static async getProgressUpdates(executionId, since = null) {
    const url = since ? `/executions/${executionId}/updates?since=${since}` : `/executions/${executionId}/updates`;
    return apiClient.get(url).then(response => response.data);
  }
}
```

#### B. Update ApiService.js
```javascript
// Add new methods to ApiService.js
export default class ApiService {
    // Existing methods...
    static runLoop = LoopApi.runLoop;  // Keep for backward compatibility

    // NEW: Async execution methods
    static startLoop = LoopApi.startLoop;
    static getExecutionStatus = LoopApi.getExecutionStatus;
    static cancelExecution = LoopApi.cancelExecution;
    static getUserExecutions = LoopApi.getUserExecutions;
    static getProgressUpdates = LoopApi.getProgressUpdates;
}
```

#### C. Update LoopDetails.vue (Enhanced)
```javascript
// LoopDetails.vue - Updated runLoop method
export default {
  setup(props) {
    const currentExecutionId = ref(null);
    const seenUpdates = ref(new Set());
    const isExecuting = ref(false);

    const runLoop = async () => {
      try {
        // Start execution (immediate response)
        loop.value.output += `\n[${getCurrentTimestamp()}] Starting loop...`;
        loopStatus.value = 'running';
        isExecuting.value = true;

        const startResponse = await ApiService.startLoop(loop.value.id);
        currentExecutionId.value = startResponse.execution_id;

        loop.value.output += `\n[${getCurrentTimestamp()}] Execution started - ID: ${startResponse.execution_id}`;

        // Start polling for status updates
        pollExecutionStatus(startResponse.execution_id);

      } catch (error) {
        loopStatus.value = 'error';
        isExecuting.value = false;
        loop.value.output += `\n[${getCurrentTimestamp()}] Error starting loop: ${error.message}`;
        alert('Error starting loop: ' + error.message);
      }
    };

    const pollExecutionStatus = async (executionId) => {
      try {
        const status = await ApiService.getExecutionStatus(executionId);

        // Update status indicator
        loopStatus.value = status.status;

        // Add new progress updates to console
        if (status.progress_updates) {
          status.progress_updates.forEach(update => {
            const updateId = `${update.timestamp}_${update.type}_${update.message}`;
            if (!seenUpdates.value.has(updateId)) {
              const timestamp = new Date(update.timestamp * 1000).toISOString();
              loop.value.output += `\n[${timestamp}] ${update.message}`;
              seenUpdates.value.add(updateId);
            }
          });
        }

        // Handle completion
        if (status.status === 'completed') {
          isExecuting.value = false;
          loopStatus.value = 'completed';
          loop.value.output += `\n[${getCurrentTimestamp()}] Loop completed successfully!`;

          if (status.result && status.result.broadcast_collection) {
            loop.value.output += `\n[${getCurrentTimestamp()}] Results: ${status.result.broadcast_collection.length} items processed`;
          }

        } else if (status.status === 'failed') {
          isExecuting.value = false;
          loopStatus.value = 'error';
          loop.value.output += `\n[${getCurrentTimestamp()}] Loop failed: ${status.error}`;

        } else if (status.status === 'cancelled') {
          isExecuting.value = false;
          loopStatus.value = 'not-started';
          loop.value.output += `\n[${getCurrentTimestamp()}] Loop execution was cancelled`;

        } else {
          // Continue polling for running/queued status
          setTimeout(() => pollExecutionStatus(executionId), 2000);
        }

      } catch (error) {
        isExecuting.value = false;
        loopStatus.value = 'error';
        loop.value.output += `\n[${getCurrentTimestamp()}] Error checking status: ${error.message}`;
      }
    };

    const cancelExecution = async () => {
      if (currentExecutionId.value && isExecuting.value) {
        try {
          await ApiService.cancelExecution(currentExecutionId.value);
          loop.value.output += `\n[${getCurrentTimestamp()}] Cancellation requested...`;
        } catch (error) {
          loop.value.output += `\n[${getCurrentTimestamp()}] Error requesting cancellation: ${error.message}`;
        }
      }
    };

    // Return new methods
    return {
      // ... existing returns
      runLoop,
      cancelExecution,
      isExecuting,
      currentExecutionId
    };
  }
};
```

#### D. Update LoopDetails.vue Template (Add Cancel Button)
```html
<template>
  <div class="loop-details">
    <!-- Existing elements... -->
    <span class="loop-status-icon" :class="loopStatus"></span>
    <button class="button" @click="runLoop" :disabled="isExecuting">
      {{ isExecuting ? 'Running...' : 'Run' }}
    </button>
    <button class="button" @click="cancelExecution" :disabled="!isExecuting" v-show="isExecuting">
      Cancel
    </button>
    <!-- Rest of template... -->
  </div>
</template>
```

#### E. Optional: Real-time Updates with Server-Sent Events
```javascript
// Alternative to polling - use SSE for better real-time updates
const streamExecutionUpdates = (executionId) => {
  const eventSource = new EventSource(`/api/executions/${executionId}/stream`);

  eventSource.onmessage = function(event) {
    const update = JSON.parse(event.data);
    const timestamp = new Date(update.timestamp * 1000).toISOString();

    loop.value.output += `\n[${timestamp}] ${update.message}`;

    if (update.type === 'completion') {
      loopStatus.value = 'completed';
      isExecuting.value = false;
      eventSource.close();
    } else if (update.type === 'error') {
      loopStatus.value = 'error';
      isExecuting.value = false;
      eventSource.close();
    }
  };

  eventSource.onerror = function() {
    loop.value.output += `\n[${getCurrentTimestamp()}] Connection to updates lost, falling back to polling`;
    eventSource.close();
    pollExecutionStatus(executionId);  // Fallback to polling
  };
};
```

#### F. Add Execution History Component (Optional Enhancement)
```javascript
// New component: ExecutionHistory.vue
export default {
  name: 'ExecutionHistory',
  data() {
    return {
      executions: [],
      loading: false
    }
  },

  async mounted() {
    await this.loadExecutions();
  },

  methods: {
    async loadExecutions() {
      this.loading = true;
      try {
        const response = await ApiService.getUserExecutions(this.userId);
        this.executions = response.executions;
      } catch (error) {
        console.error('Error loading executions:', error);
      } finally {
        this.loading = false;
      }
    },

    async cancelExecution(executionId) {
      try {
        await ApiService.cancelExecution(executionId);
        await this.loadExecutions();  // Refresh list
      } catch (error) {
        alert('Error cancelling execution: ' + error.message);
      }
    }
  }
};
```

### 7. Legacy Files to Remove

#### A. Files That Will Be Completely Removed
```
web/services/threaded_loop_executor.py          - Complex async isolation, replaced by async_loop_manager.py
web/services/web_loop_runner.py                 - Blocking loop execution, logic moved to async_loop_manager.py
web/services/concurrent_web_loop_runner.py      - If exists, experimental concurrency attempts
```

#### B. Functions/Code Blocks to Remove
```python
# From web/routes/loops.py - remove any blocking execution functions:
def execute_loop_synchronously(...)             # Replaced by async manager
def run_loop_blocking(...)                      # Direct blocking execution

# From web/routes/agents.py - remove blocking agent execution:
def execute_agent_action_blocking(...)          # Replaced by async manager

# From app initialization files:
import gevent.monkey                            # Remove gevent imports
gevent.monkey.patch_all()                       # Remove monkey patching
```

#### C. Dependencies to Remove from requirements.txt
```diff
- gevent==24.2.1                               # Core gevent library
- gevent-websocket==0.10.1                     # WebSocket support for gevent
- flask-socketio==5.3.6                        # If using gevent backend (keep if using threading)
```

#### D. Configuration to Update
```python
# In SocketIO initialization:
# REMOVE:
socketio = SocketIO(app, async_mode='gevent')

# REPLACE WITH:
socketio = SocketIO(app, async_mode='threading')
```

#### E. Import Statements to Remove/Update
```python
# Remove these imports from various files:
from web.services.threaded_loop_executor import execute_loop_in_isolated_thread
from web.services.web_loop_runner import run_loop_sync
from gevent import monkey
import gevent

# Replace with:
from web.services.async_loop_manager import get_async_loop_manager
```

#### F. Database/Model Changes (if any)
```python
# If there are any tables/fields specifically for blocking execution:
# - Remove execution_status fields that assume blocking behavior
# - Add execution_id tracking fields if needed
```

#### G. Frontend Files That May Become Unused
```javascript
// If there are any gevent/blocking-specific frontend utilities:
// src/utils/blockingRequestHandler.js       - If exists
// src/services/longPollingService.js        - If replaced by SSE
```

#### H. Configuration Files to Clean Up
```yaml
# docker-compose.yml - remove gevent-specific environment variables:
# - GEVENT_SUPPORT=1
# - ASYNC_MODE=gevent

# .env files - remove gevent-related configurations:
# - GEVENT_POOL_SIZE=1000
# - SOCKETIO_ASYNC_MODE=gevent
```

#### I. Test Files That Will Need Updates
```python
# Tests that assume blocking behavior:
tests/test_blocking_loop_execution.py          # Update to test async execution
tests/test_gevent_integration.py               # Remove if gevent-specific
tests/test_threaded_executor.py                # Update to test async_loop_manager

# Integration tests:
tests/integration/test_long_running_loops.py   # Update to use execution_id pattern
```

#### J. Documentation to Update/Remove
```
docs/gevent_setup.md                          # Remove gevent setup instructions
docs/blocking_execution.md                    # Update to async execution
README.md                                      # Update installation/setup instructions
DEPLOYMENT.md                                  # Remove gevent-related deployment steps
```

#### K. Helper Scripts/Utilities
```bash
scripts/start_gevent_server.sh                # Remove gevent startup scripts
scripts/gevent_worker_monitor.sh              # Remove gevent monitoring
scripts/patch_gevent.py                       # Remove gevent patching utilities
```

#### L. Potential Backup/Archive Strategy
Before deletion, consider archiving these files:
```bash
mkdir -p archive/removed_files/$(date +%Y%m%d)
mv web/services/threaded_loop_executor.py archive/removed_files/$(date +%Y%m%d)/
mv web/services/web_loop_runner.py archive/removed_files/$(date +%Y%m%d)/
# Archive other removed files...
```

### 8. Testing Concurrent Execution

#### Test Script: `test_concurrent_loops.py`
```python
import asyncio
import aiohttp
import time

async def start_loop(session, loop_id):
    """Start a loop and measure response time"""
    start_time = time.time()

    async with session.post(f'/api/loops/{loop_id}/start') as response:
        result = await response.json()
        response_time = time.time() - start_time

        print(f"Loop {loop_id} started in {response_time:.3f}s - execution_id: {result['execution_id']}")
        return result['execution_id']

async def test_concurrent_execution():
    """Test that multiple loops can start simultaneously"""
    async with aiohttp.ClientSession() as session:
        # Start 5 loops simultaneously
        tasks = [start_loop(session, i) for i in range(1, 6)]
        execution_ids = await asyncio.gather(*tasks)

        print(f"All 5 loops started simultaneously. Execution IDs: {execution_ids}")

        # Verify all are running
        for exec_id in execution_ids:
            async with session.get(f'/api/executions/{exec_id}/status') as response:
                status = await response.json()
                print(f"Execution {exec_id}: {status['status']}")

if __name__ == "__main__":
    asyncio.run(test_concurrent_execution())
```

### 9. Implementation Steps

#### Step 1: Backend Implementation
1. **Create async loop manager** - `web/services/async_loop_manager.py`
2. **Remove gevent dependencies** - Update `requirements.txt` and remove monkey patching
3. **Replace route endpoints** - Direct replacement in `loops.py` and `agents.py`
4. **Update SocketIO backend** - Change from gevent to threading mode

#### Step 2: Frontend Updates
1. **Update LoopApi.js** - Add new async execution methods
2. **Update ApiService.js** - Expose new methods
3. **Update LoopDetails.vue** - Replace blocking calls with async polling
4. **Add cancellation UI** - Cancel button and execution state management

#### Step 3: Cleanup
1. **Remove `threaded_loop_executor.py`** - Replace with simple async manager
2. **Convert async operations to sync** - Replace aiohttp with requests, etc.
3. **Remove complex isolation code** - Simplify to direct thread execution

#### Step 4: Testing
1. **Test concurrent execution** - Multiple simultaneous loops
2. **Test status tracking** - Progress updates and completion
3. **Test cancellation** - Ability to stop running loops

### 10. Benefits After Implementation

✅ **True Concurrent Execution**: Multiple loops run simultaneously in thread pool
✅ **No AsyncToSync Conflicts**: No gevent interference with asyncio
✅ **Immediate Response**: HTTP requests return instantly with execution_id
✅ **Progress Tracking**: Real-time updates via polling or SSE
✅ **Better UX**: Loading states, progress bars, cancellation
✅ **Simpler Architecture**: Less complex than current gevent+asyncio hybrid
✅ **Scalable**: ThreadPoolExecutor handles resource management
✅ **Maintainable**: Standard Python concurrency patterns

### 11. Performance Expectations

- **Request Response Time**: < 100ms (vs current 5-30 minutes)
- **Concurrent Loops**: 20+ simultaneous executions (configurable)
- **Memory Usage**: Lower (no gevent overhead)
- **CPU Usage**: Better (proper thread isolation)
- **Error Rate**: Near zero (no async conflicts)

This plan provides a clear path to eliminate all current concurrency issues while enabling true simultaneous loop execution with proper progress tracking.