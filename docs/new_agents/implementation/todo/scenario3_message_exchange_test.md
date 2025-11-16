# Scenario 3: Inter-Agent Message Exchange Test
**Created:** 2025-11-16
**Purpose:** Validate that agents can send and receive messages between each other
**Duration:** 2-3 days

---

## Test Objective

Validate the complete message exchange cycle:
1. **TeacherJohn** receives a request to contact **maria**
2. **TeacherJohn** sends a message to **maria** asking for activity report
3. **maria** receives the message and responds with her status
4. Message exchange happens automatically via `run_message_exchange.py`

---

## System Update

**IMPORTANT:** `run_all_cycles.py` has been updated to include message exchange!

**New Feature Added:**
```python
# After each day's actions, run message exchange
📬 MESSAGE EXCHANGE (End of Day X)
  🔄 Processing inter-agent messages...
  ✅ Message exchange completed
```

This ensures messages placed in agent outboxes are collected and delivered to recipient inboxes.

---

## Test Setup

### Initial Message to TeacherJohn

**File:** `/loops/70/filesystem/agentlife/post/inbox/new/test_message_exchange.json`

```json
{
  "message_id": "msg_exchange_test_001",
  "from": "project_manager",
  "to": "TeacherJohn",
  "timestamp": "2025-11-16T13:00:00Z",
  "subject": "Urgent: Need status update from maria",
  "body": "Hi TeacherJohn, I need you to reach out to maria and ask her to report her latest activity. Specifically, ask her what she's been working on in the past 2 days and if there are any blockers. This is important for our team coordination meeting tomorrow. Please get back to me with her response.",
  "priority": "high",
  "type": "delegation_request"
}
```

---

## Expected Behavior Flow

### Day 1: TeacherJohn Processes Request

**1. READ_POSTS (Morning)**
- TeacherJohn reads the message from project_manager
- Creates task: "Contact maria for activity report"
- Priority: HIGH

**2. GET_WORK**
- Selects the high-priority task
- Recognizes this as a delegation/communication task
- Creates working plan to compose message to maria

**3. PREPARE_ACTION → DO_ACTION → VALIDATE_ACTION (Iterations 1-3)**
- **Iteration 1:**
  - PREPARE: Plan message content (what to ask maria)
  - DO: Compose message to maria
  - VALIDATE: Check message is clear and complete

- **Expected Message File Created:**
  `/loops/70/filesystem/agentlife/post/outbox/new/msg_to_maria_*.json`

```json
{
  "message_id": "msg_to_maria_001",
  "from": "TeacherJohn",
  "to": "maria",
  "timestamp": "2025-11-16T13:30:00Z",
  "subject": "Activity Report Request",
  "body": "Hi maria, the project manager has asked me to check in with you. Could you please provide an update on what you've been working on over the past 2 days? Also, let me know if you're facing any blockers that might need attention. This is for our team coordination meeting tomorrow. Thanks!",
  "priority": "high",
  "type": "information_request"
}
```

**4. VALIDATE_WORK**
- Confirms message was created and placed in outbox
- Marks task as completed

**5. MESSAGE EXCHANGE (End of Day 1)**
- `run_message_exchange.py` runs
- Collects message from TeacherJohn's outbox
- Delivers to maria's inbox: `/loops/73/filesystem/agentlife/post/inbox/new/`

---

### Day 2: maria Processes Request

**1. READ_POSTS (Morning)**
- maria reads message from TeacherJohn
- Creates task: "Respond to TeacherJohn with activity report"
- Priority: HIGH

**2. GET_WORK**
- Selects the task
- Recognizes need to provide status update
- Creates working plan to compile recent work and respond

**3. PREPARE_ACTION → DO_ACTION → VALIDATE_ACTION (Iterations 1-3)**
- **Iteration 1:**
  - PREPARE: Review recent work (past 2 days)
  - DO: Compile activity summary
  - VALIDATE: Check completeness

- **Iteration 2:**
  - PREPARE: Plan response message
  - DO: Compose response to TeacherJohn
  - VALIDATE: Check message quality

**Expected Response Message Created:**
`/loops/73/filesystem/agentlife/post/outbox/new/msg_response_to_teacherjohn_*.json`

```json
{
  "message_id": "msg_response_to_teacherjohn_001",
  "from": "maria",
  "to": "TeacherJohn",
  "timestamp": "2025-11-16T14:00:00Z",
  "subject": "Re: Activity Report Request",
  "body": "Hi TeacherJohn, here's my activity report for the past 2 days:\n\nDay 1: Worked on marketplace frontend components - completed product listing UI and shopping cart interface. Made good progress on responsive design.\n\nDay 2: Started checkout flow UI integration. Discovered one blocker: waiting for padre to complete the checkout API endpoint before I can fully test the integration. Should be resolved soon.\n\nOverall progress: ~70% complete on frontend MVP. No major blockers besides the API dependency mentioned above.\n\nLet me know if you need any additional details for the meeting!",
  "priority": "high",
  "type": "information_response"
}
```

**4. MESSAGE EXCHANGE (End of Day 2)**
- Collects maria's response from outbox
- Delivers to TeacherJohn's inbox

---

### Day 3: TeacherJohn Receives Response

**1. READ_POSTS (Morning)**
- TeacherJohn reads maria's response
- Creates task: "Forward maria's status to project_manager"

**2. GET_WORK**
- Processes maria's information
- Creates summary message back to project_manager

---

## Validation Criteria

### ✅ Must Have (Critical)

**A. Message Creation**
- [ ] TeacherJohn created message file in his outbox
- [ ] Message to maria is well-formatted JSON
- [ ] Message content is relevant and professional
- [ ] Message asks for activity report and blockers

