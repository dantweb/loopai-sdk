# Loop 70 Simplified Configuration Plan
**Date:** 2025-11-16
**Agent:** TeacherJohn (Agent 8, Loop 70)
**Goal:** Simplify to 3-action daily workflow embodying Living Agent principles

---

## Current State Analysis

### Actions Currently in Loop 70

| Action File | Status | Used in Orchestration? | Decision |
|------------|--------|----------------------|----------|
| WAKEUP.yaml | ✅ Active | No (utility) | **KEEP** - System health check |
| RECEIVE_POST.yaml | ✅ Active | No (triggered by agent_post) | **KEEP** - Message receiving |
| READ_POSTS.yaml | ✅ Active | ✅ YES - Daily cycle | **KEEP** - Protocol-based ✓ |
| GET_WORK.yaml | ✅ Active | ✅ YES - Daily cycle | **KEEP & UPDATE** - Add Living Agent decision logic |
| VALIDATE_WORK.yaml | ✅ Active | ✅ YES - Daily cycle | **KEEP** - Already protocol-based ✓ |
| REFLEX.yaml | ✅ Active | ✅ YES - Weekly (every 5 days) | **KEEP** - Protocol-based ✓ |
| **DO_ACTION.yaml** | ❌ Unused | ❌ NO | **REMOVE** - Not used |
| **PREPARE_ACTION.yaml** | ❌ Unused | ❌ NO | **REMOVE** - Not used |
| **VALIDATE_ACTION.yaml** | ❌ Unused | ❌ NO | **REMOVE** - Not used |

### Python Config Files

| Python File | Paired with YAML | Decision |
|------------|-----------------|----------|
| WAKEUP.py | WAKEUP.yaml | **KEEP** |
| READ_POSTS.py | READ_POSTS.yaml | **KEEP** |
| GET_WORK.py | GET_WORK.yaml | **KEEP & UPDATE** |
| REFLEX.py | REFLEX.yaml | **KEEP** |
| VALIDATE.py | VALIDATE_WORK.yaml | **KEEP** (rename to VALIDATE_WORK.py) |
| **DO_WORK.py** | ❌ No YAML | **REMOVE** - Orphaned file |

### Current Protocol Files

| Protocol | Location | Status |
|----------|----------|--------|
| read_posts_protocol.json | /protocols/read_posts/ | ✅ Good |
| get_work_protocol.json | /protocols/get_work/ | ⚠️ Needs update for Living Agent principles |
| validate_protocol.json | /protocols/validate/ | ✅ Good |
| reflex_protocol.json | /protocols/reflex/ | ✅ Good |

---

## Living Agent Workflow (Simplified)

### Daily Cycle (3 Actions)

```
┌─────────────────────────────────────────────────────────┐
│         SIMPLIFIED LIVING AGENT DAILY CYCLE              │
└─────────────────────────────────────────────────────────┘

🌅 MORNING: READ_POSTS (Protocol-based)
───────────────────────
• Process inbox messages
• Create tasks from requests
• Identify urgent vs normal priority
• Update: post/inbox/new/*.json → tasks/new/*.json

💼 WORK: GET_WORK (Protocol-based with Living Agent intelligence)
─────────────────
Agent's Context-Aware Decision Making:

1. ASSESS Current State:
   ├─ Scan all tasks: tasks/new/*.json
   ├─ Review priorities (high/medium/low)
   ├─ Check dependencies and blockers
   ├─ Consider urgency and deadlines
   └─ Evaluate cognitive load

2. DECIDE What to Work On:
   ├─ "Which task is most important NOW?"
   ├─ "Do I have all info needed?"
   ├─ "Is anyone blocked waiting for me?"
   └─ Make intelligent selection

3. EXECUTE Selected Work:
   ├─ Move selected task: tasks/new/ → tasks/running/
   ├─ Create work plan (working_plan.json)
   ├─ Gather context (related_content.json)
   ├─ Break into actions
   ├─ Perform work
   ├─ Generate deliverables
   └─ Update: current_work/ with results

✅ VALIDATION: VALIDATE_WORK (Protocol-based)
────────────────────────
• Load requirements and work result
• Validate quality against criteria
• Decision:
  ├─ VALID → Move task to tasks/done/, continue
  └─ INVALID → Document issues, retry or skip

📊 WEEKLY: REFLEX (Every 5 days)
──────────────────────
• Review completed work
• Analyze performance
• Generate insights
• Identify improvements
```

---

## Key Living Agent Principles in GET_WORK

### Current GET_WORK Approach
❌ **OLD:** "Select first available task → create plan → execute"

