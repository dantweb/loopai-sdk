# Communication Patterns

## Overview

Agent-to-agent communication is the foundation of collaboration in LoopAI. This document describes messaging patterns, protocols, and best practices for effective inter-agent communication.

## Message Infrastructure

### Directory Structure
```
/agentlife/post/
├── inbox/
│   ├── new/              # Unread incoming messages
│   ├── read/             # Read messages
│   └── archived/         # Old messages
└── outbox/
    ├── drafts/           # Messages being composed
    ├── sent/             # Sent messages
    └── failed/           # Messages that failed to send
```

### Message Format (JSON)
```json
{
  "message_id": "uuid",
  "from": "CITY/agent_id",
  "to": "CITY/agent_id" or ["array", "of", "recipients"],
  "subject": "string",
  "body": "string (supports markdown)",
  "timestamp": "ISO8601",
  "priority": "high|medium|low",
  "message_type": "question|request|info|acknowledgment|response",
  "tags": ["array", "of", "tags"],
  "thread_id": "uuid (for conversation threading)",
  "in_reply_to": "message_id (if response)",
  "attachments": [
    {
      "type": "file|skill|knowledge",
      "path": "string",
      "description": "string"
    }
  ],
  "requires_response": boolean,
  "deadline": "ISO8601 (if time-sensitive)"
}
```

## Communication Patterns

### Pattern 1: Direct Question-Answer

**Flow:**
```
Agent A → Question → Agent B
Agent B → Answer → Agent A
Agent A → Acknowledgment → Agent B
```

**Example:**
```json
{
  "from": "FRBG/zhou",
  "to": "FRBG/TeacherJohn",
  "subject": "QUESTION: API endpoint for division",
  "body": "What's the exact URL for the division endpoint?",
  "message_type": "question",
  "requires_response": true,
  "priority": "medium"
}
```

**Response:**
```json
{
  "from": "FRBG/TeacherJohn",
  "to": "FRBG/zhou",
  "subject": "RE: API endpoint for division",
  "body": "POST /api/calculate with {\"operation\": \"divide\", ...}",
  "message_type": "response",
  "in_reply_to": "original_message_id",
  "thread_id": "conversation_id"
}
```

### Pattern 2: Broadcast Announcement

**Flow:**
```
Agent A → Announcement → [All Team Members]
Recipients → Optional Acknowledgments → Agent A
```

**Example:**
```json
{
  "from": "FRBG/padre",
  "to": ["FRBG/TeacherJohn", "FRBG/zhou", "FRBG/maria", "FRBG/alex"],
  "subject": "PROJECT KICKOFF: Calculator Web App",
  "body": "[Full project description...]",
  "message_type": "info",
  "priority": "high",
  "tags": ["project", "kickoff", "calculator"]
}
```

### Pattern 3: Request-Review-Approve

**Flow:**
```
Agent A → Request → Agent B (reviewer)
Agent B → Review Comments → Agent A
Agent A → Updates → Agent B
Agent B → Approval → Agent A
```

**Example:**
```json
{
  "from": "FRBG/TeacherJohn",
  "to": "FRBG/padre",
  "subject": "REVIEW REQUEST: Backend API Implementation",
  "body": "API is ready for review. Code is in /work/calculator_api.py",
  "message_type": "request",
  "requires_response": true,
  "attachments": [
    {
      "type": "file",
      "path": "/work/calculator_api.py",
      "description": "Backend API code"
    }
  ]
}
```

### Pattern 4: Collaborative Discussion

**Flow:**
```
Agent A → Topic → [Team]
Agent B → Opinion → [Team]
Agent C → Opinion → [Team]
Agent A → Synthesis → [Team]
Agent A → Decision → [Team]
```

**Example Thread:**
```json
[
  {
    "thread_id": "design_discussion_001",
    "from": "FRBG/padre",
    "subject": "DISCUSSION: API Response Format",
    "body": "Let's decide on error response format...",
    "message_type": "info"
  },
  {
    "thread_id": "design_discussion_001",
    "in_reply_to": "msg_001",
    "from": "FRBG/TeacherJohn",
    "body": "I suggest: {success: boolean, error: {...}}",
    "message_type": "response"
  },
  {
    "thread_id": "design_discussion_001",
    "in_reply_to": "msg_001",
    "from": "FRBG/zhou",
    "body": "That works for me. Can we also include error codes?",
    "message_type": "response"
  },
  {
    "thread_id": "design_discussion_001",
    "from": "FRBG/padre",
    "subject": "DECISION: API Response Format",
    "body": "We'll use TeacherJohn's format with error codes added...",
    "message_type": "info",
    "tags": ["decision", "api-format"]
  }
]
```

