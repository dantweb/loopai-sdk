# Sprint 2: Rollout to Loops 71-74
**Duration:** Week 2
**Goal:** Extend Living Agent implementation to cityhall, padre, maria, and zhou
**Status:** Planned
**Prerequisites:** Sprint 1 completed successfully

**Reference:** `/docs/loop70_living_agent_complex_workflow.md` - Section "Agent Roles and Specializations"

---

## ⚠️ Docker Environment

**IMPORTANT:** All operations run in Docker containers.

**Key Commands for This Sprint:**
```bash
# Backup agents (from host)
cd /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/71
tar -czf ~/loop71_backup_$(date +%Y%m%d).tar.gz .

# Edit configs on host (use your IDE)
# Files immediately available in containers (mounted volume)

# Test agent (from host)
curl http://localhost:5050/api/public/agent/9/action/GET_WORK/

# Run team orchestration (agent_post container)
docker exec -it agent_post python run_all_cycles.py --days 1

# Monitor
docker logs -f agent_post
```

**📖 Docker Guide:** `/docs/new_agents/implementation/plan/docker_environment.md`

---

## Sprint Objectives

1. ⏳ Roll out enhanced protocols to 4 additional agents
2. ⏳ Customize protocols for each agent's role
3. ⏳ Test team collaboration scenarios
4. ⏳ Validate cross-agent messaging
5. ⏳ Establish team performance baseline

---

## Agent Target List

| Agent | Loop ID | Role | Complexity | Priority |
|-------|---------|------|------------|----------|
| cityhall | 71 | Coordinator/PM | Medium | 1st (coordinator) |
| padre | 72 | Backend Dev | Medium | 2nd |
| maria | 73 | Frontend Dev | Medium | 3rd |
| zhou | 74 | QA/Testing | Low | 4th |

**Rollout Order Rationale:**
- cityhall first (coordinates team, needs to assign work)
- padre & maria next (collaborate on API contracts)
- zhou last (validates team deliverables)

---

## Tasks

### A. Loop 71: cityhall (Project Coordinator) ⏳

#### A1. Backup & Preparation
- [ ] Backup Loop 71 configuration (from host):
  ```bash
  cd /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/71
  tar -czf ~/loop71_backup_$(date +%Y%m%d).tar.gz .
  ```
- [ ] Review current Loop 71 actions: `ls config/*.yaml`
- [ ] Identify which actions need protocol updates
- [ ] Create rollout checklist

#### A2. Protocol Customization
- [ ] Copy GET_WORK protocol v2.0 to Loop 71
- [ ] Customize for cityhall role:
  - Philosophy: "You are cityhall, the team coordinator and project manager"
  - Decision criteria: Add "team capacity" and "project dependencies"
  - Decision patterns: Add "if_new_project" → assign to appropriate agent
  - Examples: Team coordination scenarios
- [ ] Update READ_POSTS protocol with coordination focus
- [ ] Update VALIDATE_WORK protocol with project management criteria
- [ ] Update REFLEX protocol with team performance analysis

**Key Customization:** cityhall focuses on team organization, work distribution, and project tracking

#### A3. Python Config Updates
- [ ] Copy PREPARE_ACTION.py, DO_ACTION.py from Loop 70
- [ ] Update PREPARE_ACTION.py with coordination language
- [ ] Update DO_ACTION.py with project management prompts
- [ ] Verify VALIDATE_WORK.py exists and is correct

#### A4. Testing cityhall
- [ ] Send test message: "New project: Build marketplace MVP"
- [ ] Run READ_POSTS → verify task created
- [ ] Run GET_WORK → verify cityhall creates coordination plan
- [ ] **Expected:** cityhall decides to create tasks for TeacherJohn, padre, maria, zhou
- [ ] Run 1-day cycle
- [ ] Verify coordination behavior

#### A5. Documentation
- [ ] Create `loop71_cityhall_customization.md`
- [ ] Document role-specific decision patterns
- [ ] Note any issues or special behaviors

---

### B. Loop 72: padre (Backend Developer) ⏳

#### B1. Backup & Preparation
- [ ] Backup Loop 72 configuration
- [ ] Review current Loop 72 actions (16 actions)
- [ ] Create rollout checklist

#### B2. Protocol Customization
- [ ] Copy GET_WORK protocol v2.0 to Loop 72
- [ ] Customize for padre role:
  - Philosophy: "You are padre, backend developer specializing in APIs and databases"
  - Decision criteria: Add "API integration needs" and "database considerations"
  - Decision patterns: Add "if_api_contract_needed" → coordinate with maria
  - Examples: Backend development scenarios
- [ ] Update protocols with backend development focus
- [ ] Add collaboration patterns with maria (frontend)

