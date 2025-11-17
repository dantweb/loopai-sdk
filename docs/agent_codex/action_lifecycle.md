# Agent Action Lifecycle

## Overview

Agents in LoopAI operate on a daily action cycle, executing a sequence of predefined actions that enable them to read messages, select work, perform tasks, validate results, and collaborate with peers.

## Daily Action Sequence

Each virtual day, agents execute actions in this order:

```
1. READ_POSTS       - Read and process incoming messages
2. GET_WORK         - Select tasks to work on
3. PREPARE_ACTION   - Plan approach for selected task
4. DO_ACTION        - Execute the task
5. VALIDATE_ACTION  - Verify work quality
6. PREPARE_ACTION   - Plan next task (cycle 2)
7. DO_ACTION        - Execute next task (cycle 2)
8. VALIDATE_ACTION  - Verify work (cycle 2)
9. PREPARE_ACTION   - Plan third task (cycle 3)
10. DO_ACTION       - Execute third task (cycle 3)
11. VALIDATE_ACTION - Verify work (cycle 3)
12. VALIDATE_WORK   - End-of-day review
13. MESSAGE_EXCHANGE - Send/receive messages with peers
```

### Action Timing
- 15-second delay between actions
- 20-second delay between days
- Actions execute asynchronously via REST API

## Action Details

### 1. READ_POSTS

**Purpose:** Process incoming messages and create actionable tasks

**Input:**
- Messages in `/post/inbox/new/`
- Agent's `/self/self_identity.json`
- `skills/project_thinking/protocols/read_posts/read_posts_protocol.json`

**Process:**
1. Load agent identity to understand specialization
2. Read all messages from inbox
3. Parse message content and identify work items
4. Extract technical deliverables (not just acknowledgments)
5. Create task files in `/tasks/new/` for each work item
6. Move messages to `/post/inbox/read/`

**Output:**
- Task files in `/tasks/new/`
- Updated inbox (messages moved to read)

**Example Task Created:**
```json
{
  "task_id": "build_calculator_api",
  "description": "Build REST API with endpoints for add, subtract, multiply, and divide operations",
  "source": "calculator_project_message_id",
  "priority": "high",
  "deliverables": ["API code with 4 endpoints", "Request/response format defined"],
  "role": "Backend Developer",
  "estimated_effort": "4 hours",
  "dependencies": [],
  "created_at": "2025-11-16T10:00:00Z"
}
```

### 2. GET_WORK

**Purpose:** Select which task to work on next

**Input:**
- Tasks in `/tasks/new/`
- Agent's current capacity and context
- `skills/project_thinking/protocols/get_work/get_work_protocol.json`

**Process:**
1. Review all available tasks in `/tasks/new/`
2. Evaluate tasks based on:
   - Priority (high/medium/low)
   - Deadline urgency
   - Dependencies (are prereqs complete?)
   - Agent's expertise match
   - Estimated effort
3. Select highest-value task
4. Move selected task to `/tasks/active/`

**Output:**
- One task moved from `/tasks/new/` to `/tasks/active/`
- Work context updated

**Selection Criteria:**
```json
{
  "selection_rules": [
    "High priority tasks first",
    "Tasks blocking others prioritized",
    "Tasks matching expertise preferred",
    "Quick wins when energy/time limited",
    "Balance urgent vs important"
  ]
}
```

### 3. PREPARE_ACTION

**Purpose:** Plan approach for the selected task

**Input:**
- Active task from `/tasks/active/`
- Agent's expertise and capabilities
- Available skills and tools
- `skills/project_thinking/protocols/prepare_action/prepare_action_protocol.json`

**Process:**
1. Analyze task requirements
2. Break down into subtasks if complex
3. Identify required resources/skills
4. Determine approach/methodology
5. Estimate time and effort
6. Create action plan
7. Identify risks and mitigation

**Output:**
- Action plan file in `/tasks/active/plans/`
- Updated task with execution strategy

**Example Action Plan:**
```json
{
  "task_id": "build_calculator_api",
  "plan": {
    "approach": "REST API using Flask",
    "steps": [
      {
        "step": "Create Flask app structure",
        "estimated_minutes": 15
      },
      {
        "step": "Implement /api/calculate endpoint",
        "estimated_minutes": 30
      },
      {
        "step": "Add error handling",
        "estimated_minutes": 20
      },
      {
        "step": "Write API documentation",
        "estimated_minutes": 15
      }
    ],
    "tools_needed": ["Python", "Flask", "JSON"],
    "risks": [
      {
        "risk": "API format mismatch with frontend",
        "mitigation": "Coordinate format with zhou before implementing"
      }
    ],
    "total_estimated_minutes": 80
  }
}
```

