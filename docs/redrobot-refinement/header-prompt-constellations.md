# RedRobot Header Prompt Constellations

This document provides diverse prompt patterns to generate varied, distinctive headlines across different content types.

## Problem Statement

Current issue: All generated titles follow similar patterns ("X Reshapes Y Amid Z", "X: Driving Y and Z"), making content appear formulaic and repetitive.

Solution: Use specific structural patterns and constraints for each content type to create natural variation.

---

## 1. NEWS-STYLE HEADERS (Reuters/Bloomberg Format)

### Variant A: Direct Action News
**Pattern:** `[Company/Entity] + [Action Verb] + [Object/Amount]`

**Prompt Instructions:**
```
Create a news headline using this structure:
- Start with the primary actor (company, organization, person)
- Use a strong action verb (announces, launches, reports, raises, cuts, expands)
- Include specific numbers or details where applicable
- Keep to 6-10 words maximum
- Use standard capitalization (only first word and proper nouns)

Examples:
- "Amae Health raises $25 million for AI mental health platform"
- "Ledger unveils Nano Gen5 hardware wallet for institutions"
- "FDA approves new pathway for personalized gene therapies"
- "Bitcoin drops below $100K as ETF outflows hit $800M"
```

### Variant B: Impact-First News
**Pattern:** `[Effect/Outcome] + as/after + [Cause/Event]`

**Prompt Instructions:**
```
Lead with the consequence or market impact, then explain the trigger:
- Begin with what happened (price move, market shift, adoption surge)
- Use "as" or "after" to connect to the cause
- Keep factual and specific
- 8-12 words maximum

Examples:
- "Crypto markets tumble as Fed signals slower rate cuts"
- "Vienna emerges as crypto hub after MiCA regulations"
- "Healthcare costs drop 40% following AI diagnostic rollout"
- "DeFi protocols see record inflows after Ethereum upgrade"
```

### Variant C: Event Reporting
**Pattern:** `[Event/Development] + [Context/Location/Timeframe]`

**Prompt Instructions:**
```
Report the event with essential context:
- State what occurred
- Add when, where, or scope
- Avoid adjectives like "major" or "significant"
- 7-11 words maximum

Examples:
- "DeepSeek launches AI trading model in Asian markets"
- "European startups secure $200M in Series A rounds"
- "Cross-chain bridge hacks decline 60% in Q4 2024"
- "Telemedicine adoption reaches 80% across OECD nations"
```

---

## 2. ANALYTICAL HEADERS (In-Depth, Thesis-Driven)

### Variant A: Explanatory Analysis
**Pattern:** `How/Why [Topic] + [Verb] + [Outcome/Implication]`

**Prompt Instructions:**
```
Frame as an explanatory investigation:
- Start with "How" or "Why"
- Focus on mechanisms or causation
- Avoid buzzwords like "reshapes" or "transforms"
- 8-13 words maximum

Examples:
- "How liquid staking derivatives unlock yield in proof-of-stake"
- "Why institutional Bitcoin accumulation signals market maturity"
- "How FinOps practices cut enterprise cloud costs by 30%"
- "Why MCP protocol adoption accelerates AI integration in healthcare"
```

### Variant B: Thesis Statement
**Pattern:** `[Subject]: [Claim/Observation]`

**Prompt Instructions:**
```
Make a clear analytical claim with a colon:
- Subject before colon (max 4 words)
- Claim after colon (specific, provable)
- Avoid vague terms like "changes," "shifts"
- 8-12 words total

Examples:
- "Zero-knowledge rollups: Scaling solution or regulatory risk?"
- "Wearable AI: Privacy concerns outpace innovation in Europe"
- "GPU cloud computing: Enterprise ROI exceeds 200% in 18 months"
- "Tokenized assets: Institutional adoption reaches $4B TVL"
```

### Variant C: Comparative Analysis
**Pattern:** `[Topic A] vs. [Topic B]: [Finding/Insight]`

**Prompt Instructions:**
```
Compare two approaches, regions, or technologies:
- Clearly state what's being compared
- Present a non-obvious finding
- Use data or specific outcomes
- 9-14 words maximum

Examples:
- "US vs. EU crypto regulation: Divergent paths shape market structure"
- "On-premise vs. cloud AI: TCO analysis reveals hidden costs"
- "Proof-of-work vs. proof-of-stake: Energy metrics show 99% reduction"
- "Northern vs. Southern Europe: SaaS funding patterns diverge"
```

### Variant D: Causal Investigation
**Pattern:** `[Recent Event/Data] + signals/reveals/shows + [Deeper Trend]`

