# AI Model Configuration Fix Guide
**Created:** 2025-11-16
**Issue:** External API 404 error blocking agent AI responses
**Status:** CRITICAL - Affects ALL 5 Living Agents

---

## Problem Summary

**Error Message:**
```
openai.NotFoundError: Error code: 404 -
{'error': {'message': 'The model `deepseek-chat` does not exist.',
'type': 'invalid_request_error', 'param': None, 'code': 'model_not_found'}}
```

**Impact:**
- ALL 5 agents (Loops 70-74) unable to generate AI responses
- Orchestration cycles complete architecturally but produce no intelligent output
- Living Agent decision-making completely blocked

**Root Cause:**
- Model name `deepseek-chat` not found at configured API endpoints
- Incorrect API endpoint configuration for DeepSeek API
- Possible service unavailability or API changes

---

## Current Configuration Analysis

### .env Configuration by Agent

| Loop ID | Agent Name | API URL | API Key | Status |
|---------|------------|---------|---------|--------|
| **70** | TeacherJohn | `https://api.deepseek.com` | `sk-90cb...de81` | FAILING |
| **71** | cityhall | `https://api.deepseek.com` | `sk-e374...40b5` | FAILING |
| **72** | padre | `https://api.deepseek.com` | `sk-b3fc...59e8` | FAILING |
| **73** | maria | `https://api.deepseek.com` | `sk-6242...732c` | FAILING |
| **74** | zhou | `https://api.featherless.ai/v1` | `rc_3b78...72e` | UNKNOWN |

**Key Finding:**
- Loops 70-73: Using `api.deepseek.com` endpoint (4 agents FAILING)
- Loop 74: Using `api.featherless.ai/v1` endpoint (status unknown, different config)

### Model Configuration in YAML Files

All action YAML files specify: `model: deepseek-chat`

**Affected Files per Agent:**
- `DO_ACTION.yaml` → model: deepseek-chat
- `GET_WORK.yaml` → model: deepseek-chat
- `PREPARE_ACTION.yaml` → model: deepseek-chat
- `READ_POSTS.yaml` → model: deepseek-chat
- `REFLEX.yaml` → model: deepseek-chat
- `VALIDATE_ACTION.yaml` → model: deepseek-chat
- `VALIDATE_WORK.yaml` → model: deepseek-chat

**Total Files to Update:** 7 YAML files × 5 agents = 35 files

---

## Fix Options

### Option 1: Use Featherless.ai (Recommended - Quick Fix)

**Advantages:**
- Already configured in Loop 74
- API keys already available (commented out in loops 70-73)
- Featherless.ai provides DeepSeek models via proxy

**Steps:**

1. **Update .env files for Loops 70-73**

```bash
# Loop 70
sed -i.bak 's|^FEATHERLESS_API_KEY=sk-|#FEATHERLESS_API_KEY=sk-|' /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/70/config/.env
sed -i.bak 's|^FEATHERLESS_API_URL=https://api.deepseek.com|#FEATHERLESS_API_URL=https://api.deepseek.com|' /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/70/config/.env
sed -i.bak 's|^#FEATHERLESS_API_KEY=rc_|FEATHERLESS_API_KEY=rc_|' /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/70/config/.env
sed -i.bak 's|^#FEATHERLESS_API_URL=https://api.featherless.ai|FEATHERLESS_API_URL=https://api.featherless.ai|' /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/70/config/.env

# Loop 71
sed -i.bak 's|^FEATHERLESS_API_KEY=sk-|#FEATHERLESS_API_KEY=sk-|' /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/71/config/.env
sed -i.bak 's|^FEATHERLESS_API_URL=https://api.deepseek.com|#FEATHERLESS_API_URL=https://api.deepseek.com|' /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/71/config/.env
sed -i.bak 's|^#FEATHERLESS_API_KEY=rc_|FEATHERLESS_API_KEY=rc_|' /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/71/config/.env
sed -i.bak 's|^#FEATHERLESS_API_URL=https://api.featherless.ai|FEATHERLESS_API_URL=https://api.featherless.ai|' /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/71/config/.env

# Loop 72
sed -i.bak 's|^FEATHERLESS_API_KEY=sk-|#FEATHERLESS_API_KEY=sk-|' /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/72/config/.env
sed -i.bak 's|^FEATHERLESS_API_URL=https://api.deepseek.com|#FEATHERLESS_API_URL=https://api.deepseek.com|' /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/72/config/.env
sed -i.bak 's|^#FEATHERLESS_API_KEY=rc_|FEATHERLESS_API_KEY=rc_|' /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/72/config/.env
sed -i.bak 's|^#FEATHERLESS_API_URL=https://api.featherless.ai|FEATHERLESS_API_URL=https://api.featherless.ai|' /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/72/config/.env

# Loop 73
sed -i.bak 's|^FEATHERLESS_API_KEY=sk-|#FEATHERLESS_API_KEY=sk-|' /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/73/config/.env
sed -i.bak 's|^FEATHERLESS_API_URL=https://api.deepseek.com|#FEATHERLESS_API_URL=https://api.deepseek.com|' /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/73/config/.env
sed -i.bak 's|^#FEATHERLESS_API_KEY=rc_|FEATHERLESS_API_KEY=rc_|' /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/73/config/.env
sed -i.bak 's|^#FEATHERLESS_API_URL=https://api.featherless.ai|FEATHERLESS_API_URL=https://api.featherless.ai|' /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/73/config/.env
```

