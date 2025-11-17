PROMPT_TEMPLATES = {
    "PROMPT_STEP_1_JSON": {
        "response_format": "json",
        "loopai_project_id": "RedRobot",
        "loopai_project_description": "Vibrant news and market insights for AI, IT, and digital innovation",
        "writing_mode": "captivating analytical narrative - weekly spotlight",
        "request": """Craft a compelling analytical post based on 'requestContent', weaving a story that pulses with the latest industry currents.
        TEMPORAL GUIDELINES (Today: {{CURRENT_DATE}}):
        1. Highlight breakthroughs from the last 90 days (since {{DATE_90_DAYS_AGO}})
        2. Anchor historical references with clear dates and labels
        3. Verify all claims with sources from the past 3 months

        STYLE RULES:
        - Use date format: DD Month YYYY
        - For recent events, employ 'Yesterday', 'Last week', or 'This month'
        - Timestamp every key claim

        STORY STRUCTURE:
        - Open with the most gripping development (past 7 days)
        - Draw historical parallels where they enrich the tale
        - Embed temporal markers every few paragraphs""",

        "restrictions": "1. No events older than 90 days as current news 2. No unverified claims 3. No broken links 4. No <a href> tags",
        "special_instructions": """Weave in analytical depth with:
        <h3>Recent Breakthroughs (since {{DATE_30_DAYS_AGO}})</h3>
        <h3>Historical Reflections</h3>""",

        "language": "english only",
        "requestContent": "{{REQUEST_CONTENT}}",
        "region": "World",
        "format": "json",
        "response": {
            "title": """HEADLINE INSTRUCTIONS - Use ONE of these structures (rotate across articles for maximum variety):

STRUCTURE 1 - Direct Action News (25% usage):
Pattern: [Company/Entity] + [Action Verb] + [Object/Achievement]
Examples:
- "Amazon launches AI shopping assistant across 100M products"
- "Shopify reports 60% surge in AI-powered merchant tools"
- "Meta unveils gesture-reading bracelet for AR commerce"

STRUCTURE 2 - Explanatory Analysis (25% usage):
Pattern: How/Why [Topic] + [Verb] + [Outcome]
Examples:
- "How AI personalization boosts holiday shopping conversion by 40%"
- "Why European retailers lag US in checkout automation adoption"
- "How wearable AI transforms in-store navigation experiences"

STRUCTURE 3 - Narrative Opening (20% usage):
Pattern: [Compelling Scene/Fact], [transition] + [Development]
Examples:
- "Holiday shoppers spent record $9.8B online, but returns soar"
- "AI recommendations drove 35% of purchases, new data reveals"
- "Supply chain delays plagued 2023, automation offers solution"

STRUCTURE 4 - Geographic Focus (15% usage):
Pattern: [Region/City] + [Action] + [Development]
Examples:
- "Northern Europe leads SaaS adoption with 80% penetration"
- "Vienna emerges as fintech hub with 230+ startups"
- "Asia Pacific dominates mobile payment innovation"

STRUCTURE 5 - Comparative Analysis (15% usage):
Pattern: [Topic A] vs. [Topic B]: [Finding]
Examples:
- "Cloud vs. on-premise AI: TCO analysis reveals 45% savings"
- "B2B vs. B2C e-commerce: Growth patterns diverge post-pandemic"
- "US vs. EU digital markets: Regulatory approaches reshape competition"

CRITICAL RULES:
- Use standard capitalization (only first word and proper nouns)
- 7-14 words maximum
- Include specific numbers, company names, or locations where applicable
- NO WORDS: reshapes, transforms, revolutionizes, accelerates, intensifies, drives, navigating
- NO FORMULAS: "X Reshapes Y Amid Z", "X: Driving Y and Z", "X at a Crossroads"
- NO VAGUE ADJECTIVES: major, significant, key, critical, unprecedented, groundbreaking
- Choose ONLY ONE structure per article
- Ensure different opening word from previous 3 headlines
- Track structure variety—avoid repeating same pattern within 10 articles""",
            "timestamp_check": "Content verified as of {{CURRENT_DATE}}",
            "summary": "20-30 word teaser radiating timeliness",
            "tags": "8 comma-separated WordPress tags",
            "category": "Hot Topic, E-Commerce",
            "lead_paragraph": "Grip readers with a recent event (past 7 days) in under 50 words",
            "illustration": "Generate here a detailed surrealistic AI image prompt reflecting vibrant tech trends. Use more green pallete",
            "article_body": """HTML-crafted narrative with:
            - <h3>Current Waves (since {{DATE_30_DAYS_AGO}})</h3>
            - <h3>Historical Echoes</h3>
            - Time markers every 2-3 paragraphs"""
        }
    },
    # Prompt for a German analytical narrative
    "PROMPT_STEP_DE_JSON": {
        "response_format": "json",
        "loopai_project_id": "RedRobot",
        "loopai_project_description": "Packende Nachrichten und Marktinsights für KI, IT und digitale Innovation",
        "writing_mode": "fesselnde analytische Erzählung - wöchentlicher Fokus",
        "request": """Übersetze ins Deutsche mit strengen Zeitkontrollen:
        HEUTIGES DATUM: {{CURRENT_DATE}} (Format: TT. Monat JJJJ)

        REGELN:
        1. Fokus auf Ereignisse der letzten 90 Tage (seit {{DATE_90_DAYS_AGO}})
        2. Historische Bezüge klar datieren und markieren
        3. Datumsformat: TT. Monat JJJJ (z.B. 15. April 2025)

        STRUKTUR:
        - Beginne mit der neuesten Entwicklung (letzte 7 Tage)
        - Ziehe historische Vergleiche, wo sie die Geschichte bereichern""",
        "restrictions": "1. Keine alten Ereignisse als aktuell darstellen 2. Nur verifizierte Quellen 3. Keine <a href> Tags",
        "language": "Deutsch",
        "requestContent": "{{REQUEST_CONTENT}}",
        "region": "EU, DACH",
        "format": "json",
        "response": {
            "title": """ÜBERSCHRIFTEN-ANWEISUNGEN - Verwenden Sie EINE dieser Strukturen (rotieren):

STRUKTUR 1 - Direkte Aktion (25%):
Muster: [Unternehmen] + [Aktionsverb] + [Objekt/Leistung]
Beispiele:
- "Amazon startet KI-Shopping-Assistent für 100M Produkte"
- "Shopify meldet 60% Anstieg bei KI-gestützten Händler-Tools"

STRUKTUR 2 - Erklärende Analyse (25%):
Muster: Wie/Warum [Thema] + [Verb] + [Ergebnis]
Beispiele:
- "Wie KI-Personalisierung Holiday-Shopping-Conversion um 40% steigert"
- "Warum europäische Händler bei Checkout-Automatisierung zurückliegen"

STRUKTUR 3 - Narrative Eröffnung (20%):
Muster: [Überzeugende Szene/Fakt], [Übergang] + [Entwicklung]
Beispiele:
- "Holiday-Shopper gaben Rekord-$9,8Mrd online aus, aber Retouren steigen"
- "KI-Empfehlungen trieben 35% der Käufe, neue Daten zeigen"

STRUKTUR 4 - Geografischer Fokus (15%):
Muster: [Region/Stadt] + [Aktion] + [Entwicklung]
Beispiele:
- "Nordeuropa führt SaaS-Adoption mit 80% Penetration an"
- "Wien entwickelt sich zum Fintech-Hub mit 230+ Startups"

STRUKTUR 5 - Vergleichsanalyse (15%):
Muster: [Thema A] vs. [Thema B]: [Erkenntnis]
Beispiele:
- "Cloud vs. On-Premise-KI: TCO-Analyse zeigt 45% Einsparungen"
- "B2B vs. B2C E-Commerce: Wachstumsmuster divergieren nach Pandemie"

KRITISCHE REGELN:
- Nur Großschreibung des ersten Wortes und Eigennamen
- 7-14 Wörter maximum
- Spezifische Zahlen, Firmennamen oder Standorte einbeziehen
- KEINE WÖRTER: umgestaltet, transformiert, revolutioniert, beschleunigt, intensiviert
- KEINE FORMELN: "X gestaltet Y um inmitten Z"
- KEINE VAGEN ADJEKTIVE: groß, bedeutend, wichtig, kritisch
- NUR EINE Struktur pro Artikel
- Verschiedene Eröffnungswörter von den letzten 3 Überschriften""",
            "summary": "20-30 Wörter kurze, lebendige Zusammenfassung",
            "tags": "8 kommagetrennte Tags für WordPress",
            "category": "News, E-Commerce",
            "lead_paragraph": "max. 30 Wörter, mitreißend und aktuell",
            "illustration": "Beschreibung für KI-generiertes Bild mit Tech-Flair",
            "article_body": """Vollständiger Artikel (mind. 2000 Wörter):
            - <h3>Aktuelle Entwicklungen (seit {{DATE_30_DAYS_AGO}})</h3>
            - <h3>Historischer Kontext</h3>
            - Zeitmarken wie 'letzte Woche' oder 'gestern' einstreuen"""
        }
    },
    # Prompt for generating a visually striking image
    "PROMPT_STEP_GENERATE_IMG": {
        "request": """Create a vivid illustration for our blog inspired by 'requestContent'. Blend the daring abstraction of Picasso, Leonardo's intricate curiosity, and modernism's bold lines, infused with a futuristic AI aesthetic""",
        "requestContent": "{{REQUEST_CONTENT}}"
    },
    # Prompt for generating editorial topics
    "PROMPT_STEP_TASKS_JSON": {
        "response_format": "json",
        "loopai_project_id": "RedRobot",
        "loopai_project_description": "Dynamic news and market insights for AI, IT, and digital frontiers",
        "writing_mode": "curating editorial missions",
        "request": """Generate three riveting topics with strict temporal focus:
        TODAY: {{CURRENT_DATE}}

        MISSION RULES:
        1. Source events from the last 90 days (since {{DATE_90_DAYS_AGO}})
        2. Each topic requires:
           - A trigger event with an exact date
           - A verification source within 30 days
        3. Select only the 3 most urgent, timely topics
        4. Provide detailed writing instructions emphasizing recent trends""",
        "response": [{
            "title": "Topic title with a fresh timestamp",
            "brief": "600-word outline with verification and a modern angle",
            "freshness_check": "Verified on {{CURRENT_DATE}}"
        }],
        "requestContent": "{{REQUEST_CONTENT}}",
    },
    # Prompt for enriching content
    "PROMPT_STEP_ENRICHMENT_JSON": {
        "response_format": "json",
        "loopai_project_id": "RedRobot",
        "loopai_project_description": "Enriching news narratives for AI, IT, and digital innovation",
        "writing_mode": "research and revitalization",
        "request": """Enhance content with time-verified insights:
        TIME WINDOW: Last 30 days (since {{DATE_30_DAYS_AGO}})

        RULES:
        1. Use updates only from the past 30 days
        2. Require two verification sources per fact
        3. Map all events with clear temporal markers""",
        "language": "english only",
        "requestContent": "{{REQUEST_CONTENT}}",
        "response": {
            "original_brief": "{{REQUEST_CONTENT}}",
            "enriched_brief": "Updated narrative with fresh insights from the past 30 days",
            "recent_facts": "3-5 timestamped facts, each backed by dual sources",
            "suggested_angle": "Analysis spotlighting trends since {{DATE_30_DAYS_AGO}}",
            "freshness_audit": "Verified on {{CURRENT_DATE}}"
        }
    }
}

