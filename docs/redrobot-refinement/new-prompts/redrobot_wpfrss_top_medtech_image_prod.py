PROMPT_TEMPLATES = {
    # prompt for the first step defined in the loop yaml
    "PROMPT_STEP_1_JSON": {
        "response_type": "json",
        "loopai_project_id": "RedRobot",
        "looai_project_descitption": "News and market review for AI, IT and digital industry",
        "looai_writing_mode": "analytical story - summary of the week",
        "request": """Write an anyltical post on the topic, described in the field 'requestContent' in this json. Use real facts. Use quotations of other experts.
        When you write that someone anounced something, point exacly who and where.
        Consider current date from the input. Keep the article news actual.
        Refer to where the information comes from: pres-release, or announcement, or some other news source writes about, or blog says...
        Check links and do not put failed urls to hrefs in the text if you cant receive response 200.

        Consider current date from the input. Keep the article news actual.
        Keep filed names strictly as in 'response' - those fields are required. Do not create unfinished json.
        Your response should be a valid JSON.
        Strict ANSI symbols, respect json rules.""",

        "restrictions": "",
        "special_instructions": """For each news article provided, add the last two paragraphs that offer analytical and fact-based background context related to the current event or trend,
        Instructions: If the article describes a current event (e.g., "Apple reports record profit in 2024"): The final two paragraphs should reference related events or data from the past
        (e.g., previous years' profits, similar events involving Apple or competitors). Include relevant comparisons or historical data that give readers a deeper understanding of the current development.
        If the article describes an ongoing trend (e.g., "AI revolutionizes the Asian market"): The last two paragraphs should highlight precedents—other
        technologies or innovations that have had a similar transformative effect on the region or sector. Provide fact-based observations that position the current trend in a broader
        historical or technological context. Goals: Add depth and editorial value to the article. Offer readers a temporal perspective, connecting current developments with relevant past events
        or patterns. Maintain a factual and analytical tone, not speculative or opinionated. Examples: Event article: "Bitcoin hits new all-time high." Add context like: "In 2021, Bitcoin also
        saw a dramatic increase following institutional investments. Similarly, in 2017, a speculative boom pushed prices to historic highs, though it was followed by a sharp correction."
        Trend article: "AI revolutionizes Asia's e-commerce landscape." Add context like: "A similar digital transformation occurred in 2010s when mobile payment systems like Alipay and WeChat Pay
        reshaped consumer behavior in China. These innovations laid the foundation for today's AI-driven personalization and logistics. """,

        "language": "english",
        "requestContent": "{{REQUEST_CONTENT}}",
        "region": "USA",
        "format": "json",
        "response": {
            "title": """HEADLINE INSTRUCTIONS - Use ONE of these structures (rotate across articles for analytical medtech content):

STRUCTURE 1 - Explanatory Analysis (25% usage):
Pattern: How/Why [Medical Topic] + [Verb] + [Outcome/Impact]
Examples:
- "How AI diagnostics reduce hospital readmissions by 34%"
- "Why MCP protocol adoption accelerates healthcare AI integration"
- "How wearable AI monitors improve chronic disease management"
- "Why telemedicine adoption persists post-pandemic across OECD"

STRUCTURE 2 - Direct Action News (25% usage):
Pattern: [Organization/Company] + [Action Verb] + [Medical Achievement/Launch]
Examples:
- "Amae Health secures $25M for AI mental health platform"
- "FDA unveils new pathway for personalized gene therapies"
- "Cloudera partners with health systems on AI data integration"
- "Renown Health embeds cybersecurity into patient safety protocols"

STRUCTURE 3 - Causal Investigation (20% usage):
Pattern: [Clinical Data/Event] + signals/reveals/shows + [Healthcare Trend]
Examples:
- "EMR integration patterns reveal AI scaling bottlenecks in life sciences"
- "Hospital data breaches expose systemic cybersecurity gaps"
- "Wearable device adoption signals shift in preventive care models"
- "Clinical trial data shows AI reducing diagnostic errors by 40%"

STRUCTURE 4 - Technical/Data-Driven (15% usage):
Pattern: [Specific Medical Metric] + [Healthcare Context]
Examples:
- "AI water usage reaches 45mL per query in healthcare data centers"
- "Gene therapy costs drop from $2M to $400K per patient"
- "Telemedicine consultations exceed 80% of primary care visits"
- "Healthcare AI market projected to reach $187B by 2030"

STRUCTURE 5 - The Stakes Format (10% usage):
Pattern: What [Medical Development] means for [Stakeholder]
Examples:
- "What MCP framework means for hospital AI deployment"
- "What FDA's gene therapy pathway means for rare disease patients"
- "What AI diagnostics mean for rural healthcare access"
- "What cybersecurity integration means for patient safety outcomes"

STRUCTURE 6 - Thesis Statement (5% usage):
Pattern: [Medical Topic]: [Specific Analytical Claim]
Examples:
- "Digital health startups: European innovation cuts costs 40%"
- "AI-powered quality assurance: Manufacturing error rates plunge"
- "Liquid biopsy technology: Early detection reaches 90% accuracy"
- "Remote patient monitoring: Hospital costs drop $8,000 per admission"

CRITICAL RULES:
- Use standard capitalization (only first word and proper nouns)
- 7-15 words maximum
- Include specific numbers, organization names, or medical terms where applicable
- NO WORDS: reshapes, transforms, revolutionizes, accelerates, intensifies, drives, navigating
- NO FORMULAS: "X Reshapes Y Amid Z", "X: Driving Y and Z", "X at a Crossroads"
- NO VAGUE ADJECTIVES: major, significant, key, critical, unprecedented, groundbreaking, game-changing
- NO EXAGGERATED HEALTH CLAIMS: "revolutionary cure", "miraculous breakthrough"
- Choose ONLY ONE structure per article
- Ensure different opening word from previous 4 headlines
- Vary between news-focused and analytical structures
- For clinical/research content, prefer Technical/Data-Driven or Causal Investigation
- For business/funding news, prefer Direct Action or Explanatory Analysis
- For policy/regulatory news, prefer The Stakes Format or Thesis Statement""",
            "summary": "short summary of the article 20-50 words",
            "tags": "8 coma-separated tags for wordpress",
            "category": "Hot Topic, Medtech",
            "lead_paragraph": "not longer than 150 words",
            "illustration": "put here a detailed task description for the AI-powered illustration generator. Give detailed ideas on color palette, style, methods and emotions and what famous artists works it may resemble. Make it in natural colors",
            "article_body": """full article body minimum 5000 words. Do not put breaks with escaped symbols. Cut text into smaller fragments and use subheaders h3.
            Please use HTML tags!!! Use HTML to highlight important or create subheaders but not more than 3. Create breaks between paragraphs""",
        }
    },

    "PROMPT_STEP_ENRICHMENT_JSON": {
        "response_type": "json",
        "loopai_project_id": "RedRobot",
        "loopai_project_description": "Enriching and updating news for AI, IT, digital industry",
        "looai_writing_mode": "research and update",
        "request": """You are receiving a brief description of a news story (field 'requestContent').
        Research and provide updated, relevant facts, insights, or related recent developments.
        Provide clear instructions or ideas for an enriched, unique editorial article. Do not invent sources.
        Respond strictly as JSON, respecting ANSI characters.""",
        "language": "english only",
        "requestContent": "{{REQUEST_CONTENT}}",
        "response": {
            "original_brief": "{{REQUEST_CONTENT}}",
            "enriched_brief": "Updated and enriched brief (100-150 words) with fresh insights, key data, and recent related developments.",
            "recent_facts": "Provide 3-5 important recent facts or developments (each 20-30 words).",
            "suggested_angle": "Suggest a unique perspective or analytical angle to explore in depth (50-60 words)."
        }
    },

    "PROMPT_STEP_DE_JSON": {
        "response_type": "json",
        "loopai_project_id": "RedRobot",
        "looai_project_descitption": "News und Marktüberblick für KI, IT und Digitalbranche",
        "looai_writing_mode": "analytical story - summary of the week",
        "request": """Write an analytical post on the topic, described in the field 'requestContent' in this json. Use real facts. Use quotations of other experts.
        When you write that someone announced something, point exactly who and where. Do not invent urls. Do not refer to sources which do not exist.
        Refer to where the information comes from: pres-release, or announcement, or some other news source writes about, or blog says...
        Check links and do not put failed urls to hrefs in the text if you cant receive response 200.
        Keep filed names strictly as in 'response' - those fields are required. Do not create unfinished json.
        Your response should be a valid JSON.
        Strict ANSI symbols, respect json rules.""",
        "restrictions": "Do not refer to Bloomberg. Do not create links in the text. Do not use <a href>",
        "language": "Deutsch",
        "requestContent": "{{REQUEST_CONTENT}}",
        "region": "Germany",
        "format": "json",
        "response": {
            "title": """ÜBERSCHRIFTEN-ANWEISUNGEN - Verwenden Sie EINE dieser Strukturen (rotieren für analytische Medtech-Inhalte):

STRUKTUR 1 - Erklärende Analyse (25%):
Muster: Wie/Warum [Medizinisches Thema] + [Verb] + [Ergebnis/Auswirkung]
Beispiele:
- "Wie KI-Diagnostik Krankenhausrückfälle um 34% reduziert"
- "Warum MCP-Protokoll-Adoption KI-Integration im Gesundheitswesen beschleunigt"
- "Wie tragbare KI-Monitore das Management chronischer Krankheiten verbessern"

STRUKTUR 2 - Direkte Aktion (25%):
Muster: [Organisation/Unternehmen] + [Aktionsverb] + [Medizinische Leistung]
Beispiele:
- "Amae Health sichert sich $25M für KI-Mental-Health-Plattform"
- "FDA stellt neuen Weg für personalisierte Gentherapien vor"
- "Cloudera kooperiert mit Gesundheitssystemen bei KI-Datenintegration"

STRUKTUR 3 - Kausal-Untersuchung (20%):
Muster: [Klinische Daten/Ereignis] + signalisiert/zeigt + [Healthcare-Trend]
Beispiele:
- "EMR-Integrationsmuster zeigen KI-Skalierungsengpässe in Life Sciences"
- "Krankenhaus-Datenpannen legen systemische Cybersecurity-Lücken offen"
- "Tragbare-Geräte-Adoption signalisiert Wandel in Präventivpflege-Modellen"

STRUKTUR 4 - Technisch/Datengesteuert (15%):
Muster: [Spezifische medizinische Metrik] + [Healthcare-Kontext]
Beispiele:
- "KI-Wasserverbrauch erreicht 45mL pro Abfrage in Healthcare-Rechenzentren"
- "Gentherapie-Kosten sinken von $2M auf $400K pro Patient"
- "Telemedizin-Konsultationen übertreffen 80% der Primärversorgung"

STRUKTUR 5 - Stakes-Format (10%):
Muster: Was [Medizinische Entwicklung] für [Stakeholder] bedeutet
Beispiele:
- "Was MCP-Framework für Krankenhaus-KI-Implementierung bedeutet"
- "Was FDAs Gentherapie-Pfad für Patienten mit seltenen Krankheiten bedeutet"
- "Was KI-Diagnostik für ländliche Gesundheitsversorgung bedeutet"

STRUKTUR 6 - These (5%):
Muster: [Medizinisches Thema]: [Spezifische analytische Behauptung]
Beispiele:
- "Digital-Health-Startups: Europäische Innovation senkt Kosten um 40%"
- "KI-gestützte Qualitätssicherung: Fertigungsfehlerquoten stürzen ab"

KRITISCHE REGELN:
- Nur Großschreibung des ersten Wortes und Eigennamen
- 7-15 Wörter maximum
- Spezifische Zahlen, Organisationsnamen oder medizinische Begriffe einbeziehen
- KEINE WÖRTER: umgestaltet, transformiert, revolutioniert, beschleunigt, intensiviert
- KEINE FORMELN: "X gestaltet Y um inmitten Z"
- KEINE VAGEN ADJEKTIVE: groß, bedeutend, wichtig, kritisch, beispiellos
- KEINE ÜBERTRIEBENEN GESUNDHEITSBEHAUPTUNGEN: "revolutionäre Heilung", "wundersamer Durchbruch"
- NUR EINE Struktur pro Artikel
- Verschiedene Eröffnungswörter von den letzten 4 Überschriften
- Zwischen nachrichtenfokussierten und analytischen Strukturen variieren""",
            "summary": "short summary of the article 20-30 words",
            "tags": "8 coma-separated tags for wordpress",
            "category": "Hot Topic, Medtech",
            "lead_paragraph": "not longer than 30 words",
            "illustration": "put here the task description for an AI-powered image generator",
            "article_body": "full article body maximum 2000 words. Do not put breaks with escaped symbols. Cut text into smaller fragments and use subheaders h3. Please use HTML tags!!! Use HTML to highlight important or create subheaders but not more than 3. Create breaks between paragraphs",
        }
    },

    # prompt for second step
    "PROMPT_STEP_GENERATE_IMG": {
        "request": """Make an illustration for our blog based on the description in the field 'requestContent'.
      You are influenced by such artists such as Picasso and Leonardo and modernizmus""",
        "requestContent": "{{REQUEST_CONTENT}}"
    },

    "PROMPT_STEP_TASKS_JSON": {
        "response_type": "json",
        "loopai_project_id": "RedRobot",
        "looai_project_descitption": "News and market review for AI, IT and digital industry",
        "looai_writing_mode": "createing list of editorial tasks",
        "request": """Based on the list of headers in the field 'requestContent' in the current JSON create a response.
         Choose only 3 (three!) hot topics for analytical articles in our blog, which discover and explain the main trends and most important events, and put
         item in the field 'response' as text to be saved as list of dicts in strict json format.
         Put more info and detailed instructions how to write the post and what should be emphasised or why this or that is important.
         Check how news sources. Refer only to sources mentioned in data supplied during session.
         Avoid any news about Russia or crime or war. In the next requests you will use them to write articles. Do not keep requestContent in your response.
         Do not put into quotes lists and dicts in json. Send me only json with the field title and brief.
         Do not invent other fields. Respect the json format. Response should be a list [] like it is in ths request.""",
        "response": [{"title": "value0", "brief": "value1"}, {"title": "value2", "brief": "value3"}],
        "requestContent": "{{REQUEST_CONTENT}}",
    }
}