### 4. DO_ACTION

**Purpose:** Execute the planned work

**Input:**
- Task from `/tasks/active/`
- Action plan from PREPARE_ACTION
- Skills and protocols
- Available tools and resources

**Process:**
1. Follow action plan
2. Execute each step
3. Create deliverables
4. Document decisions and issues
5. Save work artifacts
6. Log progress

**Output:**
- Work artifacts in `/work/`
- Progress log
- Updated task status

**Example Execution:**
```python
# DO_ACTION creates actual deliverable:
/work/calculator_api.py

"""
Calculator REST API
Implements add, subtract, multiply, divide operations
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    operation = data.get('operation')
    num1 = data.get('num1')
    num2 = data.get('num2')

    # Error handling
    if not all([operation, num1 is not None, num2 is not None]):
        return jsonify({
            "success": False,
            "error": {
                "code": "INVALID_INPUT",
                "message": "Missing required fields"
            }
        }), 400

    # Operations
    operations = {
        'add': num1 + num2,
        'subtract': num1 - num2,
        'multiply': num1 * num2,
        'divide': num1 / num2 if num2 != 0 else None
    }

    if operation not in operations:
        return jsonify({
            "success": False,
            "error": {
                "code": "INVALID_OPERATION",
                "message": f"Unknown operation: {operation}"
            }
        }), 400

    result = operations[operation]

    if result is None:
        return jsonify({
            "success": False,
            "error": {
                "code": "DIV_BY_ZERO",
                "message": "Division by zero is not allowed"
            }
        }), 400

    return jsonify({
        "success": True,
        "result": result
    })

if __name__ == '__main__':
    app.run(debug=True)
```

### 5. VALIDATE_ACTION

**Purpose:** Verify the work meets quality standards

**Input:**
- Completed work from DO_ACTION
- Original task requirements
- Quality criteria
- `skills/project_thinking/protocols/validate_action/validate_action_protocol.json`

**Process:**
1. Review deliverables against requirements
2. Test functionality (if code)
3. Check documentation completeness
4. Verify error handling
5. Assess code quality/clarity
6. Identify any issues or improvements

**Output:**
- Validation report
- List of issues found
- Decision: PASS, NEEDS_WORK, or FAIL

**Example Validation:**
```json
{
  "task_id": "build_calculator_api",
  "validation_result": "PASS",
  "checks_performed": [
    {
      "check": "All required endpoints present",
      "result": "PASS",
      "details": "All 4 operations implemented"
    },
    {
      "check": "Error handling complete",
      "result": "PASS",
      "details": "Division by zero, invalid input, invalid operation handled"
    },
    {
      "check": "Code documentation",
      "result": "PASS",
      "details": "Functions documented, clear variable names"
    },
    {
      "check": "API format consistency",
      "result": "NEEDS_VERIFICATION",
      "details": "Need to confirm format matches frontend expectations"
    }
  ],
  "issues": [],
  "suggestions": [
    "Add unit tests for edge cases",
    "Document API format in separate file"
  ],
  "overall_quality": "high",
  "ready_for_delivery": true
}
```

### 6-11. PREPARE_ACTION, DO_ACTION, VALIDATE_ACTION (Cycles 2 & 3)

Agents repeat the PREPARE → DO → VALIDATE cycle up to 3 times per day, allowing them to complete multiple tasks or iterations.

**Iteration Strategies:**
- **Multiple Small Tasks:** Complete 3 different small tasks
- **One Large Task:** Break large task into 3 work sessions
- **Iterative Refinement:** Initial implementation, improvements, polish

### 12. VALIDATE_WORK

**Purpose:** End-of-day review and reflection

**Input:**
- All work completed during the day
- All tasks moved to completion
- Day's communication and collaboration

**Process:**
1. Review all completed tasks
2. Assess overall day's productivity
3. Identify lessons learned
4. Document knowledge gained
5. Prepare status update for team
6. Archive completed work
7. Plan tomorrow's priorities

**Output:**
- Daily summary report
- Completed tasks moved to `/tasks/completed/`
- Knowledge documents in `/knowledge/learned/`
- Status message prepared for team

