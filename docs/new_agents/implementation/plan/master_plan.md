# Living Agent Implementation - Master Plan
**Created:** 2025-11-16
**Status:** Sprint 1 In Progress
**Target Completion:** 4 weeks

---

## Vision

Transform all LoopAI agents (Loops 69-75) into Living Agents that:
- Make autonomous, context-aware decisions
- Collaborate as a team
- Adapt to changing priorities
- Show transparent reasoning
- Continuously learn and improve

**Core Philosophy:** Agents are autonomous professionals, not mechanical task executors.

---

## Docker Environment

**IMPORTANT:** LoopAI runs in a **containerized Docker environment**.

### Key Containers
- **loopai_web** - Main Flask application, agent execution
- **agent_post** - Message routing and orchestration
- **postgres** - Database
- **loopai_view** - Vue.js frontend

### Essential Commands
```bash
# Container management
make up / make down / make upp

# Access containers
make bash    # loopai_web
make post    # agent_post

# Test agents (from host)
curl http://localhost:5050/api/public/agent/8/action/GET_WORK/

# Run orchestration (inside agent_post container)
docker exec -it agent_post python run_all_cycles.py --days 1
```

**📖 Complete Guide:** See `plan/docker_environment.md` for detailed Docker instructions.

---

## Implementation Strategy

### Phase 1: Pilot (Loop 70 - TeacherJohn)
**Status:** ✅ 90% Complete
**Timeline:** Week 1

**Completed:**
- ✅ Enhanced GET_WORK protocol with Living Agent intelligence (v2.0)
- ✅ Created missing Python prompt files (PREPARE_ACTION, DO_ACTION)
- ✅ Updated run_all_cycles.py with complex workflow (12 actions/day)
- ✅ Comprehensive documentation

**Remaining:**
- ⏳ Test full 5-day cycle with real messages
- ⏳ Validate Living Agent decision-making
- ⏳ Performance baseline metrics

### Phase 2: Expansion (Loops 71-74)
**Status:** 📋 Planned
**Timeline:** Week 2

**Agents:**
- Loop 71: cityhall (coordination/project management)
- Loop 72: padre (backend development)
- Loop 73: maria (frontend development)
- Loop 74: zhou (testing/quality)

**Approach:** Copy Loop 70 enhanced protocols → customize per agent role

### Phase 3: Enhancement
**Status:** 📋 Planned
**Timeline:** Week 3

**Goals:**
- Create protocols for PREPARE_ACTION, DO_ACTION, VALIDATE_ACTION
- Add cross-agent collaboration tracking
- Implement project state management
- Enhanced REFLEX with team insights

### Phase 4: Optimization
**Status:** 📋 Future
**Timeline:** Week 4

**Goals:**
- Adaptive workflow (dynamic iteration count)
- Meta-learning across agents
- Performance optimization
- Production readiness

---

## Success Criteria

### Technical Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Task completion rate | >80% | tasks/done vs tasks/new |
| Action validation pass rate | >85% | VALIDATE_ACTION success |
| Work validation pass rate | >90% | VALIDATE_WORK success |
| Average task completion time | <1 day | timestamp analysis |
| REFLEX insight quality | >7/10 | manual review |

### Behavioral Metrics

| Behavior | Target | Evidence |
|----------|--------|----------|
| Context-aware decisions | 100% | GET_WORK shows reasoning |
| Team collaboration | >50% decisions | "Unblock teammate" pattern |
| Adaptive behavior | >3 scenarios | Handles blocked, urgent, multiple tasks |
| Transparent reasoning | 100% | All decisions include "because..." |
| Continuous learning | Weekly | REFLEX generates actionable insights |

---

## Resource Requirements

### Infrastructure
- ✅ Docker environment (loopai_web, agent_post)
- ✅ PostgreSQL database
- ✅ LLM access (deepseek-chat, gpt-4)
- ✅ File system structure

### Development
- ⏳ Protocol creation (3 new protocols)
- ⏳ Testing scenarios (10+ test cases)
- ⏳ Monitoring tools
- ⏳ Documentation updates

### Time Allocation
- Week 1: Loop 70 testing & refinement (20 hours)
- Week 2: Rollout to 71-74 (30 hours)
- Week 3: Protocol enhancements (20 hours)
- Week 4: Optimization & production (20 hours)
**Total:** ~90 hours

---

## Risk Management

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| LLM context overflow | Medium | High | Protocol optimization, summarization |
| Action execution failures | Medium | Medium | Retry logic, error handling |
| Protocol ambiguity | High | Medium | Clear examples, extensive testing |
| Performance degradation | Low | Medium | Monitoring, optimization |

### Operational Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Complex workflow too slow | Medium | High | Optimize iteration count, parallel execution |
| Agents make poor decisions | Low | High | Extensive testing, decision logging, rollback plan |
| Protocol maintenance burden | Medium | Low | Template standardization, documentation |

---

## Sprint Structure

