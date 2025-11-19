# Cycle Management Design - Variable X-Day Cycles

**Date:** November 19, 2025
**Component:** Cycle Management System
**Status:** Design Proposal

---

## Overview

This document details the design for variable-length cycle management, allowing users to configure and run agent cycles of any duration (1-30 days) with flexible scheduling, control, and monitoring capabilities.

---

## Current Limitations

### run_all_cycles.py (Current Implementation)
```python
# Hardcoded values that need to be configurable:
daily_actions = ["READ_POSTS", "GET_WORK", "PREPARE_ACTION", ...]  # Fixed sequence
work_cycle_iterations = 3  # Fixed iteration count
days_per_reflex = 5  # Fixed reflection frequency
action_wait = 15  # Fixed wait time (seconds)
day_wait = 20  # Fixed wait time (seconds)

# Command-line only:
run(num_days=args.days)  # No pause, resume, or monitoring
```

**Problems:**
1. No way to change action sequences without editing code
2. Cannot pause or resume running cycles
3. No monitoring or progress tracking
4. No scheduling or automation
5. No preset configurations
6. No error recovery or retry logic

---

## Design Goals

### 1. Flexibility
- Configure cycle duration (1-30 days)
- Customize action sequences per cycle
- Set custom wait times
- Schedule cycles to run at specific times

### 2. Control
- Start, pause, resume, stop cycles
- Monitor real-time progress
- Intervene on errors or warnings
- Override agent-specific actions

### 3. Reusability
- Save cycle configurations as presets
- Clone and modify existing cycles
- Share presets across users (permissions allowing)
- Import/export cycle definitions

### 4. Observability
- Real-time cycle progress tracking
- Per-agent status visibility
- Execution logs and history
- Performance metrics and analytics

### 5. Reliability
- Error detection and alerting
- Automatic retry on transient failures
- Graceful degradation
- State persistence across restarts

---

## Data Models

### CycleConfiguration (Database Model)

```python
class CycleConfiguration(db.Model):
    """Configuration for an agent cycle."""
    __tablename__ = 'cycle_configurations'

    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Cycle parameters
    days = db.Column(db.Integer, nullable=False, default=1)  # 1-30
    agents = db.Column(db.JSON, nullable=False)  # ["FRBG/agent1", "FRBG/agent2"]

    # Action constellation reference
    constellation_id = db.Column(db.String(36), db.ForeignKey('action_constellations.id'))

    # Timing configuration
    action_wait_seconds = db.Column(db.Integer, default=15)
    day_wait_seconds = db.Column(db.Integer, default=20)
    reflection_frequency_days = db.Column(db.Integer, default=5)

    # Scheduling
    scheduled_start = db.Column(db.DateTime, nullable=True)  # UTC
    auto_repeat = db.Column(db.Boolean, default=False)
    repeat_interval_days = db.Column(db.Integer, nullable=True)

    # Status and metadata
    status = db.Column(db.Enum('draft', 'scheduled', 'active', 'archived'), default='draft')
    is_preset = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=False)
    tags = db.Column(db.JSON, default=[])

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    executions = db.relationship('CycleExecution', back_populates='configuration', cascade='all, delete-orphan')
    constellation = db.relationship('ActionConstellation', back_populates='cycles')
    creator = db.relationship('User', back_populates='cycle_configurations')
```

### CycleExecution (Database Model)

```python
class CycleExecution(db.Model):
    """Runtime execution state of a cycle."""
    __tablename__ = 'cycle_executions'

    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    configuration_id = db.Column(db.String(36), db.ForeignKey('cycle_configurations.id'), nullable=False)

    # Execution state
    status = db.Column(db.Enum('queued', 'running', 'paused', 'completed', 'failed', 'stopped'), default='queued')
    current_day = db.Column(db.Integer, default=1)
    total_days = db.Column(db.Integer, nullable=False)
    current_action_index = db.Column(db.Integer, default=0)
    current_action_name = db.Column(db.String(100), nullable=True)

    # Timestamps
    queued_at = db.Column(db.DateTime, default=datetime.utcnow)
    started_at = db.Column(db.DateTime, nullable=True)
    paused_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    failed_at = db.Column(db.DateTime, nullable=True)

    # Progress metrics
    total_actions = db.Column(db.Integer, default=0)
    completed_actions = db.Column(db.Integer, default=0)
    failed_actions = db.Column(db.Integer, default=0)
    skipped_actions = db.Column(db.Integer, default=0)

    # Execution details
    agent_states = db.Column(db.JSON, default={})  # {agent_id: {status, last_action, ...}}
    error_message = db.Column(db.Text, nullable=True)
    execution_metadata = db.Column(db.JSON, default={})

    # Relationships
    configuration = db.relationship('CycleConfiguration', back_populates='executions')
    logs = db.relationship('CycleExecutionLog', back_populates='execution', cascade='all, delete-orphan')
```

