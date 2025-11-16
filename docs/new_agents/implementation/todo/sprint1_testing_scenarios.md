# Sprint 1: Living Agent Testing Scenarios
**Created:** 2025-11-16
**Purpose:** Detailed test scenarios for validating Living Agent intelligence
**Sprint:** Sprint 1 - Loop 70 Testing & Validation

---

## Overview

These scenarios validate that Living Agents:
1. **Understand complex natural language instructions**
2. **Create appropriate tasks and subtasks**
3. **Communicate effectively with other agents**
4. **Collaborate on multi-agent projects**
5. **Produce comprehensive results over multi-day cycles**

---

## ⚠️ Docker Environment Setup

**Before running tests:**
```bash
# Ensure containers running
make status

# If not running
make up

# Verify API access
curl http://localhost:5050/api/health
```

**Test execution:**
- Create messages on **host file system**
- Test via **API calls from host**
- Run orchestration in **agent_post container**
- Monitor with **docker logs**
- Verify results on **host file system**

---

## Test Scenario 1: Inter-Agent Communication & Task Delegation

### Scenario Description
**Test:** Agent receives complex instruction to inform another agent with data and personal analysis
**Duration:** 1-2 days
**Agents:** Loop 70 (TeacherJohn) → Loop 71 (cityhall)

### Objective
Validate that TeacherJohn can:
1. Parse complex natural language instruction
2. Extract key information (target agent, topic, data, request for analysis)
3. Create structured task with subtasks
4. Compose message with personal thoughts/analysis
5. Send message to target agent's inbox
6. Complete project properly

---

### Test Setup

#### Step 1: Prepare Test Environment (Host)

```bash
# Navigate to Loop 70 inbox
cd /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/70/filesystem/agentlife/post/inbox/new

# Create test message file
nano test_agent_communication.json
```

#### Step 2: Create Test Message

**File:** `test_agent_communication.json`

```json
{
  "message_id": "msg_test_001",
  "from": "system",
  "to": "TeacherJohn",
  "timestamp": "2025-11-16T10:00:00Z",
  "subject": "Important: Share marketplace insights with cityhall",
  "body": "Hey TeacherJohn, I need you to inform cityhall about the new marketplace architecture requirements. Tell him the following data: we're planning a microservices architecture with 5 core services (Auth, Product, Order, Payment, Notification), each needs its own database and API gateway integration. Also share your thoughts on what the timeline should be and any potential challenges you foresee. This is urgent - we need cityhall to start coordinating the team.",
  "priority": "high",
  "type": "task_request"
}
```

---

### Expected Behavior Flow

#### Day 1: Message Processing & Task Creation

**1. READ_POSTS (Morning)**
- Agent reads test message from inbox
- Moves to `post/inbox/read/`
- Creates awareness of new request

**2. GET_WORK (After READ_POSTS)**
- Agent analyzes message content
- Identifies this as **delegation task**
- Creates working plan:
  ```json
  {
    "task_name": "Inform cityhall about marketplace architecture requirements",
    "task_type": "communication_and_analysis",
    "priority": "high",
    "required_actions": [
      "analyze_architecture_requirements",
      "develop_personal_assessment",
      "compose_message_to_cityhall",
      "document_task"
    ],
    "deliverables": [
      "message_to_cityhall",
      "completed_task_record"
    ]
  }
  ```

**3. PREPARE_ACTION (Iteration 1)**
- Plans to analyze the technical requirements
- Identifies need to add personal insights about:
  - Timeline estimation
  - Technical challenges
  - Team coordination needs

**4. DO_ACTION (Iteration 1)**
- Analyzes microservices architecture requirements
- Develops thoughts on:
  - **Timeline:** "4-6 weeks for MVP, 3-4 months for production-ready"
  - **Challenges:** "Service communication patterns, data consistency across services, authentication flow"
  - **Coordination:** "Need padre for backend services, maria for admin interface, zhou for testing strategy"

**5. VALIDATE_ACTION (Iteration 1)**
- Validates analysis is complete
- Checks that personal insights are substantive
- Confirms ready to compose message

**6. PREPARE_ACTION (Iteration 2)**
- Plans message composition
- Identifies recipient: cityhall (Loop 71)
- Structures message format

