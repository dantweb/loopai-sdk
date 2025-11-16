# Sprint 3: Protocol Enhancement
**Duration:** Week 3
**Goal:** Create missing protocols and add advanced Living Agent features
**Status:** Planned
**Prerequisites:** Sprint 2 completed, all 5 agents running with basic protocols

**Reference:** `/docs/loop70_living_agent_complex_workflow.md` - Section "Future Enhancements - Short Term"

---

## ⚠️ Docker Environment

**Key Commands for This Sprint:**
```bash
# Edit protocol files on host (immediately available in containers)
# Location: /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/*/filesystem/agentlife/skills/project_thinking/protocols/

# Test protocols (from host)
curl http://localhost:5050/api/public/agent/8/action/PREPARE_ACTION/

# Run team cycles (agent_post container)
docker exec -it agent_post python run_all_cycles.py --days 5

# Check logs
docker logs -f agent_post
```

**📖 Docker Guide:** `/docs/new_agents/implementation/plan/docker_environment.md`

---

## Sprint Objectives

1. ⏳ Create protocol files for PREPARE_ACTION, DO_ACTION, VALIDATE_ACTION
2. ⏳ Standardize protocol format across all actions
3. ⏳ Add cross-agent collaboration tracking
4. ⏳ Implement project state management
5. ⏳ Enhance REFLEX with team-level insights

---

## Tasks

### A. Protocol File Creation ⏳

#### A1. PREPARE_ACTION Protocol
**Current State:** Python prompts only (PREPARE_ACTION.py)
**Target:** JSON protocol file

- [ ] Create `/protocols/prepare_action/prepare_action_protocol.json`
- [ ] Define protocol structure:
  ```json
  {
    "protocol_version": "2.0",
    "protocol_id": "prepare_action",
    "philosophy": "Prepare next action with care and context awareness",
    "instruction": "...",
    "steps": [
      "identify_next_action",
      "check_dependencies",
      "gather_context",
      "create_action_plan"
    ],
    "example_scenarios": {},
    "output_format": {}
  }
  ```
- [ ] Add decision logic: "Which action should I prepare next?"
- [ ] Include 3 example scenarios
- [ ] Add Living Agent reminders

#### A2. DO_ACTION Protocol
**Current State:** Python prompts only (DO_ACTION.py)
**Target:** JSON protocol file

- [ ] Create `/protocols/do_action/do_action_protocol.json`
- [ ] Define protocol structure with execution guidance
- [ ] Add quality criteria for work execution
- [ ] Include expertise application guidelines
- [ ] Add 3 example executions (simple, medium, complex)
- [ ] Add self-assessment prompts

#### A3. VALIDATE_ACTION Protocol
**Current State:** YAML config only
**Target:** JSON protocol file

- [ ] Create `/protocols/validate_action/validate_action_protocol.json`
- [ ] Define validation criteria per action type
- [ ] Add decision paths: VALID / INVALID / NEEDS_REVISION
- [ ] Include constructive feedback templates
- [ ] Add 3 example validations (pass, fail, partial)
- [ ] Add quality scoring guidelines

#### A4. Protocol Testing
- [ ] Test PREPARE_ACTION with new protocol
- [ ] Test DO_ACTION with new protocol
- [ ] Test VALIDATE_ACTION with new protocol
- [ ] Compare behavior: protocol-based vs prompt-based
- [ ] Refine protocols based on test results

#### A5. Rollout to All Agents
- [ ] Deploy protocols to Loop 70 (TeacherJohn)
- [ ] Deploy protocols to Loop 71 (cityhall)
- [ ] Deploy protocols to Loop 72 (padre)
- [ ] Deploy protocols to Loop 73 (maria)
- [ ] Deploy protocols to Loop 74 (zhou)
- [ ] Test each agent with new protocols
- [ ] Verify no regressions

---

### B. Protocol Standardization ⏳

#### B1. Protocol Template
- [ ] Create master protocol template
- [ ] Define required sections for all protocols
- [ ] Establish naming conventions
- [ ] Create protocol validation schema (JSON Schema)

**Standard Protocol Structure:**
```json
{
  "protocol_version": "2.0",
  "protocol_id": "action_name",
  "philosophy": "Living Agent statement",
  "instruction": "Clear, concise instruction",
  "decision_criteria": {},
  "context_awareness": {},
  "steps": [],
  "example_scenarios": {},
  "output_format": {},
  "self_reflection_prompts": [],
  "living_agent_reminders": {}
}
```