**Prompt Instructions:**
```
Use surface indicators to expose underlying trends:
- Start with observable, recent development
- Connect to broader implication
- Be specific about the mechanism
- 10-15 words maximum

Examples:
- "ETF flow reversals reveal institutional de-risking in volatile crypto markets"
- "Vienna startup density signals shift in European fintech geography"
- "Hardware wallet pre-orders indicate institutional custody demand surge"
- "AI water usage data exposes data center sustainability crisis"
```

---

## 3. FEATURE/STORY HEADERS (Engaging, Human-Interest)

### Variant A: Narrative Opening
**Pattern:** `[Compelling Scene/Fact], [and now/but/yet] + [Development]`

**Prompt Instructions:**
```
Create a mini-story arc in the headline:
- Open with a hook or surprising fact
- Use comma or colon for pacing
- Connect to current development
- 10-16 words maximum

Examples:
- "AI models used 45mL of water per query, sparking efficiency debate"
- "Satellite collisions threatened space industry, until AI arrived"
- "Gene therapy cost $2M per patient—FDA's new path could change that"
- "Cross-chain bridges lost $2B in 2023, but security's improving"
```

### Variant B: The Stakes Format
**Pattern:** `What [Development] means for [Stakeholder/Industry]`

**Prompt Instructions:**
```
Frame around impact on specific audience:
- Use "What [X] means for [Y]" structure
- Be specific about the stakeholder
- Imply practical consequences
- 7-12 words maximum

Examples:
- "What Trump's Zhao pardon means for crypto exchange compliance"
- "What MCP framework means for healthcare AI deployment"
- "What FinOps adoption means for enterprise cloud strategy"
- "What MiCA regulations mean for European crypto startups"
```

### Variant C: Emerging Pattern
**Pattern:** `[Number/Trend] + [Development] + [Signal/Indicator]`

**Prompt Instructions:**
```
Highlight a trend just becoming visible:
- Start with quantifiable observation
- Name the pattern
- Suggest what it indicates
- 9-13 words maximum

Examples:
- "Three AI breakthroughs in September point to AGI timeline shift"
- "Five European cities emerge as unexpected blockchain innovation hubs"
- "Crypto ETF flows turn negative for first time since launch"
- "Enterprise GPU adoption doubles quarterly, signaling infrastructure shift"
```

---

## 4. TECHNICAL/DATA-DRIVEN HEADERS (Precise, Metrics-Focused)

### Variant A: By-The-Numbers
**Pattern:** `[Specific Metric/Data Point] + [Context/Implication]`

**Prompt Instructions:**
```
Lead with hard data:
- Open with precise number or percentage
- Provide just enough context
- Avoid interpretive language
- 7-11 words maximum

Examples:
- "Bitcoin ETF outflows reach $800M in single week"
- "Ethereum gas fees drop 85% post-Dencun upgrade"
- "Healthcare AI reduces hospital readmissions by 34%"
- "Enterprise cloud waste averages 30% of annual spend"
```

### Variant B: Technical Milestone
**Pattern:** `[Technology/Protocol] + achieves/reaches + [Specific Achievement]`

**Prompt Instructions:**
```
Report technical accomplishments:
- Name the specific technology
- Use precise achievement metrics
- Avoid hyperbole
- 8-12 words maximum

Examples:
- "zkSync achieves 2,000 TPS on mainnet in stress test"
- "Llama 3 reaches GPT-4 parity on coding benchmarks"
- "Ledger Flex integrates direct DeFi protocol interaction"
- "MCP protocol connects 15 major EHR systems"
```

---

## 5. INVESTMENT/STRATEGY HEADERS

### Variant A: Opportunity Framing
**Pattern:** `Why [Asset/Strategy] + [Action Verb] + [Investment Case]`

**Prompt Instructions:**
```
Position as investment thesis:
- Start with "Why" + specific asset
- Use verbs like "offers," "presents," "provides"
- Include the core thesis
- 8-13 words maximum

Examples:
- "Why liquid staking derivatives offer yield in proof-of-stake era"
- "Why cross-chain bridges present asymmetric risk-reward profiles"
- "Why GPU cloud investments outperform traditional infrastructure plays"
- "Why tokenized treasuries attract institutional capital in 2025"
```

### Variant B: Risk/Reward Balance
**Pattern:** `[Investment/Technology]: [Opportunity] + amid/despite + [Challenge]`

**Prompt Instructions:**
```
Present balanced view:
- Name the investment/topic
- State the upside
- Acknowledge the risk
- 9-14 words maximum

Examples:
- "ZK rollups: Scaling solution with strong tailwinds amid security concerns"
- "Crypto ETFs: Institutional access despite continued regulatory uncertainty"
- "AI agents: Efficiency gains tempered by hallucination risks"
- "DeFi protocols: High yields persist amid evolving regulatory landscape"
```

---

## 6. REGIONAL/COMPARATIVE HEADERS

### Variant A: Geographic Focus
**Pattern:** `[Region/City] + [Action] + [Development/Position]`