### Sprint 1: Pilot Completion (Week 1)
**Goal:** Complete Loop 70 implementation and validate Living Agent behavior
**Deliverables:**
- Test results from 5-day cycle
- Performance metrics baseline
- Decision quality assessment
- Bug fixes and refinements

### Sprint 2: Team Rollout (Week 2)
**Goal:** Roll out enhanced protocols to Loops 71-74
**Deliverables:**
- 4 agents with Living Agent protocols
- Role-specific customizations
- Integration testing
- Team collaboration validation

### Sprint 3: Protocol Enhancement (Week 3)
**Goal:** Create missing protocols and add advanced features
**Deliverables:**
- 3 new protocol files (PREPARE, DO, VALIDATE_ACTION)
- Cross-agent collaboration tracking
- Project state management
- Enhanced REFLEX

### Sprint 4: Optimization (Week 4)
**Goal:** Optimize performance and prepare for production
**Deliverables:**
- Adaptive workflow implementation
- Performance optimization
- Monitoring dashboard
- Production deployment plan

---

## Agent Roles and Specializations

### Loop 70: TeacherJohn (Architect/Educator)
**Role:** Technical architecture, code review, education
**Decision Patterns:**
- Prioritizes educational value
- Focuses on code quality
- Mentors other agents

### Loop 71: cityhall (Coordinator)
**Role:** Project management, team coordination
**Decision Patterns:**
- Prioritizes team needs
- Assigns work to appropriate agents
- Tracks project progress

### Loop 72: padre (Backend Developer)
**Role:** Backend development, API design, database
**Decision Patterns:**
- Focuses on backend tasks
- Collaborates with TeacherJohn on architecture
- Coordinates with maria on API contracts

### Loop 73: maria (Frontend Developer)
**Role:** Frontend development, UI/UX
**Decision Patterns:**
- Focuses on frontend tasks
- Collaborates with padre on API integration
- Emphasizes user experience

### Loop 74: zhou (QA/Testing)
**Role:** Testing, quality assurance, validation
**Decision Patterns:**
- Prioritizes quality checks
- Tests integrations
- Validates team deliverables

---

## Protocol Templates

### Standard Protocol Structure
```json
{
  "protocol_version": "2.0",
  "protocol_id": "action_name",
  "philosophy": "Living Agent statement",
  "instruction": "Clear, role-aware instruction",
  "decision_criteria": {
    "key_considerations": [],
    "decision_patterns": {}
  },
  "context_awareness": {},
  "steps": [],
  "example_scenarios": {},
  "output_format": {},
  "self_reflection_prompts": [],
  "living_agent_reminders": {}
}
```

### Role-Specific Customization
Each agent's protocols customized for their role:
- **TeacherJohn:** Educational focus, architecture emphasis
- **cityhall:** Team coordination, project management
- **padre:** Backend development expertise
- **maria:** Frontend development expertise
- **zhou:** Testing and quality focus

---

## Testing Strategy

### Unit Testing (Per Action)
- Test each action individually with mock inputs
- Verify output format compliance
- Check error handling

### Integration Testing (Full Workflow)
- Run complete 12-action daily cycle
- Verify action sequencing
- Check file operations

### Behavioral Testing (Living Agent)
- Test decision-making scenarios
- Validate reasoning transparency
- Check team collaboration patterns

### Performance Testing
- Measure execution time per action
- Track LLM token usage
- Monitor file system operations

### Load Testing
- Run 10-day cycles
- Test with multiple concurrent agents
- Stress test message handling

---

## Monitoring and Observability

### Key Metrics Dashboard
```
Agent Performance:
- Tasks completed per day
- Action success rate
- Average task duration
- Decision quality score

Team Collaboration:
- Messages sent/received
- Blockers resolved
- Cross-agent dependencies
- Response time to requests

System Health:
- Action execution time
- Error rate
- LLM token usage
- File system usage
```

### Logging Strategy
- **Decision logs:** Every GET_WORK decision with reasoning
- **Execution logs:** Every action with inputs/outputs
- **Validation logs:** All validation results
- **Reflection logs:** Weekly REFLEX insights

---

## Rollback Plan

### Emergency Rollback
If Living Agent implementation fails critically:

**Step 1: Stop Orchestration**
```bash
docker stop loopai_web agent_post
```

**Step 2: Restore Backups**
```bash
cd /loopai_src/var/users/1/loops
for loop_id in 70 71 72 73 74; do
  tar -xzf ~/loop${loop_id}_backup_*.tar.gz
  mv backup/* ${loop_id}/
done
```

**Step 3: Revert run_all_cycles.py**
```bash
git checkout agent_post/run_all_cycles.py
```

**Step 4: Restart System**
```bash
docker start loopai_web agent_post
```

**Step 5: Verify**
```bash
curl http://localhost:5050/api/public/agent/8/action/WAKEUP/
```

### Partial Rollback
Roll back individual agents while keeping others:
1. Restore specific loop directory from backup
2. Keep successful agents running
3. Debug and fix failed agent separately

---

## Communication Plan

