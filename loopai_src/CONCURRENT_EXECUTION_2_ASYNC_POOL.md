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

### 3. Update Existing Route Files

#### Update `web/routes/loops.py` - Add New Endpoints
```python
from web.services.async_loop_manager import get_async_loop_manager
from flask import Response
import json
import time

# Keep existing endpoints for backward compatibility
@loops_bp.route('/runloop/<int:loop_id>', methods=['GET'])  # Existing blocking endpoint
def run_loop_blocking(loop_id):
    """Legacy blocking endpoint - keep for backward compatibility"""
    # Current implementation stays the same
    pass

# NEW: Add async execution endpoints
@loops_bp.route('/api/loops/<int:loop_id>/start', methods=['POST'])
def start_loop_async(loop_id):
    """Start loop execution asynchronously"""
    try:
        user_id = get_current_user_id()  # Use your existing auth method
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

#### Update `web/routes/agents.py` - Add New Endpoints
```python
from web.services.async_loop_manager import get_async_loop_manager

# Keep existing endpoints for backward compatibility
@agents_bp.route('/api/public/agent/<int:agent_id>/action/<action_name>/', methods=['POST'])
def run_agent_action_blocking(agent_id, action_name):
    """Legacy blocking endpoint - keep for backward compatibility"""
    # Current implementation stays the same for now
    # Will be updated to use async manager in later phases
    pass

# NEW: Add async execution endpoints for agents
@agents_bp.route('/api/agents/<int:agent_id>/action/<action_name>/start', methods=['POST'])
def start_agent_action_async(agent_id, action_name):
    """Start agent action asynchronously"""
    try:
        # For authenticated agent actions
        user_id = get_current_user_id() if hasattr(g, 'current_user') else None
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

@agents_bp.route('/api/public/agent/<int:agent_id>/action/<action_name>/start', methods=['POST'])
def start_public_agent_action_async(agent_id, action_name):
    """Start public agent action asynchronously"""
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
            "message": f"Public agent {agent_id} action {action_name} started"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
```

### 4. Gradually Update Existing Endpoints

#### Phase 1: Keep Both Old and New
```python
# In web/routes/loops.py - during migration phase

@loops_bp.route('/runloop/<int:loop_id>', methods=['GET'])
def run_loop_legacy(loop_id):
    """Legacy blocking endpoint - will be deprecated"""
    # Current blocking implementation
    # Add deprecation warning in response headers
    response = make_response(current_blocking_implementation())
    response.headers['X-Deprecated'] = 'Use /api/loops/{loop_id}/start for async execution'
    return response

@loops_bp.route('/api/loops/run', methods=['POST'])
def run_loop_api(loop_id):
    """Updated to use async execution"""
    # Gradually migrate this to use async manager
    # Can return execution_id instead of blocking
    manager = get_async_loop_manager()
    execution_id = manager.start_execution(...)

    return jsonify({
        "success": True,
        "execution_id": execution_id,
        "message": "Loop execution started. Check status at /api/executions/{execution_id}/status"
    })
```

#### Phase 2: Update Frontend Routes
```python
# After frontend is updated, modify existing endpoints to be async
@loops_bp.route('/runloop/<int:loop_id>', methods=['GET'])
def run_loop_updated(loop_id):
    """Updated to return execution_id instead of blocking"""
    manager = get_async_loop_manager()
    execution_id = manager.start_execution(...)

    return jsonify({
        "success": True,
        "execution_id": execution_id,
        "redirect_to_status": f"/api/executions/{execution_id}/status"
    })
```

### 5. Convert Async Operations to Sync

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

### 7. Code to Drop

#### A. Remove gevent-specific code
- `web/services/threaded_loop_executor.py` - Replace with simpler async manager
- Any gevent monkey patching in app initialization
- gevent-specific SocketIO configuration

#### B. Remove complex async isolation code
```python
# Remove all this complex event loop handling:
def run_async_in_executor():
    with app.app_context():
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            # ... complex isolation logic
```

#### C. Simplify to direct thread execution
```python
# Replace with simple:
def run_loop_in_thread(execution_id, loop_id):
    with app.app_context():
        result = execute_loop_synchronously(loop_id)
        store_result(execution_id, result)
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

### 9. Migration Steps

#### Phase 1: Preparation
1. Create async loop manager
2. Add new API endpoints
3. Test new endpoints alongside old ones

#### Phase 2: Frontend Update
1. Update frontend to use new async endpoints
2. Add progress UI components
3. Test concurrent execution from UI

#### Phase 3: Remove gevent
1. Remove gevent from requirements.txt
2. Remove gevent-specific code
3. Update SocketIO to use threading backend
4. Remove old blocking endpoints

#### Phase 4: Cleanup
1. Remove complex async isolation code
2. Simplify loop execution to pure sync in threads
3. Remove unused files and functions

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