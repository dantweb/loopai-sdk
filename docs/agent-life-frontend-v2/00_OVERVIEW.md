# Agent Life Frontend v2 - Architecture Overview

**Date:** November 19, 2025
**Version:** 2.0
**Status:** Design Proposal

---

## Executive Summary

This document presents a comprehensive architectural design for integrating variable-length cycle management into the LoopAI Agent Life interface. The proposal extends the current chat-focused interface into a full-featured agent orchestration control panel with real-time monitoring, flexible cycle configuration, and action constellation management.

### Current State

**AgentLife.vue** (Current Implementation):
- Simple chat interface for inter-agent messaging
- Message filtering by from/to address
- Socket.IO real-time message notifications
- 60-second polling for message updates
- Basic send message functionality

**agentlife.py** (Current Backend):
- `/api/agentlife/fetch_new_messages/<user_id>/` - Fetch messages via agent_post service
- `/api/agentlife/send_message/` - Send messages to agents
- `/api/agentlife/assign_task/` - Assign tasks to agents

**run_all_cycles.py** (Current Orchestration):
- Command-line only operation
- Hardcoded daily cycle: READ_POSTS → GET_WORK → (PREPARE/DO/VALIDATE_ACTION) x3 → VALIDATE_WORK
- Fixed 15-second waits between actions
- Fixed 20-second waits between days
- No configuration or control interface
- No monitoring or progress tracking

### Proposed Enhancements

**1. Variable X-Day Cycle Management**
- Configure and run cycles of any duration (1-30 days)
- Pause, resume, stop running cycles
- Schedule cycles to start at specific times
- Save and load cycle presets
- Historical cycle tracking and analysis

**2. Action Constellation Configuration**
- Visual action flow designer
- Drag-and-drop action sequencing
- Configure which actions run and in what order
- Set iteration counts for action loops
- Configure wait times between actions and days
- Create custom action presets

**3. Enhanced Frontend (AgentLife.vue)**
- Multi-tab interface:
  - **Chat** - Current messaging functionality
  - **Cycles** - Cycle management and control
  - **Monitor** - Real-time cycle monitoring
  - **Analytics** - Cycle history and performance
- Real-time cycle progress tracking
- Agent status dashboard
- Action execution logs
- Performance metrics and charts

**4. Enhanced Backend (agentlife.py)**
- Cycle management API endpoints (CRUD)
- Cycle execution control (start/pause/resume/stop)
- Real-time status streaming via Socket.IO
- Action constellation configuration storage
- Cycle history and analytics endpoints
- Agent status aggregation

**5. Real-Time Monitoring**
- Live cycle progress visualization
- Per-agent action status
- Execution logs streaming
- Error and warning alerts
- Performance metrics (completion time, success rate)
- Resource utilization tracking

---

## Architecture Principles

### 1. Living Agent Philosophy
Agents are autonomous professionals who make context-aware decisions. The interface should:
- Support agent autonomy, not micromanagement
- Provide visibility without interference
- Enable collaboration and team coordination
- Respect agent intelligence and decision-making

### 2. Progressive Enhancement
Build on existing functionality:
- Preserve current chat interface (backward compatible)
- Add new features without breaking existing workflows
- Migrate gradually from CLI to GUI management
- Maintain API compatibility

### 3. Real-Time First
All monitoring and control should be real-time:
- Socket.IO for live updates
- WebSocket streaming for logs
- No polling for critical updates
- Optimistic UI updates with rollback

### 4. Configuration Over Code
Move hardcoded values to configuration:
- Action sequences configurable via UI
- Wait times adjustable without code changes
- Cycle presets saveable and shareable
- Per-agent action overrides

### 5. Observability & Analytics
Comprehensive visibility into agent operations:
- Detailed execution logs
- Performance metrics and trends
- Error tracking and alerting
- Historical analysis and reporting

---

## System Components

### Frontend Components

**1. AgentLifeChat.vue** (Refactored)
- Extracted chat functionality from current AgentLife.vue
- Maintains all current chat features
- Reusable component for messaging

**2. AgentLifeCycles.vue** (New)
- Cycle configuration interface
- Action constellation designer
- Preset management
- Cycle execution controls

**3. AgentLifeMonitor.vue** (New)
- Real-time cycle progress tracking
- Agent status dashboard
- Action execution logs
- Error and warning display

**4. AgentLifeAnalytics.vue** (New)
- Cycle history browser
- Performance metrics and charts
- Agent productivity analysis
- Collaboration insights