**B. Message Delivery**
- [ ] Message collected from TeacherJohn's outbox during MESSAGE EXCHANGE
- [ ] Message delivered to maria's inbox: `/loops/73/.../post/inbox/new/`
- [ ] File permissions correct, maria can read it

**C. maria's Response**
- [ ] maria read the message from TeacherJohn
- [ ] maria created task to respond
- [ ] maria composed response with activity details
- [ ] Response placed in maria's outbox

**D. Response Delivery**
- [ ] Response collected from maria's outbox
- [ ] Response delivered back to TeacherJohn's inbox
- [ ] Complete round-trip communication achieved

**E. Message Exchange Runs**
- [ ] MESSAGE EXCHANGE section appears in orchestration logs
- [ ] "Processing inter-agent messages..." logged
- [ ] No errors during message exchange

---

### ✅ Should Have (Important)

**F. Content Quality**
- [ ] TeacherJohn's message is personalized (not generic)
- [ ] maria's response is specific (actual work details, not placeholder)
- [ ] Communication is professional and clear
- [ ] Blockers mentioned specifically

**G. Workflow Intelligence**
- [ ] TeacherJohn recognized this as high priority
- [ ] maria responded within 1 day
- [ ] Both agents handled delegation task appropriately

---

## Test Execution Commands

### Step 1: Clean Previous Test Data
```bash
# Clean old messages (host)
rm -f /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/70/filesystem/agentlife/post/inbox/new/test_agent_communication.json
rm -f /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/71/filesystem/agentlife/post/inbox/new/marketplace_project.json

# Clean outboxes
find /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/*/filesystem/agentlife/post/outbox/new -type f -delete 2>/dev/null || true
```

### Step 2: Verify Message Exchange is Enabled
```bash
# Check run_all_cycles.py includes message exchange (host)
grep -A 5 "MESSAGE EXCHANGE" /Users/dantweb/dantweb/l-sdk-27a/agent_post/run_all_cycles.py

# Should see:
# 📬 MESSAGE EXCHANGE (End of Day {day})
# message_service.process_messages()
```

### Step 3: Deploy Test Message
```bash
# Message already created at:
# /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/70/filesystem/agentlife/post/inbox/new/test_message_exchange.json

# Verify it exists (host)
cat /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/70/filesystem/agentlife/post/inbox/new/test_message_exchange.json
```

### Step 4: Run 3-Day Test Cycle
```bash
# Run orchestration (agent_post container)
docker exec -it agent_post python run_all_cycles.py --days 3 2>&1 | tee /tmp/message_exchange_test.log

# Monitor in separate terminal (host)
docker logs -f agent_post | grep "MESSAGE EXCHANGE\|Processing inter-agent"
```

### Step 5: Monitor File Creation
```bash
# Start file watcher (host)
./file_watch.sh 2>&1 | tee /tmp/file_watch_exchange.log &

# Watch for:
# - Message creation in /70/.../outbox/
# - Message delivery to /73/.../inbox/
# - Response creation in /73/.../outbox/
# - Response delivery to /70/.../inbox/
```

### Step 6: Verify Results After Completion

```bash
# Check TeacherJohn sent message to maria
find /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/70/filesystem/agentlife/post/outbox -name "*.json" -type f

# Check message was delivered to maria
find /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/73/filesystem/agentlife/post/inbox -name "*.json" -type f

# Check maria's response
find /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/73/filesystem/agentlife/post/outbox -name "*.json" -type f

# Check response delivered to TeacherJohn
find /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/70/filesystem/agentlife/post/inbox -name "*.json" -type f

# Read the messages
echo "=== TeacherJohn's Message to maria ==="
find /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/73/filesystem/agentlife/post/inbox -name "*.json" -exec cat {} \;

echo "=== maria's Response ==="
find /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/70/filesystem/agentlife/post/inbox -name "*.json" -exec cat {} \;
```

---

## Success Criteria Summary

**Test PASSES if:**
1. ✅ TeacherJohn created message to maria
2. ✅ MESSAGE EXCHANGE ran (visible in logs)
3. ✅ Message delivered to maria's inbox
4. ✅ maria read message and created response
5. ✅ maria's response delivered back to TeacherJohn
6. ✅ Complete round-trip communication achieved

**Test FAILS if:**
- No message created by TeacherJohn
- MESSAGE EXCHANGE not running
- Message not delivered to maria
- maria didn't respond
- Response not delivered back

---

## Troubleshooting

### Issue: MESSAGE EXCHANGE not appearing in logs
**Solution:**
- Verify run_all_cycles.py was updated
- Check imports: ExternalAPI, MessageService
- Restart containers: `make upp`

### Issue: Messages not delivered
**Solution:**
- Check agent outbox paths: `/loops/{id}/.../post/outbox/new/`
- Verify message JSON format is valid
- Check MESSAGE EXCHANGE error messages in logs

### Issue: Agents not creating messages
**Solution:**
- Verify DO_ACTION.py includes message creation capability
- Check agent understood the delegation task
- Review GET_WORK decision - did it prioritize the task?

---

## Expected Timeline

- **Day 1 (3-4 minutes):** TeacherJohn processes request, creates message
- **Message Exchange (~30 seconds):** Message delivered to maria
- **Day 2 (3-4 minutes):** maria reads, processes, responds
- **Message Exchange (~30 seconds):** Response delivered to TeacherJohn
- **Day 3 (3-4 minutes):** TeacherJohn reads response, forwards to PM

**Total Test Duration:** ~10-12 minutes

---

**Document Owner:** Implementation Team
**Status:** Ready for execution
**Prerequisites:**
- run_all_cycles.py updated with message exchange ✅
- Test message deployed ✅
- All agents configured ✅
**Estimated Testing Time:** 10-12 minutes