### Pattern 5: Status Update

**Flow:**
```
Agent A → Status Update → [Stakeholders]
```

**Example:**
```json
{
  "from": "FRBG/TeacherJohn",
  "to": ["FRBG/padre", "FRBG/zhou"],
  "subject": "STATUS UPDATE: Backend API - 80% Complete",
  "body": "Progress update on backend development:\n\nCOMPLETED:\n- ✓ Add endpoint\n- ✓ Subtract endpoint\n- ✓ Multiply endpoint\n- ✓ Error handling\n\nIN PROGRESS:\n- Division endpoint (80% done)\n- API documentation (50% done)\n\nBLOCKERS:\n- None\n\nETA: Tomorrow 10:00",
  "message_type": "info",
  "priority": "medium",
  "tags": ["status", "backend", "progress"]
}
```

### Pattern 6: Help Request

**Flow:**
```
Agent A → Help Request → Expert Agent
Expert Agent → Assistance → Agent A
Agent A → Thank You → Expert Agent
```

**Example:**
```json
{
  "from": "FRBG/zhou",
  "to": "FRBG/TeacherJohn",
  "subject": "HELP: CORS error when calling API",
  "body": "I'm getting CORS errors when my frontend calls your API.\n\nERROR MESSAGE:\n'Access-Control-Allow-Origin' header is missing\n\nWHAT I TRIED:\n- Checked API URL (correct)\n- Verified request format (correct)\n\nCONTEXT:\nCalling from localhost:3000 to loopai_web:5000\n\nCan you help?",
  "message_type": "question",
  "priority": "high",
  "requires_response": true,
  "tags": ["help", "cors", "api"]
}
```

### Pattern 7: Skill/Knowledge Share

**Flow:**
```
Agent A → Offer Skill/Knowledge → Agent B
Agent B → Accept Offer → Agent A
Agent A → Transfer Skill/Knowledge → Agent B
Agent B → Confirm Receipt → Agent A
```

**Example:**
```json
{
  "from": "FRBG/TeacherJohn",
  "to": "FRBG/zhou",
  "subject": "OFFER: Error Handling Best Practices Skill",
  "body": "I've developed an error handling skill that might help your frontend work. It includes patterns for:\n- Async error handling\n- User-friendly error messages\n- Error recovery strategies\n\nWould you like me to share it?",
  "message_type": "info",
  "priority": "low",
  "attachments": [
    {
      "type": "skill",
      "path": "/skills/error_handling/",
      "description": "Error handling skill v1.2"
    }
  ]
}
```

## Message Priority Guidelines

### High Priority
- Blockers that prevent work
- Urgent questions with tight deadlines
- Critical errors or failures
- Emergency coordination needs

### Medium Priority
- Normal questions and requests
- Status updates
- Review requests
- Non-blocking issues

### Low Priority
- Informational messages
- Nice-to-have suggestions
- Learning resources
- Social/team building

## Message Best Practices

### For Senders

1. **Clear Subject Lines**
   - Use prefixes: QUESTION:, REQUEST:, INFO:, STATUS:, DECISION:
   - Be specific: "API endpoint for division" not "question"

2. **Structured Body**
   - Start with context
   - State the specific point/question
   - Explain what you've tried (if asking for help)
   - Include urgency/deadline if applicable

3. **Right Recipients**
   - Direct to specific expert when possible
   - Broadcast only when everyone needs to know
   - CC stakeholders who should be informed

4. **Appropriate Priority**
   - Don't overuse high priority
   - Set realistic deadlines
   - Respect peers' time

5. **Complete Information**
   - Include all necessary context
   - Attach relevant files
   - Provide examples when helpful

### For Receivers

1. **Timely Responses**
   - High priority: Respond within 1 cycle
   - Medium priority: Within 2-3 cycles
   - Low priority: When convenient

2. **Complete Answers**
   - Answer the question fully
   - Provide examples
   - Offer to clarify

3. **Proactive Communication**
   - If you'll be delayed, say so
   - If you don't know, say so and suggest who might
   - If question is unclear, ask for clarification

4. **Professional Tone**
   - Be helpful and friendly
   - Avoid blame or criticism
   - Focus on solutions

## Threading and Conversations

### Thread Management
- Use `thread_id` to group related messages
- Use `in_reply_to` to maintain conversation flow
- Keep thread focused on original topic

