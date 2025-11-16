# Loop 70: Living Agent with Complex Workflow
**Date:** 2025-11-16
**Agent:** TeacherJohn (Agent 8, Loop 70)
**Philosophy:** Living Agent principles within complex, iterative workflow

---

## Executive Summary

This document describes how Loop 70 (TeacherJohn) implements the **Living Agent philosophy** within a **complex, multi-step workflow**. Unlike simplified approaches, this maintains the full iterative execution cycle while embedding intelligent decision-making and context awareness.

**Key Principle:** Agents are autonomous professionals who make intelligent decisions at each step, not mechanical executors following rigid scripts.

---

## System Architecture

### Message Delivery System (agent_post)

**Purpose:** Handle inter-agent communication

**Actions:**
- `WAKEUP` - Health check (called by agent_post)
- `RECEIVE_POST` - Deliver incoming messages (called by agent_post)

**Process:**
1. agent_post collects messages from agent outboxes
2. agent_post calls `/api/public/agent/{id}/action/RECEIVE_POST/` to deliver messages
3. Messages stored in `post/inbox/new/*.json`

### Daily Orchestration (run_all_cycles.py)

**Purpose:** Orchestrate daily work cycles for all agents

**Workflow Structure:**
```python
# Morning: Read and plan
morning_actions = ["READ_POSTS", "GET_WORK"]

# Work cycle: Iterative execution (3 iterations per day)
work_cycle_actions = ["PREPARE_ACTION", "DO_ACTION", "VALIDATE_ACTION"]
work_cycle_iterations = 3

# Evening: Final validation
evening_actions = ["VALIDATE_WORK"]

# Combined daily sequence
daily_actions = [
    "READ_POSTS",       # 1. Process messages
    "GET_WORK",         # 2. Select task, create plan

    "PREPARE_ACTION",   # 3. Prepare action 1
    "DO_ACTION",        # 4. Execute action 1
    "VALIDATE_ACTION",  # 5. Validate action 1

    "PREPARE_ACTION",   # 6. Prepare action 2
    "DO_ACTION",        # 7. Execute action 2
    "VALIDATE_ACTION",  # 8. Validate action 2

    "PREPARE_ACTION",   # 9. Prepare action 3
    "DO_ACTION",        # 10. Execute action 3
    "VALIDATE_ACTION",  # 11. Validate action 3

    "VALIDATE_WORK"     # 12. Final work validation
]

# Weekly: Reflection (every 5 days)
reflex_action = "REFLEX"
```

---

## Living Agent Intelligence in Each Action

### 1. READ_POSTS (Protocol-based ✓)

**Purpose:** Process incoming messages and create tasks

**Living Agent Aspects:**
- Understands message context and urgency
- Identifies priority levels (high/medium/low)
- Recognizes collaboration needs
- Creates tasks with appropriate metadata

**Protocol:** `/protocols/read_posts/read_posts_protocol.json`

**Example Intelligence:**
```
Message from cityhall: "URGENT: need marketplace architecture by EOD"
↓
Task created with:
- priority: HIGH
- source: cityhall
- deadline_implied: today
- impact: high (blocking team)
```

---

### 2. GET_WORK (Protocol-based ✓ with Living Agent enhancement)

**Purpose:** Context-aware task selection and work planning