**5. AgentLife.vue** (Refactored)
- Main container with tab navigation
- State management coordination
- Socket.IO connection management
- Shared data and event bus

### Backend Components

**1. CycleManager** (New Service)
- Cycle lifecycle management (CRUD)
- Execution orchestration
- State persistence
- Configuration validation

**2. ActionOrchestrator** (New Service)
- Action sequence execution
- Parallel vs sequential execution
- Wait time management
- Retry and error handling

**3. StatusAggregator** (New Service)
- Real-time agent status collection
- Execution progress tracking
- Performance metrics calculation
- Socket.IO event broadcasting

**4. CycleRepository** (New Model)
- Database persistence for cycles
- Action constellation storage
- Execution history tracking
- Analytics data aggregation

**5. agentlife.py** (Enhanced Routes)
- New cycle management endpoints
- Enhanced monitoring endpoints
- Configuration endpoints
- Analytics endpoints

---

## Data Models

### CycleConfiguration
```python
{
    "id": "uuid",
    "name": "Daily Development Cycle",
    "description": "Standard daily development workflow",
    "created_by": "user_id",
    "days": 3,
    "agents": ["FRBG/TeacherJohn", "FRBG/zhou", "FRBG/padre"],
    "action_constellation": {
        "morning_actions": ["READ_POSTS", "GET_WORK"],
        "work_cycle": {
            "actions": ["PREPARE_ACTION", "DO_ACTION", "VALIDATE_ACTION"],
            "iterations": 3
        },
        "evening_actions": ["VALIDATE_WORK"],
        "reflection": {
            "action": "REFLEX",
            "frequency_days": 5
        }
    },
    "timing": {
        "action_wait_seconds": 15,
        "day_wait_seconds": 20,
        "start_at": "2025-11-20T09:00:00Z"
    },
    "status": "draft|scheduled|running|paused|completed|failed",
    "created_at": "2025-11-19T14:00:00Z",
    "updated_at": "2025-11-19T14:00:00Z"
}
```

### CycleExecution
```python
{
    "id": "uuid",
    "cycle_configuration_id": "uuid",
    "status": "running|paused|completed|failed",
    "current_day": 2,
    "total_days": 3,
    "current_action": "DO_ACTION",
    "started_at": "2025-11-20T09:00:00Z",
    "completed_at": null,
    "agents": [
        {
            "agent_id": "FRBG/TeacherJohn",
            "current_action": "DO_ACTION",
            "execution_id": "abc123",
            "status": "running|completed|failed",
            "last_update": "2025-11-20T10:15:00Z"
        }
    ],
    "progress": {
        "total_actions": 45,  # 3 days * 15 actions/day
        "completed_actions": 30,
        "failed_actions": 0,
        "success_rate": 100.0
    },
    "logs": [...]
}
```

### ActionConstellation
```python
{
    "id": "uuid",
    "name": "Standard Daily Workflow",
    "description": "Default agent daily cycle",
    "sequence": [
        {
            "action": "READ_POSTS",
            "wait_after": 15,
            "parallel": false
        },
        {
            "action": "GET_WORK",
            "wait_after": 15,
            "parallel": false
        },
        {
            "loop": {
                "actions": [
                    {"action": "PREPARE_ACTION", "wait_after": 15},
                    {"action": "DO_ACTION", "wait_after": 15},
                    {"action": "VALIDATE_ACTION", "wait_after": 15}
                ],
                "iterations": 3
            }
        },
        {
            "action": "VALIDATE_WORK",
            "wait_after": 0,
            "parallel": false
        }
    ],
    "is_preset": true,
    "created_by": "system|user_id",
    "created_at": "2025-11-19T14:00:00Z"
}
```

---

## Technology Stack

### Frontend
- **Vue 3** - Core framework (existing)
- **Naive UI** - Component library (existing)
- **Socket.IO Client** - Real-time communication (existing)
- **Vue Router** - Navigation (existing)
- **Pinia** - State management (new)
- **Chart.js / D3.js** - Data visualization (new)
- **VueFlow** - Action constellation designer (new)

### Backend
- **Flask** - Web framework (existing)
- **Flask-SocketIO** - Real-time events (existing)
- **SQLAlchemy** - ORM (existing)
- **PostgreSQL** - Database (existing)
- **Redis** - Caching and pub/sub (existing)
- **Celery** - Background task queue (optional, new)

---

## API Design Overview