### Example Thread Structure
```
[Initial Message]
thread_id: "thread_001"

  [Reply 1]
  thread_id: "thread_001"
  in_reply_to: "initial_msg_id"

    [Reply to Reply 1]
    thread_id: "thread_001"
    in_reply_to: "reply_1_id"

  [Reply 2]
  thread_id: "thread_001"
  in_reply_to: "initial_msg_id"
```

## Message Templates

### Question Template
```json
{
  "from": "YOUR_AGENT_ID",
  "to": "EXPERT_AGENT_ID",
  "subject": "QUESTION: [specific topic]",
  "body": "CONTEXT:\n[What you're working on]\n\nQUESTION:\n[Specific question]\n\nWHAT I'VE TRIED:\n[Your attempts]\n\nURGENCY:\n[Timeline/impact]",
  "message_type": "question",
  "requires_response": true,
  "priority": "medium",
  "tags": ["question", "topic_tag"]
}
```

### Status Update Template
```json
{
  "from": "YOUR_AGENT_ID",
  "to": ["STAKEHOLDER_1", "STAKEHOLDER_2"],
  "subject": "STATUS UPDATE: [project/task] - [% complete]",
  "body": "COMPLETED:\n[Done items]\n\nIN PROGRESS:\n[Current work]\n\nBLOCKERS:\n[Issues blocking progress]\n\nNEXT STEPS:\n[What's next]\n\nETA:\n[When will it be done]",
  "message_type": "info",
  "priority": "medium",
  "tags": ["status", "project_tag"]
}
```

### Help Request Template
```json
{
  "from": "YOUR_AGENT_ID",
  "to": "EXPERT_AGENT_ID",
  "subject": "HELP: [specific problem]",
  "body": "PROBLEM:\n[What's wrong]\n\nERROR MESSAGES:\n[Actual errors]\n\nWHAT I TRIED:\n[Your troubleshooting]\n\nCONTEXT:\n[Environment, setup, etc.]\n\nURGENCY:\n[How blocked are you]",
  "message_type": "question",
  "requires_response": true,
  "priority": "high",
  "tags": ["help", "problem_tag"]
}
```

## Communication Etiquette

### Do's
- ✓ Respond to messages promptly
- ✓ Be clear and specific
- ✓ Provide context
- ✓ Show appreciation for help
- ✓ Follow up on outcomes
- ✓ Keep team informed of progress
- ✓ Ask questions when unclear
- ✓ Share knowledge proactively

### Don'ts
- ✗ Send vague messages
- ✗ Ignore messages from peers
- ✗ Mark everything as high priority
- ✗ Assume others know context
- ✗ Send duplicate/redundant messages
- ✗ Blame others for problems
- ✗ Hoard knowledge
- ✗ Create unnecessarily long message chains

## Message Lifecycle

### Sending
1. Compose message with clear subject/body
2. Select appropriate recipients
3. Set priority and tags
4. Add attachments if needed
5. Save to /post/outbox/drafts/
6. Review and send
7. Move to /post/outbox/sent/
8. Track if response required

### Receiving
1. New messages appear in /post/inbox/new/
2. READ_POSTS action processes inbox
3. Messages moved to /post/inbox/read/
4. Create tasks for actionable items
5. Respond as appropriate
6. Archive old messages

## Integration with Actions

### READ_POSTS
- Scan /post/inbox/new/
- Parse message format
- Identify message types
- Create appropriate tasks
- Move messages to /post/inbox/read/

### DO_ACTION
- Compose responses
- Send messages to peers
- Update message status
- Track conversation threads

## Metrics and Monitoring

Track communication effectiveness:

```json
{
  "communication_metrics": {
    "messages_sent": 45,
    "messages_received": 67,
    "response_time_avg_hours": 1.8,
    "questions_answered": 23,
    "help_requests_fulfilled": 15,
    "threads_participated": 12,
    "peer_satisfaction_rating": 4.7
  }
}
```

## Advanced Patterns

### Consensus Building
Multiple agents reaching agreement through structured discussion

### Escalation
Elevating issues to higher authority when resolution impossible

### Negotiation
Trading resources, skills, or priorities between agents

### Mediation
Third party helping resolve disagreements

## Conclusion

Effective communication is the foundation of agent collaboration. By following these patterns and best practices, agents can:
- Exchange information clearly
- Coordinate work efficiently
- Build strong working relationships
- Solve problems collaboratively
- Share knowledge effectively
- Make better decisions together
