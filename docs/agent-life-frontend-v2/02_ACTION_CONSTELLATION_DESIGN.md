# Action Constellation Design - Configurable Action Sequences

**Date:** November 19, 2025
**Component:** Action Configuration System
**Status:** Design Proposal

---

## Overview

Action Constellations define the sequence, timing, and configuration of actions that agents execute during cycles. This system replaces hardcoded action sequences with flexible, visual, user-configurable workflows.

---

## Current Limitations

### Hardcoded in run_all_cycles.py
```python
# Fixed morning actions
morning_actions = ["READ_POSTS", "GET_WORK"]

# Fixed work cycle with hardcoded iterations
work_cycle_actions = ["PREPARE_ACTION", "DO_ACTION", "VALIDATE_ACTION"]
work_cycle_iterations = 3

# Fixed evening actions
evening_actions = ["VALIDATE_WORK"]

# Fixed daily sequence
daily_actions = morning_actions + (work_cycle_actions * work_cycle_iterations) + evening_actions
```

**Problems:**
- Cannot change action order without code modification
- No way to skip or add actions
- Fixed iteration counts for loops
- No conditional execution
- No parallel action support
- No per-agent customization

---

## Design Goals

### 1. Visual Configuration
- Drag-and-drop action sequencing
- Visual flow editor (flowchart-style)
- Clear representation of loops and conditions
- Real-time validation

### 2. Flexibility
- Add, remove, reorder actions
- Configure loop iterations
- Set custom wait times per action
- Define conditional branches
- Support parallel execution

### 3. Reusability
- Save constellations as presets
- System presets (standard workflows)
- User presets (custom workflows)
- Share presets across teams

### 4. Agent Customization
- Per-agent action overrides
- Agent-specific parameters
- Selective agent inclusion/exclusion
- Role-based action filtering

---

## Data Models

### ActionConstellation (Database Model)

```python
class ActionConstellation(db.Model):
    """Defines a sequence of actions for agent cycles."""
    __tablename__ = 'action_constellations'

    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # NULL = system preset

    # Action sequence definition (JSON structure defined below)
    sequence = db.Column(db.JSON, nullable=False)

    # Metadata
    is_preset = db.Column(db.Boolean, default=False)  # System or user preset
    is_public = db.Column(db.Boolean, default=False)  # Shareable
    tags = db.Column(db.JSON, default=[])
    version = db.Column(db.Integer, default=1)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    cycles = db.relationship('CycleConfiguration', back_populates='constellation')
    creator = db.relationship('User', back_populates='action_constellations')
```

### Sequence JSON Structure

```json
{
  "version": "1.0",
  "actions": [
    {
      "id": "step1",
      "type": "action",
      "action_name": "READ_POSTS",
      "display_name": "Read Posts",
      "description": "Process incoming messages and create tasks",
      "wait_after_seconds": 15,
      "parallel": false,
      "required": true,
      "retry": {
        "enabled": true,
        "max_attempts": 3,
        "backoff_seconds": 30
      }
    },
    {
      "id": "step2",
      "type": "action",
      "action_name": "GET_WORK",
      "display_name": "Get Work",
      "description": "Select and plan task execution",
      "wait_after_seconds": 15,
      "parallel": false,
      "required": true
    },
    {
      "id": "step3",
      "type": "loop",
      "display_name": "Work Cycle",
      "description": "Execute actions iteratively",
      "iterations": 3,
      "actions": [
        {
          "id": "step3a",
          "type": "action",
          "action_name": "PREPARE_ACTION",
          "display_name": "Prepare Action",
          "wait_after_seconds": 15,
          "parallel": false
        },
        {
          "id": "step3b",
          "type": "action",
          "action_name": "DO_ACTION",
          "display_name": "Do Action",
          "wait_after_seconds": 15,
          "parallel": false
        },
        {
          "id": "step3c",
          "type": "action",
          "action_name": "VALIDATE_ACTION",
          "display_name": "Validate Action",
          "wait_after_seconds": 15,
          "parallel": false
        }
      ]
    },
    {
      "id": "step4",
      "type": "action",
      "action_name": "VALIDATE_WORK",
      "display_name": "Validate Work",
      "description": "Final validation of day's work",
      "wait_after_seconds": 0,
      "parallel": false,
      "required": true
    }
  ]
}
```

---

## System Presets

### 1. Standard Daily Workflow
**ID:** `standard-daily-workflow`
**Actions:** READ_POSTS → GET_WORK → (PREPARE/DO/VALIDATE_ACTION) x3 → VALIDATE_WORK
**Use Case:** Default agent daily cycle with iterative action execution

