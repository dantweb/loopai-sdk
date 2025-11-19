# Agent Life v2 - PlantUML Diagrams

This folder contains comprehensive PlantUML diagrams visualizing the Agent Life v2 architecture and workflows.

## Diagrams Overview

### 01_system_architecture.puml
**System Architecture Overview**
- Complete system architecture with all layers
- Frontend components (Vue.js)
- Backend services (Flask)
- Database structure (PostgreSQL)
- Caching and messaging (Redis)
- Component relationships and data flow

**Best for:** Understanding overall system design

---

### 02_component_hierarchy.puml
**Frontend Component Hierarchy**
- Detailed component tree structure
- Parent-child relationships
- Shared services (Pinia Store, Socket.IO, API Service)
- All tabs and their child components
- State management flow

**Best for:** Frontend developers understanding component structure

---

### 03_database_erd.puml
**Database Entity Relationship Diagram**
- All database tables and their relationships
- Primary keys, foreign keys, indexes
- Field types and constraints
- Sample data examples
- Entity color coding by category

**Best for:** Database design and backend development

---

### 04_cycle_execution_flow.puml
**Cycle Execution Flow**
- Complete cycle lifecycle from creation to completion
- User interactions and system responses
- Parallel operations (execution, monitoring, control)
- State transitions
- Error handling paths

**Best for:** Understanding how cycles execute end-to-end

---

### 05_realtime_event_flow.puml
**Real-Time Socket.IO Event Flow**
- Connection and subscription process
- Event propagation through the system
- Redis pub/sub integration
- Real-time UI updates
- Error event handling
- User control actions

**Best for:** Understanding real-time communication architecture

---

### 06_api_sequences.puml
**API Sequence Diagrams**
- Create and start cycle sequence
- Pause and resume cycle sequence
- Real-time monitoring subscription
- Fetch execution logs sequence
- Component interactions for each scenario

**Best for:** API integration and backend development

---

### 07_implementation_timeline.puml
**Implementation Timeline (Gantt Chart)**
- 12-week implementation schedule
- 6 phases with detailed tasks
- Task dependencies and milestones
- Color-coded by activity type
- Critical path visualization

**Best for:** Project planning and management

---

### 08_action_constellation_flow.puml
**Action Constellation Execution Flow**
- Constellation parsing and execution
- Single action execution
- Loop execution with iterations
- Conditional execution (future)
- Parallel execution (future)
- Reflection action handling

**Best for:** Understanding action orchestration logic

---

## Viewing the Diagrams

### Online Viewers
1. **PlantUML Online Server**
   - Visit: http://www.plantuml.com/plantuml/uml/
   - Paste diagram code
   - View rendered diagram

2. **PlantUML Visual Studio Code Extension**
   ```bash
   # Install extension
   code --install-extension jebbs.plantuml

   # Open .puml file and press Alt+D to preview
   ```

3. **IntelliJ IDEA Plugin**
   - Install PlantUML integration plugin
   - Open .puml files to see live preview

### Command Line (Generate PNG/SVG)
```bash
# Install PlantUML
brew install plantuml  # macOS
apt-get install plantuml  # Linux

# Generate PNG
plantuml *.puml

# Generate SVG
plantuml -tsvg *.puml

# Generate all formats
plantuml -tpng -tsvg *.puml
```

### Docker
```bash
# Generate all diagrams
docker run --rm -v $(pwd):/data plantuml/plantuml *.puml
```

---

## Diagram Colors & Legend