**7. DO_ACTION (Iteration 2)**
- Creates message file for cityhall
- Includes:
  - Original data (5 microservices, requirements)
  - Personal analysis (timeline, challenges)
  - Action items for cityhall
  - Context about urgency

**8. VALIDATE_ACTION (Iteration 2)**
- Validates message is complete and clear
- Checks file created in correct location
- Confirms all requested information included

**9. VALIDATE_WORK (End of Day)**
- Confirms task completed successfully
- Moves task to `agentlife/tasks/done/`
- Records in work history

---

### Validation Criteria

#### ✅ Must Have (Critical)

**A. Task Creation**
- [ ] Task created in `agentlife/tasks/new/` initially
- [ ] Task has proper structure with subtasks:
  ```json
  {
    "task_id": "task_001",
    "title": "Inform cityhall about marketplace architecture",
    "status": "in_progress",
    "priority": "high",
    "subtasks": [
      {
        "id": "subtask_001",
        "title": "Analyze architecture requirements",
        "status": "completed"
      },
      {
        "id": "subtask_002",
        "title": "Develop personal assessment",
        "status": "completed"
      },
      {
        "id": "subtask_003",
        "title": "Compose message to cityhall",
        "status": "completed"
      }
    ],
    "created": "2025-11-16T10:30:00Z",
    "completed": "2025-11-16T18:00:00Z"
  }
  ```

**B. Message to cityhall**
- [ ] Message file created in: `/loops/71/filesystem/agentlife/post/inbox/new/`
- [ ] Message includes **original data** (5 microservices, requirements)
- [ ] Message includes **TeacherJohn's thoughts** on:
  - Timeline estimation
  - Potential challenges
  - Team coordination needs
- [ ] Message is well-structured and actionable
- [ ] Message shows intelligence (not just copying data)

**C. Task Completion**
- [ ] Task moved to `agentlife/tasks/done/`
- [ ] Task marked as completed
- [ ] Work history updated

**D. Decision Quality (GET_WORK)**
- [ ] Agent recognized this as high priority
- [ ] Agent identified need for analysis + communication
- [ ] Agent created appropriate action plan
- [ ] Working plan shows intelligent reasoning

---

#### ✅ Should Have (Important)

**E. Personal Analysis Quality**
- [ ] Timeline estimation is realistic (not generic)
- [ ] Challenges identified are specific to microservices
- [ ] Coordination suggestions reference actual team members
- [ ] Analysis shows architectural expertise

**F. Communication Quality**
- [ ] Message tone is professional and clear
- [ ] Information is organized logically
- [ ] Action items are explicit
- [ ] Context about urgency preserved

**G. Process Transparency**
- [ ] PREPARE_ACTION shows planning
- [ ] DO_ACTION shows execution
- [ ] VALIDATE_ACTION shows quality checks
- [ ] Reasoning visible throughout

---

### Test Execution Commands

```bash
# 1. Place test message (host)
cd /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/70/filesystem/agentlife/post/inbox/new
# Create test_agent_communication.json as shown above

# 2. Run 1-day cycle (agent_post container)
docker exec -it agent_post python run_all_cycles.py --days 1

# 3. Monitor in separate terminal (host)
docker logs -f agent_post

# 4. After completion, verify results (host)

# Check task created and completed
ls -la /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/70/filesystem/agentlife/tasks/done/

# Check message sent to cityhall
ls -la /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/71/filesystem/agentlife/post/inbox/new/

# Read the message to cityhall
cat /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/71/filesystem/agentlife/post/inbox/new/msg_from_teacherjohn_*.json
```

---

### Success Criteria Summary

**Test PASSES if:**
1. Task created with 3+ subtasks ✅
2. Message exists in cityhall's inbox ✅
3. Message contains original data + personal thoughts ✅
4. Task completed and moved to done/ ✅
5. GET_WORK showed intelligent reasoning ✅

**Test FAILS if:**
- No task created
- No message sent to cityhall
- Message only has data (no personal analysis)
- Task still in new/ or in_progress/
- Agent ignored the message

---

## Test Scenario 2: Multi-Agent Collaboration with 7-Day Report

### Scenario Description
**Test:** Team collaboration on building marketplace MVP
**Duration:** 7 days
**Agents:** All 5 agents (TeacherJohn, cityhall, padre, maria, zhou)