### 2. Simplified Single-Action Workflow
**ID:** `simple-single-action`
**Actions:** READ_POSTS → GET_WORK → PREPARE_ACTION → DO_ACTION → VALIDATE_WORK
**Use Case:** Single action execution per day (no iterations)

### 3. Intensive Multi-Action Workflow
**ID:** `intensive-multi-action`
**Actions:** READ_POSTS → GET_WORK → (PREPARE/DO/VALIDATE_ACTION) x5 → VALIDATE_WORK
**Use Case:** High-productivity agents executing 5 actions per day

### 4. Communication-Focused Workflow
**ID:** `communication-focused`
**Actions:** READ_POSTS → VALIDATE_WORK
**Use Case:** Agents focused on message processing without task execution

### 5. Reflection-Only Workflow
**ID:** `reflection-only`
**Actions:** REFLEX
**Use Case:** Periodic self-reflection without task execution

---

## API Endpoints

### 1. Constellation Management

#### Create Constellation
```http
POST /api/agentlife/constellations/
Content-Type: application/json
Authorization: Bearer <token>

Request:
{
  "name": "Custom Development Workflow",
  "description": "Tailored workflow for backend development tasks",
  "sequence": {
    "version": "1.0",
    "actions": [...]
  },
  "is_preset": true,
  "is_public": false,
  "tags": ["development", "backend"]
}

Response (201):
{
  "success": true,
  "constellation": {
    "id": "const-uuid-...",
    "name": "Custom Development Workflow",
    "version": 1,
    "created_at": "2025-11-19T14:00:00Z"
  }
}
```

#### List Constellations
```http
GET /api/agentlife/constellations/?is_preset=true&tags=development
Authorization: Bearer <token>

Response (200):
{
  "success": true,
  "constellations": [
    {
      "id": "standard-daily-workflow",
      "name": "Standard Daily Workflow",
      "description": "Default agent daily cycle",
      "is_preset": true,
      "is_public": true,
      "created_by": null,  # System preset
      "action_count": 7,
      "loop_count": 1,
      "tags": ["default", "standard"]
    }
  ],
  "total": 5
}
```

#### Get Constellation
```http
GET /api/agentlife/constellations/<constellation_id>/
Authorization: Bearer <token>

Response (200):
{
  "success": true,
  "constellation": {
    "id": "const-uuid-...",
    "name": "Custom Development Workflow",
    "description": "...",
    "sequence": {
      "version": "1.0",
      "actions": [...]
    },
    "metadata": {
      "total_actions": 7,
      "loop_count": 1,
      "estimated_duration_minutes": 120,
      "required_actions": ["READ_POSTS", "GET_WORK", "VALIDATE_WORK"]
    },
    "usage": {
      "cycles_using": 12,
      "last_used": "2025-11-19T10:00:00Z"
    },
    "created_at": "2025-11-15T14:00:00Z",
    "updated_at": "2025-11-19T14:00:00Z"
  }
}
```

#### Validate Constellation
```http
POST /api/agentlife/constellations/validate/
Content-Type: application/json
Authorization: Bearer <token>

Request:
{
  "sequence": {
    "version": "1.0",
    "actions": [...]
  }
}

Response (200):
{
  "success": true,
  "valid": true,
  "validation": {
    "total_actions": 7,
    "has_loops": true,
    "estimated_duration_minutes": 120,
    "warnings": [
      "No retry configuration for critical action READ_POSTS"
    ],
    "errors": []
  }
}

# Invalid example
Response (200):
{
  "success": true,
  "valid": false,
  "validation": {
    "errors": [
      "Missing required action: READ_POSTS",
      "Loop at step3 has 0 iterations",
      "Invalid action_name: UNKNOWN_ACTION"
    ],
    "warnings": []
  }
}
```

---

## UI Components

### 1. Constellation Selector

**Location:** `AgentLifeCycles.vue` (Cycle configuration form)

**Features:**
- Dropdown with constellation presets
- Preview of selected constellation
- "Create New" / "Edit" buttons
- Quick stats (actions, loops, duration)

**UI Mockup:**
```
┌────────────────────────────────────────────┐
│ Action Constellation                    [+] │
│ ┌────────────────────────────────────────┐ │
│ │ Standard Daily Workflow              ▼ │ │
│ └────────────────────────────────────────┘ │
│                                             │
│ 📊 7 actions • 1 loop • ~120 min          │
│ [View Details] [Edit Copy]                 │
└────────────────────────────────────────────┘
```

---

### 2. Constellation Designer (Visual Editor)

**Location:** `AgentLifeConstellationDesigner.vue` (New component)

**Features:**
- Drag-and-drop action nodes
- Connect actions with flow lines
- Loop container visualization
- Action configuration panel
- Real-time validation
- Preview execution flow
- Save as preset