### Stakeholder Updates
- **Daily:** Progress updates in implementation_status.md
- **Weekly:** Sprint review and metrics report
- **Ad-hoc:** Critical issues or blockers

### Documentation Updates
- Update agent_actions_inventory.md after each rollout
- Maintain implementation_status.md in real-time
- Create per-sprint summary documents

---

## Dependencies

### External Dependencies
- LLM API availability (deepseek-chat, gpt-4)
- Docker infrastructure
- PostgreSQL database
- File system access

### Internal Dependencies
```
Sprint 1 → Sprint 2 (Loop 70 must be validated before rollout)
Sprint 2 → Sprint 3 (All agents need protocols before enhancement)
Sprint 3 → Sprint 4 (Features needed before optimization)
```

### Blocking Issues
- None currently identified

---

## Future Enhancements (Post-Sprint 4)

### Short Term (1-2 months)
1. **Adaptive workflow:** Agents learn optimal action patterns
2. **Meta-learning:** Agents learn from each other's REFLEX
3. **Project tracking:** Multi-day project state management
4. **Message templates:** Standardized inter-agent communication

### Medium Term (3-6 months)
1. **Agent specialization learning:** Agents improve role-specific skills
2. **Team intelligence:** Collective decision-making
3. **Automated workflow optimization:** Self-tuning iteration counts
4. **Knowledge base:** Shared team knowledge repository

### Long Term (6-12 months)
1. **Emergent behavior:** Self-organizing team patterns
2. **Strategic planning:** Agents plan multi-week projects
3. **Resource optimization:** Intelligent load balancing
4. **External API integration:** Agents interact with external services

---

## Success Stories (Future)

*To be filled as we achieve milestones:*

### Loop 70 Success (Sprint 1)
- TBD

### Team Collaboration Success (Sprint 2)
- TBD

### Protocol Enhancement Success (Sprint 3)
- TBD

### Production Deployment Success (Sprint 4)
- TBD

---

## Appendix A: File Locations

### Implementation Tracking
```
/docs/new_agents/implementation/
├── implementation_status.md    # Overall status tracker
├── plan/                       # Implementation plans
│   ├── master_plan.md         # This document
│   ├── sprint1_plan.md        # Sprint 1 details
│   ├── sprint2_plan.md        # Sprint 2 details
│   ├── sprint3_plan.md        # Sprint 3 details
│   └── sprint4_plan.md        # Sprint 4 details
├── todo/                       # Sprint tasks
│   ├── sprint1_todo.md        # Sprint 1 task list
│   ├── sprint2_todo.md        # Sprint 2 task list
│   ├── sprint3_todo.md        # Sprint 3 task list
│   └── sprint4_todo.md        # Sprint 4 task list
└── done/                       # Completed sprints
    └── (sprint summaries)
```

### Agent Configurations
```
/loopai_src/var/users/1/loops/{loop_id}/
├── config/                     # YAML + Python configs
└── filesystem/agentlife/
    └── skills/project_thinking/protocols/
```

### Documentation
```
/docs/
├── loop70_living_agent_complex_workflow.md  # Loop 70 documentation
├── updating_agent_loops_2.md                # Living Agent concept
├── agent_actions_inventory.md               # Agent status
└── session_summary_2025-11-16.md            # Today's work
```

---

## Appendix B: Quick Reference Commands

**⚠️ IMPORTANT:** Commands run in Docker containers. See `plan/docker_environment.md` for details.

### Container Management
```bash
# Start/stop containers
make up          # Start all containers
make down        # Stop all containers
make upp         # Rebuild and start
make status      # Check status
make logs        # View logs
```

### Testing (from host)
```bash
# Test single agent action (API call to loopai_web)
curl http://localhost:5050/api/public/agent/8/action/GET_WORK/

# Check execution result
curl http://localhost:5050/api/public/execution/{execution_id}/result/
```

### Orchestration (in agent_post container)
```bash
# Option 1: Enter container then run
make post
python run_all_cycles.py --days 1

# Option 2: Direct execution from host
docker exec -it agent_post python run_all_cycles.py --days 1

# Option 3: Background execution
docker exec -d agent_post python run_all_cycles.py --days 5
docker logs -f agent_post
```

### Monitoring (from host)
```bash
# Check tasks (host file system - mounted volume)
ls /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/70/filesystem/agentlife/tasks/

# Check current work
ls /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/70/filesystem/agentlife/current_work/

# View logs
docker logs -f agent_post
docker logs -f loopai_web
```

### Backup (from host)
```bash
# Backup agent configuration (from host file system)
cd /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/70
tar -czf ~/loop70_backup_$(date +%Y%m%d_%H%M%S).tar.gz .
```

### Database
```bash
# Access PostgreSQL
docker exec -it postgres psql -U postgres -d loopai

# Query agents
docker exec -it postgres psql -U postgres -d loopai -c "SELECT id, public_name, loop_id FROM agent;"
```

---

**Document Owner:** Implementation Team
**Last Updated:** 2025-11-16
**Next Review:** Start of Sprint 2
**Status:** Living Document (update as needed)