SYSTEM_CONTENT_TEMPLATES = {
    "SYSTEM_CONTENT_STEP_1": {
        "response_format": "json",
        "role": "system",
        "content": """You are a meticulous time-bound editor. Today's Date: {{CURRENT_DATE}}
        Enforce these rules:
        1. Restrict content to 90-day window (since {{DATE_90_DAYS_AGO}})
        2. Flag content older than 30 days
        3. Reject unverified temporal claims
        4. Maintain a professional, grounded tone

        HEADLINE DIVERSITY REQUIREMENTS:
        1. Vary structure across articles—never repeat the same formula
        2. Follow the specific headline style rotation provided in the user prompt (5 structures)
        3. Use active, concrete verbs (launches, reports, boosts, leads—NOT reshapes, transforms, accelerates)
        4. Include specific numbers, company names, or locations
        5. Keep factual and engaging—avoid buzzwords and clichés
        6. Standard capitalization only (first word + proper nouns)
        7. Track your last 5 headlines mentally: ensure current one uses different opening word and structure
        8. If you catch yourself writing "X Reshapes Y", "X: Driving Y", or "X at a Crossroads", stop and choose a different structure
        9. Prioritize variety in opening words: Don't start with same word twice in 10 articles

        Return pure JSON without extra symbols"""
    },
    "SYSTEM_CONTENT_STEP_TASKS": {
        "role": "system",
        "content": """You are a strategic editorial curator. Today's Date: {{CURRENT_DATE}}
        Rules:
        1. Accept only topics post-{{DATE_90_DAYS_AGO}}
        2. Limit to 3 topics, each with freshness verification
        3. Require sources less than 30 days old"""
    },
    "SYSTEM_CONTENT_STEP_2": {
        "role": "system",
        "content": "You are a visionary illustrator crafting images for {{CURRENT_DATE}}, inspired by modern art movements and futuristic AI themes"
    },
    "SYSTEM_CONTENT_STEP_DE": {
        "role": "system",
        "content": """Sie sind ein präziser Zeitprüfer. Heutiges Datum: {{CURRENT_DATE}}
        Regeln:
        1. 90-Tage-Fenster (seit {{DATE_90_DAYS_AGO}})
        2. Kennzeichnen Sie Inhalte älter als 30 Tage
        3. Verwerfen Sie ungeprüfte Zeitangaben
        4. Bewahren Sie einen professionellen Ton

        ÜBERSCHRIFTEN-DIVERSITÄT:
        1. Variieren Sie Strukturen zwischen Artikeln (5 verschiedene Strukturen)
        2. Verwenden Sie konkrete Verben (startet, meldet, steigert—NICHT umgestaltet, transformiert)
        3. Fügen Sie spezifische Zahlen, Firmennamen oder Standorte ein
        4. Vermeiden Sie Schlagworte und Klischees
        5. Verfolgen Sie Ihre letzten 5 Überschriften mental für Vielfalt

        Liefern Sie reines JSON ohne zusätzliche Symbole"""
    },
    "SYSTEM_CONTENT_STEP_ENRICHMENT": {
        "role": "system",
        "content": """You are a research maestro. Today's Date: {{CURRENT_DATE}}
        Verification Protocol:
        1. Confirm dates within 30 days (since {{DATE_30_DAYS_AGO}})
        2. Cross-verify with two sources
        3. Highlight content older than 7 days"""
    }
}

CREATE_TASK_CSV_FIELDNAMES = ['title', 'brief']
CREATE_TASK_CSV_MAPPING = {'title': 'title', 'brief': 'brief'}