**Visual Editor Layout:**
```
┌─────────────────────────────────────────────────────────┐
│ Constellation Designer - "Custom Workflow"          [✓] │
├──────────────────┬──────────────────────────────────────┤
│ Actions Palette  │ Canvas                               │
│                  │                                      │
│ 📥 READ_POSTS    │     ┌───────────────┐              │
│ 📋 GET_WORK      │     │  READ_POSTS   │              │
│ 🔧 PREPARE       │     └───────┬───────┘              │
│ ⚙️  DO_ACTION    │             │                       │
│ ✅ VALIDATE      │     ┌───────▼───────┐              │
│ 🤔 REFLEX        │     │   GET_WORK    │              │
│                  │     └───────┬───────┘              │
│ Structures:      │             │                       │
│ 🔄 Loop          │     ┌───────▼───────────────┐      │
│ ❓ Condition     │     │  Loop (3x)            │      │
│ ⚡ Parallel      │     │  - PREPARE_ACTION     │      │
│                  │     │  - DO_ACTION          │      │
│ [Save Preset]    │     │  - VALIDATE_ACTION    │      │
│                  │     └───────┬───────────────┘      │
│                  │             │                       │
│                  │     ┌───────▼───────┐              │
│                  │     │ VALIDATE_WORK │              │
│                  │     └───────────────┘              │
├──────────────────┴──────────────────────────────────────┤
│ Properties Panel (Selected: Loop)                      │
│ Iterations: [3] ───────────────────────────────       │
│ Break on error: [✓] Continue on error: [ ]            │
│ Wait after loop: [15] seconds                          │
└─────────────────────────────────────────────────────────┘
```

**Interaction:**
- Drag actions from palette to canvas
- Click action to configure properties
- Drag connections between actions
- Double-click to delete action/connection
- Right-click for context menu

---

### 3. Constellation List View

**Location:** `AgentLifeConstellations.vue` (New tab in AgentLife.vue)

**Features:**
- List all user constellations
- System preset library
- Search and filter
- Usage statistics
- Quick actions (edit, clone, delete)

**Card View:**
```
┌─────────────────────────────────────────┐
│ Standard Daily Workflow      [System]   │
│ Default agent daily cycle                │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━       │
│ 7 actions • 1 loop • ~120 min           │
│ Used in 42 cycles                        │
│ [Use] [Clone] [View]                     │
└─────────────────────────────────────────┘
```

---

## Business Logic

### ConstellationManager Service

```python
class ConstellationManager:
    """Service for managing action constellations."""

    def __init__(self, db):
        self.db = db
        self.validator = ConstellationValidator()

    def create_constellation(self, user_id, data):
        """Create a new action constellation."""
        # Validate sequence
        validation = self.validator.validate(data['sequence'])
        if not validation['valid']:
            raise ValueError(f"Invalid constellation: {validation['errors']}")

        # Create database record
        constellation = ActionConstellation(
            created_by=user_id if not data.get('is_preset') else None,
            **data
        )
        self.db.session.add(constellation)
        self.db.session.commit()

        return constellation

    def get_presets(self):
        """Get all system and public presets."""
        return ActionConstellation.query.filter_by(is_preset=True).all()

    def calculate_estimated_duration(self, sequence):
        """Calculate estimated execution time for a constellation."""
        total_seconds = 0

        for action_def in sequence['actions']:
            if action_def['type'] == 'action':
                total_seconds += 30  # Average action execution time
                total_seconds += action_def.get('wait_after_seconds', 0)
            elif action_def['type'] == 'loop':
                loop_seconds = sum(
                    30 + a.get('wait_after_seconds', 0)
                    for a in action_def['actions']
                )
                total_seconds += loop_seconds * action_def['iterations']

        return total_seconds / 60  # Return minutes
```

### ConstellationValidator