2. **Update model name if needed**

Check what models Featherless.ai supports for `deepseek-chat`. If the model name needs changing:

```bash
# Check available models at Featherless.ai
curl https://api.featherless.ai/v1/models -H "Authorization: Bearer rc_a250b328f44aff98d14d875fa030a122b3ffc84424b86511e30132c554abce85"

# If model name needs changing (e.g., to "deepseek/deepseek-chat"), update all YAML files:
for loop_id in 70 71 72 73 74; do
  for yaml_file in /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/$loop_id/config/*.yaml; do
    sed -i.bak 's|model: deepseek-chat|model: deepseek/deepseek-chat|g' "$yaml_file"
  done
done
```

3. **Restart containers**

```bash
make upp
```

4. **Test single agent**

```bash
# Test Loop 70 GET_WORK action
curl http://localhost:5050/api/public/agent/8/action/GET_WORK/
```

**Estimated Time:** 5-10 minutes

---

### Option 2: Fix DeepSeek API Configuration

**Advantages:**
- Direct connection to DeepSeek (if preferred)
- May have better performance

**Challenges:**
- Need to verify correct DeepSeek API endpoint
- May require new API keys
- Current endpoint `https://api.deepseek.com` returning 404

**Steps:**

1. **Verify DeepSeek API endpoint**

Research DeepSeek's official API documentation to find:
- Correct API base URL
- Correct model name format
- Authentication requirements

2. **Update .env files**

```bash
# Update with correct DeepSeek endpoint (example)
for loop_id in 70 71 72 73; do
  cat > /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/$loop_id/config/.env <<EOF
FEATHERLESS_API_KEY=<your_deepseek_api_key>
FEATHERLESS_API_URL=<correct_deepseek_endpoint>
EOF
done
```

3. **Update model names in YAML files**

4. **Test and validate**

**Estimated Time:** 30-60 minutes (including research)

---

### Option 3: Switch to OpenAI or Anthropic (Most Reliable)

**Advantages:**
- Well-documented, stable APIs
- High reliability
- Better model capabilities (GPT-4, Claude)

**Disadvantages:**
- Requires new API keys
- May have higher costs
- Larger changes to configuration

**Steps:**

1. **For OpenAI:**

```bash
# Update .env files
for loop_id in 70 71 72 73 74; do
  cat > /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/$loop_id/config/.env <<EOF
OPENAI_API_KEY=<your_openai_key>
OPENAI_API_URL=https://api.openai.com/v1
EOF
done

# Update model in YAML files
for loop_id in 70 71 72 73 74; do
  for yaml_file in /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/$loop_id/config/*.yaml; do
    sed -i.bak 's|model: deepseek-chat|model: gpt-4o-mini|g' "$yaml_file"
  done
done
```

2. **For Anthropic Claude:**

```bash
# Update .env files
for loop_id in 70 71 72 73 74; do
  cat > /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/$loop_id/config/.env <<EOF
ANTHROPIC_API_KEY=<your_anthropic_key>
ANTHROPIC_API_URL=https://api.anthropic.com/v1
EOF
done

# Update model in YAML files
for loop_id in 70 71 72 73 74; do
  for yaml_file in /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/$loop_id/config/*.yaml; do
    sed -i.bak 's|model: deepseek-chat|model: claude-3-5-sonnet-20241022|g' "$yaml_file"
  done
done
```

**Estimated Time:** 15-20 minutes