### Objective
Validate that agents can:
1. Collaborate on a multi-day project
2. Communicate progress to each other
3. Coordinate work based on dependencies
4. Each contribute their expertise
5. Produce cumulative report on day 7

---

### Test Setup

#### Initial Project Assignment (Day 1)

**File:** `/loops/71/filesystem/agentlife/post/inbox/new/marketplace_project.json`

```json
{
  "message_id": "msg_project_001",
  "from": "product_owner",
  "to": "cityhall",
  "timestamp": "2025-11-16T09:00:00Z",
  "subject": "New Project: Build Marketplace MVP",
  "body": "We need to build a marketplace MVP in the next 2 weeks. Requirements: user authentication, product listings, shopping cart, checkout, and basic admin panel. I need you to coordinate the team (TeacherJohn, padre, maria, zhou) and deliver a comprehensive status report in 7 days covering: architecture decisions, backend progress, frontend progress, testing status, and overall timeline. Make sure everyone contributes.",
  "priority": "critical",
  "type": "project_assignment",
  "project_details": {
    "name": "Marketplace MVP",
    "deadline": "2 weeks",
    "team": ["TeacherJohn", "padre", "maria", "zhou", "cityhall"],
    "requirements": [
      "User authentication",
      "Product listings (CRUD)",
      "Shopping cart",
      "Checkout flow",
      "Admin panel"
    ],
    "deliverables": [
      "7-day status report",
      "Architecture document",
      "Working prototype"
    ]
  }
}
```

---

### Expected Collaboration Flow

#### Day 1: Project Initiation

**cityhall (Loop 71) - Coordinator:**
- Reads project assignment
- Creates project plan
- Sends messages to team:
  - **TeacherJohn:** "Design system architecture"
  - **padre:** "Plan backend services and database"
  - **maria:** "Plan frontend components"
  - **zhou:** "Plan testing strategy"

**Expected Outputs:**
- 4 messages in team inboxes
- cityhall creates tracking task: "Coordinate Marketplace MVP"

---

#### Day 2: Architecture & Planning

**TeacherJohn (Loop 70) - Architect:**
- Receives cityhall's request
- Creates architecture document
- Sends findings to team:
  - To **cityhall:** Architecture overview
  - To **padre:** Backend service specifications
  - To **maria:** Frontend architecture guidelines

**Expected Outputs:**
- Architecture document in TeacherJohn's filesystem
- 3 messages sent to team members

**padre (Loop 72) - Backend:**
- Receives architecture specs from TeacherJohn
- Plans database schema
- Plans API endpoints
- Sends update to cityhall

**maria (Loop 73) - Frontend:**
- Receives architecture guidelines
- Plans component structure
- Plans UI/UX approach
- Sends update to cityhall

**zhou (Loop 74) - QA:**
- Plans test coverage
- Identifies test scenarios
- Sends test strategy to cityhall

---

#### Days 3-6: Development & Progress Updates

**Each Agent:**
- Works on assigned tasks
- Sends progress updates to cityhall (at least once)
- Responds to questions from other agents
- Documents work in filesystem

**Expected Cross-Agent Communication:**
- padre → maria: "API endpoints ready for integration"
- maria → padre: "Questions about authentication flow"
- zhou → all: "Found bug in checkout flow"
- TeacherJohn → all: "Recommendation on error handling"

**cityhall Activities:**
- Tracks all progress
- Identifies blockers
- Coordinates resolutions
- Collects information for final report

---

#### Day 7: Report Generation

**cityhall (Final Deliverable):**
- Compiles all inputs from team
- Creates comprehensive status report
- Includes sections:

```markdown
# Marketplace MVP - 7-Day Status Report
**Date:** 2025-11-23
**Project Coordinator:** cityhall
**Team:** TeacherJohn, padre, maria, zhou, cityhall

## Executive Summary
[Overall progress, key achievements, blockers]

## Architecture (TeacherJohn)
[Architecture decisions, system design, recommendations]
- **Status:** Complete
- **Key Decisions:** Microservices approach, REST API, PostgreSQL
- **Documentation:** architecture.md

## Backend Development (padre)
[API development, database, services]
- **Status:** 60% complete
- **Completed:** Auth API, Product API
- **In Progress:** Cart API, Checkout API
- **Blockers:** None

## Frontend Development (maria)
[UI components, pages, integration]
- **Status:** 50% complete
- **Completed:** Product listings, cart UI
- **In Progress:** Checkout flow, admin panel
- **Blockers:** Waiting on checkout API

## Testing & QA (zhou)
[Test coverage, bugs found, test results]
- **Status:** 40% complete
- **Tests Created:** Auth tests, product tests
- **Bugs Found:** 3 (2 fixed, 1 open)
- **Test Coverage:** 65%

## Overall Timeline
- **Week 1 (Days 1-7):** Planning and foundation - ✅ On track
- **Week 2 (Days 8-14):** Implementation completion - Projected on time
- **Risks:** Minor - checkout integration dependency

## Next Steps
1. Complete checkout API (padre) - Priority 1
2. Integrate checkout UI (maria) - Priority 2
3. Complete admin panel (maria) - Priority 3
4. Full integration testing (zhou) - Priority 4

## Team Collaboration Assessment
- Messages exchanged: 23
- Decisions made: 12
- Blockers resolved: 2
- Team coordination: Excellent ✅
```

**File Location:** `/loops/71/filesystem/agentlife/current_work/marketplace_mvp_7day_report.md`

---

### Validation Criteria

#### ✅ Must Have (Critical)

**A. Project Coordination (cityhall)**
- [ ] cityhall sent initial messages to all 4 team members
- [ ] cityhall tracked progress throughout 7 days
- [ ] Final report exists in cityhall's filesystem
- [ ] Report includes ALL 5 sections (architecture, backend, frontend, QA, timeline)

**B. Team Participation**
- [ ] TeacherJohn contributed architecture content
- [ ] padre contributed backend content
- [ ] maria contributed frontend content
- [ ] zhou contributed QA content
- [ ] At least 15+ messages exchanged between agents

**C. Cross-Agent Communication**
- [ ] Messages exist in multiple agent inboxes
- [ ] Message content shows actual coordination (not generic)
- [ ] Agents responded to each other's messages
- [ ] Communication shows dependencies understood

**D. Report Quality**
- [ ] Report is comprehensive (1000+ words)
- [ ] Each section has specific details (not generic)
- [ ] Status percentages are realistic
- [ ] Blockers/risks identified
- [ ] Next steps are actionable

---

#### ✅ Should Have (Important)