**Living Agent Aspects:**
- **Reviews ALL available tasks** before selecting
- **Considers multiple factors:**
  - Priority level (high/medium/low)
  - Dependencies satisfied
  - Team impact (who's blocked?)
  - Cognitive complexity
  - Estimated effort
- **Shows reasoning:** "I chose X because... I did NOT choose Y because..."
- **Adaptive:** Decision changes based on context

**Protocol:** `/protocols/get_work/get_work_protocol.json` (v2.0 - Enhanced)

**Decision Patterns:**
```
Scenario 1: Multiple tasks available
→ Select highest priority task with satisfied dependencies

Scenario 2: Teammate is blocked
→ Prioritize unblocking teammate (team success > individual work)

Scenario 3: All tasks blocked
→ Send clarification messages, work on documentation, offer help

Scenario 4: No clear priority
→ Choose highest impact task aligned with team goals
```

**Example Output:**
```json
{
  "selected_task": "marketplace_mvp",
  "reasoning": "Selected marketplace_mvp because: (1) HIGH priority from cityhall, (2) All dependencies available, (3) fibonacci_optimization is only medium priority, (4) workshop_planning is blocked on padre. Team needs this architecture urgently.",
  "working_plan": {
    "actions": [
      "action1: Analyze requirements",
      "action2: Design architecture",
      "action3: Create API specs"
    ]
  }
}
```

---

### 3. PREPARE_ACTION (Needs protocol or enhanced prompts)

**Purpose:** Prepare the next action for execution

**Living Agent Aspects:**
- Identifies which action comes next (based on working_plan)
- Gathers specific context needed for this action
- Creates detailed execution plan
- Anticipates potential issues

**Current State:** Has Python prompts (PREPARE_ACTION.py)
**Improvement Needed:** Could benefit from protocol-based approach

**Process:**
1. Review working_plan.json to identify next pending action
2. Load related_content.json for context
3. Create action-specific plan in current_work/action/action_plan.json
4. Gather necessary resources in current_work/action/context.json

---

### 4. DO_ACTION (Needs protocol or enhanced prompts)

**Purpose:** Execute the prepared action

**Living Agent Aspects:**
- Understands the action plan
- Executes with expertise and judgment
- Generates high-quality deliverables
- Documents decisions and process

**Current State:** Has Python prompts (DO_ACTION.py)
**Improvement Needed:** Could benefit from protocol-based approach

**Process:**
1. Read current_work/action/action_plan.json
2. Load current_work/action/context.json
3. Execute the work
4. Create deliverables in current_work/action/result/
5. Log execution in current_work/action/execution_log.json

---

### 5. VALIDATE_ACTION (Needs protocol or enhanced prompts)

**Purpose:** Validate individual action completion

**Living Agent Aspects:**
- Checks action quality against plan
- Verifies deliverables meet requirements
- Provides constructive feedback if issues found
- Decides: VALID (continue) or INVALID (retry/fix)

**Current State:** Has YAML config (VALIDATE_ACTION.yaml)
**Improvement Needed:** Needs protocol file

**Validation Criteria:**
- Deliverable exists and is complete
- Meets requirements from action_plan.json
- Quality is acceptable
- No obvious errors or omissions

**Decision Paths:**
- **VALID:** Mark action complete, move to next action
- **INVALID:** Document issues, queue for retry or manual review

---

### 6. VALIDATE_WORK (Protocol-based ✓)

**Purpose:** Final validation of entire work task

**Living Agent Aspects:**
- Reviews all completed actions holistically
- Checks overall work quality
- Verifies original task requirements met
- Provides final assessment

**Protocol:** `/protocols/validate/validate_protocol.json`

**Process:**
1. Load task requirements from tasks/running/
2. Load all action results from current_work/
3. Validate completeness and quality
4. Create validation report or issue log

**Decision Paths:**
- **VALID:** Move task to tasks/done/, work complete
- **INVALID:** Document issues in invalid_result/, queue fixes

---

### 7. REFLEX (Protocol-based ✓)

**Purpose:** Weekly self-reflection and continuous improvement

**Living Agent Aspects:**
- Reviews completed work over the week
- Identifies patterns and learnings
- Generates insights for improvement
- Suggests process optimizations

**Protocol:** `/protocols/reflex/reflex_protocol.json`

**Frequency:** Every 5 virtual days

**Example Insights:**
```
"I noticed that 3 tasks this week were blocked waiting for external info.
In the future, I should send clarification requests earlier rather than
waiting until GET_WORK discovers the blocker. This would save time and
reduce context switching."
```

---

## Complete Daily Flow Example

### Morning - Day 1

**8:00 AM - agent_post delivers messages**
```bash
# agent_post calls for each received message:
POST /api/public/agent/8/action/RECEIVE_POST/
# Message stored in: post/inbox/new/message_001.json
```

**8:15 AM - READ_POSTS (run_all_cycles)**
```bash
curl http://localhost:5050/api/public/agent/8/action/READ_POSTS/
```
**Result:**
- Reads post/inbox/new/message_001.json
- Creates tasks/new/marketplace_mvp.json (priority: HIGH)
- Creates tasks/new/fibonacci_optimization.json (priority: medium)

**8:30 AM - GET_WORK (run_all_cycles)**
```bash
curl http://localhost:5050/api/public/agent/8/action/GET_WORK/
```
**Agent's Decision Process:**
```
Available tasks:
1. marketplace_mvp (HIGH priority, ready)
2. fibonacci_optimization (medium priority, ready)

Decision: marketplace_mvp
Reasoning: HIGH priority from cityhall, likely urgent deadline,
           may be blocking other team members. fibonacci can wait.

Creates:
- tasks/running/marketplace_mvp.json
- current_work/working_plan.json (3 actions defined)
- current_work/related_content.json
- current_work/action1/action_description.json
- current_work/action2/action_description.json
- current_work/action3/action_description.json
```

### Work Cycle - Action 1

**9:00 AM - PREPARE_ACTION (run_all_cycles)**
```bash
curl http://localhost:5050/api/public/agent/8/action/PREPARE_ACTION/
```
**Process:**
- Identifies action1 as next (from working_plan.json)
- Gathers context for "Analyze requirements"
- Creates current_work/action/action_plan.json
- Creates current_work/action/context.json

**9:15 AM - DO_ACTION (run_all_cycles)**
```bash
curl http://localhost:5050/api/public/agent/8/action/DO_ACTION/
```
**Process:**
- Reads action_plan.json
- Performs requirement analysis
- Creates current_work/action/result/requirements_analysis.md
- Logs execution in execution_log.json

**9:30 AM - VALIDATE_ACTION (run_all_cycles)**
```bash
curl http://localhost:5050/api/public/agent/8/action/VALIDATE_ACTION/
```
**Process:**
- Reviews requirements_analysis.md
- Checks against success criteria
- Result: VALID ✓
- Creates current_work/action/validation/report.json
- Marks action1 as complete

### Work Cycle - Action 2

**9:45 AM - PREPARE_ACTION**
- Prepares action2: "Design architecture"

**10:00 AM - DO_ACTION**
- Creates architecture_diagram.md

**10:15 AM - VALIDATE_ACTION**
- Validates architecture → VALID ✓

### Work Cycle - Action 3

**10:30 AM - PREPARE_ACTION**
- Prepares action3: "Create API specs"

**10:45 AM - DO_ACTION**
- Creates api_specification.json

**11:00 AM - VALIDATE_ACTION**
- Validates API spec → VALID ✓

### Evening - Final Validation

**11:15 AM - VALIDATE_WORK (run_all_cycles)**
```bash
curl http://localhost:5050/api/public/agent/8/action/VALIDATE_WORK/
```
**Process:**
- Reviews all 3 completed actions
- Checks against original marketplace_mvp task
- Verifies deliverables complete
- Result: VALID ✓
- Moves tasks/running/marketplace_mvp.json → tasks/done/
- Creates project completion report

**Day 1 Complete!** ✅

---

## Weekly Reflection - Day 5

**REFLEX (run_all_cycles)**
```bash
curl http://localhost:5050/api/public/agent/8/action/REFLEX/
```
**Process:**
- Reviews all tasks completed over 5 days
- Identifies patterns:
  - "marketplace_mvp was completed efficiently in 1 day"
  - "fibonacci_optimization took 2 days (waited for code)"
  - "Collaboration with padre was smooth, responded quickly"
- Generates insights:
  - "Could improve: Send clarification requests earlier"
  - "Strength: Good prioritization of urgent tasks"
  - "Observation: High-priority tasks get done same day"
- Creates reflections/new/reflection_day5.json

---

## Configuration Files

### Loop 70 Actions (All present)

| Action | Type | Protocol | Purpose |
|--------|------|----------|---------|
| WAKEUP.yaml | utility | N/A | Health check (agent_post) |
| RECEIVE_POST.yaml | utility | N/A | Message delivery (agent_post) |
| READ_POSTS.yaml | daily | ✅ read_posts_protocol.json | Process messages |
| GET_WORK.yaml | daily | ✅ get_work_protocol.json (v2.0) | Task selection + planning |
| PREPARE_ACTION.yaml | work cycle | ⚠️ Needs protocol | Prepare next action |
| DO_ACTION.yaml | work cycle | ⚠️ Needs protocol | Execute action |
| VALIDATE_ACTION.yaml | work cycle | ⚠️ Needs protocol | Validate action |
| VALIDATE_WORK.yaml | daily | ✅ validate_protocol.json | Final validation |
| REFLEX.yaml | weekly | ✅ reflex_protocol.json | Self-reflection |

### Protocol Files Location
```
/loops/70/filesystem/agentlife/skills/project_thinking/protocols/
├── read_posts/
│   └── read_posts_protocol.json (v1.0)
├── get_work/
│   └── get_work_protocol.json (v2.0 - Living Agent enhanced)
├── validate/
│   └── validate_protocol.json (v1.0)
└── reflex/
    └── reflex_protocol.json (v1.0)
```

### Python Config Files
```
/loops/70/config/
├── WAKEUP.py (simple)
├── READ_POSTS.py (references protocol)
├── GET_WORK.py (references protocol)
├── PREPARE_ACTION.py (has prompts, could use protocol)
├── DO_ACTION.py (has prompts, could use protocol)
├── VALIDATE_WORK.py (references protocol)
└── REFLEX.py (references protocol)
```

---

## Living Agent Philosophy Summary

### Core Principles Applied

**1. Autonomy**
- Agents make their own decisions at each step
- GET_WORK demonstrates true choice (not first-available selection)
- Context-aware actions throughout workflow

**2. Context Awareness**
- GET_WORK reviews ALL tasks before deciding
- Considers priority, dependencies, team impact
- Adapts based on changing conditions

**3. Team Collaboration**
- Recognizes when teammates are blocked
- Prioritizes unblocking colleagues
- Shows collaborative reasoning

**4. Transparency**
- Shows decision reasoning at each step
- Documents execution process
- Provides clear validation feedback

**5. Continuous Learning**
- REFLEX provides weekly insights
- Identifies improvement opportunities
- Builds institutional knowledge

### Complex Workflow Advantages

**Why 3 iterations per day?**
1. Allows completing multi-step tasks in one day
2. Provides granular progress tracking
3. Enables per-action validation (catch issues early)
4. Matches realistic work complexity

**Why not simplify to 3 actions?**
- Real work is iterative, not monolithic
- Granular steps allow better error recovery
- Validation at each step improves quality
- Matches how humans actually work

**Balance:**
- **Simplicity:** Clear orchestration (12 actions per day)
- **Intelligence:** Agents decide HOW to use each action
- **Flexibility:** Agents adapt within the structure
- **Quality:** Multiple validation points ensure excellence

---

## Success Metrics

### Quantitative
| Metric | Target | Measurement |
|--------|--------|-------------|
| Task completion rate | >80% | Tasks completed successfully per day |
| Action validation pass rate | >85% | Actions validated on first attempt |
| Work validation pass rate | >90% | Final work validated without rework |
| Average actions per task | 2-4 | Complexity indicator |
| Daily task throughput | 1-2 | Tasks completed per virtual day |

### Qualitative
- ✅ Agents demonstrate intelligent decision-making
- ✅ Reasoning is transparent and logical
- ✅ Team collaboration is evident in choices
- ✅ Context awareness visible in decisions
- ✅ Continuous improvement via REFLEX insights

---

## Comparison: Simple vs Complex Workflow

| Aspect | Simple (3 actions) | Complex (12 actions) | Winner |
|--------|-------------------|---------------------|--------|
| **Orchestration simplicity** | ✅ Very simple | ⚠️ More complex | Simple |
| **Work granularity** | ❌ Monolithic | ✅ Fine-grained | Complex |
| **Error recovery** | ❌ All-or-nothing | ✅ Per-action | Complex |
| **Progress tracking** | ❌ Opaque | ✅ Transparent | Complex |
| **Quality control** | ⚠️ End-only | ✅ Continuous | Complex |
| **Realism** | ❌ Artificial | ✅ Realistic | Complex |
| **Living Agent fit** | ⚠️ Limited | ✅ Natural | Complex |

**Conclusion:** Complex workflow better supports Living Agent philosophy

---

## Future Enhancements

### Short Term
1. **Create protocols for PREPARE_ACTION, DO_ACTION, VALIDATE_ACTION**
   - Move intelligence from Python prompts to JSON protocols
   - Enable easier modification without code changes
   - Standardize format across all actions

2. **Add action retry logic**
   - If VALIDATE_ACTION fails, retry with feedback
   - Max 2 retries per action

3. **Implement dynamic iteration count**
   - Instead of fixed 3 iterations, run until working_plan complete
   - More flexible for varying task complexity

### Medium Term
1. **Cross-agent collaboration tracking**
   - Monitor who's blocked on whom
   - Suggest proactive unblocking actions
   - Visualize team dependency graph

2. **Project state management**
   - Track multi-day projects
   - Resume partially complete work
   - Handle project blocking/unblocking

3. **Enhanced REFLEX**
   - Compare performance across agents
   - Identify best practices from successful patterns
   - Generate team-level insights

### Long Term
1. **Adaptive workflow**
   - Agents adjust iteration count based on task complexity
   - Learn optimal action breakdown patterns
   - Self-optimize process over time

2. **Meta-learning**
   - Agents learn from each other's REFLEX insights
   - Build shared knowledge base
   - Collective intelligence emergence

---

## Documentation References

- **Living Agent Concept:** `/docs/updating_agent_loops_2.md`
- **Protocol Modernization:** `/docs/dev_reports/2025-11-16_loop70_protocol_modernization.md`
- **Agent Actions Inventory:** `/docs/agent_actions_inventory.md`
- **Simplified Config Plan:** `/docs/loop70_simplified_config_plan.md` (archive)

---

## Appendix: Running the Orchestration

### Run 1 Day
```bash
cd /Users/dantweb/dantweb/l-sdk-27a/agent_post
python run_all_cycles.py --days 1
```

### Run 5 Days (with REFLEX)
```bash
python run_all_cycles.py --days 5
```

### Test Single Action
```bash
# Test GET_WORK with Living Agent intelligence
curl http://localhost:5050/api/public/agent/8/action/GET_WORK/

# Check execution result
curl http://localhost:5050/api/public/execution/{execution_id}/result/
```

### Monitor Agent
```bash
# Check tasks
ls /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/70/filesystem/agentlife/tasks/

# Check current work
ls /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/70/filesystem/agentlife/current_work/

# Check reflections
ls /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/70/filesystem/agentlife/reflections/
```

---

**Document Status:** ✅ Complete
**Implementation Status:** ✅ Complex workflow implemented, protocols enhanced
**Next Steps:** Test orchestration, create remaining protocols, monitor agent behavior
**Philosophy:** Living Agent intelligence within complex, realistic workflow structure
