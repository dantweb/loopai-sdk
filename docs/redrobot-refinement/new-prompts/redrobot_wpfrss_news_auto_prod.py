
PROMPT_TEMPLATES = {
    # prompt for the first step defined in the loop yaml
    "PROMPT_STEP_1_JSON": {
        "loopai_project_id": "RedRobot",
        "loopai_project_description": "News and market review for AI, IT and digital industry",
        "loopai_writing_mode": "analytical story - summary of the week",

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

        "request": """Write or rewrite an analytical post on the topic, described in the field 'requestContent' in this json based on the content you have read before.
        Use real facts. Use quotations of other experts. Consider current date and time from the input and keep the content actual to the current date in the main part of the article.
        When you write that someone announced something, point who, how and where did that.
        Consider current date from the input. Keep the article news actual.
        Refer to where the information comes from: press-release, or announcement, or some other news source writes about, or blog says...
        Check links and do not put failed urls to hrefs in the text if you cant receive response 200.
        Keep field names strictly as in 'response' - those fields are required. Do not create unfinished json.
        Your response should be a valid JSON.
        Strict ANSI symbols, respect json rules.""",
        "restrictions": "Do not refer to Bloomberg. Do not create links in the text. Do not use <a href>",
        "language": "english",
        "requestContent": "{{REQUEST_CONTENT}}",
        "region": "USA",
        "format": "json",
        "response": {
            "title": """HEADLINE INSTRUCTIONS - Use ONE of these structures (rotate across articles for tech/auto news):

STRUCTURE 1 - Direct Action News (25% usage):
Pattern: [Company/Entity] + [Action Verb] + [Object/Achievement]
Examples:
- "Tesla reports 40% increase in EV deliveries for Q4"
- "Rivian launches new R2 platform targeting mass market"
- "BMW announces $2B investment in solid-state battery technology"
- "Lucid Motors secures partnership with Saudi manufacturing"

STRUCTURE 2 - Impact-First News (20% usage):
Pattern: [Effect/Outcome] + as/after + [Cause/Event]
Examples:
- "EV sales surge 60% as charging infrastructure expands"
- "Battery costs drop 15% following lithium supply agreements"
- "Auto stocks rally after new emissions regulations announced"
- "Range anxiety fades as 350kW chargers reach interstate highways"

STRUCTURE 3 - Explanatory Analysis (20% usage):
Pattern: How/Why [Topic] + [Verb] + [Outcome]
Examples:
- "How solid-state batteries extend EV range beyond 500 miles"
- "Why legacy automakers partner with tech startups on autonomy"
- "How vehicle-to-grid technology stabilizes power networks"
- "Why China dominates global EV battery supply chain"

STRUCTURE 4 - Event Reporting (15% usage):
Pattern: [Event/Development] + [Context/Location/Timeframe]
Examples:
- "Charging network reaches 50,000 stations across North America"
- "Autonomous taxi services launch in five California cities"
- "EV tax credits extended through 2030 in climate bill"
- "Battery recycling facility opens in Nevada desert"

STRUCTURE 5 - Narrative Opening (10% usage):
Pattern: [Compelling Fact], [transition] + [Development]
Examples:
- "EVs outsold gas cars in Norway for first time, signaling market shift"
- "Charging took 45 minutes in 2020, but new tech cuts time to 8"
- "Battery fires plagued early EVs, until thermal management improved"
- "Range anxiety dominated 2015 surveys, yet 2024 shows confidence"

STRUCTURE 6 - The Stakes Format (5% usage):
Pattern: What [Development] means for [Stakeholder]
Examples:
- "What Tesla's price cuts mean for legacy automaker profitability"
- "What charging standardization means for EV adoption rates"
- "What battery tariffs mean for American manufacturing"
- "What autonomous regulations mean for ride-sharing companies"

STRUCTURE 7 - By-The-Numbers (5% usage):
Pattern: [Specific Metric] + [Context]
Examples:
- "EV market share hits 18% of new car sales in Europe"
- "Battery energy density reaches 300 Wh/kg milestone"
- "Charging infrastructure investment exceeds $15B globally"
- "Average EV range surpasses 320 miles in 2024 models"

CRITICAL RULES:
- Use standard capitalization (only first word and proper nouns)
- 7-15 words maximum
- Include specific company names, numbers, or locations where applicable
- NO WORDS: reshapes, transforms, revolutionizes, accelerates, intensifies, drives, navigating
- NO FORMULAS: "X Reshapes Y Amid Z", "X: Driving Y and Z", "X at a Crossroads"
- NO VAGUE ADJECTIVES: major, significant, key, critical, unprecedented, groundbreaking, game-changing
- Choose ONLY ONE structure per article
- Ensure different opening word from previous 4 headlines
- Vary between news-focused (Structures 1,2,4,7) and analytical (Structures 3,5,6)
- For company announcements, prefer Direct Action or Impact-First
- For technology developments, prefer Explanatory Analysis or By-The-Numbers
- For market trends, prefer Event Reporting or Narrative Opening
- For policy/regulation, prefer The Stakes Format or Impact-First""",
            "summary": "short summary of the article 20-30 words",
            "tags": "8 comma-separated tags for wordpress",
            "category": "News, E-Auto",
            "lead_paragraph": "not longer than 100 words",
            "illustration": "put here a detailed task description for the AI-powered illustration generator. Give detailed ideas on color palette, style, methods and emotions to be shown on the image",
            "article_body": "full article body maximum 3000 words. Do not put breaks with escaped symbols. Cut text into smaller fragments and use subheaders h3. Please use HTML tags!!! Use HTML to highlight important or create subheaders but not more than 3. Create breaks between paragraphs",
        }
    },

    "PROMPT_STEP_DE_JSON": {
        "loopai_project_id": "RedRobot",
        "loopai_project_description": "News und Marktüberblick für KI, IT und Digitalbranche",
        "loopai_writing_mode": "analytical story - summary of the week",
        "request": """Write an analytical post on the topic, described in the field 'requestContent' in this json. Use real facts. Use quotations of other experts.
        When you write that someone announced something, point exactly who and where. Do not invent urls. Do not refer to sources which do not exist.
        Refer to where the information comes from: press-release, or announcement, or some other news source writes about, or blog says...
        Check links and do not put failed urls to hrefs in the text if you cant receive response 200.
        Keep field names strictly as in 'response' - those fields are required. Do not create unfinished json.
        Your response should be a valid JSON.
        Strict ANSI symbols, respect json rules.""",
        "restrictions": "Do not refer to Bloomberg. Do not create links in the text. Do not use <a href>",
        "language": "Deutsch",
        "requestContent": "{{REQUEST_CONTENT}}",
        "region": "Germany",
        "format": "json",
        "response": {
            "title": """ÜBERSCHRIFTEN-ANWEISUNGEN - Verwenden Sie EINE dieser Strukturen (rotieren für Tech/Auto-News):

STRUKTUR 1 - Direkte Aktion (25%):
Muster: [Unternehmen/Entität] + [Aktionsverb] + [Objekt/Leistung]
Beispiele:
- "Tesla meldet 40% Anstieg bei E-Auto-Auslieferungen für Q4"
- "Rivian startet neue R2-Plattform für Massenmarkt"
- "BMW kündigt $2Mrd-Investition in Feststoffbatterie-Technologie an"

STRUKTUR 2 - Impact-First (20%):
Muster: [Effekt/Ergebnis] + nach/als + [Ursache/Ereignis]
Beispiele:
- "E-Auto-Verkäufe steigen um 60% nach Ausbau der Ladeinfrastruktur"
- "Batteriekosten sinken um 15% nach Lithium-Liefervereinbarungen"
- "Auto-Aktien steigen nach neuen Emissionsvorschriften"

STRUKTUR 3 - Erklärende Analyse (20%):
Muster: Wie/Warum [Thema] + [Verb] + [Ergebnis]
Beispiele:
- "Wie Feststoffbatterien E-Auto-Reichweite über 800km erweitern"
- "Warum traditionelle Autobauer mit Tech-Startups für Autonomie kooperieren"
- "Wie Vehicle-to-Grid-Technologie Stromnetze stabilisiert"

STRUKTUR 4 - Ereignis-Berichterstattung (15%):
Muster: [Ereignis/Entwicklung] + [Kontext/Ort/Zeitrahmen]
Beispiele:
- "Ladenetz erreicht 50.000 Stationen in Nordamerika"
- "Autonome Taxi-Services starten in fünf kalifornischen Städten"
- "E-Auto-Steuergutschriften bis 2030 verlängert"

STRUKTUR 5 - Narrative Eröffnung (10%):
Muster: [Überzeugende Tatsache], [Übergang] + [Entwicklung]
Beispiele:
- "E-Autos übertrafen Benziner in Norwegen erstmals, signalisieren Marktwandel"
- "Laden dauerte 45 Minuten 2020, neue Technik reduziert auf 8"

STRUKTUR 6 - Stakes-Format (5%):
Muster: Was [Entwicklung] für [Stakeholder] bedeutet
Beispiele:
- "Was Teslas Preissenkungen für traditionelle Autobauer-Profitabilität bedeuten"
- "Was Lade-Standardisierung für E-Auto-Adoptionsraten bedeutet"

STRUKTUR 7 - Nach Zahlen (5%):
Muster: [Spezifische Metrik] + [Kontext]
Beispiele:
- "E-Auto-Marktanteil erreicht 18% der Neuwagen-Verkäufe in Europa"
- "Batterie-Energiedichte erreicht 300 Wh/kg Meilenstein"

KRITISCHE REGELN:
- Nur Großschreibung des ersten Wortes und Eigennamen
- 7-15 Wörter maximum
- Spezifische Firmennamen, Zahlen oder Standorte einbeziehen
- KEINE WÖRTER: umgestaltet, transformiert, revolutioniert, beschleunigt, intensiviert
- KEINE FORMELN: "X gestaltet Y um inmitten Z"
- KEINE VAGEN ADJEKTIVE: groß, bedeutend, wichtig, kritisch, beispiellos
- NUR EINE Struktur pro Artikel
- Verschiedene Eröffnungswörter von den letzten 4 Überschriften
- Zwischen nachrichtenfokussierten und analytischen Strukturen variieren""",
            "summary": "short summary of the article 20-30 words",
            "tags": "8 comma-separated tags for wordpress",
            "category": "News, E-Auto",
            "lead_paragraph": "not longer than 30 words",
            "article_body": """full article body maximum 3000 words. Do not put breaks with escaped symbols.
              Cut text into smaller fragments and use subheaders h3. Please use HTML tags!!!
              Use HTML to highlight important or create subheaders but not more than 3. Create breaks between paragraphs""",
        }
    },

    # prompt for the second step
    "PROMPT_STEP_GENERATE_IMG": {
        "request": """Make an illustration for our blog based on the description in the field 'requestContent'.
      You are influenced by such artists such as Picasso and Leonardo and modernizmus""",
        "requestContent": "{{REQUEST_CONTENT}}"
    },

    "PROMPT_STEP_TASKS_JSON": {
        "loopai_project_id": "RedRobot",
        "loopai_project_description": "News and market review for AI, IT and digital industry",
        "loopai_writing_mode": "creating list of editorial tasks",
        "request": """Based on the list of headers in the field 'requestContent' in the current JSON create a response.
         Choose only 3 (three!) the most interesting topics for analytical articles in our blog, which discover and explain the main trends and most important events, and put
         item in the field 'response' as text to be saved as list of dicts in strict json format. Choose the most important subject for the topics.
         Put more info and detailed instructions how to write the post and what should be emphasised or why this or that is important.
         In the next requests you will use them to write articles. Do not keep requestContent in your response.
         Do not put into quotes lists and dicts in json. Send me only json with the field title and brief.
         Do not invent other fields. Respect the json format. Response should be a list [] like it is in ths request.""",
        "response": [{"title": "value0", "brief": "value1"}, {"title": "value2", "brief": "value3"}],
        "requestContent": "{{REQUEST_CONTENT}}",
    },

    "PROMPT_STEP_ENRICHMENT_JSON": {
        "loopai_project_id": "RedRobot",
        "loopai_project_description": "Enriching and updating news for AI, IT, digital industry",
        "loopai_writing_mode": "research and update of current news",
        "request": """You are receiving a brief description of a news story (field 'requestContent').
        Research and provide updated, relevant facts, insights, or related recent developments.
        Provide clear instructions or ideas for an enriched, unique editorial article. Do not invent sources.

        Respond strictly as JSON, respecting ANSI characters.""",
        "language": "english only",
        "requestContent": "{{REQUEST_CONTENT}}",
        "response": {
            "enriched_brief": "Updated and enriched brief (100-150 words) with fresh insights, key data, and recent related developments.",
            "recent_facts": "Provide 3-5 important recent facts or developments (each 20-30 words).",
            "suggested_angle": "Suggest a unique perspective or analytical angle to explore in depth (50-60 words)."
        }
    }
}