### CycleExecutionLog (Database Model)

```python
class CycleExecutionLog(db.Model):
    """Detailed execution log entries."""
    __tablename__ = 'cycle_execution_logs'

    id = db.Column(db.Integer, primary_key=True)
    execution_id = db.Column(db.String(36), db.ForeignKey('cycle_executions.id'), nullable=False)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    level = db.Column(db.Enum('debug', 'info', 'warning', 'error', 'critical'), default='info')

    agent_id = db.Column(db.String(100), nullable=True)
    action_name = db.Column(db.String(100), nullable=True)
    message = db.Column(db.Text, nullable=False)
    details = db.Column(db.JSON, nullable=True)

    # Relationships
    execution = db.relationship('CycleExecution', back_populates='logs')
```

---

## API Endpoints

### 1. Cycle Configuration Management

#### Create Cycle Configuration
```http
POST /api/agentlife/cycles/
Content-Type: application/json
Authorization: Bearer <token>

Request:
{
  "name": "3-Day Calculator Project Cycle",
  "description": "Full development cycle for calculator project with 3 agents",
  "days": 3,
  "agents": ["FRBG/TeacherJohn", "FRBG/zhou", "FRBG/padre"],
  "constellation_id": "standard-daily-workflow",
  "action_wait_seconds": 15,
  "day_wait_seconds": 20,
  "reflection_frequency_days": 5,
  "scheduled_start": null,
  "auto_repeat": false,
  "tags": ["development", "calculator", "collaboration"]
}

Response (201):
{
  "success": true,
  "cycle": {
    "id": "a1b2c3d4-...",
    "name": "3-Day Calculator Project Cycle",
    "status": "draft",
    "created_at": "2025-11-19T14:00:00Z",
    ...
  }
}
```

#### List Cycle Configurations
```http
GET /api/agentlife/cycles/?status=draft&tags=development&limit=20&offset=0
Authorization: Bearer <token>

Response (200):
{
  "success": true,
  "cycles": [
    {
      "id": "...",
      "name": "...",
      "status": "draft",
      "days": 3,
      "agents": [...],
      "created_at": "...",
      "last_execution": {
        "id": "...",
        "status": "completed",
        "completed_at": "..."
      }
    }
  ],
  "total": 42,
  "limit": 20,
  "offset": 0
}
```

#### Get Cycle Configuration
```http
GET /api/agentlife/cycles/<cycle_id>/
Authorization: Bearer <token>

Response (200):
{
  "success": true,
  "cycle": {
    "id": "a1b2c3d4-...",
    "name": "3-Day Calculator Project Cycle",
    "description": "...",
    "days": 3,
    "agents": ["FRBG/TeacherJohn", "FRBG/zhou", "FRBG/padre"],
    "constellation": {
      "id": "standard-daily-workflow",
      "name": "Standard Daily Workflow",
      "sequence": [...]
    },
    "timing": {
      "action_wait_seconds": 15,
      "day_wait_seconds": 20,
      "reflection_frequency_days": 5
    },
    "scheduling": {
      "scheduled_start": null,
      "auto_repeat": false,
      "repeat_interval_days": null
    },
    "status": "draft",
    "executions": [
      {
        "id": "...",
        "status": "completed",
        "started_at": "...",
        "completed_at": "...",
        "success_rate": 98.5
      }
    ],
    "created_at": "2025-11-19T14:00:00Z",
    "updated_at": "2025-11-19T14:00:00Z"
  }
}
```

#### Update Cycle Configuration
```http
PUT /api/agentlife/cycles/<cycle_id>/
Content-Type: application/json
Authorization: Bearer <token>

Request:
{
  "name": "5-Day Calculator Project Cycle",  # Updated
  "days": 5,  # Updated
  "action_wait_seconds": 20  # Updated
}

Response (200):
{
  "success": true,
  "cycle": {
    "id": "a1b2c3d4-...",
    "name": "5-Day Calculator Project Cycle",
    "days": 5,
    "action_wait_seconds": 20,
    "updated_at": "2025-11-19T15:30:00Z"
  }
}
```