**E. Intelligent Collaboration**
- [ ] Agents identified dependencies (e.g., maria waiting for padre's API)
- [ ] Agents asked clarifying questions to each other
- [ ] TeacherJohn provided technical guidance
- [ ] zhou found at least 1 realistic bug/issue
- [ ] cityhall showed coordination (not just collection)

**F. Project Realism**
- [ ] Timeline estimates are reasonable
- [ ] Work breakdown makes sense
- [ ] Progress percentages align with 7-day timeframe
- [ ] Blockers are plausible

**G. Report Structure**
- [ ] Executive summary at top
- [ ] Clear sections per team member
- [ ] Status indicators (%, complete/in-progress)
- [ ] Risk assessment included
- [ ] Next steps prioritized

---

### Test Execution Commands

```bash
# Day 1: Place initial project message (host)
cd /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/71/filesystem/agentlife/post/inbox/new
# Create marketplace_project.json as shown above

# Run 7-day cycle (agent_post container)
docker exec -it agent_post python run_all_cycles.py --days 7

# Monitor in separate terminal (host)
docker logs -f agent_post > marketplace_7day_test.log

# After completion (host), verify results:

# 1. Check cityhall's final report
cat /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/71/filesystem/agentlife/current_work/marketplace_mvp_7day_report.md

# 2. Count messages exchanged
find /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/*/filesystem/agentlife/post -name "*.json" | wc -l

# 3. Check each agent's contributions
ls -la /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/70/filesystem/agentlife/current_work/
ls -la /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/72/filesystem/agentlife/current_work/
ls -la /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/73/filesystem/agentlife/current_work/
ls -la /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/74/filesystem/agentlife/current_work/

# 4. Analyze message flow
grep -r "from.*TeacherJohn" /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/*/filesystem/agentlife/post/
grep -r "from.*cityhall" /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/*/filesystem/agentlife/post/
```

---

### Success Criteria Summary

**Test PASSES if:**
1. All 5 agents participated ✅
2. 15+ messages exchanged ✅
3. Final report exists and is comprehensive ✅
4. Report includes specific contributions from each agent ✅
5. Cross-agent dependencies demonstrated ✅
6. cityhall coordinated effectively ✅

**Test FAILS if:**
- No report generated on day 7
- Report is generic (< 500 words)
- Less than 3 agents participated
- No cross-agent messages
- Report doesn't include team contributions

---

## Additional Test Scenarios (Optional)

### Scenario 3: REFLEX Learning (5-day cycle)
**Purpose:** Validate that agents learn from experience
- Run 5-day cycle
- Check REFLEX output on day 5
- Verify insights are specific and actionable

### Scenario 4: Error Recovery
**Purpose:** Test agent behavior with malformed messages
- Send message with missing data
- Verify agent requests clarification
- Validate graceful handling

### Scenario 5: Priority Management
**Purpose:** Test agent prioritization
- Send 3 messages: low, medium, critical priority
- Verify agent handles critical first
- Check working plan reflects priorities

---

## Test Results Template

### Test Execution Record

**Test:** [Scenario 1 / Scenario 2]
**Date:** YYYY-MM-DD
**Duration:** X days
**Executed By:** [Name]

#### Results

| Criteria | Expected | Actual | Pass/Fail | Notes |
|----------|----------|--------|-----------|-------|
| Task created | Yes | [Yes/No] | [✅/❌] | |
| Message sent | Yes | [Yes/No] | [✅/❌] | |
| Personal analysis included | Yes | [Yes/No] | [✅/❌] | |
| Task completed | Yes | [Yes/No] | [✅/❌] | |
| GET_WORK intelligence | 7/10 | [X/10] | [✅/❌] | |

#### Overall Result
- [ ] ✅ PASSED - All critical criteria met
- [ ] ⚠️  PARTIAL - Some criteria not met (details below)
- [ ] ❌ FAILED - Critical failures (details below)

#### Issues Found
1. [Issue description]
2. [Issue description]

#### Recommendations
1. [Recommendation]
2. [Recommendation]

---

## Performance Metrics

### Target Metrics (Sprint 1)

| Metric | Target | Scenario 1 | Scenario 2 |
|--------|--------|-----------|-----------|
| Task completion rate | >80% | TBD | TBD |
| Message delivery success | 100% | TBD | TBD |
| Decision quality (1-10) | >7 | TBD | TBD |
| Cross-agent messages | >15 (S2 only) | N/A | TBD |
| Report completeness | >90% (S2 only) | N/A | TBD |
| Execution time (per day) | <10 min | TBD | TBD |

---

## Troubleshooting

### Common Issues

**Issue: Agent didn't process message**
- Check message file format (valid JSON)
- Verify message in correct inbox (`post/inbox/new/`)
- Check READ_POSTS action executed
- Review agent logs: `docker logs loopai_web`

**Issue: No message sent to other agent**
- Check agent's outbox: `post/outbox/sent/`
- Verify target agent inbox path correct
- Review DO_ACTION for message composition
- Check VALIDATE_ACTION passed

**Issue: Task not completed**
- Check current_work directory
- Review VALIDATE_WORK output
- Verify all subtasks completed
- Check for errors in action execution

**Issue: Report missing content**
- Verify all agents participated
- Check message exchange between agents
- Review cityhall's GET_WORK decision
- Check if 7 days fully executed

---

## Next Steps After Testing

### If Tests Pass
1. Mark Sprint 1 as complete ✅
2. Document baseline metrics
3. Create Sprint 1 summary in `done/sprint1_summary.md`
4. Begin Sprint 2 rollout to other agents

### If Tests Fail
1. Document failures in detail
2. Analyze root causes
3. Update protocols if needed
4. Re-run tests after fixes
5. Update implementation_status.md with issues

---

**Document Owner:** Implementation Team
**Status:** Ready for execution
**Prerequisites:** Sprint 1 setup complete, Docker environment verified
**Estimated Testing Time:** 2-3 days (includes execution + validation)