**Prompt Instructions:**
```
Emphasize geographic angle:
- Lead with location
- Use active verbs (emerges, leads, adopts)
- Specify the domain
- 7-11 words maximum

Examples:
- "Vienna positions as Europe's crypto regulatory sandbox"
- "Northern Europe dominates SaaS Series A funding rounds"
- "Asia Pacific leads global wearable AI adoption metrics"
- "Silicon Valley loses AI talent to European research hubs"
```

### Variant B: Cross-Regional Analysis
**Pattern:** `[Region A] + [approaches] + while/as + [Region B] + [contrasting approach]`

**Prompt Instructions:**
```
Highlight regulatory or strategic divergence:
- Clearly state both regions
- Show the contrast
- Be specific about approaches
- 11-16 words maximum

Examples:
- "US prioritizes innovation speed while EU focuses compliance in AI race"
- "China scales AI infrastructure as Europe emphasizes energy efficiency"
- "North America embraces FinOps while Asia Pacific maintains centralized IT"
- "UK rushes crypto licensing while EU implements MiCA gradually"
```

---

## 7. ANTI-PATTERNS TO AVOID

### Overused Verbs and Formulas
❌ AVOID:
- "reshapes," "transforms," "revolutionizes"
- "X Reshapes Y Amid Z"
- "X: Driving Y and Z"
- "The Rise of X"
- "X at a Crossroads"
- "Navigating X"
- "Accelerating," "Intensifying" as lead words

### Vague Modifiers
❌ AVOID:
- "major," "significant," "important"
- "key," "critical," "crucial"
- "innovative," "groundbreaking"
- "unprecedented"

### Question Headlines (Use Sparingly)
❌ AVOID generic questions:
- "Is X the Future of Y?"
- "Will X Change Y Forever?"

✅ USE specific analytical questions:
- "Can zero-knowledge rollups scale to 10,000 TPS?"
- "Do institutional flows predict crypto market bottoms?"

---

## 8. IMPLEMENTATION GUIDE

### For News Content (Crypto, General Tech News)
Use these variations in rotation:
- 40% Direct Action News (Variant A)
- 30% Impact-First News (Variant B)
- 20% Event Reporting (Variant C)
- 10% By-The-Numbers (Technical)

### For Analytical Content (Industry Insight, Deep Dives)
Use these variations in rotation:
- 30% Explanatory Analysis (Variant A)
- 25% Causal Investigation (Variant D)
- 20% Comparative Analysis (Variant C)
- 15% Thesis Statement (Variant B)
- 10% Feature/Story Headers

### For Investment Ideas
Use exclusively:
- 50% Opportunity Framing
- 50% Risk/Reward Balance

### For Regional/European Content
Use these variations:
- 50% Geographic Focus
- 30% Cross-Regional Analysis
- 20% Comparative Analysis (from Analytical section)

---

## 9. PROMPT IMPLEMENTATION EXAMPLES

### Example 1: News Article Prompt Enhancement

**BEFORE:**
```json
"response": {
    "title": "title should be a hot news headline"
}
```

**AFTER:**
```json
"response": {
    "title": "Use ONE of these headline structures (rotate them across articles):\n
    STYLE 1 - Direct Action: [Company] + [Action Verb] + [Object/Amount]. Example: 'Amae Health raises $25M for AI mental health platform'\n
    STYLE 2 - Impact-First: [Effect] + as/after + [Cause]. Example: 'Bitcoin falls below $100K as ETF outflows hit $800M'\n
    STYLE 3 - Event Reporting: [Event] + [Context]. Example: 'DeepSeek launches AI trading model in Asian markets'\n
    \n
    CRITICAL RULES:\n
    - Use standard capitalization (only first word and proper nouns)\n
    - 6-12 words maximum\n
    - NO words: reshapes, transforms, revolutionizes, accelerates, intensifies\n
    - NO formulas: 'X Reshapes Y Amid Z' or 'X: Driving Y and Z'\n
    - Include specific numbers or names\n
    - Choose ONLY ONE style per article"
}
```

### Example 2: Analytical Article Prompt Enhancement

**BEFORE:**
```json
"response": {
    "title": "Constructive headline about industry movements"
}
```