### Updated Living Agent GET_WORK
✅ **NEW:** "Assess all context → Make intelligent decision → Execute with awareness"

**Context-Aware Decisions:**
```
Example 1: Multiple Tasks Available
Tasks:
- fibonacci_optimization (priority: medium, has all info)
- marketplace_mvp (priority: HIGH, urgent request from cityhall)
- workshop_planning (priority: low, blocked - waiting for padre)

Decision: "marketplace_mvp is HIGH priority and urgent → work on this first"
```

```
Example 2: All Tasks Blocked
Tasks:
- code_review_A (blocked: waiting for StudentMary's code)
- project_B (blocked: waiting for padre's input)
- task_C (blocked: external dependency)

Decision: "All tasks blocked → send reminder messages → work on documentation/cleanup"
```

```
Example 3: Unblock Teammate
Tasks:
- my_task_A (priority: medium)
- respond_to_padre (priority: HIGH - padre is blocked waiting for my answer!)
- my_task_B (priority: low)

Decision: "Padre is blocked → prioritize responding to unblock him"
```

**Key Intelligence:**
1. **Priority-aware**: High priority tasks get attention first
2. **Dependency-aware**: Don't start tasks missing dependencies
3. **Team-aware**: Unblock colleagues when they're waiting
4. **State-aware**: Know what's ready vs blocked vs waiting
5. **Adaptive**: Adjust to changing conditions

---

## Updated Protocol: get_work_protocol.json

### Changes to Make

**Add to Instructions:**
```json
{
  "protocol_version": "2.0",
  "protocol_id": "get_work",
  "philosophy": "Living Agent - Context-aware decision making, not blind execution",

  "instruction": "You are TeacherJohn, a professional team member coming to work.
  Review ALL available tasks with full context awareness. Make an intelligent
  decision about what to work on TODAY based on priorities, dependencies, team
  needs, and your own bandwidth. You are NOT a task executor - you are an
  autonomous agent with agency and judgment.",

  "decision_criteria": {
    "priority_levels": {
      "high": "Urgent requests, blocking others, time-sensitive",
      "medium": "Important but not urgent, standard work",
      "low": "Nice to have, can be deferred"
    },
    "consider": [
      "Task priority (high/medium/low)",
      "Dependencies satisfied? (do I have all info needed?)",
      "Is anyone blocked waiting for me?",
      "Cognitive complexity (can I handle this now?)",
      "Estimated effort (quick win vs long project)",
      "Alignment with expertise (am I the right person?)"
    ],
    "decision_patterns": {
      "if_urgent_exists": "Prioritize urgent/high-priority tasks",
      "if_teammate_blocked": "Unblock colleagues first (team success)",
      "if_all_blocked": "Send clarification requests, work on background tasks",
      "if_multiple_ready": "Choose highest impact task",
      "if_no_tasks": "Review old tasks, offer help to teammates, do reflection"
    }
  },

  "steps": [
    {
      "step_id": "assess_workload",
      "action": "Review ALL tasks in tasks/new/ with full context",
      "outputs": "Mental map of: priorities, dependencies, blockers, readiness"
    },
    {
      "step_id": "make_decision",
      "action": "Decide which task to work on based on decision_criteria",
      "outputs": "Selected task with reasoning: 'I chose X because...'"
    },
    {
      "step_id": "copy_task",
      "action": "Move selected task: tasks/new/{task_id}.json → tasks/running/{task_id}.json"
    },
    {
      "step_id": "develop_plan",
      "action": "Create detailed work plan based on task requirements",
      "outputs": "current_work/working_plan.json"
    },
    {
      "step_id": "gather_context",
      "action": "Collect all necessary context, dependencies, and resources",
      "outputs": "current_work/related_content.json"
    },
    {
      "step_id": "create_actions",
      "action": "Break work into specific actions with clear deliverables"
    },
    {
      "step_id": "execute_work",
      "action": "Perform the work, generate deliverables, document process",
      "outputs": "current_work/current_operation/result/"
    }
  ],

  "example_reasoning": {
    "scenario": "3 tasks available",
    "tasks": [
      {"id": "fibonacci", "priority": "medium", "status": "ready"},
      {"id": "marketplace", "priority": "high", "status": "ready"},
      {"id": "workshop", "priority": "low", "status": "blocked"}
    ],
    "decision": "marketplace (HIGH priority, urgent, ready)",
    "reasoning": "marketplace is marked HIGH priority and urgent from cityhall.
                  fibonacci can wait. workshop is blocked on padre's response."
  }
}
```

---

## Implementation Plan

### Phase 1: Cleanup (Remove Unused Actions)

