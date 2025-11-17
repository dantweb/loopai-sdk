# Knowledge Sharing Protocols

## Overview

Knowledge sharing enables agents to collaborate, learn from each other, and make better decisions through consultation. This document describes protocols for peer-to-peer knowledge exchange, question answering, and collaborative problem-solving.

## Core Knowledge Sharing Patterns

### 1. Ask Question Pattern
Agent needs information or clarification from a peer

### 2. Request Opinion Pattern
Agent wants validation or alternative perspective on a decision

### 3. Share Knowledge Pattern
Agent proactively shares learned information with peers

### 4. Collaborative Problem-Solving Pattern
Multiple agents work together on a complex problem

## Directory Structure

```
/agentlife/knowledge/
├── learned/                        # Knowledge acquired from others
│   ├── from_TeacherJohn/
│   │   ├── api_best_practices.md
│   │   └── error_handling_tips.json
│   └── from_zhou/
│       ├── ui_patterns.md
│       └── responsive_design_guide.md
├── shared/                         # Knowledge shared with others
│   ├── to_TeacherJohn/
│   └── to_zhou/
├── questions/                      # Questions asked to peers
│   ├── pending/
│   ├── answered/
│   └── archived/
└── experts/                        # Directory of peer expertise
    └── expertise_registry.json
```

## Protocol 1: Ask Question

### Use Case
Agent encounters a problem or needs clarification from a peer with relevant expertise.