#### Delete Cycle Configuration
```http
DELETE /api/agentlife/cycles/<cycle_id>/
Authorization: Bearer <token>

Response (200):
{
  "success": true,
  "message": "Cycle configuration deleted successfully"
}
```

#### Clone Cycle Configuration
```http
POST /api/agentlife/cycles/<cycle_id>/clone/
Content-Type: application/json
Authorization: Bearer <token>

Request:
{
  "name": "Calculator Cycle - Modified",
  "days": 7
}

Response (201):
{
  "success": true,
  "cycle": {
    "id": "new-uuid-...",
    "name": "Calculator Cycle - Modified",
    "days": 7,
    "cloned_from": "a1b2c3d4-...",
    "created_at": "2025-11-19T16:00:00Z"
  }
}
```

---

### 2. Cycle Execution Control

#### Start Cycle
```http
POST /api/agentlife/cycles/<cycle_id>/start/
Content-Type: application/json
Authorization: Bearer <token>

Request (optional):
{
  "start_immediately": true,
  "override_agents": ["FRBG/TeacherJohn"]  # Optional: run for subset of agents
}

Response (200):
{
  "success": true,
  "execution": {
    "id": "exec-uuid-...",
    "cycle_id": "a1b2c3d4-...",
    "status": "queued",
    "queued_at": "2025-11-19T16:00:00Z",
    "estimated_completion": "2025-11-22T16:00:00Z"
  }
}
```

#### Pause Cycle
```http
POST /api/agentlife/cycles/executions/<execution_id>/pause/
Authorization: Bearer <token>

Response (200):
{
  "success": true,
  "execution": {
    "id": "exec-uuid-...",
    "status": "paused",
    "paused_at": "2025-11-20T10:30:00Z",
    "can_resume": true
  }
}
```

#### Resume Cycle
```http
POST /api/agentlife/cycles/executions/<execution_id>/resume/
Authorization: Bearer <token>

Response (200):
{
  "success": true,
  "execution": {
    "id": "exec-uuid-...",
    "status": "running",
    "resumed_at": "2025-11-20T11:00:00Z"
  }
}
```

#### Stop Cycle
```http
POST /api/agentlife/cycles/executions/<execution_id>/stop/
Content-Type: application/json
Authorization: Bearer <token>

Request (optional):
{
  "reason": "User requested stop",
  "graceful": true  # Wait for current action to complete
}

Response (200):
{
  "success": true,
  "execution": {
    "id": "exec-uuid-...",
    "status": "stopped",
    "stopped_at": "2025-11-20T11:15:00Z",
    "reason": "User requested stop"
  }
}
```

---

### 3. Cycle Execution Status

#### Get Execution Status
```http
GET /api/agentlife/cycles/executions/<execution_id>/status/
Authorization: Bearer <token>

Response (200):
{
  "success": true,
  "execution": {
    "id": "exec-uuid-...",
    "cycle_id": "a1b2c3d4-...",
    "status": "running",
    "current_day": 2,
    "total_days": 3,
    "current_action": "DO_ACTION",
    "progress": {
      "percentage": 66.7,
      "total_actions": 45,
      "completed_actions": 30,
      "failed_actions": 0,
      "skipped_actions": 0,
      "success_rate": 100.0
    },
    "timing": {
      "started_at": "2025-11-19T16:00:00Z",
      "elapsed_seconds": 86400,
      "estimated_remaining_seconds": 43200,
      "estimated_completion": "2025-11-21T04:00:00Z"
    },
    "agents": [
      {
        "agent_id": "FRBG/TeacherJohn",
        "status": "running",
        "current_action": "DO_ACTION",
        "execution_id": "abc123",
        "last_update": "2025-11-20T10:15:00Z",
        "actions_completed": 10,
        "actions_failed": 0
      },
      {
        "agent_id": "FRBG/zhou",
        "status": "waiting",
        "current_action": null,
        "last_update": "2025-11-20T10:10:00Z",
        "actions_completed": 10,
        "actions_failed": 0
      }
    ]
  }
}
```