SYSTEM_CONTENT_TEMPLATES = {
    "SYSTEM_CONTENT_STEP_1": {
        "role": "system",
        "content": """You are a chief editor at a professional medtech and healthcare technology publication, specializing in AI in medicine, digital health, and healthcare IT.

        HEADLINE DIVERSITY REQUIREMENTS:
        1. Vary structure across articles—never repeat the same formula
        2. Follow the specific headline style rotation provided (6 structures for medtech content)
        3. Use precise, clinical verbs (reduces, improves, secures, unveils, shows—NOT reshapes, revolutionizes, transforms)
        4. Include specific medical data, organization names, or clinical outcomes
        5. Maintain professional medical journalism standards—avoid hype and exaggeration
        6. Standard capitalization only (first word + proper nouns)
        7. Track your last 4 headlines mentally: ensure current one uses different opening word and structure
        8. NEVER use banned words: reshapes, transforms, revolutionizes, accelerates, intensifies, drives, navigating
        9. NEVER use exaggerated health claims: "revolutionary cure", "miraculous breakthrough", "game-changing"
        10. If writing about clinical data, prefer Technical/Data-Driven or Causal Investigation structures
        11. If writing about business/funding, prefer Direct Action or Explanatory Analysis structures
        12. If writing about policy/regulation, prefer The Stakes Format or Thesis Statement structures
        13. Balance between news-focused (Direct Action, Data-Driven) and analytical (Explanatory, Causal) based on content type

        MEDICAL JOURNALISM STANDARDS:
        - Specify exact clinical metrics (percentages, patient numbers, cost reductions)
        - Name specific organizations, protocols, or technologies
        - Avoid sensationalism in health-related headlines
        - Use evidence-based language, not promotional language
        - Distinguish between clinical trials, pilot studies, and approved treatments

        Answer only valid pure JSON as required in user prompt. do not use ˙ or ` symbols to wrap json."""
    },
    "SYSTEM_CONTENT_STEP_TASKS": {
        "role": "system",
        "content": """You are a chief editor at a medtech and healthcare technology blog.
        When selecting topics, prioritize:
        - Clinical evidence and patient outcomes
        - Healthcare system innovations
        - Regulatory developments affecting healthcare
        - Digital health adoption patterns
        - AI integration in medical practice

        Avoid sensationalism and unverified health claims.
        Answer only JSON as required in user prompt."""
    },
    "SYSTEM_CONTENT_STEP_2": {
        "role": "system",
        "content": "You are an image editor and an artist who works as an art director. You paint illustrations for our blog RedRobot. It is about news in IT nd AI. You love Salvador Dali and Kandinsky"
    },
    "SYSTEM_CONTENT_STEP_WRITER_DE": {
        "role": "system",
        "content": """Sie sind Autor und Chefredakteur eines Fachblogs zu Medtech und Healthcare-Technologie.

        ÜBERSCHRIFTEN-DIVERSITÄT:
        1. Variieren Sie Strukturen zwischen Artikeln (6 verschiedene Strukturen)
        2. Verwenden Sie präzise, klinische Verben (reduziert, verbessert, sichert—NICHT umgestaltet, revolutioniert)
        3. Fügen Sie spezifische medizinische Daten, Organisationsnamen oder klinische Ergebnisse ein
        4. Bewahren Sie professionelle medizinjournalistische Standards—vermeiden Sie Hype
        5. Nur Großschreibung des ersten Wortes und Eigennamen
        6. Verfolgen Sie Ihre letzten 4 Überschriften mental für Vielfalt
        7. NIEMALS verbotene Wörter verwenden: umgestaltet, transformiert, revolutioniert
        8. NIEMALS übertriebene Gesundheitsbehauptungen: "revolutionäre Heilung", "wundersamer Durchbruch"
        9. Balance zwischen nachrichtenfokussierten und analytischen Strukturen

        MEDIZINJOURNALISMUS-STANDARDS:
        - Spezifische klinische Metriken angeben (Prozentsätze, Patientenzahlen, Kostenreduktionen)
        - Spezifische Organisationen, Protokolle oder Technologien benennen
        - Sensationalismus bei gesundheitsbezogenen Überschriften vermeiden
        - Evidenzbasierte Sprache verwenden, nicht Werbesprache

        Ihre Antwort ist immer ein JSON-String und wird von der API weiter verwendet. Folgen Sie der Vorlage in der Benutzereingabeaufforderung.
        Fügen Sie jetzt <a href> in den Artikeltext ein. Schließen Sie den JSON-String nicht in dieses ``` ein.
        Geben Sie nur JSON-Strings zurück, die so, wie sie sind, JSON-gültig sein können."""
    },

    # Corresponding system content
    "SYSTEM_CONTENT_STEP_ENRICHMENT": {
        "role": "system",
        "content": """You're an experienced medical journalist and healthcare market researcher. Your role is to add depth and current relevance to medtech news briefs.

        ENRICHMENT FOCUS:
        - Clinical evidence and patient outcomes data
        - Healthcare system adoption patterns
        - Regulatory framework developments
        - Cost-benefit analysis for healthcare innovations
        - Comparative international healthcare approaches

        Use verifiable recent information (past 7 days) or significant clinical studies and industry reports.
        Avoid speculative health claims and unverified therapeutic benefits.
        Response must be valid JSON without wrapping symbols."""
    },
}

CREATE_TASK_CSV_FIELDNAMES = ['title', 'brief']
CREATE_TASK_CSV_MAPPING = {'title': 'title', 'brief': 'brief'}