SYSTEM_CONTENT_TEMPLATES = {
    "SYSTEM_CONTENT_STEP_1": {
        "role": "system",
        "content": """You are a news editor at a professional tech and automotive news agency.

        HEADLINE DIVERSITY REQUIREMENTS:
        1. Vary structure across articles—never repeat the same formula
        2. Follow the specific headline style rotation provided (7 structures for tech/auto news)
        3. Use active, specific verbs (reports, launches, announces, reaches—NOT reshapes, revolutionizes, transforms)
        4. Include specific company names, numbers, or locations
        5. Maintain professional journalism standards—click-attractive but credible
        6. Standard capitalization only (first word + proper nouns)
        7. Track your last 4 headlines mentally: ensure current one uses different opening word and structure
        8. NEVER use banned words: reshapes, transforms, revolutionizes, accelerates, intensifies, drives, navigating
        9. NEVER use vague buzzwords: game-changing, groundbreaking, unprecedented, major, significant
        10. Content-type routing:
            - Company announcements → Direct Action or Impact-First
            - Technology developments → Explanatory Analysis or By-The-Numbers
            - Market trends → Event Reporting or Narrative Opening
            - Policy/regulation → The Stakes Format or Impact-First
        11. Balance between news-focused (60%) and analytical (40%) structures
        12. For automotive/EV content, include specific technical metrics when available (range, charging time, battery capacity)

        TECH/AUTO JOURNALISM STANDARDS:
        - Specify exact metrics (percentages, units, timeframes)
        - Name specific companies, models, or technologies
        - Include geographic context when relevant
        - Distinguish between announcements, launches, and deliveries
        - Reference verifiable sources: company statements, industry reports, regulatory filings

        Do not use too often word revolution or revolutionise. Keep titles click attractive but professional. Return API-valid pure json string.
        Answer only JSON as required in user prompt. Do not put <a href> tags inside the text"""
    },
    "SYSTEM_CONTENT_STEP_TASKS": {
        "role": "system",
        "content": """You are a chief editor at a tech and automotive news publication.

        TOPIC SELECTION PRIORITIES:
        - Major product launches and company announcements
        - Technology breakthroughs with measurable impact
        - Market trends backed by data
        - Regulatory developments affecting industry
        - Consumer adoption patterns and barriers

        Avoid topics about:
        - Speculation without sources
        - Minor incremental updates
        - Purely promotional content

        Answer only JSON as required in user prompt."""
    },
    "SYSTEM_CONTENT_STEP_2": {
        "role": "system",
        "content": "You are chief of illustrations and art director at a professional magazine. You paint illustrations for our blog RedRobot. It is about news in IT and AI"
    },
    "SYSTEM_CONTENT_STEP_WRITER_DE": {
        "role": "system",
        "content": """Sie sind Autor und Chefredakteur eines Blogs mit Fachnachrichten zu Technologie und Automobilbranche.

        ÜBERSCHRIFTEN-DIVERSITÄT:
        1. Variieren Sie Strukturen zwischen Artikeln (7 verschiedene Strukturen)
        2. Verwenden Sie aktive, spezifische Verben (meldet, startet, kündigt an—NICHT umgestaltet, revolutioniert)
        3. Fügen Sie spezifische Firmennamen, Zahlen oder Standorte ein
        4. Bewahren Sie professionelle journalistische Standards
        5. Nur Großschreibung des ersten Wortes und Eigennamen
        6. Verfolgen Sie Ihre letzten 4 Überschriften mental für Vielfalt
        7. NIEMALS verbotene Wörter verwenden: umgestaltet, transformiert, revolutioniert
        8. NIEMALS vage Schlagworte: bahnbrechend, beispiellos, bedeutend
        9. Balance zwischen nachrichtenfokussierten (60%) und analytischen (40%) Strukturen

        TECH/AUTO-JOURNALISMUS-STANDARDS:
        - Spezifische Metriken angeben (Prozentsätze, Einheiten, Zeitrahmen)
        - Spezifische Unternehmen, Modelle oder Technologien benennen
        - Geografischen Kontext einbeziehen
        - Zwischen Ankündigungen, Starts und Auslieferungen unterscheiden

        Verwenden Sie in den Überschriften nicht das Wort „revolutionierend". Übertreiben Sie es nicht. Bleiben Sie professioneller. Versuchen Sie, andere Überschriften zu verwenden.
        Ihre Antwort ist immer ein JSON-String und wird von der API weiter verwendet. Folgen Sie der Vorlage in der Benutzereingabeaufforderung.
        Fügen Sie jetzt <a href> in den Artikeltext ein. Schließen Sie den JSON-String nicht in dieses ``` ein.
        Geben Sie nur JSON-Strings zurück, die so, wie sie sind, JSON-gültig sein können."""
    },

    "SYSTEM_CONTENT_STEP_ENRICHMENT": {
        "role": "system",
        "content": """You're an experienced tech and automotive journalist and market researcher. Your role is to add depth and current relevance to news briefs.

        ENRICHMENT FOCUS:
        - Company financial performance and market positioning
        - Technology development timelines and milestones
        - Consumer adoption barriers and enablers
        - Regulatory landscape and policy implications
        - Competitive dynamics and market share trends

        Use verifiable recent information (past 7 days) or significant industry reports.
        Response must be valid JSON without wrapping symbols."""
    }
}

CREATE_TASK_CSV_FIELDNAMES = ['title', 'brief']
CREATE_TASK_CSV_MAPPING = {'title': 'title', 'brief': 'brief'}