---

## Recommended Action Plan

### Immediate Fix (Option 1 - Featherless.ai)

**Why:**
- Fastest solution (API keys already available)
- Loop 74 already configured this way
- Minimal changes required

**Steps:**
1. Switch loops 70-73 to Featherless.ai configuration
2. Verify model name compatibility
3. Restart containers
4. Run single-agent test
5. Run full orchestration cycle

**Expected Result:**
- All 5 agents operational within 10 minutes
- Living Agent decision-making restored
- Test scenarios can proceed

---

## Verification Commands

### After applying fix:

```bash
# 1. Verify .env configuration
for loop_id in 70 71 72 73 74; do
  echo "=== Loop $loop_id ==="
  grep "FEATHERLESS_API" /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/$loop_id/config/.env | grep -v "^#"
done

# 2. Verify model names in YAML
for loop_id in 70 71 72 73 74; do
  echo "=== Loop $loop_id ==="
  grep "model:" /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/$loop_id/config/GET_WORK.yaml
done

# 3. Test single agent action
curl http://localhost:5050/api/public/agent/8/action/GET_WORK/

# 4. Check for errors in logs
docker logs loopai_web 2>&1 | grep -A 5 "404\|NotFoundError\|model.*not.*exist"

# 5. Run 1-day test cycle
docker exec agent_post python run_all_cycles.py --days 1

# 6. Verify agent responses
find /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/70/filesystem/agentlife/current_work -name "*.json" -exec cat {} \;
```

---

## Success Criteria

Fix is considered SUCCESSFUL when:

1. No 404 errors in Docker logs
2. Agent actions complete with AI-generated content
3. Current work files contain intelligent responses (not empty)
4. GET_WORK protocol returns task selection with reasoning
5. Full orchestration cycle completes with meaningful output

---

## Rollback Plan

If fix causes issues:

```bash
# Restore original configuration from backups
for loop_id in 70 71 72 73; do
  cp /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/$loop_id/config/.env.bak \
     /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/$loop_id/config/.env
done

# Restore YAML files
for loop_id in 70 71 72 73 74; do
  for yaml_file in /Users/dantweb/dantweb/l-sdk-27a/loopai_src/var/users/1/loops/$loop_id/config/*.yaml.bak; do
    mv "$yaml_file" "${yaml_file%.bak}"
  done
done

# Restart containers
make upp
```

---

## Files Reference

### Configuration Files by Loop

**Loop 70 (TeacherJohn):**
- .env: `/loopai_src/var/users/1/loops/70/config/.env`
- YAMLs: `/loopai_src/var/users/1/loops/70/config/*.yaml`

**Loop 71 (cityhall):**
- .env: `/loopai_src/var/users/1/loops/71/config/.env`
- YAMLs: `/loopai_src/var/users/1/loops/71/config/*.yaml`

**Loop 72 (padre):**
- .env: `/loopai_src/var/users/1/loops/72/config/.env`
- YAMLs: `/loopai_src/var/users/1/loops/72/config/*.yaml`

**Loop 73 (maria):**
- .env: `/loopai_src/var/users/1/loops/73/config/.env`
- YAMLs: `/loopai_src/var/users/1/loops/73/config/*.yaml`

**Loop 74 (zhou):**
- .env: `/loopai_src/var/users/1/loops/74/config/.env`
- YAMLs: `/loopai_src/var/users/1/loops/74/config/*.yaml`

---

## Next Steps After Fix

1. Re-run Sprint 1 & 2 test scenarios:
   - Scenario 1: Inter-agent communication
   - Scenario 2: Multi-agent 7-day collaboration
   - Scenario 3: Message exchange round-trip

2. Validate Living Agent intelligence:
   - Check decision-making quality
   - Verify context awareness
   - Confirm task prioritization

3. Update completion report with actual AI responses

4. Proceed to Sprint 3 & 4

---

**Document Owner:** Implementation Team
**Status:** Ready for execution
**Priority:** CRITICAL
**Estimated Fix Time:** 5-10 minutes (Option 1)
**Last Updated:** 2025-11-16

---

## Support Resources

- Featherless.ai Documentation: https://docs.featherless.ai/
- DeepSeek API Documentation: https://platform.deepseek.com/
- OpenAI API Documentation: https://platform.openai.com/docs/
- Anthropic API Documentation: https://docs.anthropic.com/

**Note:** All sed commands create `.bak` backup files before making changes, allowing safe rollback if needed.