#### Get Execution Logs
```http
GET /api/agentlife/cycles/executions/<execution_id>/logs/?level=info&agent=FRBG/TeacherJohn&limit=100&offset=0
Authorization: Bearer <token>

Response (200):
{
  "success": true,
  "logs": [
    {
      "id": 12345,
      "timestamp": "2025-11-20T10:15:32Z",
      "level": "info",
      "agent_id": "FRBG/TeacherJohn",
      "action_name": "DO_ACTION",
      "message": "Action started successfully",
      "details": {
        "execution_id": "abc123"
      }
    }
  ],
  "total": 523,
  "limit": 100,
  "offset": 0
}
```

---

## UI Components

### 1. Cycle Configuration Form

**Location:** `AgentLifeCycles.vue`

**Features:**
- Cycle name and description
- Days slider (1-30) with visual calendar
- Agent multi-select with search
- Action constellation dropdown (presets)
- Advanced timing configuration (collapsible)
- Scheduling options (start time, repeat)
- Tags management
- Save as preset checkbox

**Validation:**
- Name required (3-100 chars)
- Days: 1-30
- At least one agent selected
- Action constellation selected
- Valid future date for scheduled_start

**UX Patterns:**
- Inline validation with error messages
- Autosave draft to localStorage
- "Save & Start" vs "Save Draft" buttons
- Preview mode showing execution timeline

---

### 2. Cycle List View

**Location:** `AgentLifeCycles.vue`

**Features:**
- Filterable list (status, tags, date range)
- Search by name/description
- Sort by date, name, status
- Card or table view toggle
- Bulk actions (delete, clone)
- Quick start button
- Status badges

**Card View:**
```
┌─────────────────────────────────────────┐
│ 3-Day Calculator Cycle        [Running] │
│ Started 2h ago                          │
│ ━━━━━━━━━━━━━━━━━━━━░░░ 65%           │
│ Day 2/3 • DO_ACTION                    │
│ 3 agents • 30/45 actions               │
│ [Pause] [Stop] [Monitor →]             │
└─────────────────────────────────────────┘
```

---

### 3. Cycle Control Panel

**Location:** `AgentLifeCycles.vue` (when cycle selected)

**Features:**
- Large start/pause/resume/stop buttons
- Current status indicator
- Progress bar with percentage
- Current day and action display
- Agent status summary
- Quick actions menu (clone, edit, delete)
- Navigation to monitor view

**State Transitions:**
```
Draft → Queued → Running ⇄ Paused → Completed/Failed/Stopped
          ↓
       Scheduled
```

---

## Business Logic

### CycleManager Service

```python
class CycleManager:
    """Service for managing cycle lifecycles."""

    def __init__(self, db, city_api, socket_io):
        self.db = db
        self.city_api = city_api
        self.socket_io = socket_io
        self.orchestrator = ActionOrchestrator(city_api, socket_io)

    def create_cycle(self, user_id, config_data):
        """Create a new cycle configuration."""
        # Validate configuration
        self._validate_cycle_config(config_data)

        # Create database record
        cycle = CycleConfiguration(
            created_by=user_id,
            **config_data
        )
        self.db.session.add(cycle)
        self.db.session.commit()

        return cycle

    def start_cycle(self, cycle_id, user_id):
        """Start a cycle execution."""
        # Load configuration
        cycle = CycleConfiguration.query.get_or_404(cycle_id)

        # Check permissions
        if cycle.created_by != user_id:
            raise PermissionError("Not authorized")

        # Create execution record
        execution = CycleExecution(
            configuration_id=cycle_id,
            total_days=cycle.days,
            status='queued'
        )
        self.db.session.add(execution)
        self.db.session.commit()

        # Queue execution (async)
        self._queue_execution(execution.id)

        return execution

    def pause_cycle(self, execution_id, user_id):
        """Pause a running cycle."""
        execution = CycleExecution.query.get_or_404(execution_id)

        # Verify ownership
        if execution.configuration.created_by != user_id:
            raise PermissionError("Not authorized")

        # Check if pauseable
        if execution.status != 'running':
            raise ValueError(f"Cannot pause execution in status: {execution.status}")

        # Update status
        execution.status = 'paused'
        execution.paused_at = datetime.utcnow()
        self.db.session.commit()

        # Signal orchestrator to pause
        self.orchestrator.pause_execution(execution_id)

        # Broadcast status update
        self.socket_io.emit('cycle_status_update', {
            'execution_id': execution_id,
            'status': 'paused'
        }, room=f'cycle_{execution_id}')

        return execution

    def _queue_execution(self, execution_id):
        """Queue cycle execution for background processing."""
        # Option 1: Use Celery for background execution
        from tasks import run_cycle_execution
        run_cycle_execution.delay(execution_id)

        # Option 2: Use threading for simpler setup
        # import threading
        # thread = threading.Thread(target=self.orchestrator.execute_cycle, args=(execution_id,))
        # thread.daemon = True
        # thread.start()

    def _validate_cycle_config(self, config_data):
        """Validate cycle configuration data."""
        if not config_data.get('name'):
            raise ValueError("Cycle name required")

        days = config_data.get('days', 1)
        if not (1 <= days <= 30):
            raise ValueError("Days must be between 1 and 30")

        agents = config_data.get('agents', [])
        if not agents:
            raise ValueError("At least one agent required")

        # Validate agents exist
        for agent_id in agents:
            if not self.city_api.agent_exists(agent_id):
                raise ValueError(f"Agent not found: {agent_id}")
```