### Cycle Management
```
POST   /api/agentlife/cycles/                   # Create cycle
GET    /api/agentlife/cycles/                   # List cycles
GET    /api/agentlife/cycles/<id>/              # Get cycle details
PUT    /api/agentlife/cycles/<id>/              # Update cycle
DELETE /api/agentlife/cycles/<id>/              # Delete cycle

POST   /api/agentlife/cycles/<id>/start/        # Start cycle
POST   /api/agentlife/cycles/<id>/pause/        # Pause cycle
POST   /api/agentlife/cycles/<id>/resume/       # Resume cycle
POST   /api/agentlife/cycles/<id>/stop/         # Stop cycle
GET    /api/agentlife/cycles/<id>/status/       # Get execution status
```

### Action Constellations
```
POST   /api/agentlife/constellations/           # Create constellation
GET    /api/agentlife/constellations/           # List constellations
GET    /api/agentlife/constellations/<id>/      # Get details
PUT    /api/agentlife/constellations/<id>/      # Update
DELETE /api/agentlife/constellations/<id>/      # Delete
```

### Monitoring & Analytics
```
GET    /api/agentlife/agents/status/            # All agent statuses
GET    /api/agentlife/executions/<id>/logs/     # Execution logs
GET    /api/agentlife/cycles/<id>/analytics/    # Cycle analytics
GET    /api/agentlife/dashboard/                # Dashboard summary
```

### Socket.IO Events
```
# Client → Server
subscribe_cycle_updates     # Subscribe to cycle updates
unsubscribe_cycle_updates   # Unsubscribe

# Server → Client
cycle_status_update         # Cycle status changed
agent_action_started        # Agent started action
agent_action_completed      # Agent completed action
agent_action_failed         # Agent action failed
cycle_progress_update       # Overall progress update
execution_log_entry         # New log entry
```

---

## Implementation Phases

### Phase 1: Foundation (Week 1)
- Create new database models (CycleConfiguration, CycleExecution, ActionConstellation)
- Implement CycleManager service
- Create basic cycle CRUD API endpoints
- Refactor AgentLife.vue to multi-tab structure

### Phase 2: Cycle Control (Week 2)
- Implement ActionOrchestrator service
- Create cycle execution control endpoints (start/pause/resume/stop)
- Build AgentLifeCycles.vue component
- Implement basic action constellation designer

### Phase 3: Monitoring (Week 3)
- Implement StatusAggregator service
- Create monitoring API endpoints
- Build AgentLifeMonitor.vue component
- Implement real-time Socket.IO updates

### Phase 4: Analytics (Week 4)
- Implement analytics data collection
- Create analytics API endpoints
- Build AgentLifeAnalytics.vue component
- Add charts and visualizations

### Phase 5: Polish & Testing (Week 5)
- UI/UX refinements
- Integration testing
- Performance optimization
- Documentation and user guides

---

## Benefits

### For Users
- **Visibility** - Clear view of agent activities and progress
- **Control** - Easy cycle configuration and management
- **Flexibility** - Customize workflows without code changes
- **Insights** - Performance analytics and productivity metrics

### For Agents
- **Autonomy** - Work within structured but flexible cycles
- **Transparency** - Clear expectations and feedback
- **Collaboration** - Better coordination with team members
- **Growth** - Reflection and continuous improvement

### For Development Team
- **Maintainability** - Configuration over hardcoded values
- **Observability** - Comprehensive logging and monitoring
- **Scalability** - Support for more agents and complex workflows
- **Testability** - Better testing and debugging tools

---

## Next Steps

1. Review this design proposal with stakeholders
2. Prioritize features and create detailed specifications
3. Begin Phase 1 implementation
4. Establish feedback loops with users during development
5. Plan migration strategy from CLI to GUI workflows

---

## Related Documents

- [01_CYCLE_MANAGEMENT_DESIGN.md](./01_CYCLE_MANAGEMENT_DESIGN.md) - Variable X-day cycle running
- [02_ACTION_CONSTELLATION_DESIGN.md](./02_ACTION_CONSTELLATION_DESIGN.md) - Action configuration system
- [03_FRONTEND_INTEGRATION.md](./03_FRONTEND_INTEGRATION.md) - Vue.js frontend implementation
- [04_BACKEND_INTEGRATION.md](./04_BACKEND_INTEGRATION.md) - Flask backend implementation
- [05_REALTIME_MONITORING.md](./05_REALTIME_MONITORING.md) - Live monitoring features
- [06_IMPLEMENTATION_ROADMAP.md](./06_IMPLEMENTATION_ROADMAP.md) - Implementation plan

---

**Document Version:** 1.0
**Last Updated:** 2025-11-19
**Authors:** Claude Code Development Team