**Key Customization:** padre focuses on backend tasks, API design, database work

#### B3. Testing padre
- [ ] Send test message: "Implement marketplace backend API"
- [ ] Run GET_WORK → verify backend-focused plan
- [ ] Test collaboration: Send message from maria asking about API endpoints
- [ ] **Expected:** padre prioritizes maria's question (team unblocking)
- [ ] Run 1-day cycle

---

### C. Loop 73: maria (Frontend Developer) ⏳

#### C1. Backup & Preparation
- [ ] Backup Loop 73 configuration
- [ ] Review current Loop 73 actions (16 actions)
- [ ] Create rollout checklist

#### C2. Protocol Customization
- [ ] Copy GET_WORK protocol v2.0 to Loop 73
- [ ] Customize for maria role:
  - Philosophy: "You are maria, frontend developer focusing on UI/UX"
  - Decision criteria: Add "user experience impact" and "design requirements"
  - Decision patterns: Add "if_api_dependency" → check with padre
  - Examples: Frontend development scenarios
- [ ] Update protocols with frontend development focus
- [ ] Add collaboration patterns with padre (backend)

**Key Customization:** maria focuses on frontend tasks, UI/UX, integration with backend APIs

#### C3. Testing maria
- [ ] Send test message: "Build marketplace product listing UI"
- [ ] Run GET_WORK → verify frontend-focused plan
- [ ] Test collaboration: Create scenario where maria needs API spec from padre
- [ ] **Expected:** maria creates task to request API details
- [ ] Run 1-day cycle

---

### D. Loop 74: zhou (QA/Testing) ⏳

#### D1. Backup & Preparation
- [ ] Backup Loop 74 configuration
- [ ] Review current Loop 74 actions (15 actions)
- [ ] Create rollout checklist

#### D2. Protocol Customization
- [ ] Copy GET_WORK protocol v2.0 to Loop 74
- [ ] Customize for zhou role:
  - Philosophy: "You are zhou, QA specialist ensuring quality and testing"
  - Decision criteria: Add "quality impact" and "testing coverage"
  - Decision patterns: Add "if_integration_ready" → test cross-component functionality
  - Examples: Testing and QA scenarios
- [ ] Update protocols with testing focus
- [ ] Add validation patterns for team deliverables

**Key Customization:** zhou focuses on testing, quality assurance, integration validation

#### D3. Testing zhou
- [ ] Send test message: "Test marketplace MVP integration"
- [ ] Run GET_WORK → verify testing-focused plan
- [ ] Test collaboration: zhou validates work from TeacherJohn, padre, maria
- [ ] **Expected:** zhou creates comprehensive test plan
- [ ] Run 1-day cycle

---

### E. Team Integration Testing ⏳

#### E1. Cross-Agent Messaging
- [ ] Test cityhall → TeacherJohn message delivery
- [ ] Test padre → maria API contract discussion
- [ ] Test maria → padre dependency questions
- [ ] Test zhou → all agents validation feedback
- [ ] Verify all messages delivered correctly

**Expected:** Messages route correctly via agent_post system

#### E2. Team Collaboration Scenario
**Scenario:** Marketplace MVP Development

- [ ] **Day 1:** cityhall receives marketplace request
  - cityhall creates coordination plan
  - cityhall sends tasks to TeacherJohn (architecture), padre (backend), maria (frontend), zhou (testing)

- [ ] **Day 2:** Agents receive tasks and start work
  - TeacherJohn designs architecture
  - padre works on backend (blocked - needs architecture)
  - maria works on frontend (blocked - needs backend API)
  - zhou plans testing approach

- [ ] **Day 3:** Dependencies resolve
  - TeacherJohn completes architecture → sends to padre & maria
  - padre unblocked → implements backend API
  - maria still blocked → waits for padre
  - zhou continues test planning

- [ ] **Day 4:** Integration begins
  - padre completes backend API → sends spec to maria
  - maria unblocked → implements frontend with API integration
  - zhou begins integration testing

- [ ] **Day 5:** Final validation
  - All agents complete their parts
  - zhou validates integration
  - REFLEX runs for all agents
  - Team reviews progress

**Metrics to Track:**
- How many times agents unblocked each other
- Average response time to teammate questions
- Task completion rate with dependencies
- Team coordination quality

#### E3. Edge Case: All Agents Blocked
- [ ] Create scenario where all agents waiting on external input
- [ ] Verify agents don't sit idle
- [ ] Check agents send reminder messages
- [ ] Confirm agents work on documentation/improvement tasks

**Expected:** Adaptive team behavior, no idle waiting

---

### F. Run_all_cycles Updates ⏳