**Example Daily Summary:**
```json
{
  "date": "2025-11-16",
  "agent_id": "FRBG/TeacherJohn",
  "summary": {
    "tasks_completed": 2,
    "tasks_in_progress": 1,
    "deliverables_created": [
      "/work/calculator_api.py",
      "/work/api_documentation.md"
    ],
    "messages_sent": 5,
    "messages_received": 8,
    "questions_answered": 3,
    "collaboration_sessions": 2,
    "productivity_rating": "high",
    "energy_level": "good",
    "blockers": [],
    "lessons_learned": [
      "Coordinating API format early prevents rework",
      "Clear error messages improve frontend integration"
    ],
    "tomorrow_priorities": [
      "Complete API unit tests",
      "Help zhou with frontend integration",
      "Document deployment process"
    ]
  }
}
```

### 13. MESSAGE_EXCHANGE (WAKEUP)

**Purpose:** Deliver messages to peers and wake up for next cycle

**Input:**
- Messages in `/post/outbox/sent/`
- Recipients' inbox paths

**Process:**
1. Collect all messages ready to send
2. Deliver to recipients' `/post/inbox/new/`
3. Confirm delivery
4. Update message status
5. Prepare agent for next day

**Output:**
- Messages delivered to peers
- Delivery confirmations
- Agent ready for next cycle

## Action Execution via API

Actions are triggered via REST API endpoints:

```
POST /api/public/agent/{agent_id}/action/{ACTION_NAME}/
```

**Response:**
```json
{
  "success": true,
  "execution_id": "uuid",
  "agent_id": 8,
  "action_name": "READ_POSTS",
  "status": "running",
  "created_at": "ISO8601"
}
```

**Check Progress:**
```
GET /api/public/execution/{execution_id}/progress/
```

**Get Result:**
```
GET /api/public/execution/{execution_id}/result/
```

## Execution Flow Diagram

```
┌─────────────────┐
│   READ_POSTS    │  Read messages, create tasks
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    GET_WORK     │  Select task to work on
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ PREPARE_ACTION  │  Plan approach
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   DO_ACTION     │  Execute work
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│VALIDATE_ACTION  │  Check quality
└────────┬────────┘
         │
         ▼
     [Repeat 2 more times]
         │
         ▼
┌─────────────────┐
│ VALIDATE_WORK   │  Daily review
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│MESSAGE_EXCHANGE │  Send messages
└────────┬────────┘
         │
         ▼
    [Next Day]
```

## Error Handling

### Action Failure
If an action fails:
1. Error logged to `/var/logs/`
2. Task remains in current state
3. Agent can retry on next cycle
4. Critical failures escalated

### Recovery Strategies
- **Transient Errors:** Retry on next cycle
- **Missing Dependencies:** Request help from peers
- **Knowledge Gaps:** Ask questions, acquire skills
- **Blocked Tasks:** Skip and work on other tasks

## Monitoring and Metrics

Track agent performance:

```json
{
  "lifecycle_metrics": {
    "actions_executed_today": 13,
    "actions_successful": 12,
    "actions_failed": 1,
    "avg_action_duration_seconds": 18,
    "tasks_completed_today": 2,
    "messages_processed": 8,
    "deliverables_created": 2,
    "efficiency_rating": 0.85
  }
}
```

## Best Practices

### READ_POSTS
- Extract all work items, not just acknowledgments
- Create separate tasks for distinct deliverables
- Set appropriate priorities
- Identify dependencies

### GET_WORK
- Balance urgent vs important
- Consider task dependencies
- Match work to expertise
- Don't overcommit

### PREPARE_ACTION
- Break complex tasks into steps
- Identify risks early
- Coordinate with peers when needed
- Estimate realistically

### DO_ACTION
- Follow the plan
- Document as you go
- Handle errors gracefully
- Create quality deliverables

### VALIDATE_ACTION
- Test thoroughly
- Check against requirements
- Be honest about issues
- Suggest improvements

### VALIDATE_WORK
- Reflect on day's work
- Share lessons learned
- Update team on progress
- Plan tomorrow

## Integration with Skills

Each action uses corresponding skill protocols:
- READ_POSTS → `skills/project_thinking/protocols/read_posts/`
- GET_WORK → `skills/project_thinking/protocols/get_work/`
- PREPARE_ACTION → `skills/project_thinking/protocols/prepare_action/`
- DO_ACTION → `skills/specialized/{domain}/protocols/do_action/`
- VALIDATE_ACTION → `skills/project_thinking/protocols/validate_action/`
- VALIDATE_WORK → `skills/project_thinking/protocols/validate_work/`

## Conclusion

The action lifecycle provides structure and consistency to agent behavior while allowing flexibility for different types of work. By following this pattern daily, agents can:
- Process information systematically
- Select work intelligently
- Plan approaches carefully
- Execute work effectively
- Validate quality rigorously
- Reflect and improve continuously
- Collaborate seamlessly with peers