**Files to Remove:**
```bash
config/DO_ACTION.yaml
config/PREPARE_ACTION.yaml
config/VALIDATE_ACTION.yaml
config/DO_WORK.py
```

**Result:** Clean configuration with only actively used actions

### Phase 2: Update GET_WORK Protocol

**File to Update:**
```
filesystem/agentlife/skills/project_thinking/protocols/get_work/get_work_protocol.json
```

**Changes:**
- Add Living Agent philosophy statement
- Add decision_criteria section
- Add decision_patterns (if/then logic)
- Update instruction to emphasize autonomous decision-making
- Add example_reasoning with multi-task scenario

### Phase 3: Ensure Python Configs are Minimal

**Files to Update:**
```
config/GET_WORK.py - Ensure it simply references REQUEST_CONTENT
config/VALIDATE.py → rename to VALIDATE_WORK.py
```

All intelligence should be in protocols, not Python files.

### Phase 4: Test Updated Workflow

**Test Scenario:**
1. Send 3 messages to TeacherJohn with different priorities
2. Run READ_POSTS → creates 3 tasks
3. Run GET_WORK → should select highest priority
4. Run VALIDATE_WORK → should validate result

**Expected Behavior:**
- Agent demonstrates context awareness
- Selects appropriate task based on criteria
- Shows reasoning in logs

---

## Success Criteria

### Simplicity
- ✅ Only 6 action files (WAKEUP, RECEIVE_POST, READ_POSTS, GET_WORK, VALIDATE_WORK, REFLEX)
- ✅ No unused/orphaned files
- ✅ Clear purpose for each action

### Living Agent Intelligence
- ✅ GET_WORK demonstrates decision-making
- ✅ Context-aware task selection
- ✅ Handles multiple scenarios (urgent, blocked, team needs)
- ✅ Shows reasoning in execution logs

### Protocol-Based
- ✅ READ_POSTS: protocol-based ✓
- ✅ GET_WORK: protocol-based ✓
- ✅ VALIDATE_WORK: protocol-based ✓
- ✅ REFLEX: protocol-based ✓

### Maintainability
- ✅ Easy to understand workflow
- ✅ Easy to modify agent behavior (edit JSON, not Python)
- ✅ Easy to add new decision patterns

---

## Final Configuration Summary

### Daily Orchestration (run_all_cycles.py)
```python
daily_actions = ["READ_POSTS", "GET_WORK", "VALIDATE_WORK"]
reflex_action = "REFLEX"  # Every 5 days
```

### Action Purposes
| Action | Purpose | Intelligence Level |
|--------|---------|-------------------|
| WAKEUP | System health check | Simple (bash) |
| RECEIVE_POST | Receive messages | Simple (lambda) |
| READ_POSTS | Process messages → tasks | Medium (protocol) |
| **GET_WORK** | **Context-aware work selection + execution** | **HIGH (Living Agent)** |
| VALIDATE_WORK | Validate work quality | Medium (protocol) |
| REFLEX | Weekly reflection | Medium (protocol) |

### Agent Behavior
**Before (Mechanical):**
"I execute tasks in order without thinking"

**After (Living Agent):**
"I review my workload, consider priorities and team needs, make intelligent decisions about what to work on, and execute with awareness"

---

## Comparison: Document Proposal vs Simplified Reality

### Complex Proposal (updating_agent_loops_2.md)
- 9 actions: ASSESS_WORKLOAD, CREATE_PROJECT, PREPARE_ACTION, RUN_SUBTASK, VALIDATE_SUBTASK, VALIDATE_PROJECT, etc.
- Hierarchical project structure
- Multiple subtask loops
- **Complexity:** HIGH

### Simplified Reality (This Implementation)
- 3 daily actions: READ_POSTS, GET_WORK, VALIDATE_WORK
- Existing task structure (tasks/new, tasks/running, tasks/done)
- Intelligence embedded IN the actions
- **Complexity:** LOW

**Philosophy:**
✅ KISS Principle (Keep It Simple, Stupid)
✅ Intelligence in the agents, not the orchestration
✅ Easy to understand, easy to modify

---

## Next Steps

1. ✅ Backup Loop 70 (already done previously)
2. 🔄 Remove unused action files
3. 🔄 Update get_work_protocol.json with Living Agent intelligence
4. 🔄 Test with multiple task scenarios
5. 🔄 Verify agent demonstrates decision-making
6. 🔄 Document results

---

**Status:** 📋 Ready for Implementation
**Approval:** Awaiting user confirmation
**Estimated Time:** 30 minutes
**Risk:** LOW (reverting is easy)