### System Architecture (01)
- **Light Blue** (#B0E0E6) - Frontend components
- **Light Orange** (#FFE4B5) - Backend services
- **Light Yellow** (#FFFFE0) - Database
- **Light Purple** (#DDA0DD) - Cache/Messaging
- **Light Green** (#90EE90) - UI Components
- **Light Pink** (#FFB6C1) - Services

### Component Hierarchy (02)
- **Blue** (#4169E1) - Root container
- **Red** (#FF6347) - Shared services
- **Green** (#32CD32) - Chat tab
- **Sky Blue** (#1E90FF) - Cycles tab
- **Pink** (#FF69B4) - Monitor tab
- **Purple** (#9370DB) - Constellations tab
- **Gold** (#FFD700) - Analytics tab

### Database ERD (03)
- **Blue** (#4169E1) - Users & Auth
- **Green** (#32CD32) - Cycle Configuration
- **Red** (#FF6347) - Execution State
- **Gold** (#FFD700) - Logs & Audit
- **Purple** (#9370DB) - Action Config
- **Pink** (#FF69B4) - Agents

### Implementation Timeline (07)
- **Light Blue** - Backend Development
- **Light Green** - Frontend Development
- **Pink** - Testing
- **Yellow** - Optimization & Documentation
- **Orange** - Deployment
- **Red** - Milestones

---

## Updating Diagrams

When making changes to the design:

1. **Update corresponding .puml file**
2. **Test rendering** to ensure no syntax errors
3. **Update this README** if adding new diagrams
4. **Regenerate images** (optional, for documentation)
5. **Commit changes** with descriptive message

Example:
```bash
# Edit diagram
vim 01_system_architecture.puml

# Test rendering
plantuml -tpng 01_system_architecture.puml

# Commit
git add 01_system_architecture.puml
git commit -m "Update system architecture: Add Redis pub/sub"
```

---

## Integration with Documentation

These diagrams complement the design documentation in the parent folder:

- **00_OVERVIEW.md** ← Use diagrams 01, 02
- **01_CYCLE_MANAGEMENT_DESIGN.md** ← Use diagrams 03, 04, 06
- **02_ACTION_CONSTELLATION_DESIGN.md** ← Use diagram 08
- **03_FRONTEND_INTEGRATION.md** ← Use diagram 02
- **04_BACKEND_INTEGRATION.md** ← Use diagrams 01, 03, 06
- **05_REALTIME_MONITORING.md** ← Use diagram 05
- **06_IMPLEMENTATION_ROADMAP.md** ← Use diagram 07

---

## Tips for Reading PlantUML

### Basic Syntax
```plantuml
' Comments start with single quote

package "Package Name" {
  component "Component" as Alias
}

Alias --> OtherComponent : "relationship label"

note right of Alias
  Additional information
end note
```

### Common Elements
- **Rectangles** - Components/Services
- **Databases** - Database icons
- **Actors** - User/external systems
- **Clouds** - External services
- **Arrows** - Relationships/data flow
- **Colors** - Functional grouping
- **Notes** - Additional context

### Reading Sequence Diagrams
- **Time flows down** (top to bottom)
- **Horizontal arrows** - Messages/calls
- **Activation bars** - Component is processing
- **Return arrows** - Response/result
- **Alt/Opt boxes** - Conditional flows

---

## Common Issues

### Diagram Won't Render
1. Check for syntax errors (missing brackets, quotes)
2. Verify PlantUML server is accessible
3. Try online viewer for debugging
4. Check for unsupported features in your PlantUML version

### Colors Not Showing
1. Ensure color codes are valid hex colors
2. Use `skinparam` for global styling
3. Use `#HEX` for inline colors
4. Try different themes with `!theme`

### Layout Issues
1. Use `skinparam linetype ortho` for straight lines
2. Add `hidden` arrows to adjust spacing
3. Use `left to right direction` to change orientation
4. Group related components in packages

---

## Resources

### PlantUML Documentation
- Official docs: https://plantuml.com/
- Sequence diagrams: https://plantuml.com/sequence-diagram
- Activity diagrams: https://plantuml.com/activity-diagram-beta
- Component diagrams: https://plantuml.com/component-diagram

### Themes
- Available themes: https://plantuml.com/theme
- Custom themes: https://plantuml.com/skinparam

### Examples
- Real World PlantUML: https://real-world-plantuml.com/
- PlantUML Examples: https://github.com/plantuml/plantuml/tree/master/examples

---

## Contributing

When adding new diagrams:

1. **Follow naming convention**: `NN_descriptive_name.puml`
2. **Use consistent colors** across diagrams
3. **Add legend** for color meanings
4. **Include notes** for complex parts
5. **Update this README** with diagram description
6. **Test rendering** before committing

---

**Last Updated:** 2025-11-19
**Diagrams Version:** 1.0
**PlantUML Version:** Latest (tested with online server)