```python
class ConstellationValidator:
    """Validates action constellation definitions."""

    REQUIRED_ACTIONS = ['READ_POSTS', 'GET_WORK', 'VALIDATE_WORK']
    VALID_ACTIONS = [
        'READ_POSTS', 'GET_WORK', 'PREPARE_ACTION', 'DO_ACTION',
        'VALIDATE_ACTION', 'VALIDATE_WORK', 'REFLEX', 'WAKEUP'
    ]

    def validate(self, sequence):
        """Validate a constellation sequence."""
        errors = []
        warnings = []

        # Check version
        if sequence.get('version') != '1.0':
            errors.append("Unsupported sequence version")

        # Check required actions
        action_names = self._extract_action_names(sequence)
        for required in self.REQUIRED_ACTIONS:
            if required not in action_names:
                warnings.append(f"Missing recommended action: {required}")

        # Validate each action
        for action_def in sequence.get('actions', []):
            self._validate_action(action_def, errors, warnings)

        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }

    def _validate_action(self, action_def, errors, warnings):
        """Validate a single action definition."""
        # Check type
        if action_def.get('type') not in ['action', 'loop', 'condition', 'parallel']:
            errors.append(f"Invalid action type: {action_def.get('type')}")

        if action_def['type'] == 'action':
            # Validate action name
            action_name = action_def.get('action_name')
            if action_name not in self.VALID_ACTIONS:
                errors.append(f"Invalid action_name: {action_name}")

            # Check retry config for critical actions
            if action_name in self.REQUIRED_ACTIONS:
                if not action_def.get('retry', {}).get('enabled'):
                    warnings.append(f"No retry config for critical action: {action_name}")

        elif action_def['type'] == 'loop':
            # Validate iterations
            iterations = action_def.get('iterations', 0)
            if iterations < 1:
                errors.append(f"Loop must have at least 1 iteration")
            if iterations > 10:
                warnings.append(f"Loop has {iterations} iterations (high)")

            # Validate nested actions
            for nested_action in action_def.get('actions', []):
                self._validate_action(nested_action, errors, warnings)

    def _extract_action_names(self, sequence):
        """Recursively extract all action names from sequence."""
        names = []
        for action_def in sequence.get('actions', []):
            if action_def['type'] == 'action':
                names.append(action_def.get('action_name'))
            elif action_def['type'] == 'loop':
                names.extend(self._extract_action_names({'actions': action_def['actions']}))
        return names
```

---

## Advanced Features (Future)

### 1. Conditional Actions
Execute actions based on conditions:
```json
{
  "type": "condition",
  "condition": "agent.role == 'Backend Developer'",
  "true_actions": [...],
  "false_actions": [...]
}
```

### 2. Parallel Execution
Run multiple actions simultaneously:
```json
{
  "type": "parallel",
  "actions": [
    {"action_name": "PREPARE_ACTION"},
    {"action_name": "FETCH_DATA"}
  ],
  "wait_for_all": true
}
```

### 3. Dynamic Parameters
Pass runtime parameters to actions:
```json
{
  "type": "action",
  "action_name": "CUSTOM_ACTION",
  "parameters": {
    "priority": "high",
    "context": "${cycle.context}"
  }
}
```

---

## Migration from Hardcoded Sequences

### Step 1: Create System Presets
```python
# Migration script
def create_system_presets():
    # Standard Daily Workflow
    standard = ActionConstellation(
        id='standard-daily-workflow',
        name='Standard Daily Workflow',
        description='Default agent daily cycle with iterative action execution',
        created_by=None,  # System preset
        sequence=STANDARD_SEQUENCE,
        is_preset=True,
        is_public=True,
        tags=['default', 'standard']
    )
    db.session.add(standard)

    # ... create other presets ...

    db.session.commit()
```

### Step 2: Update Existing Cycles
```python
# Assign default constellation to existing cycles
def migrate_existing_cycles():
    cycles = CycleConfiguration.query.filter_by(constellation_id=None).all()

    for cycle in cycles:
        cycle.constellation_id = 'standard-daily-workflow'

    db.session.commit()
```

### Step 3: Deprecate Hardcoded Sequences
```python
# Update run_all_cycles.py to use constellation
def run_with_constellation(cycle_id):
    cycle = CycleConfiguration.query.get(cycle_id)
    constellation = cycle.constellation

    # Execute actions from constellation.sequence
    for action_def in constellation.sequence['actions']:
        execute_action(action_def)
```

---

## Testing Strategy

### Unit Tests
- Constellation validation logic
- Action sequence parsing
- Duration estimation
- Preset creation

### Integration Tests
- Constellation CRUD operations
- Cycle execution with constellations
- Visual editor save/load
- Preset cloning

### UI Tests
- Drag-and-drop interactions
- Action configuration panels
- Validation feedback
- Real-time updates

---

## Performance Considerations

1. **Caching**
   - Cache system presets in Redis
   - Cache frequently used constellations
   - Invalidate on updates

2. **Validation**
   - Client-side validation for immediate feedback
   - Server-side validation for security
   - Cache validation results

3. **Visual Editor**
   - Lazy load action palette
   - Virtual scrolling for large constellations
   - Debounce auto-save

---

## Next Steps

1. Review and approve design
2. Implement data models and migrations
3. Build ConstellationManager service
4. Create API endpoints
5. Build visual editor component
6. Create system presets
7. Migration tooling
8. Testing and documentation

---

**Document Version:** 1.0
**Last Updated:** 2025-11-19
**Related:** [00_OVERVIEW.md](./00_OVERVIEW.md), [01_CYCLE_MANAGEMENT_DESIGN.md](./01_CYCLE_MANAGEMENT_DESIGN.md)
