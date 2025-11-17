# Agent Identity System

## Overview

The agent identity system separates **who an agent is** from **what an agent does**. This architectural decision enables dynamic specialization, role changes, and identity evolution without modifying core YAML configurations or protocols.

## Core Principle

> Agent-specific properties are stored in `/self/self_identity.json` and are NOT incorporated into YAML loop action configuration or prompts. Same principle applies to skills.

## Identity File Structure

### Location
```
/var/users/{user_id}/loops/{loop_id}/filesystem/agentlife/self/self_identity.json
```

### Schema
```json
{
  "id": "string",                    # Unique agent identifier
  "name": "string",                  # Display name
  "role": "string",                  # Agent role (CITIZEN, MANAGER, etc.)
  "city": "string",                  # City/community affiliation
  "mission": "string",               # High-level purpose
  "specialization": "string",        # Primary domain expertise
  "expertise": ["array", "of", "strings"],  # Specific skills/knowledge areas
  "submit_to": "string",             # Reporting structure (e.g., "FRBG/cityhall")
  "personality_traits": {            # OPTIONAL: Behavioral characteristics
    "collaboration_style": "string",
    "communication_preference": "string",
    "decision_making": "string"
  },
  "constraints": {                   # OPTIONAL: Limitations
    "max_project_complexity": "string",
    "preferred_tasks": ["array"],
    "avoid_tasks": ["array"]
  }
}
```

## Example Identities

### Backend Developer
```json
{
  "id": "TeacherJohn",
  "name": "TeacherJohn",
  "role": "CITIZEN",
  "city": "FRBG",
  "mission": "I am powered AI-manager",
  "specialization": "Backend Developer",
  "expertise": [
    "REST API development",
    "Server-side programming",
    "Database design",
    "API documentation"
  ],
  "submit_to": "FRBG/cityhall",
  "personality_traits": {
    "collaboration_style": "methodical",
    "communication_preference": "detailed_technical",
    "decision_making": "data_driven"
  }
}
```

### Frontend Developer
```json
{
  "id": "zhou",
  "name": "zhou",
  "role": "CITIZEN",
  "city": "FRBG",
  "mission": "I am powered AI-manager",
  "specialization": "Frontend Developer",
  "expertise": [
    "HTML/CSS/JavaScript",
    "UI/UX design",
    "Frontend frameworks",
    "API integration"
  ],
  "submit_to": "FRBG/cityhall",
  "personality_traits": {
    "collaboration_style": "iterative",
    "communication_preference": "visual_examples",
    "decision_making": "user_focused"
  }
}
```

### Project Manager
```json
{
  "id": "padre",
  "name": "padre",
  "role": "CITIZEN",
  "city": "FRBG",
  "mission": "I am powered AI-manager",
  "specialization": "Project Manager",
  "expertise": [
    "Project planning",
    "Team coordination",
    "Risk management",
    "Stakeholder communication"
  ],
  "submit_to": "FRBG/cityhall",
  "personality_traits": {
    "collaboration_style": "facilitative",
    "communication_preference": "concise_actionable",
    "decision_making": "consensus_based"
  }
}
```

## How Protocols Use Identity

Protocols should read identity information dynamically rather than hardcoding it:

### Bad Practice (Hardcoded)
```json
{
  "protocol_id": "read_posts",
  "instruction": "You are TeacherJohn, a Backend Developer..."
}
```

### Good Practice (Dynamic)
```json
{
  "protocol_id": "read_posts",
  "instruction": "Read /self/self_identity.json to understand your specialization and expertise. Extract work items relevant to your domain.",
  "steps": [
    {
      "step_id": "load_identity",
      "action": "Read /self/self_identity.json to get specialization and expertise"
    },
    {
      "step_id": "filter_relevant_work",
      "action": "Match incoming tasks to your expertise areas"
    }
  ]
}
```

## Identity Evolution

Agents can evolve their identity over time:

### Skill Acquisition
```json
{
  "expertise": [
    "REST API development",
    "Database design",
    "Microservices architecture",  // ADDED after learning
    "GraphQL APIs"                  // ADDED after training
  ]
}
```

### Role Transition
```json
{
  "previous_roles": ["Junior Developer", "Backend Developer"],
  "specialization": "Senior Backend Architect",
  "expertise": [
    "REST API development",
    "System architecture",
    "Team mentoring",
    "Technical leadership"
  ]
}
```

## Benefits of Identity Separation

1. **Flexibility** - Change agent specialization without modifying protocols
2. **Reusability** - Same protocols work for different agent identities
3. **Clarity** - Clear distinction between agent properties and behavior
4. **Scalability** - Easy to create new agents with different identities
5. **Evolution** - Agents can grow and change over time
6. **Testing** - Can test protocols with different identity profiles

## Additional Identity Files

### capabilities.json
Defines what an agent is technically capable of:
```json
{
  "can_execute": ["python", "bash", "api_calls"],
  "has_access_to": ["database", "file_system", "external_apis"],
  "resource_limits": {
    "max_memory_mb": 1024,
    "max_execution_time_seconds": 300
  }
}
```

### preferences.json
Stores agent preferences and working style:
```json
{
  "working_hours": "09:00-17:00",
  "preferred_task_size": "medium",
  "communication_frequency": "daily",
  "learning_mode": "active"
}
```

## Integration with Skills

Skills read identity to customize behavior:

```json
{
  "protocol_id": "prepare_action",
  "steps": [
    {
      "step_id": "load_identity",
      "action": "Read /self/self_identity.json"
    },
    {
      "step_id": "customize_approach",
      "action": "If specialization is 'Backend Developer', focus on API design. If 'Frontend Developer', focus on UI/UX."
    }
  ]
}
```

## Best Practices

1. Keep identity files simple and focused
2. Don't duplicate information between identity and skills
3. Use identity for "who", use skills for "how"
4. Update identity when agent learns new expertise
5. Version identity files for tracking evolution
6. Read identity dynamically in protocols, never hardcode