---

## Error Handling

### Error Types

1. **Validation Errors** (400)
   - Invalid configuration parameters
   - Missing required fields
   - Invalid agent IDs

2. **Authorization Errors** (403)
   - User doesn't own cycle
   - Insufficient permissions

3. **State Errors** (409)
   - Cannot pause non-running cycle
   - Cycle already running
   - Conflicting operations

4. **Execution Errors** (500)
   - Agent API failures
   - Database errors
   - Orchestration failures

### Error Response Format

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid cycle configuration",
    "details": {
      "days": "Must be between 1 and 30",
      "agents": "At least one agent required"
    }
  }
}
```

---

## Performance Considerations

1. **Database Indexing**
   - Index on `status` for filtering
   - Index on `created_by` for user queries
   - Index on `created_at` for sorting
   - Composite index on `(status, created_by)`

2. **Query Optimization**
   - Eager load relationships when needed
   - Use pagination for large result sets
   - Cache constellation definitions

3. **Real-Time Updates**
   - Use Redis pub/sub for status broadcasts
   - Debounce frequent updates (max 1/sec per execution)
   - Use Socket.IO rooms for targeted updates

4. **Background Execution**
   - Use Celery for long-running executions
   - Store execution state in Redis for recovery
   - Implement heartbeat mechanism for monitoring

---

## Security Considerations

1. **Authorization**
   - Users can only manage their own cycles
   - Admin role can view/manage all cycles
   - Public cycles are read-only for non-owners

2. **Input Validation**
   - Sanitize all user inputs
   - Validate agent IDs against whitelist
   - Limit max cycles per user

3. **Rate Limiting**
   - Max 10 concurrent executions per user
   - Max 100 cycle configurations per user
   - Throttle API requests (100/minute)

4. **Audit Logging**
   - Log all cycle start/stop operations
   - Log configuration changes
   - Track execution failures

---

## Testing Strategy

### Unit Tests
- Cycle configuration validation
- State transition logic
- Permission checks
- Error handling

### Integration Tests
- Full cycle execution flow
- Pause/resume functionality
- Multi-agent coordination
- Database persistence

### End-to-End Tests
- UI → API → Execution → UI feedback loop
- Real agent execution (staging environment)
- Error recovery scenarios
- Performance under load

---

## Migration Plan

### Phase 1: Parallel Operation
- Keep existing CLI workflow functional
- Add GUI alongside CLI
- Users can choose either method

### Phase 2: Feature Parity
- GUI matches all CLI capabilities
- Add migration tools (import CLI configs)
- Document transition guide

### Phase 3: GUI Primary
- Recommend GUI for new users
- Mark CLI as deprecated
- Maintain CLI for automation/scripts

### Phase 4: CLI Retirement
- Remove CLI after 6-month deprecation period
- Archive documentation
- Provide legacy support if needed

---

## Next Steps

1. Review and approve this design
2. Create database migrations
3. Implement backend services and API
4. Build frontend components
5. Integration testing
6. User acceptance testing
7. Deployment and monitoring

---

**Document Version:** 1.0
**Last Updated:** 2025-11-19
**Related:** [00_OVERVIEW.md](./00_OVERVIEW.md), [02_ACTION_CONSTELLATION_DESIGN.md](./02_ACTION_CONSTELLATION_DESIGN.md)