### Protocol File
```json
{
  "protocol_version": "1.0",
  "protocol_id": "ask_question",
  "instruction": "When stuck or needing clarification, identify expert peers and ask specific questions",

  "steps": [
    {
      "step_id": "identify_need",
      "action": "Recognize that you need external help",
      "triggers": [
        "Blocked on task for >30 minutes",
        "Uncertainty about approach",
        "Need domain-specific expertise",
        "Want validation before proceeding"
      ]
    },
    {
      "step_id": "identify_expert",
      "action": "Find agent with relevant expertise",
      "method": "Read /knowledge/experts/expertise_registry.json or analyze peer identities in /self/"
    },
    {
      "step_id": "formulate_question",
      "action": "Create clear, specific question with context",
      "question_structure": {
        "subject": "QUESTION: [topic]",
        "context": "What I'm working on and why",
        "specific_question": "Clear, answerable question",
        "what_tried": "Approaches already attempted",
        "urgency": "high|medium|low"
      }
    },
    {
      "step_id": "send_question",
      "action": "Post question to peer's inbox",
      "file_operation": {
        "target": "/post/outbox/sent/question_to_{peer}_{timestamp}.json",
        "recipient_inbox": "/{peer_path}/post/inbox/new/"
      }
    },
    {
      "step_id": "track_question",
      "action": "Create tracking task",
      "file_operation": {
        "path": "/knowledge/questions/pending/question_{id}.json",
        "content": {
          "question_id": "string",
          "asked_to": "agent_id",
          "asked_at": "ISO8601",
          "topic": "string",
          "urgency": "string",
          "status": "pending"
        }
      }
    },
    {
      "step_id": "await_response",
      "action": "Check for answer in subsequent READ_POSTS cycles"
    },
    {
      "step_id": "process_answer",
      "action": "When answer received, apply knowledge and archive question",
      "file_operations": [
        {
          "move": "/knowledge/questions/pending/question_{id}.json",
          "to": "/knowledge/questions/answered/question_{id}.json"
        },
        {
          "create": "/knowledge/learned/from_{peer}/answer_{id}.md",
          "content": "Answer content for future reference"
        }
      ]
    },
    {
      "step_id": "thank_peer",
      "action": "Send thank you message acknowledging help"
    }
  ],

  "example_question": {
    "from": "FRBG/zhou",
    "to": "FRBG/TeacherJohn",
    "subject": "QUESTION: Best practice for API error responses",
    "body": "Hi TeacherJohn,\n\nI'm building the frontend for our calculator project and need to handle errors from your backend API.\n\nSPECIFIC QUESTION:\nWhat error response format will your API return when there's a problem (e.g., division by zero or invalid input)?\n\nCONTEXT:\nI need to:\n- Display error messages to users\n- Handle different error types appropriately\n- Provide helpful feedback\n\nWHAT I'M THINKING:\nShould I expect something like:\n{\n  \"error\": true,\n  \"message\": \"Division by zero not allowed\",\n  \"code\": \"DIV_BY_ZERO\"\n}\n\nOr a different format?\n\nURGENCY: Medium (working on error handling today)\n\nThanks for your help!\n\n- zhou",
    "timestamp": "2025-11-16T10:30:00Z",
    "priority": "medium",
    "tags": ["question", "api", "error-handling"]
  },

  "example_answer": {
    "from": "FRBG/TeacherJohn",
    "to": "FRBG/zhou",
    "subject": "RE: Best practice for API error responses",
    "body": "Hi zhou,\n\nGreat question! Here's the error format I'm implementing:\n\n```json\n{\n  \"success\": false,\n  \"error\": {\n    \"code\": \"DIV_BY_ZERO\",\n    \"message\": \"Division by zero is not allowed\",\n    \"details\": {\n      \"operation\": \"divide\",\n      \"operand1\": 10,\n      \"operand2\": 0\n    }\n  }\n}\n```\n\nERROR CODES:\n- DIV_BY_ZERO - Division by zero attempt\n- INVALID_INPUT - Non-numeric input\n- INVALID_OPERATION - Unknown operation\n- SERVER_ERROR - Internal server error\n\nFor successful responses:\n```json\n{\n  \"success\": true,\n  \"result\": 42\n}\n```\n\nI'll document this in the API docs today.\n\nLet me know if you need clarification!\n\n- TeacherJohn",
    "timestamp": "2025-11-16T11:15:00Z"
  }
}
```

## Protocol 2: Request Second Opinion

### Use Case
Agent has made a decision but wants validation or alternative perspectives before proceeding.

### Protocol File
```json
{
  "protocol_version": "1.0",
  "protocol_id": "request_opinion",
  "instruction": "Request peer review or second opinion on decisions, designs, or approaches",

  "steps": [
    {
      "step_id": "identify_decision",
      "action": "Recognize decision that would benefit from review",
      "decision_types": [
        "Architecture or design choice",
        "Implementation approach",
        "Problem-solving strategy",
        "Risk assessment",
        "Priority ordering"
      ]
    },
    {
      "step_id": "prepare_context",
      "action": "Document decision context",
      "required_info": {
        "situation": "Current state and problem",
        "proposed_solution": "Your recommendation",
        "alternatives_considered": "Other options you evaluated",
        "reasoning": "Why you prefer this approach",
        "concerns": "Any doubts or uncertainties",
        "impact": "Who/what this affects"
      }
    },
    {
      "step_id": "select_reviewers",
      "action": "Choose 1-2 peers with relevant expertise",
      "criteria": [
        "Domain expertise",
        "Different perspective (e.g., frontend reviewing backend)",
        "Experience with similar decisions"
      ]
    },
    {
      "step_id": "send_request",
      "action": "Send opinion request with full context"
    },
    {
      "step_id": "collect_opinions",
      "action": "Gather responses from reviewers"
    },
    {
      "step_id": "synthesize_feedback",
      "action": "Analyze all opinions and integrate insights",
      "considerations": [
        "Points of agreement across reviewers",
        "Concerns raised by multiple people",
        "New alternatives suggested",
        "Risks identified"
      ]
    },
    {
      "step_id": "make_final_decision",
      "action": "Make informed decision incorporating feedback"
    },
    {
      "step_id": "communicate_decision",
      "action": "Share final decision with reviewers and stakeholders"
    }
  ],

  "example_request": {
    "from": "FRBG/TeacherJohn",
    "to": "FRBG/padre, FRBG/zhou",
    "subject": "REVIEW REQUEST: API Endpoint Design",
    "body": "Hi team,\n\nI'd like a second opinion on the API endpoint design for our calculator.\n\nPROPOSED DESIGN:\nSingle endpoint: POST /api/calculate\nBody: {\"operation\": \"add|subtract|multiply|divide\", \"num1\": number, \"num2\": number}\n\nALTERNATIVE CONSIDERED:\nSeparate endpoints: POST /api/add, POST /api/subtract, etc.\n\nMY REASONING:\n- Single endpoint is simpler\n- Easier to add new operations later\n- Less code duplication\n- Follows DRY principle\n\nCONCERNS:\n- Might be less RESTful?\n- Operation as parameter vs URL path\n\nIMPACT:\n- Affects frontend API calls (zhou's work)\n- Affects API documentation\n- Hard to change later\n\nWhat do you think? Any concerns or alternative suggestions?\n\nThanks,\nTeacherJohn",
    "timestamp": "2025-11-16T09:00:00Z",
    "priority": "high",
    "tags": ["review", "architecture", "api-design"]
  },

  "example_opinions": [
    {
      "from": "FRBG/padre",
      "opinion": "I support the single endpoint approach. It's more maintainable and the operation as a parameter is fine for this use case. Document it clearly and it'll work well.",
      "concerns": [],
      "suggestions": ["Add API versioning from the start: /api/v1/calculate"]
    },
    {
      "from": "FRBG/zhou",
      "opinion": "From frontend perspective, single endpoint is easier to work with. I can have one API call function that just changes the operation parameter.",
      "concerns": ["Make sure error messages specify which operation failed"],
      "suggestions": ["Return the operation in the response so I can show 'Addition result: 42'"]
    }
  ]
}
```

## Protocol 3: Share Knowledge Proactively

### Use Case
Agent learns something valuable and wants to share with team.

### Protocol File
```json
{
  "protocol_version": "1.0",
  "protocol_id": "share_knowledge",
  "instruction": "Proactively share useful knowledge, tips, and lessons learned with peers",

  "steps": [
    {
      "step_id": "identify_shareable_knowledge",
      "action": "Recognize information that would benefit others",
      "triggers": [
        "Solved a difficult problem",
        "Learned a better approach",
        "Discovered useful resource",
        "Identified common pitfall",
        "Found efficiency improvement"
      ]
    },
    {
      "step_id": "determine_audience",
      "action": "Identify who would benefit most",
      "options": [
        "Specific peer with related work",
        "Team working on same project",
        "All agents in domain",
        "Entire community"
      ]
    },
    {
      "step_id": "package_knowledge",
      "action": "Create clear, reusable documentation",
      "formats": {
        "quick_tip": "Short message with tip",
        "how_to_guide": "Step-by-step instructions",
        "lesson_learned": "Problem, solution, outcome",
        "resource_share": "Link/file with explanation"
      }
    },
    {
      "step_id": "share_knowledge",
      "action": "Distribute to identified audience",
      "methods": [
        "Direct message to specific peers",
        "Post to team channel",
        "Add to /knowledge/shared/",
        "Update skill documentation"
      ]
    },
    {
      "step_id": "make_discoverable",
      "action": "Ensure knowledge can be found later",
      "actions": [
        "Tag appropriately",
        "Add to knowledge index",
        "Update relevant skill READMEs"
      ]
    }
  ],

  "example_share": {
    "from": "FRBG/zhou",
    "to": "FRBG/team",
    "subject": "TIP: Handling Async API Calls in Frontend",
    "body": "Hey team,\n\nI just solved an issue with async API calls that might help others.\n\nPROBLEM:\nCalculator buttons were clickable multiple times during API call, causing duplicate requests.\n\nSOLUTION:\nDisable buttons during API call:\n\n```javascript\nconst button = document.getElementById('addButton');\nbutton.disabled = true;\n\ntry {\n  const result = await fetch('/api/calculate', {...});\n  // handle result\n} finally {\n  button.disabled = false; // Re-enable even if error\n}\n```\n\nKEY INSIGHT:\nAlways use try/finally to re-enable UI, even on errors.\n\nI've added this pattern to our frontend guidelines.\n\nHope this helps!\n- zhou",
    "timestamp": "2025-11-16T14:30:00Z",
    "tags": ["tip", "frontend", "async", "best-practice"]
  }
}
```

## Protocol 4: Collaborative Problem-Solving

### Use Case
Multiple agents work together on a complex problem requiring combined expertise.

### Protocol File
```json
{
  "protocol_version": "1.0",
  "protocol_id": "collaborative_problem_solving",
  "instruction": "Coordinate with multiple peers to solve complex problems requiring diverse expertise",

  "steps": [
    {
      "step_id": "recognize_complexity",
      "action": "Identify problem requiring multi-agent collaboration",
      "indicators": [
        "Crosses multiple domains",
        "Requires diverse expertise",
        "Too large for single agent",
        "High impact/risk",
        "Tight interdependencies"
      ]
    },
    {
      "step_id": "assemble_team",
      "action": "Identify agents needed for solution",
      "considerations": [
        "Required expertise areas",
        "Current workload of agents",
        "Past collaboration success",
        "Complementary perspectives"
      ]
    },
    {
      "step_id": "frame_problem",
      "action": "Create shared problem statement",
      "components": {
        "problem_description": "Clear statement of issue",
        "constraints": "Limitations and requirements",
        "success_criteria": "What defines solution",
        "timeline": "When solution needed",
        "stakeholders": "Who is affected"
      }
    },
    {
      "step_id": "brainstorm_approaches",
      "action": "Each agent contributes perspective",
      "process": [
        "Sequential sharing (avoid groupthink)",
        "Build on each other's ideas",
        "Challenge assumptions respectfully",
        "Document all suggestions"
      ]
    },
    {
      "step_id": "evaluate_options",
      "action": "Collectively assess approaches",
      "criteria": [
        "Feasibility",
        "Risk",
        "Resource requirements",
        "Timeline fit",
        "Quality of outcome"
      ]
    },
    {
      "step_id": "decide_approach",
      "action": "Reach consensus on solution",
      "methods": [
        "Unanimous agreement (preferred)",
        "Majority vote if needed",
        "Escalate to manager if deadlock"
      ]
    },
    {
      "step_id": "divide_work",
      "action": "Assign responsibilities to agents",
      "considerations": [
        "Leverage individual expertise",
        "Balance workload",
        "Identify dependencies",
        "Set checkpoints"
      ]
    },
    {
      "step_id": "execute_collaboratively",
      "action": "Work with frequent sync-ups",
      "practices": [
        "Daily progress updates",
        "Immediate communication of blockers",
        "Share work-in-progress for feedback",
        "Adjust plan as needed"
      ]
    },
    {
      "step_id": "integrate_solution",
      "action": "Combine individual contributions",
      "activities": [
        "Merge components",
        "Test integration",
        "Resolve conflicts",
        "Validate against criteria"
      ]
    },
    {
      "step_id": "retrospective",
      "action": "Learn from collaboration",
      "questions": [
        "What worked well?",
        "What could improve?",
        "What did we learn?",
        "How can we collaborate better next time?"
      ]
    }
  ],

  "example_collaboration": {
    "problem": "Calculator project integration failing",
    "team": ["FRBG/TeacherJohn", "FRBG/zhou", "FRBG/padre"],
    "timeline": [
      {
        "time": "09:00",
        "action": "padre identifies integration issues and assembles team"
      },
      {
        "time": "09:15",
        "action": "Team meets virtually (via messages) to frame problem"
      },
      {
        "time": "09:30",
        "action": "Each agent shares perspective: backend works standalone, frontend works standalone, but together they fail"
      },
      {
        "time": "10:00",
        "action": "Brainstorm: API URL mismatch? CORS issue? Data format mismatch?"
      },
      {
        "time": "10:30",
        "action": "Discover issue: frontend sending operation as 'add' but backend expects 'addition'"
      },
      {
        "time": "11:00",
        "action": "Decide: Standardize on backend terms, update frontend"
      },
      {
        "time": "11:30",
        "action": "zhou updates frontend, TeacherJohn confirms backend expectations"
      },
      {
        "time": "12:00",
        "action": "padre tests integration - SUCCESS"
      },
      {
        "time": "12:15",
        "action": "Team retrospective: Document API contract from the start next time"
      }
    ]
  }
}
```

## Expertise Registry

Agents maintain a registry of peer expertise:

```json
{
  "expertise_registry": {
    "last_updated": "2025-11-16T16:00:00Z",
    "agents": [
      {
        "agent_id": "FRBG/TeacherJohn",
        "specialization": "Backend Developer",
        "expertise": ["REST API development", "Database design", "Server-side programming"],
        "availability": "active",
        "response_time_avg_hours": 2,
        "helpfulness_rating": 4.8
      },
      {
        "agent_id": "FRBG/zhou",
        "specialization": "Frontend Developer",
        "expertise": ["HTML/CSS/JavaScript", "UI/UX design", "API integration"],
        "availability": "active",
        "response_time_avg_hours": 1.5,
        "helpfulness_rating": 4.9
      },
      {
        "agent_id": "FRBG/padre",
        "specialization": "Project Manager",
        "expertise": ["Project planning", "Team coordination", "Integration testing"],
        "availability": "active",
        "response_time_avg_hours": 1,
        "helpfulness_rating": 5.0
      }
    ]
  }
}
```

## Best Practices

### For Asking Questions
1. Search existing knowledge first
2. Be specific and provide context
3. Explain what you've already tried
4. Respect peer time - ask when truly needed
5. Follow up and share outcome

### For Answering Questions
1. Respond promptly (within 1-2 cycles)
2. Provide complete, actionable answers
3. Include examples when possible
4. Offer to clarify if needed
5. Don't just answer - teach the concept

### For Sharing Knowledge
1. Share proactively when knowledge is fresh
2. Make knowledge discoverable with tags
3. Provide context and examples
4. Update when you learn better approaches
5. Credit sources and collaborators

### For Collaboration
1. Communicate frequently and clearly
2. Document decisions and reasoning
3. Respect diverse perspectives
4. Focus on problem, not personalities
5. Learn from every collaboration

## Measuring Knowledge Sharing Success

Track metrics to improve collaboration:

```json
{
  "knowledge_metrics": {
    "questions_asked": 15,
    "questions_answered": 23,
    "response_time_avg_hours": 1.8,
    "knowledge_documents_created": 8,
    "skills_traded": 3,
    "collaboration_sessions": 5,
    "peer_satisfaction_rating": 4.7,
    "knowledge_reuse_count": 47
  }
}
```

## Integration with Actions

Knowledge sharing integrates into the daily action lifecycle:

- **READ_POSTS**: Check for questions, opinion requests, knowledge shares
- **GET_WORK**: Prioritize helping peers when expertise matches
- **DO_ACTION**: Execute consultation, create knowledge artifacts
- **VALIDATE_ACTION**: Ensure knowledge shared was accurate and helpful
- **VALIDATE_WORK**: Reflect on what was learned, document for future

## Conclusion

Effective knowledge sharing transforms individual agents into a collaborative community that:
- Solves problems faster through collective intelligence
- Avoids repeated mistakes by learning from each other
- Builds institutional knowledge that persists
- Improves continuously through shared insights
- Creates stronger solutions through diverse perspectives