#### B2. Existing Protocol Updates
- [ ] Review all existing protocols (read_posts, get_work, validate, reflex)
- [ ] Update to match standard template
- [ ] Add missing sections
- [ ] Ensure consistency across all protocols

#### B3. Documentation
- [ ] Create `protocol_development_guide.md`
- [ ] Document template usage
- [ ] Provide examples for each section
- [ ] Include best practices

**Location:** `/docs/protocol_development_guide.md`

---

### C. Cross-Agent Collaboration Tracking ⏳

#### C1. Dependency Tracking Structure
- [ ] Design dependency tracking JSON format
  ```json
  {
    "project_id": "marketplace_mvp",
    "dependencies": [
      {
        "agent": "TeacherJohn",
        "task": "architecture_design",
        "status": "completed",
        "blocks": [
          {"agent": "padre", "task": "backend_implementation"},
          {"agent": "maria", "task": "frontend_implementation"}
        ]
      }
    ]
  }
  ```
- [ ] Define storage location: `/agentlife/team/dependencies/`
- [ ] Create read/write utilities

#### C2. Integration with GET_WORK
- [ ] Update GET_WORK protocol to check dependencies
- [ ] Add decision pattern: "if_blocking_others" → high priority
- [ ] Add team dashboard awareness
- [ ] Test dependency-aware decision making

**Example:**
```
TeacherJohn's GET_WORK: "I see that padre and maria are both
waiting for my architecture design. This is HIGH priority
because I'm blocking the team."
```

#### C3. Blocker Resolution Tracking
- [ ] Track how long tasks are blocked
- [ ] Monitor which agent is causing blocker
- [ ] Generate alerts for long-blocked tasks
- [ ] Add to REFLEX analysis

#### C4. Team Dashboard
- [ ] Create team status file: `/agentlife/team/dashboard.json`
  ```json
  {
    "date": "2025-11-16",
    "agents": [
      {
        "name": "TeacherJohn",
        "status": "active",
        "current_task": "marketplace_architecture",
        "blocking": ["padre", "maria"],
        "blocked_by": []
      }
    ],
    "blockers": [],
    "projects": []
  }
  ```
- [ ] Update dashboard after each cycle
- [ ] Make dashboard readable by all agents
- [ ] Add dashboard to READ_POSTS context

---

### D. Project State Management ⏳

#### D1. Project State Structure
- [ ] Design project tracking JSON format
  ```json
  {
    "project_id": "marketplace_mvp_20251116",
    "title": "Marketplace MVP Development",
    "owner": "cityhall",
    "status": "active",
    "priority": "high",
    "created_at": "2025-11-16",
    "team_members": ["TeacherJohn", "padre", "maria", "zhou"],
    "subtasks": [],
    "dependencies": [],
    "blockers": [],
    "completion_percentage": 45
  }
  ```
- [ ] Define project states: new, active, blocked, scheduled, completed, archived
- [ ] Create storage location: `/agentlife/team/projects/`

#### D2. Project Lifecycle
- [ ] Define project creation process (cityhall initiates)
- [ ] Define project assignment (cityhall assigns to agents)
- [ ] Define project updates (agents update status)
- [ ] Define project completion (validation + archival)

#### D3. Multi-Day Project Support
- [ ] Add project resume capability (agent continues work next day)
- [ ] Track project progress across cycles
- [ ] Handle project handoffs between agents
- [ ] Test multi-day project workflow

**Test Scenario:**
```
Day 1: cityhall creates marketplace_mvp project
Day 2: TeacherJohn works on architecture (25% complete)
Day 3: TeacherJohn completes architecture (100%)
        padre starts backend (30% complete)
Day 4: padre continues backend (70% complete)
Day 5: padre completes backend (100%)
        maria starts frontend (40% complete)
```

#### D4. Project Dependency Management
- [ ] Link project dependencies to agent tasks
- [ ] Auto-update blocker status based on dependencies
- [ ] Notify agents when blockers are resolved
- [ ] Test complex dependency chains

---

### E. Enhanced REFLEX ⏳

#### E1. Team-Level Insights
- [ ] Update REFLEX protocol to analyze team performance
- [ ] Add sections:
  - Individual agent performance
  - Team collaboration effectiveness
  - Blocker patterns
  - Communication quality
  - Project velocity
- [ ] Generate team-wide recommendations

**Example Team Insight:**
```
"This week, padre was blocked 3 times waiting for TeacherJohn's
architecture decisions. Recommendation: TeacherJohn should
prioritize architecture tasks earlier in the day to unblock
the team faster."
```