**AFTER:**
```json
"response": {
    "title": "Use ONE of these analytical headline structures (rotate across articles):\n
    STYLE 1 - Explanatory: How/Why [Topic] + [Verb] + [Outcome]. Example: 'How liquid staking derivatives unlock yield in proof-of-stake'\n
    STYLE 2 - Thesis: [Subject]: [Specific Claim]. Example: 'GPU cloud computing: Enterprise ROI exceeds 200% in 18 months'\n
    STYLE 3 - Causal: [Data/Event] + signals/reveals + [Trend]. Example: 'ETF flow reversals reveal institutional de-risking in volatile markets'\n
    STYLE 4 - Comparative: [A] vs. [B]: [Finding]. Example: 'US vs. EU crypto regulation: Divergent paths shape market structure'\n
    \n
    CRITICAL RULES:\n
    - 8-15 words maximum\n
    - NO buzzwords: reshapes, transforms, revolutionizes, drives, accelerates\n
    - NO vague adjectives: major, significant, key, critical\n
    - NO formulas: 'X Reshapes Y', 'X: Driving Y'\n
    - Must make a specific, verifiable claim\n
    - Choose ONLY ONE style per article"
}
```

### Example 3: System Content Enhancement

**BEFORE:**
```json
"SYSTEM_CONTENT_STEP_1": {
    "role": "system",
    "content": "You are a chef editor at a blog about finances and hi-tech at Reuters."
}
```

**AFTER:**
```json
"SYSTEM_CONTENT_STEP_1": {
    "role": "system",
    "content": "You are a chief editor at Reuters. When writing headlines:\n
    1. Vary your structure across articles—never repeat the same formula\n
    2. Follow the specific headline style provided in the user prompt\n
    3. Use active, specific verbs (announces, raises, reports, launches—NOT reshapes, drives, transforms)\n
    4. Include concrete numbers and proper nouns\n
    5. Keep factual and direct—avoid interpretive language\n
    6. Standard capitalization only (first word + proper nouns)\n
    7. If you catch yourself writing 'X Reshapes Y' or 'X: Driving Y', stop and rewrite with a different structure"
}
```

---

## 10. TESTING & QUALITY CONTROL

### Diversity Check
Every 10 headlines should include:
- At least 6 different opening words
- At least 4 different structural patterns
- No more than 2 headlines with colons
- No more than 2 headlines starting with "How" or "Why"
- Zero instances of: reshapes, transforms, revolutionizes, drives

### Specificity Check
Every headline must include at least ONE of:
- Specific number or percentage
- Company or product name
- Geographic location
- Technical term or protocol name
- Timeframe (month, quarter, year)

### Verb Diversity
Rotate through these verbs (never use the same verb twice in 10 headlines):
- announces, launches, reports, raises, cuts, expands (news)
- reveals, shows, signals, indicates, suggests (analysis)
- reaches, achieves, hits, exceeds, crosses (milestones)
- emerges, positions, leads, dominates (regional)
- offers, presents, provides (investment)

---

## 11. QUICK REFERENCE CHECKLIST

Before approving any headline, verify:
- [ ] Does NOT use: reshapes, transforms, revolutionizes, drives, accelerates
- [ ] Does NOT follow formula: "X Reshapes Y Amid Z" or "X: Driving Y"
- [ ] Uses standard capitalization (not title case)
- [ ] Includes specific detail (number, name, location, or timeframe)
- [ ] Follows ONE of the defined structural patterns
- [ ] Different structure from previous 3 headlines
- [ ] Under 16 words
- [ ] Would pass the "Reuters desk editor" test

---

## 12. MONTHLY REVIEW PROTOCOL

Track headline performance:
1. Export all headlines from past month
2. Count repeated structural patterns
3. Identify overused verbs (flag if used >3 times)
4. Check for forbidden formulas ("reshapes," "transforms")
5. Update prompt weights to emphasize underused patterns

---

## APPENDIX: FULL VERB LIBRARY

### News Verbs (Direct Action)
announces, launches, reports, raises, secures, unveils, releases, expands, cuts, adds, opens, closes, acquires, sells, merges, partners, appoints, elects, approves, rejects, delays, accelerates, halts, resumes

### Analysis Verbs (Investigation/Insight)
reveals, shows, signals, indicates, suggests, exposes, highlights, demonstrates, confirms, contradicts, challenges, supports, undermines

### Achievement Verbs (Milestones)
reaches, achieves, hits, exceeds, crosses, breaks, sets, attains, surpasses, meets, misses, approaches

### Position Verbs (Status/Ranking)
leads, dominates, emerges, positions, ranks, trails, overtakes, threatens, challenges, defends

### Investment Verbs (Opportunity)
offers, presents, provides, yields, delivers, promises, risks, threatens, enables, unlocks

### Comparison Verbs
outperforms, underperforms, matches, mirrors, diverges, converges, contrasts, compares, differs

---

## NOTES ON USAGE

This document should be referenced when:
1. Creating or updating prompt templates
2. Reviewing LLM-generated content for quality
3. Training new content editors
4. Troubleshooting repetitive headline patterns
5. A/B testing different headline approaches

Update this document quarterly based on:
- User engagement metrics
- Editorial feedback
- Emerging industry terminology
- New content categories

---

**Document Version:** 1.0
**Last Updated:** 2025-11-17
**Next Review:** 2026-02-17