#### F1. Multi-Agent Orchestration
- [ ] Verify run_all_cycles.py handles 5 agents (currently handles all in addresses list)
- [ ] Test orchestration runs all agents in sequence
- [ ] Monitor for timing issues
- [ ] Check for concurrent execution problems

#### F2. Agent-Specific Timing
- [ ] Consider if different agents need different wait times
- [ ] Test if 15s between actions sufficient for all agents
- [ ] Adjust if needed

---

### G. Performance Baseline (Team) ⏳

#### G1. Team Metrics
- [ ] Measure total cycle time (5 agents × 12 actions)
- [ ] Track cross-agent message delivery time
- [ ] Monitor dependency resolution time
- [ ] Calculate team throughput (tasks completed per day)

**Target Metrics:**
- Full team cycle: <60 minutes
- Message delivery: <30 seconds
- Dependency resolution: <1 day
- Team throughput: 5-8 tasks/day

#### G2. Collaboration Metrics
- [ ] Count messages sent between agents
- [ ] Track "unblock teammate" decisions
- [ ] Measure response time to colleague requests
- [ ] Assess collaboration quality

**Target Metrics:**
- Inter-agent messages: >10 per day
- Unblock decisions: >20% of GET_WORK choices
- Response time: <1 cycle
- Collaboration quality: >7/10

---

### H. Sprint Deliverables ⏳

#### H1. Configuration Package
- [ ] All 4 agents configured with Living Agent protocols
- [ ] Role-specific customizations documented
- [ ] Backup files saved
- [ ] Configuration checklist completed

#### H2. Test Results Report
- [ ] Create `sprint2_rollout_results.md`
- [ ] Individual agent test results
- [ ] Team collaboration test results
- [ ] Issues encountered and resolutions
- [ ] Performance metrics

**Location:** `/docs/new_agents/implementation/done/sprint2_rollout_results.md`

#### H3. Team Collaboration Report
- [ ] Create `sprint2_team_collaboration.md`
- [ ] Collaboration patterns observed
- [ ] Dependency handling effectiveness
- [ ] Cross-agent communication quality
- [ ] Recommendations for improvement

**Location:** `/docs/new_agents/implementation/done/sprint2_team_collaboration.md`

#### H4. Updated Agent Inventory
- [ ] Update agent_actions_inventory.md
- [ ] Mark Loops 71-74 as "Living Agent Enabled"
- [ ] Add role-specific notes
- [ ] Update testing status

**Location:** `/docs/agent_actions_inventory.md`

---

## Sprint Success Criteria

### Must Have (Blocker for Sprint 3)
- ⏳ All 4 agents rolled out with customized protocols
- ⏳ Each agent demonstrates role-specific decision-making
- ⏳ Team collaboration scenario completes successfully
- ⏳ Cross-agent messaging works correctly

### Should Have
- ⏳ 5-day team cycle with REFLEX completes
- ⏳ Dependency resolution works smoothly
- ⏳ Team throughput meets targets
- ⏳ No critical bugs in multi-agent orchestration

### Nice to Have
- ⏳ All edge cases tested with team
- ⏳ Automated team metrics collection
- ⏳ Multiple team scenarios tested

---

## Risk & Issues

### Current Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Protocol customization errors | Medium | High | Test each agent individually before team test |
| Circular dependencies | Low | High | Clear task dependency tracking |
| Message delivery failures | Medium | Medium | Robust error handling in agent_post |
| Orchestration timing issues | Medium | Low | Monitor and adjust wait times |

### Blocking Issues
- Waiting for Sprint 1 completion

### Open Questions
- Should agents have different iteration counts based on role complexity?
- How to handle project management state for cityhall?
- What's optimal wait time between actions for different agents?

---

## Timeline

**Week 2 Schedule:**

**Day 1: cityhall Rollout**
- Configure Loop 71
- Test individually
- Verify coordination behavior

**Day 2: padre & maria Rollout**
- Configure Loops 72-73
- Test individually
- Test padre ↔ maria collaboration

**Day 3: zhou Rollout + Integration**
- Configure Loop 74
- Test individually
- Begin team integration testing

**Day 4: Team Scenarios**
- Run marketplace MVP scenario
- Test edge cases
- Collect team metrics

**Day 5: Analysis & Documentation**
- Analyze team performance
- Create deliverables
- Sprint retrospective
- Prepare for Sprint 3

---

## Next Sprint Preview

**Sprint 3: Protocol Enhancement**
- Create protocol files for PREPARE_ACTION, DO_ACTION, VALIDATE_ACTION
- Add cross-agent collaboration tracking
- Implement project state management
- Enhanced REFLEX with team insights

**Prerequisite:** Sprint 2 "Must Have" criteria all met

---

**Sprint Owner:** Implementation Team
**Start Date:** TBD (after Sprint 1)
**Target End:** +1 week
**Status:** Planned