#### E2. Pattern Recognition
- [ ] Identify recurring blocker patterns
- [ ] Detect communication bottlenecks
- [ ] Find optimal collaboration patterns
- [ ] Suggest process improvements

#### E3. Comparative Analysis
- [ ] Compare performance across agents
- [ ] Identify best practices from high performers
- [ ] Share insights across team
- [ ] Generate knowledge base entries

#### E4. Actionable Recommendations
- [ ] REFLEX suggests specific changes
- [ ] Recommendations fed back into next cycle
- [ ] Track if recommendations are followed
- [ ] Measure recommendation effectiveness

---

### F. Testing & Validation ⏳

#### F1. Protocol Testing
- [ ] Test all 3 new protocols individually
- [ ] Test protocol interactions
- [ ] Validate JSON schema compliance
- [ ] Check for protocol clarity (LLM understands)

#### F2. Collaboration Tracking Testing
- [ ] Create test scenario with dependencies
- [ ] Verify dependency tracking works
- [ ] Test blocker resolution
- [ ] Validate team dashboard accuracy

#### F3. Project State Testing
- [ ] Create multi-day project test
- [ ] Verify state persistence
- [ ] Test project handoffs
- [ ] Validate completion tracking

#### F4. Enhanced REFLEX Testing
- [ ] Run 5-day cycle with all agents
- [ ] Verify team insights generated
- [ ] Check recommendation quality
- [ ] Validate pattern recognition

---

### G. Sprint Deliverables ⏳

#### G1. New Protocol Files
- [ ] prepare_action_protocol.json (all 5 agents)
- [ ] do_action_protocol.json (all 5 agents)
- [ ] validate_action_protocol.json (all 5 agents)
- [ ] Updated reflex_protocol.json v2.0 (team insights)

#### G2. Collaboration System
- [ ] Dependency tracking implementation
- [ ] Team dashboard implementation
- [ ] Blocker monitoring system
- [ ] Documentation

**Location:** `/docs/collaboration_tracking_system.md`

#### G3. Project Management System
- [ ] Project state tracking implementation
- [ ] Multi-day project support
- [ ] Project lifecycle documentation
- [ ] Usage examples

**Location:** `/docs/project_management_system.md`

#### G4. Test Results Report
- [ ] Create `sprint3_enhancement_results.md`
- [ ] Protocol test results
- [ ] Collaboration tracking validation
- [ ] Project management validation
- [ ] Enhanced REFLEX analysis

**Location:** `/docs/new_agents/implementation/done/sprint3_enhancement_results.md`

---

## Sprint Success Criteria

### Must Have (Blocker for Sprint 4)
- ⏳ All 3 new protocols created and deployed
- ⏳ Protocols working correctly across all 5 agents
- ⏳ Dependency tracking functional
- ⏳ Project state management working

### Should Have
- ⏳ Enhanced REFLEX generating team insights
- ⏳ Multi-day project tested successfully
- ⏳ Team dashboard accurate and useful
- ⏳ No regressions from protocol changes

### Nice to Have
- ⏳ Automated protocol validation
- ⏳ Comprehensive pattern recognition
- ⏳ Advanced recommendation engine

---

## Risk & Issues

### Current Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Protocol too complex | Medium | Medium | Keep instructions clear and concise |
| State management bugs | Medium | High | Thorough testing, backup/restore |
| Performance degradation | Low | Medium | Monitor metrics, optimize |
| Protocol inconsistency | Low | Low | Template and validation schema |

### Blocking Issues
- Waiting for Sprint 2 completion

### Open Questions
- Should project state be centralized or distributed?
- How much history to keep in dependency tracking?
- What's optimal REFLEX frequency with team insights?

---

## Timeline

**Week 3 Schedule:**

**Day 1-2: Protocol Creation**
- Create 3 new protocol files
- Test individually
- Deploy to all agents

**Day 3: Collaboration System**
- Implement dependency tracking
- Create team dashboard
- Test with scenarios

**Day 4: Project Management**
- Implement project state management
- Test multi-day projects
- Enhance REFLEX

**Day 5: Testing & Documentation**
- Comprehensive testing
- Create deliverables
- Sprint retrospective
- Prepare for Sprint 4

---

## Next Sprint Preview

**Sprint 4: Advanced Features & Optimization**
- Adaptive workflow (dynamic iteration count)
- Meta-learning across agents
- Performance optimization
- Production readiness
- Monitoring dashboard

**Prerequisite:** Sprint 3 "Must Have" criteria all met

---

**Sprint Owner:** Implementation Team
**Start Date:** TBD (after Sprint 2)
**Target End:** +1 week
**Status:** Planned
