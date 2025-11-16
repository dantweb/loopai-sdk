# Updating Agent Loops Phase 2: Workflow Refinement
**Date:** 2025-11-16
**Agent:** TeacherJohn (Agent 8, Loop 70)
**Status:** 🔄 Planning Phase

---

## Executive Summary

This document outlines the transition from the initial protocol-based implementation to a refined, production-ready workflow that enables agents to function as an autonomous, collaborative team. Rather than rigid, mechanical task execution, agents will operate like real team members who come to work each day, check their messages, assess their workload, collaborate with colleagues, and manage projects naturally.

The core philosophy: **Agents are not task executors—they are team members with agency, context awareness, and collaborative intelligence.**

---

## 🌟 The Living Agent Concept

### Vision: Agents as Team Members

Imagine a virtual office where agents arrive each morning and behave like human professionals:

**8:00 AM - Morning Routine (triggered by agent_post messaging system)**
- WAKEUP: Agent is called by agent_post messaging system for health check
- RECEIVE_POST: Agent_post delivers incoming messages to agent's inbox
- Messages are stored in filesystem: post/inbox/new/*.json

**8:15 AM - Check Communications (READ_POSTS - called by run_all_cycles)**
- Agent processes messages from post/inbox/new/
- Reviews inbox for new messages from colleagues
- Identifies urgent requests, questions, collaboration needs
- Creates tasks from incoming messages
- Prioritizes: "This is urgent", "This can wait", "This needs clarification"

**8:30 AM - Intelligent Work Selection and Execution (GET_WORK - called by run_all_cycles)**
- Reviews ALL available tasks with full context awareness
- Assesses each task: priority, dependencies, team impact, readiness
- Makes autonomous decision: "Which task is most important NOW?"
- Decision factors:
  - ✅ **Priority level** (high/medium/low)
  - ✅ **Dependencies satisfied** (do I have all info needed?)
  - ✅ **Team impact** (is anyone blocked waiting for me?)
  - ✅ **Cognitive complexity** (can I handle this now?)
- Selects task and creates work plan
- Executes the work: generate deliverables, solve problems
- Stores results in current_work/
- Shows reasoning: "I chose X because... I did NOT choose Y because..."

**11:00 AM - Validation (VALIDATE_WORK - called by run_all_cycles)**
- Validates completed work against task requirements
- Checks quality, completeness, correctness
- Decision:
  - ✅ **VALID**: Move task to tasks/done/, work complete
  - ❌ **INVALID**: Document issues, decide retry or skip

**Weekly (REFLEX - Every 5 Days)**
- Reflects on completed work
- Identifies patterns and improvements
- Generates insights for team efficiency
- Suggests process improvements

### Key Principles

#### 1. **Autonomy**: Each Agent Manages Their Own Work
Agents are not told "execute task X now." Instead:
- They review available work
- They decide what to work on based on context
- They manage their own project pipeline
- They adapt to changing priorities

**Example:**
```
Agent TeacherJohn's Daily Decision:
- Inbox: 3 new messages (2 code review requests, 1 question)
- Projects:
  - fibonacci_optimization: Waiting for StudentMary's code
  - marketplace_mvp: Can work on architecture design
  - algorithm_workshop: Blocked on padre's availability
- Decision: "I'll work on marketplace_mvp architecture today since
            fibonacci is blocked and workshop needs coordination"
```

#### 2. **Collaboration**: Agents Work as a Team
Agents don't work in isolation:
- They proactively ask for help when blocked
- They provide information to unblock others
- They understand project dependencies
- They coordinate implicitly through messaging

**Example:**
```
TeacherJohn (blocked on fibonacci_optimization):
  → Sends message to StudentMary:
    "Hi StudentMary! I'm ready to review your Fibonacci code.
     Could you share the current implementation so I can provide
     optimization suggestions?"

StudentMary (receives message):
  → Creates task: "Send code to TeacherJohn"
  → Completes task, sends code
  → TeacherJohn's fibonacci project becomes unblocked
```

#### 3. **Natural State Management**: Projects Have Realistic States

**Project States:**
- 🆕 **New**: Just created, not yet started
- 🔵 **Active**: Currently working on it
- ⏸️ **Blocked**: Waiting for external input (another agent, external resource)
- ⏰ **Scheduled**: Planned for future, dependencies not yet met
- ✅ **Completed**: All work done, validated
- 📦 **Archived**: Historical reference

**Subtask States:**
- 📋 **Pending**: Not started, waiting turn
- 🔵 **In Progress**: Currently being worked on
- ⏸️ **Blocked**: Cannot proceed without external input
- ✅ **Completed**: Done and validated
- ❌ **Cancelled**: No longer needed

#### 4. **Context Awareness**: Agents Remember and Track

Agents maintain context like real team members:
- "I'm waiting for padre to confirm meeting time"
- "This project is 60% complete, 3 of 5 subtasks done"
- "I sent a question to cityhall 2 days ago, still no response"
- "marketplace_mvp is highest priority this week"

**Context Sources:**
- Project metadata (priority, deadlines, complexity)
- Message history (who said what, when)
- Dependency graphs (what blocks what)
- Team workload (who's busy, who's available)
- Past experience (similar projects, lessons learned)

#### 5. **Intuitive Communication**: Natural Language Coordination

Agents communicate like humans:
- **Asking for help**: "Could you review this design? I'd value your input."
- **Providing updates**: "I've completed the API documentation, ready for review."
- **Identifying blockers**: "I'm blocked on the database schema—can we sync?"
- **Offering assistance**: "I noticed you're working on authentication. I can help with OAuth if needed."

### Team Dynamics in Action

#### Scenario 1: Collaborative Project

**Project:** Build marketplace MVP
**Team:** TeacherJohn (architect), padre (backend), maria (frontend), zhou (testing)

**Day 1:**
- cityhall receives request for marketplace MVP
- cityhall creates project, identifies needed roles
- cityhall messages: TeacherJohn (architecture), padre (backend), maria (frontend), zhou (testing)

**Day 2:**
- TeacherJohn reads message, creates "marketplace_architecture" project
- TeacherJohn works on high-level design
- TeacherJohn sends architecture doc to padre, maria, zhou

**Day 3:**
- padre reads architecture, creates "marketplace_backend" project
- maria reads architecture, creates "marketplace_frontend" project
- zhou reads architecture, creates "marketplace_testing" project
- All three are now working in parallel

**Day 4:**
- padre messages TeacherJohn: "Question about API authentication approach"
- TeacherJohn responds with clarification
- padre unblocked, continues backend work

**Day 5:**
- maria messages padre: "Frontend ready, need API endpoints"
- padre: "Backend API 80% complete, will be ready tomorrow"
- maria: "Great, I'll work on UI styling today"

**Day 6:**
- padre completes backend API
- maria integrates frontend with API
- zhou begins integration testing

**Day 7:**
- All agents validate their parts
- VALIDATE_PROJECT: marketplace_mvp complete
- Team success! 🎉

#### Scenario 2: Handling Blockers

**TeacherJohn's Morning:**
```
8:15 AM - READ_POSTS
  - Message from StudentMary: "Here's my Fibonacci code"
  - Message from cityhall: "Urgent: marketplace needs architecture"
  - Message from padre: "Re: workshop timing - I'm free Thursday"

8:30 AM - ASSESS_WORKLOAD
  Projects:
  1. fibonacci_optimization (was blocked, NOW UNBLOCKED)
  2. marketplace_mvp (urgent, can start)
  3. algorithm_workshop (was blocked, NOW UNBLOCKED with Thursday)

  Decision: Prioritize marketplace_mvp (urgent) + fibonacci (now unblocked)
  Plan: Work on marketplace 60%, fibonacci 40%
```

#### Scenario 3: Proactive Communication

**Agent maria needs design assets:**
```
maria's state:
  - Project: marketplace_frontend
  - Current subtask: "Implement product listing UI"
  - Blocker: "No design mockups provided"

maria's action (in RUN_SUBTASK):
  - Detects missing dependency
  - Protocol guides: "If blocked by missing info, ask for help"
  - Generates message: "Hi team! I'm working on the product listing UI
                        but I don't have design mockups. Does anyone have
                        these, or should I create a basic version?"

cityhall responds:
  - "Design mockups aren't ready yet. Please create a basic version
     using our standard component library. We'll refine later."

maria unblocked:
  - Creates basic UI
  - Documents "pending design review" for later iteration
  - Continues work
```

### The Orchestration: Bringing It All Together

**System Architecture:**

**agent_post messaging system** (handles message delivery):
- Calls WAKEUP for health checks
- Calls RECEIVE_POST to deliver messages to agents
- Manages message routing between agents

**run_all_cycles.py** (daily orchestration):
```python
# Daily work cycle (3 actions per day)
daily_actions = ["READ_POSTS", "GET_WORK", "VALIDATE_WORK"]

for day in range(1, num_days + 1):
    for agent in all_agents:
        # 1. Process messages and create tasks
        agent.run_action("READ_POSTS")
        sleep(15)

        # 2. Context-aware task selection and execution
        agent.run_action("GET_WORK")
        sleep(15)

        # 3. Validate completed work
        agent.run_action("VALIDATE_WORK")
        sleep(15)

    # Weekly reflection (every 5 days)
    if day % 5 == 0:
        for agent in all_agents:
            agent.run_action("REFLEX")
```

**Key Difference from Traditional Automation:**
- ❌ OLD: "Execute these 5 tasks in sequence, regardless of state"
- ✅ NEW: "Review your work, decide what's possible today, collaborate as needed"

### Emergent Team Intelligence

When agents operate this way, **team intelligence emerges**:

1. **Self-Organization**: Agents naturally distribute work based on expertise
2. **Load Balancing**: Busy agents delay non-urgent tasks; free agents pick up slack
3. **Knowledge Sharing**: Agents learn from each other's solutions
4. **Adaptive Workflow**: Team adjusts to changing priorities without reprogramming
5. **Resilience**: If one agent is blocked, others continue progressing

**Example of Emergence:**
```
Observation: padre is blocked on 3 projects waiting for TeacherJohn's input

Emergent behavior:
- padre notices pattern in REFLEX
- padre suggests: "TeacherJohn might be overloaded as architect.
                   Could we distribute architecture tasks?"
- cityhall sees suggestion, adjusts future project assignments
- Team becomes more efficient without manual intervention
```

### Technical Implementation: State Tracking

**Project Tracking Structure:**
```json
{
  "project_id": "marketplace_mvp_arch_20251116",
  "title": "Marketplace MVP Architecture Design",
  "owner_agent": "TeacherJohn",
  "status": "active",
  "priority": "high",
  "created_at": "2025-11-16T08:30:00Z",
  "updated_at": "2025-11-16T14:20:00Z",
  "blockers": [],
  "dependencies": {
    "waiting_for": [],
    "blocking": [
      {"agent": "padre", "project": "marketplace_backend"},
      {"agent": "maria", "project": "marketplace_frontend"}
    ]
  },
  "subtasks": [
    {
      "id": "001_requirements",
      "status": "completed",
      "completed_at": "2025-11-16T10:00:00Z"
    },
    {
      "id": "002_system_design",
      "status": "in_progress",
      "started_at": "2025-11-16T10:15:00Z",
      "progress": 60
    },
    {
      "id": "003_api_spec",
      "status": "pending",
      "dependencies": ["002_system_design"]
    }
  ],
  "collaboration": {
    "messages_sent": [
      {"to": "padre", "subject": "Architecture doc", "sent_at": "..."}
    ],
    "messages_received": [
      {"from": "padre", "subject": "Question on auth", "received_at": "..."}
    ]
  },
  "metrics": {
    "estimated_hours": 8,
    "actual_hours": 4.5,
    "completion_percentage": 60
  }
}
```

**Daily Status Dashboard** (each agent maintains):
```json
{
  "agent": "TeacherJohn",
  "date": "2025-11-16",
  "workload_status": "moderate",
  "active_projects": 3,
  "blocked_projects": 1,
  "completed_today": 2,
  "messages_handled": 5,
  "blockers_resolved": 1,
  "collaboration_score": 8.5,
  "focus_areas": [
    "marketplace architecture",
    "fibonacci optimization"
  ],
  "tomorrow_plan": [
    "Complete API specification",
    "Review padre's backend progress",
    "Start algorithm workshop planning"
  ]
}
```

### Why This Matters: Real-World Alignment

This approach mirrors how real software teams work:

| Real Team | Agent Team |
|-----------|------------|
| Daily standup | ASSESS_WORKLOAD |
| Slack messages | READ_POSTS / PREPARE_OUTBOX |
| JIRA board | Project tracking files |
| Code review requests | Messages between agents |
| Blockers | Explicit blocker state + messages |
| Sprint retrospective | REFLEX |
| Project handoffs | Dependency tracking |
| Knowledge sharing | Context files + message history |

**Result**: Agents that feel alive, adaptive, and genuinely collaborative.

---

## Current State Analysis

### Existing Actions in Loop 70

| Current Action | Status | Usage | Recommendation |
|----------------|--------|-------|----------------|
| WAKEUP | ✅ Keep | Health check | No change |
| RECEIVE_POST | ✅ Keep | Message receiving (called by agent_post) | No change |
| READ_POSTS | ✅ Keep | Process messages → create tasks | Already protocol-based ✓ |
| GET_WORK | ❌ Replace | OLD: Select task → create work plan | → **CREATE_PROJECT** |
| PREPARE_ACTION | ⚠️ Update | Prepare next action | Needs protocol |
| DO_ACTION | ❌ Replace | Execute action | → **RUN_SUBTASK** |
| VALIDATE_ACTION | ❌ Replace | Validate action result | → **VALIDATE_SUBTASK** |
| VALIDATE_WORK | ❌ Replace | Validate work result | → **VALIDATE_PROJECT** |
| REFLEX | ✅ Keep | Self-reflection | Already protocol-based ✓ |

### Existing Protocols

| Protocol File | Current Name | Status | New Name |
|---------------|--------------|--------|----------|
| read_posts_protocol.json | ✅ Good | Keep | read_posts_protocol.json |
| get_work_protocol.json | ❌ Outdated | Update | → create_project_protocol.json |
| validate_protocol.json | ⚠️ Generic | Split | → validate_subtask_protocol.json<br>→ validate_project_protocol.json |
| reflex_protocol.json | ✅ Good | Keep | reflex_protocol.json |
| N/A | ❌ Missing | Create | prepare_action_protocol.json |
| N/A | ❌ Missing | Create | run_subtask_protocol.json |

---

## Proposed Workflow Model: Adaptive & Context-Aware

### Adaptive Daily Workflow (NOT Rigid Sequence)

Unlike traditional automation that executes fixed sequences, agents make **context-aware decisions** each day:

```
┌─────────────────────────────────────────────────────────────────┐
│            AGENT'S ADAPTIVE DAILY WORKFLOW                       │
│  (Each agent independently decides what to work on)              │
└─────────────────────────────────────────────────────────────────┘

🌅 MORNING ROUTINE
─────────────────
1. WAKEUP
   └─> Send queued messages from yesterday
   └─> Wake up system, check health
   └─> Load agent's context and memory

2. READ_POSTS (Protocol-based ✓)
   └─> Process new inbox messages
   └─> Create tasks from requests/questions
   └─> Identify urgent vs normal priority
   └─> Example: "StudentMary sent code" → create fibonacci_review task

💼 WORKLOAD ASSESSMENT (NEW: ASSESS_WORKLOAD)
───────────────────────
3. ASSESS_WORKLOAD (NEW - Core Intelligence)

   Agent reviews ALL current state:
   ├─> Scan projects/{all}/status.json
   ├─> Identify project states:
   │   ├─> 🆕 NEW tasks in tasks/new/ → Can start
   │   ├─> 🔵 ACTIVE projects → Continue
   │   ├─> ⏸️ BLOCKED projects → Check if unblocked
   │   └─> ⏰ SCHEDULED projects → Check if ready
   │
   ├─> Check dependencies:
   │   └─> "fibonacci was blocked, but code arrived → NOW READY"
   │
   ├─> Evaluate priorities:
   │   ├─> Urgent messages → High priority
   │   ├─> Blocking others → High priority (don't block teammates)
   │   ├─> Near completion → Medium priority (finish what started)
   │   └─> New requests → Low/Medium priority
   │
   └─> MAKE DECISION:
       ├─> Option A: Start NEW project (if high-priority task exists)
       ├─> Option B: Continue ACTIVE project (make progress)
       ├─> Option C: Respond to BLOCKERS (unblock teammates)
       ├─> Option D: Wait/Idle (if everything blocked)
       └─> Can work on MULTIPLE projects in parallel!

   Example Decision:
   "I have 3 projects:
    - fibonacci_optimization (was blocked, NOW READY) → WORK 50%
    - marketplace_mvp (urgent, ACTIVE) → WORK 50%
    - workshop_planning (blocked on padre) → WAIT
   Decision: Split time between fibonacci + marketplace today"

🛠️ PROJECT EXECUTION (Adaptive Loop)
──────────────────────
4. WORK_ON_PROJECTS (NEW - Replaces rigid sequence)

   For each selected project:

   4a. Is project new? → CREATE_PROJECT
       └─> Transform task → project structure
       └─> Break into subtasks
       └─> Set up tracking
       └─> Status: NEW → ACTIVE

   4b. Is project active? → Continue work

       PREPARE_ACTION:
       ├─> Find next READY subtask (dependencies met)
       ├─> If ALL blocked → Send message, mark project BLOCKED
       ├─> If subtask ready → Gather context, prepare plan
       └─> Status: PENDING → IN_PROGRESS

       RUN_SUBTASK:
       ├─> Execute work based on action plan
       ├─> Generate deliverables
       ├─> If need info → Message colleague, mark BLOCKED
       ├─> If completed → Generate output files
       └─> Log execution details

       VALIDATE_SUBTASK:
       ├─> Check quality against success criteria
       ├─> If VALID → Mark COMPLETED, continue to next
       ├─> If INVALID → Document issues, retry
       └─> If BLOCKED → Message for help, mark WAITING

       Loop until:
       ├─> All subtasks done → Go to VALIDATE_PROJECT
       ├─> Hit blocker → Mark project BLOCKED, switch to other work
       ├─> Time limit reached → Save state, continue tomorrow
       └─> Urgent message arrived → Context switch

   4c. All project subtasks done? → VALIDATE_PROJECT
       ├─> Final quality check
       ├─> Verify all deliverables present
       ├─> Create completion report
       ├─> Archive: projects/{id} → projects/completed/{id}
       ├─> Mark: tasks/{task_id} → tasks/done/{task_id}
       └─> Send notification if applicable

🌆 END OF DAY
─────────────
5. PREPARE_OUTBOX (NEW)
   └─> Queue messages to send tomorrow morning
   └─> Update all project statuses
   └─> Document any blockers
   └─> Plan tomorrow's priorities based on today's progress

📊 WEEKLY REFLECTION
────────────────────
6. REFLEX (Every 5 days - Protocol-based ✓)
   └─> Review completed projects
   └─> Analyze team collaboration
   └─> Identify process improvements
   └─> Generate insights for efficiency
```

### Key Differences: Rigid vs Adaptive

| Aspect | OLD Rigid Workflow | NEW Adaptive Workflow |
|--------|-------------------|----------------------|
| **Decision Making** | Execute predetermined sequence | Agent decides based on context |
| **Multiple Projects** | ❌ One at a time | ✅ Can juggle multiple |
| **Blockers** | ❌ Stuck, waiting | ✅ Switch to other work, message for help |
| **Priorities** | ❌ Fixed order | ✅ Dynamic based on urgency/dependencies |
| **Collaboration** | ❌ Not considered | ✅ Actively coordinate with team |
| **State Awareness** | ❌ Blind execution | ✅ Full context of all projects |
| **Flexibility** | ❌ Can't adapt | ✅ Responds to changing conditions |

### Real-World Example: TeacherJohn's Adaptive Day

**Morning (9:00 AM):**
```
WAKEUP:
  - Sent 2 messages queued yesterday

READ_POSTS:
  - New message from StudentMary: "Here's my Fibonacci code"
  - New message from cityhall: "URGENT: marketplace architecture needed"
  - Created 2 tasks

ASSESS_WORKLOAD:
  Current projects:
  1. fibonacci_optimization
     - Status: BLOCKED → NOW READY (code arrived!)
     - Priority: Medium
     - Progress: 0% (just unblocked)

  2. marketplace_mvp_architecture
     - Status: NEW (just created from cityhall's message)
     - Priority: HIGH (marked urgent)
     - Progress: 0%

  3. algorithm_workshop
     - Status: BLOCKED (waiting for padre's availability)
     - Priority: Low
     - Progress: 10% (planning only)

  DECISION:
  - Start marketplace_mvp (urgent, 60% time)
  - Also work on fibonacci (now unblocked, 40% time)
  - Skip workshop (still blocked)
```

**Work Session 1 (9:30 AM - 11:30 AM):**
```
WORK_ON_PROJECTS(marketplace_mvp):
  - CREATE_PROJECT:
    * Break down into 4 subtasks
    * Create project structure
    * Status: NEW → ACTIVE

  - PREPARE_ACTION(subtask_001_requirements):
    * Load cityhall's request
    * Gather marketplace context
    * Create action plan

  - RUN_SUBTASK(001_requirements):
    * Analyze requirements
    * Create requirements document
    * Generate deliverable: requirements.md

  - VALIDATE_SUBTASK(001):
    * Check completeness → VALID
    * Mark: subtask_001 COMPLETED
    * Progress: 25%

  - PREPARE_ACTION(subtask_002_architecture):
    * Load requirements
    * Start architecture design
    * [OUT OF TIME - save state]
    * Status: subtask_002 IN_PROGRESS (50%)
```

**Work Session 2 (11:30 AM - 12:30 PM):**
```
WORK_ON_PROJECTS(fibonacci_optimization):
  - CREATE_PROJECT:
    * Break into 3 subtasks
    * Create project structure

  - PREPARE_ACTION(subtask_001_analyze):
    * Load StudentMary's code
    * Review implementation

  - RUN_SUBTASK(001_analyze):
    * Analyze code complexity
    * Identify bottlenecks
    * Create analysis report

  - VALIDATE_SUBTASK(001):
    * Check quality → VALID
    * Mark: subtask_001 COMPLETED
    * Progress: 33%
```

**Afternoon Check (1:00 PM):**
```
READ_POSTS (mid-day check):
  - New message from padre: "Question about marketplace API auth"
  - Creates task: "Answer padre's auth question"
  - Priority: HIGH (blocking teammate!)

ASSESS_WORKLOAD (re-evaluate):
  - padre is BLOCKED on my response → HIGH PRIORITY
  - Pause current work
  - Respond to padre immediately

WORK_ON_PROJECTS(respond_to_padre):
  - Quick message with auth approach
  - padre UNBLOCKED → Can continue backend work
```

**End of Day (5:00 PM):**
```
PREPARE_OUTBOX:
  - Message to padre: "Responded to your auth question"
  - Message to cityhall: "Marketplace requirements done, architecture 50% complete"
  - Message to StudentMary: "Analyzed your code, will send optimization suggestions tomorrow"

Update project statuses:
  - marketplace_mvp: ACTIVE, 37% complete (1.5/4 subtasks done)
  - fibonacci_optimization: ACTIVE, 33% complete (1/3 subtasks done)
  - algorithm_workshop: BLOCKED (waiting padre)

Tomorrow's plan:
  - Priority 1: Finish marketplace architecture (50% → 100%)
  - Priority 2: Continue fibonacci optimization
  - Check if workshop unblocked
```

### Orchestration Intelligence

The orchestration script doesn't dictate rigid sequences—it **enables autonomous agents**:

```python
# run_all_cycles.py (Adaptive version)

daily_workflow = {
    "morning": [
        "WAKEUP",          # All agents send messages
        "READ_POSTS",      # All agents read inbox
    ],
    "planning": [
        "ASSESS_WORKLOAD"  # Each agent decides what to work on
    ],
    "work": [
        "WORK_ON_PROJECTS" # Agents work on selected projects
                           # (internally: CREATE/PREPARE/RUN/VALIDATE as needed)
    ],
    "evening": [
        "PREPARE_OUTBOX"   # Queue tomorrow's messages
    ]
}

# Weekly reflection
if day % 5 == 0:
    run_action_for_all("REFLEX")
```

**Note:** The orchestration is **simple** because intelligence is in the **agents**, not the script!

### Comparison: OLD vs NEW

| Aspect | OLD (GET_WORK) | NEW (CREATE_PROJECT) |
|--------|----------------|---------------------|
| **Granularity** | Single "work" blob | Multiple subtasks |
| **Iteration** | One-shot execution | Iterative loop with validation |
| **Structure** | Flat current_work/ | Hierarchical projects/{id}/ |
| **Validation** | End-only | Per-subtask + project-level |
| **Tracking** | Unclear progress | Clear subtask completion states |
| **Flexibility** | Rigid | Adaptive (can add/remove subtasks) |

---

## Detailed Action Specifications

### 1. WAKEUP (Keep as-is)
**Purpose:** Health check and system readiness signal

**Type:** Simple lambda/bash executor

**No changes needed**

---

### 2. RECEIVE_POST (Keep as-is)
**Purpose:** Receive incoming messages (triggered by agent_post system)

**Type:** Lambda executor

**No changes needed**

---

### 3. READ_POSTS ✓ (Already protocol-based)
**Purpose:** Process inbox messages and create tasks

**Protocol:** `read_posts_protocol.json` ✓

**Status:** Working correctly, tested successfully

**No changes needed**

---

### 4. CREATE_PROJECT (NEW - replaces GET_WORK)
**Purpose:** Transform task into structured project with subtasks

**Current Name:** GET_WORK (to be renamed/replaced)

**Protocol:** Create `create_project_protocol.json` (evolved from get_work_protocol.json)

**Key Changes from GET_WORK:**
- More detailed project planning
- Break down into explicit subtasks with dependencies
- Create hierarchical project structure
- Define success criteria per subtask
- Estimate effort and complexity

**Input:**
- Protocol: `/protocols/create_project/create_project_protocol.json`
- Tasks: `/tasks/new/*.json`

**Output:**
- Project structure: `/projects/{project_id}/`
  - `project_plan.json` - Overall project plan
  - `subtasks/subtask_*.json` - Individual subtasks
  - `context.json` - Gathered context and resources
  - `status.json` - Project status tracking

**Example Project Plan:**
```json
{
  "project_id": "fibonacci_optimization_20251116",
  "source_task_id": "review_fibonacci_code",
  "objective": "Review and optimize Python Fibonacci function",
  "estimated_complexity": "medium",
  "subtasks": [
    {
      "subtask_id": "001_analyze_current",
      "title": "Analyze current implementation",
      "description": "Review StudentMary's code and identify bottlenecks",
      "estimated_effort": "1 hour",
      "dependencies": [],
      "deliverable": "analysis_report.md"
    },
    {
      "subtask_id": "002_design_solution",
      "title": "Design optimized solution",
      "description": "Design memoization or dynamic programming approach",
      "estimated_effort": "1 hour",
      "dependencies": ["001_analyze_current"],
      "deliverable": "optimization_design.md"
    },
    {
      "subtask_id": "003_implement",
      "title": "Implement optimized version",
      "description": "Write optimized code with proper documentation",
      "estimated_effort": "2 hours",
      "dependencies": ["002_design_solution"],
      "deliverable": "fibonacci_optimized.py"
    },
    {
      "subtask_id": "004_benchmark",
      "title": "Benchmark and compare",
      "description": "Run performance tests comparing old vs new",
      "estimated_effort": "1 hour",
      "dependencies": ["003_implement"],
      "deliverable": "benchmark_results.json"
    }
  ],
  "success_criteria": [
    "All subtasks completed",
    "Performance improvement demonstrated",
    "Code properly documented",
    "StudentMary receives clear recommendations"
  ],
  "created_at": "2025-11-16T11:00:00Z",
  "status": "in_progress"
}
```

---

### 5. PREPARE_ACTION (NEW - needs protocol)
**Purpose:** Prepare the next subtask for execution

**Current Status:** Exists but no protocol

**Protocol:** Create `prepare_action_protocol.json`

**Input:**
- Protocol: `/protocols/prepare_action/prepare_action_protocol.json`
- Current project: `/projects/{project_id}/`
- Subtasks: `/projects/{project_id}/subtasks/`

**Output:**
- Action plan: `/projects/{project_id}/current_action/action_plan.json`
- Context: `/projects/{project_id}/current_action/context.json`

**Workflow:**
1. Scan subtasks for next pending item (respecting dependencies)
2. Load subtask requirements
3. Gather necessary context from previous subtasks
4. Create detailed action plan
5. Set environment for RUN_SUBTASK

**Example Action Plan:**
```json
{
  "action_id": "action_20251116_110530",
  "subtask_id": "001_analyze_current",
  "subtask_title": "Analyze current implementation",
  "prepared_at": "2025-11-16T11:05:30Z",
  "context_loaded": [
    "StudentMary's original request",
    "Task requirements from project_plan.json"
  ],
  "deliverable_path": "/projects/fibonacci_optimization_20251116/deliverables/analysis_report.md",
  "success_criteria": [
    "Identify performance bottlenecks",
    "Document time complexity",
    "List optimization opportunities"
  ],
  "ready_to_execute": true
}
```

---

### 6. RUN_SUBTASK (NEW - replaces DO_ACTION)
**Purpose:** Execute the prepared subtask and generate deliverables

**Current Name:** DO_ACTION (to be renamed/replaced)

**Protocol:** Create `run_subtask_protocol.json`

**Input:**
- Protocol: `/protocols/run_subtask/run_subtask_protocol.json`
- Action plan: `/projects/{project_id}/current_action/action_plan.json`
- Context: `/projects/{project_id}/current_action/context.json`

**Output:**
- Deliverable: `/projects/{project_id}/deliverables/{filename}`
- Execution log: `/projects/{project_id}/current_action/execution_log.json`
- Artifacts: `/projects/{project_id}/artifacts/`

**Workflow:**
1. Load action plan
2. Understand requirements and success criteria
3. Execute subtask (LLM generates content)
4. Create deliverable files
5. Log execution details
6. Mark subtask as "pending_validation"

**Example Deliverable (analysis_report.md):**
```markdown
# Fibonacci Implementation Analysis

## Current Implementation Review
StudentMary's code uses recursive approach:
- Time complexity: O(2^n) - exponential
- Space complexity: O(n) - call stack
- No memoization

## Performance Bottlenecks
1. Redundant calculations: fib(5) called 5 times for fib(10)
2. No caching of intermediate results
3. Deep recursion for large n causes stack overflow

## Optimization Opportunities
1. Add memoization (dict or @lru_cache)
2. Use iterative dynamic programming
3. Consider matrix exponentiation for very large n

## Recommendations
Priority: Implement memoization - easiest with biggest impact
Expected improvement: O(2^n) → O(n)
```

---

### 7. VALIDATE_SUBTASK (NEW - replaces VALIDATE_ACTION)
**Purpose:** Validate completed subtask against success criteria

**Current Name:** VALIDATE_ACTION (to be renamed/replaced)

**Protocol:** Create `validate_subtask_protocol.json`

**Input:**
- Protocol: `/protocols/validate_subtask/validate_subtask_protocol.json`
- Subtask: `/projects/{project_id}/subtasks/{subtask_id}.json`
- Deliverable: `/projects/{project_id}/deliverables/{filename}`
- Action log: `/projects/{project_id}/current_action/execution_log.json`

**Output:**
- Validation report: `/projects/{project_id}/validations/subtask_{id}_validation.json`
- If valid: Update subtask status to "completed"
- If invalid: Create retry action with feedback

**Workflow:**
1. Load subtask success criteria
2. Review deliverable quality
3. Check completeness
4. Verify against requirements
5. Decision: VALID or INVALID
   - VALID: Mark complete, continue to next subtask
   - INVALID: Document issues, queue for retry

**Example Validation (Valid):**
```json
{
  "validation_id": "val_001_20251116_110800",
  "subtask_id": "001_analyze_current",
  "validated_at": "2025-11-16T11:08:00Z",
  "result": "VALID",
  "checks_passed": [
    "Bottlenecks identified",
    "Time complexity documented",
    "Optimization opportunities listed",
    "Clear recommendations provided"
  ],
  "quality_score": 9,
  "notes": "Excellent analysis with specific examples",
  "next_action": "proceed_to_next_subtask"
}
```

**Example Validation (Invalid):**
```json
{
  "validation_id": "val_001_20251116_110800",
  "subtask_id": "001_analyze_current",
  "validated_at": "2025-11-16T11:08:00Z",
  "result": "INVALID",
  "checks_failed": [
    "Missing time complexity analysis",
    "No concrete optimization suggestions"
  ],
  "issues": [
    "Analysis is too generic",
    "Lacks specific code examples",
    "No mention of memoization"
  ],
  "required_improvements": [
    "Add Big-O notation analysis",
    "Include code snippet examples",
    "Suggest specific Python optimization techniques"
  ],
  "next_action": "retry_subtask_with_feedback"
}
```

---

### 8. VALIDATE_PROJECT (NEW - replaces VALIDATE_WORK)
**Purpose:** Final validation of entire project completion

**Current Name:** VALIDATE_WORK (to be renamed/replaced)

**Protocol:** Create `validate_project_protocol.json`

**Input:**
- Protocol: `/protocols/validate_project/validate_project_protocol.json`
- Project: `/projects/{project_id}/`
- All subtasks: `/projects/{project_id}/subtasks/*.json`
- All deliverables: `/projects/{project_id}/deliverables/`

**Output:**
- Final report: `/projects/{project_id}/project_completion_report.json`
- If valid: Move project to `/projects/completed/{project_id}/`
- If invalid: Document missing pieces, queue remaining work

**Workflow:**
1. Verify all subtasks completed
2. Check all deliverables present
3. Validate against original task requirements
4. Assess overall quality
5. Decision: PROJECT_COMPLETE or INCOMPLETE
   - COMPLETE: Archive project, notify requester
   - INCOMPLETE: Document gaps, create follow-up tasks

**Example Project Validation:**
```json
{
  "validation_id": "proj_val_fibonacci_20251116",
  "project_id": "fibonacci_optimization_20251116",
  "validated_at": "2025-11-16T12:00:00Z",
  "result": "PROJECT_COMPLETE",
  "subtasks_completed": 4,
  "subtasks_total": 4,
  "deliverables_created": [
    "analysis_report.md",
    "optimization_design.md",
    "fibonacci_optimized.py",
    "benchmark_results.json"
  ],
  "success_criteria_met": [
    "All subtasks completed ✓",
    "Performance improvement demonstrated ✓",
    "Code properly documented ✓",
    "StudentMary receives clear recommendations ✓"
  ],
  "quality_assessment": {
    "completeness": 10,
    "quality": 9,
    "documentation": 10,
    "overall": 9.7
  },
  "recommendations": [
    "Send optimization guide to StudentMary",
    "Archive project as reference for future code reviews"
  ],
  "next_steps": [
    "Create outbound message to StudentMary",
    "Move to completed projects",
    "Mark original task as done"
  ]
}
```

---

### 9. REFLEX ✓ (Already protocol-based)
**Purpose:** Periodic self-reflection on completed work

**Protocol:** `reflex_protocol.json` ✓

**Status:** Working correctly

**No changes needed** - runs every 5 days via orchestration

---

## File System Structure Changes

### OLD Structure (current_work/)
```
/agentlife/
├── tasks/
│   ├── new/              # Incoming tasks
│   ├── running/          # Active task (single)
│   └── done/             # Completed tasks
├── current_work/         # Flat work directory
│   ├── task.json
│   ├── working_plan.json
│   ├── related_content.json
│   └── current_operation/
│       └── result/
└── post/
    ├── inbox/
    └── outbox/
```

**Problems:**
- ❌ Flat structure - hard to track progress
- ❌ Only one task at a time
- ❌ No subtask granularity
- ❌ Unclear completion state

### NEW Structure (projects/)
```
/agentlife/
├── tasks/
│   ├── new/              # Incoming tasks
│   └── done/             # Completed tasks (moved after validation)
│
├── projects/             # NEW: Project-based structure
│   ├── {project_id}/     # Active project
│   │   ├── project_plan.json
│   │   ├── status.json
│   │   ├── context.json
│   │   ├── subtasks/
│   │   │   ├── subtask_001.json (status: completed)
│   │   │   ├── subtask_002.json (status: in_progress)
│   │   │   └── subtask_003.json (status: pending)
│   │   ├── current_action/
│   │   │   ├── action_plan.json
│   │   │   ├── context.json
│   │   │   └── execution_log.json
│   │   ├── deliverables/
│   │   │   ├── analysis_report.md
│   │   │   ├── optimization_design.md
│   │   │   └── fibonacci_optimized.py
│   │   ├── validations/
│   │   │   ├── subtask_001_validation.json
│   │   │   └── subtask_002_validation.json
│   │   └── artifacts/
│   │       └── benchmark_results.json
│   │
│   └── completed/        # Archived successful projects
│       └── {project_id}/
│           └── project_completion_report.json
│
├── post/
│   ├── inbox/
│   └── outbox/
│
└── reflections/
    └── new/
```

**Benefits:**
- ✅ Clear project isolation
- ✅ Granular subtask tracking
- ✅ Progress visibility
- ✅ Easy to resume/rollback
- ✅ Deliverables organized
- ✅ Validation history preserved

---

## Protocol Files Specification

### Protocols to CREATE

#### 1. create_project_protocol.json
**Location:** `/protocols/create_project/create_project_protocol.json`

**Key Sections:**
```json
{
  "protocol_version": "2.0",
  "protocol_id": "create_project",
  "instruction": "Transform a task into a structured project with subtasks",
  "steps": [
    {"step_id": "select_task", "action": "Choose highest-priority task"},
    {"step_id": "analyze_requirements", "action": "Break down requirements"},
    {"step_id": "create_subtasks", "action": "Define granular subtasks"},
    {"step_id": "estimate_effort", "action": "Estimate complexity and time"},
    {"step_id": "define_deliverables", "action": "Specify expected outputs"},
    {"step_id": "create_structure", "action": "Generate project files"}
  ],
  "example_output": {
    "updated_files": [
      {"path": "projects/{id}/project_plan.json", "file_operation": "create"},
      {"path": "projects/{id}/subtasks/subtask_*.json", "file_operation": "create"}
    ]
  }
}
```

#### 2. prepare_action_protocol.json
**Location:** `/protocols/prepare_action/prepare_action_protocol.json`

**Key Sections:**
```json
{
  "protocol_version": "2.0",
  "protocol_id": "prepare_action",
  "instruction": "Prepare next subtask for execution",
  "steps": [
    {"step_id": "identify_next", "action": "Find next pending subtask"},
    {"step_id": "check_dependencies", "action": "Verify dependencies met"},
    {"step_id": "gather_context", "action": "Load required context"},
    {"step_id": "create_plan", "action": "Generate detailed action plan"}
  ]
}
```

#### 3. run_subtask_protocol.json
**Location:** `/protocols/run_subtask/run_subtask_protocol.json`

**Key Sections:**
```json
{
  "protocol_version": "2.0",
  "protocol_id": "run_subtask",
  "instruction": "Execute subtask and generate deliverables",
  "steps": [
    {"step_id": "load_plan", "action": "Read action plan"},
    {"step_id": "execute", "action": "Perform subtask work"},
    {"step_id": "create_deliverable", "action": "Generate output files"},
    {"step_id": "log_execution", "action": "Document what was done"}
  ]
}
```

#### 4. validate_subtask_protocol.json
**Location:** `/protocols/validate_subtask/validate_subtask_protocol.json`

**Key Sections:**
```json
{
  "protocol_version": "2.0",
  "protocol_id": "validate_subtask",
  "instruction": "Validate subtask completion and quality",
  "validation_criteria": [
    "Deliverable exists",
    "Success criteria met",
    "Quality acceptable",
    "No obvious errors"
  ],
  "decision_paths": {
    "valid": "mark_complete_continue_next",
    "invalid": "document_issues_queue_retry"
  }
}
```

#### 5. validate_project_protocol.json
**Location:** `/protocols/validate_project/validate_project_protocol.json`

**Key Sections:**
```json
{
  "protocol_version": "2.0",
  "protocol_id": "validate_project",
  "instruction": "Final validation of entire project",
  "steps": [
    {"step_id": "check_subtasks", "action": "Verify all subtasks complete"},
    {"step_id": "check_deliverables", "action": "Confirm all outputs present"},
    {"step_id": "assess_quality", "action": "Evaluate overall quality"},
    {"step_id": "verify_objectives", "action": "Check original task met"}
  ],
  "completion_actions": [
    "Create project completion report",
    "Archive project to completed/",
    "Move task to done/",
    "Notify requester if applicable"
  ]
}
```

### Protocols to UPDATE

#### get_work_protocol.json → create_project_protocol.json
- Rename file and directory
- Update from "work plan" to "project with subtasks"
- Add subtask breakdown logic
- Add dependency management
- Add deliverable specification

#### validate_protocol.json → Split into two:
- validate_subtask_protocol.json (granular validation)
- validate_project_protocol.json (final validation)

---

## Migration Plan

### Phase 1: Preparation (Day 1)
**Status:** 📋 Planning

1. **Backup current configuration**
   ```bash
   cd /loopai_src/var/users/1/loops/70
   tar -czf ~/loop70_pre_workflow_update_$(date +%Y%m%d).tar.gz .
   ```

2. **Create new protocol files**
   - create_project_protocol.json
   - prepare_action_protocol.json
   - run_subtask_protocol.json
   - validate_subtask_protocol.json
   - validate_project_protocol.json

3. **Update protocol directory structure**
   ```
   protocols/
   ├── read_posts/         (keep)
   ├── create_project/     (new, from get_work)
   ├── prepare_action/     (new)
   ├── run_subtask/        (new)
   ├── validate_subtask/   (new)
   ├── validate_project/   (new)
   └── reflex/             (keep)
   ```

### Phase 2: YAML Configuration Updates (Day 1)
**Status:** 📋 Planning

1. **Rename/Update YAML files**
   - GET_WORK.yaml → CREATE_PROJECT.yaml
   - DO_ACTION.yaml → RUN_SUBTASK.yaml
   - VALIDATE_ACTION.yaml → VALIDATE_SUBTASK.yaml
   - VALIDATE_WORK.yaml → VALIDATE_PROJECT.yaml
   - Update PREPARE_ACTION.yaml (add protocol)

2. **Update input paths in all YAMLs**
   - Point to new protocol directories
   - Update filesystem paths to projects/ structure

3. **Update Python config files**
   - GET_WORK.py → CREATE_PROJECT.py
   - DO_ACTION.py → RUN_SUBTASK.py
   - VALIDATE_ACTION.py → VALIDATE_SUBTASK.py
   - VALIDATE_WORK.py → VALIDATE_PROJECT.py
   - Update PREPARE_ACTION.py

4. **Remove unused configs**
   - Archive old GET_WORK files to backup
   - Clean up any legacy configs

### Phase 3: Filesystem Migration (Day 1)
**Status:** 📋 Planning

1. **Create new directory structure**
   ```bash
   mkdir -p /agentlife/projects
   mkdir -p /agentlife/projects/completed
   ```

2. **Migrate existing work (if any)**
   - Move current_work/ content to projects/ format
   - Archive old structure

### Phase 4: Testing (Day 2)
**Status:** 📋 Planning

1. **Test individual actions**
   - CREATE_PROJECT: Select task → create project structure
   - PREPARE_ACTION: Load subtask → create action plan
   - RUN_SUBTASK: Execute → generate deliverable
   - VALIDATE_SUBTASK: Check quality → mark complete/retry
   - VALIDATE_PROJECT: Final check → archive

2. **Test full workflow**
   ```bash
   # Send test message
   curl http://localhost:5050/api/public/agent/8/action/READ_POSTS/

   # Run full cycle
   curl http://localhost:5050/api/public/agent/8/action/CREATE_PROJECT/
   curl http://localhost:5050/api/public/agent/8/action/PREPARE_ACTION/
   curl http://localhost:5050/api/public/agent/8/action/RUN_SUBTASK/
   curl http://localhost:5050/api/public/agent/8/action/VALIDATE_SUBTASK/
   # Repeat PREPARE/RUN/VALIDATE for each subtask
   curl http://localhost:5050/api/public/agent/8/action/VALIDATE_PROJECT/
   ```

3. **Verify outputs**
   - Check project structure created correctly
   - Verify subtask progression
   - Validate deliverables generated
   - Confirm project completion

### Phase 5: Orchestration Update (Day 2)
**Status:** 📋 Planning

1. **Update run_all_cycles.py**
   ```python
   daily_actions = [
       "READ_POSTS",
       "CREATE_PROJECT",
       "PREPARE_ACTION",
       "RUN_SUBTASK",
       "VALIDATE_SUBTASK",
       # Loop PREPARE/RUN/VALIDATE until all subtasks done
       "VALIDATE_PROJECT"
   ]
   ```

2. **Implement subtask loop logic**
   - Check if subtasks remain
   - If yes: PREPARE → RUN → VALIDATE (repeat)
   - If no: VALIDATE_PROJECT

3. **Test multi-day cycles**
   ```bash
   python run_all_cycles.py --days 5
   ```

### Phase 6: Rollout to Other Agents (Week 2)
**Status:** 📋 Future

1. Loop 71 (cityhall)
2. Loop 72 (padre)
3. Loop 73 (maria)
4. Loop 74 (zhou)

---

## Updated Daily Orchestration

### Revised run_all_cycles.py Logic

```python
daily_actions = [
    "READ_POSTS",        # Process messages → tasks
    "CREATE_PROJECT"     # Select task → project + subtasks
]

subtask_loop = [
    "PREPARE_ACTION",    # Prepare next subtask
    "RUN_SUBTASK",       # Execute subtask
    "VALIDATE_SUBTASK"   # Validate completion
]

project_finalization = [
    "VALIDATE_PROJECT"   # Final project validation
]

reflex_action = "REFLEX"  # Every 5 days
```

### Execution Flow
```
Day N:
  1. READ_POSTS
  2. CREATE_PROJECT (if new tasks exist)
  3. Loop until all subtasks complete:
     - PREPARE_ACTION
     - RUN_SUBTASK
     - VALIDATE_SUBTASK
     - Check: More subtasks? If yes, repeat
  4. VALIDATE_PROJECT (when all subtasks done)

Day N % 5 == 0:
  5. REFLEX
```

---

## Success Metrics

### Key Performance Indicators

| Metric | Target | Measurement |
|--------|--------|-------------|
| Subtask completion rate | >90% | Subtasks completed without retry |
| Project completion time | <1 day | Time from CREATE_PROJECT to VALIDATE_PROJECT |
| Quality score | >8.5/10 | Average validation quality score |
| Iteration count | <1.5 | Average retries per subtask |
| Deliverable accuracy | 100% | All required deliverables present |

### Qualitative Goals

- ✅ Clear progress visibility
- ✅ Easy to understand what agent is doing
- ✅ Ability to pause/resume projects
- ✅ Granular tracking for debugging
- ✅ Reusable project templates

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Protocol instructions unclear | High | Extensive testing, clear examples |
| Subtask loop infinite | High | Add max iteration limit, timeout |
| File structure too complex | Medium | Simplify if needed, add cleanup |
| LLM context overflow | Medium | Limit context size, summarize |
| Validation too strict | Low | Adjust criteria based on results |

---

## Rollback Plan

If new workflow doesn't work:

1. **Stop orchestration**
   ```bash
   docker stop loopai_web
   ```

2. **Restore backup**
   ```bash
   cd /loopai_src/var/users/1/loops
   rm -rf 70
   tar -xzf ~/loop70_pre_workflow_update_*.tar.gz
   mv loop70_backup_* 70
   ```

3. **Restart system**
   ```bash
   docker start loopai_web
   ```

4. **Verify with old workflow**
   ```bash
   curl http://localhost:5050/api/public/agent/8/action/GET_WORK/
   ```

---

## Next Steps

### Immediate Actions Required

1. **Review this document** - Confirm approach is correct
2. **Create protocol files** - Write all 5 new protocols
3. **Update YAML configs** - Rename and modify action YAMLs
4. **Update Python configs** - Simplify with protocol references
5. **Create filesystem structure** - Set up projects/ directory
6. **Test single action** - Verify CREATE_PROJECT works
7. **Test full workflow** - Run complete cycle end-to-end
8. **Update orchestration** - Modify run_all_cycles.py
9. **Deploy to production** - Replace GET_WORK with new workflow

### Questions to Answer

1. Should we keep GET_WORK as fallback during transition?
2. How many subtasks is reasonable per project? (suggest 3-8)
3. Should subtask retry have a limit? (suggest max 2 retries)
4. Do we need project priority/queuing if multiple tasks exist?
5. Should PREPARE_ACTION auto-detect next subtask or require manual trigger?

---

## Appendix A: File Naming Conventions

### Project IDs
```
Format: {task_name}_{YYYYMMDD}_{HHMMSS}
Example: fibonacci_optimization_20251116_110000
```

### Subtask IDs
```
Format: {sequence_number}_{brief_name}
Example: 001_analyze_current
Example: 002_design_solution
```

### Deliverable Names
```
Format: {descriptive_name}.{extension}
Example: analysis_report.md
Example: fibonacci_optimized.py
Example: benchmark_results.json
```

### Validation IDs
```
Format: val_{subtask_id}_{YYYYMMDD}_{HHMMSS}
Example: val_001_20251116_110800
```

---

## Appendix B: Action Dependencies

```
WAKEUP
  └─> Health check (standalone)

RECEIVE_POST
  └─> Triggered by agent_post (standalone)

READ_POSTS
  └─> Creates tasks in tasks/new/

CREATE_PROJECT
  ├─> Depends on: tasks in tasks/new/
  └─> Creates: projects/{id}/

PREPARE_ACTION
  ├─> Depends on: projects/{id}/ with pending subtasks
  └─> Creates: current_action/action_plan.json

RUN_SUBTASK
  ├─> Depends on: current_action/action_plan.json
  └─> Creates: deliverables/{filename}

VALIDATE_SUBTASK
  ├─> Depends on: deliverables/{filename}
  └─> Marks: subtask complete OR retry

(Loop back to PREPARE_ACTION if more subtasks)

VALIDATE_PROJECT
  ├─> Depends on: all subtasks complete
  └─> Archives: projects/completed/{id}/

REFLEX (Every 5 days)
  ├─> Depends on: completed projects
  └─> Creates: reflections/new/
```

---

## Appendix C: Comparison with Industry Practices

### This Workflow vs. Software Development

| Our Workflow | Software Dev Equivalent |
|--------------|------------------------|
| CREATE_PROJECT | Sprint planning, breaking stories into tasks |
| PREPARE_ACTION | Pull next ticket from backlog, assign to dev |
| RUN_SUBTASK | Developer implements feature |
| VALIDATE_SUBTASK | Code review, unit tests |
| VALIDATE_PROJECT | Integration testing, acceptance criteria |
| REFLEX | Retrospective, process improvement |

**Alignment:** ✅ This workflow mirrors real-world iterative development practices!

---

**Document Status:** 📋 Draft - Awaiting Review and Approval
**Next Review Date:** 2025-11-16 (Today)
**Approval Required From:** User
**Implementation Start:** Upon approval
