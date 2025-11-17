PROMPT_TEMPLATES = {
    "PROMPT_STEP_1_JSON":
    {
        "loopai_project_id": "RedRobot",
        "loopai_project_description": "Enterprise cloud computing and infrastructure analysis",
        "writing_mode": "analytical cloud industry analysis",
        "request": "Write an analytical article on the cloud computing topic described in 'requestContent'. Focus on enterprise implications, market dynamics, and technological innovations. Use real facts from credible sources like industry reports, official announcements, or reputable publications. Incorporate quotations from experts, executives, or analysts, specifying their names, affiliations, and context.\n        When citing announcements, specify exactly who (e.g., company CEO or spokesperson), where (e.g., press release, earnings call), and include verifiable details. Add exact dates only if known and relevant, in format DD Month YYYY. Do not invent dates, events, or URLs.\n        Do not refer to non-existent sources. Explicitly reference information sources: e.g., 'according to a Gartner report,' 'as stated in Microsoft's earnings call,' or 'AWS announced in their re:Invent keynote.'\n        Check conceptual plausibility of any technical claims. Consider current date for timeliness and relevance.\n        Focus on enterprise cloud adoption, multi-cloud strategies, AI infrastructure, and competitive dynamics between AWS, Azure, and Google Cloud.\n        Maintain objective, professional tone akin to Forbes or Financial Times: balanced, insightful, data-driven. Include quantitative data, market statistics, and enterprise adoption metrics.\n        CRITICAL: Return ONLY valid JSON format with no additional text, markdown, or explanations. Ensure all strings are properly quoted.",
        "restrictions": "1. No invented sources or events 2. Maintain enterprise focus 3. Avoid retail cloud services discussion 4. Return ONLY JSON format",
        "special_instructions": "For cloud computing articles, add analytical context about:\n        - Enterprise adoption trends and migration patterns\n        - Competitive positioning among cloud providers (AWS, Azure, GCP)\n        - Economic implications of cloud spending optimization\n        - Technical innovation timelines and market impact\n        Structure with professional cloud industry sections using <h3> tags",
        "language": "professional business English",
        "requestContent": "{{REQUEST_CONTENT}}",
        "region": "Global",
        "format": "json",
        "json_structure": {
            "title": "string: Professional headline focusing on cloud market developments",
            "summary": "string: 25-35 word executive summary highlighting enterprise implications",
            "tags": "string: 6-8 cloud industry tags (multi-cloud, infrastructure, enterprise, etc)",
            "category": "Cloud, Hot Topic",
            "lead_paragraph": "string: Context-setting opening with market or technical context",
            "illustration": "Professional visualization - be creative, make specifications for interesting color pallete, inspired by classic barokko paintings. Sometimes surrealstic image which will be created by another AI",
            "article_body": "string: Sophisticated analysis with enterprise focus, using HTML tags for structure"
        },
        "response": {
            "title": "Professional headline focusing on cloud market developments",
            "summary": "25-35 word executive summary highlighting enterprise implications",
            "tags": "6-8 cloud industry tags separated by commas",
            "category": "Cloud, Hot Topic",
            "lead_paragraph": "Context-setting opening with market or technical context",
            "illustration": "Professional visualization - be creative, make specifications for interesting color pallete, inspired by classic barokko paintings. Sometimes surrealstic image which will be created by another AI",
            "article_body": "Sophisticated analysis with enterprise focus, using HTML tags for structure"
        }
    },


    "PROMPT_STEP_DE_JSON": {
        "loopai_project_id": "RedRobot",
        "loopai_project_description": "Enterprise Cloud Computing und Infrastruktur Analyse",
        "writing_mode": "analytische Cloud-Branchenanalyse",
        "request": "Übersetzen Sie den 'requestContent' in diesem JSON. Verwenden Sie echte Fakten aus seriösen Quellen wie Branchenberichten, offiziellen Ankündigungen oder angesehenen Veröffentlichungen.\n        Wenn Sie schreiben, dass jemand etwas angekündigt hat, geben Sie genau an, wer (z.B. Firmen-CEO oder Sprecher), wo (z.B. in einer Pressemitteilung, Earnings Call oder Interview) und fügen Sie überprüfbare Details hinzu. Erfinden Sie keine URLs. Beziehen Sie sich nicht auf Quellen, die nicht existieren.\n        Beziehen Sie sich explizit auf die Herkunft der Informationen: z.B. 'laut einer Pressemitteilung von Company X', 'wie in einem aktuellen Gartner-Bericht berichtet' oder 'Analysten bei McKinsey stellten in ihrer neuesten Studie fest.'\n        Überprüfen Sie Links konzeptionell auf Plausibilität und fügen Sie keine fehlerhaften oder hypothetischen URLs in hrefs ein.\n        Halten Sie die Feldnamen genau wie in 'response' - diese Felder sind erforderlich. Erstellen Sie keinen unvollständigen JSON.\n        Ihre Antwort sollte ein gültiges JSON sein.\n        Strenge ANSI-Symbole, beachten Sie JSON-Regeln.",
        "restrictions": "Beziehen Sie sich nicht auf Bloomberg. Erstellen Sie keine Links im Text. Verwenden Sie kein <a href>",
        "language": "Deutsch",
        "requestContent": "{{REQUEST_CONTENT}}",
        "region": "Global",
        "format": "json",
        "response": {
            "title": "Der Titel sollte eine aktuelle, professionelle Schlagzeile sein, im Stil von Forbes oder Financial Times: Großschreibung wichtiger Wörter, Vermeidung von Sensationalismus, Fokus auf Schlüsselfakten oder Implikationen.",
            "summary": "Kurzfassung des Artikels 20-30 Wörter",
            "tags": "8 durch Kommas getrennte Tags für WordPress",
            "category": "Cloud, Hot Topic",
            "lead_paragraph": "nicht länger als 50 Wörter. Der Lead-Paragraph sollte nicht die Zusammenfassung kopieren. Er sollte andere Wörter enthalten und mit Details und Fakten interessanter sein",
            "illustration": "Hier die Aufgabenbeschreibung für einen KI-gestützten Bildgenerator einfügen",
            "article_body": "Vollständiger Artikeltext mindestens 2000 Wörter. Strukturieren Sie professionell: verwenden Sie <h3> Unterüberschriften für Abschnitte (3-5 insgesamt), <p> für Absätze, <strong> oder <em> sparsam für Hervorhebungen. Fügen Sie Datenpunkte, Zitate und Analysen ein. Sicherstellen Sie einen logischen Fluss: Einleitung, Hauptteil mit Beweisen, Schlussfolgerung mit Implikationen.\n          Verwenden Sie keine Umbrüche mit Escape-Symbolen. Teilen Sie den Text in kleinere Fragmente auf und verwenden Sie Unterüberschriften h3. Bitte verwenden Sie HTML-Tags!!!\n          Verwenden Sie HTML, um Wichtiges hervorzuheben oder Unterüberschriften zu erstellen, aber nicht mehr als 3-4. Erstellen Sie Absätze zwischen den Absätzen"
        }
    },
    "PROMPT_STEP_GENERATE_IMG": {
        "request": """Create a professional illustration for cloud computing blog content based on the description in 'requestContent'.  
         Use allegoric and methaphoric approach""",
        "requestContent": "{{REQUEST_CONTENT}}"
    },
    "PROMPT_STEP_TASKS_JSON": {
        "loopai_project_id": "RedRobot",
        "loopai_project_description": "Enterprise cloud computing and infrastructure analysis",
        "writing_mode": "strategic cloud topic development",
        "request": """Based on cloud computing content in 'requestContent', select 3 most important, insightful topics for in-depth articles exploring:
        - Enterprise cloud adoption trends and challenges
        - Multi-cloud and hybrid infrastructure strategies
        - AI/ML infrastructure and GPU cloud computing
        - Cloud security, compliance, and governance
        - Cost optimization and FinOps practices
        - Focus on subjects with broad enterprise impact and technological significance.
        - Ensure topics are current and relevant to cloud industry developments.
        Provide detailed analytical frameworks for each topic with emphasis on:      
        - Market analysis and competitive dynamics
        - Enterprise adoption patterns and case studies
        - Technical innovation and implementation challenges
        - Economic implications and ROI considerations
        CRITICAL: Return ONLY valid JSON format. No additional text or explanations.""",
        "json_structure": [{
            "title": "string: Professional cloud computing topic title",
            "brief": "string: 400-600 word analytical framework with enterprise focus"
        }],
        "requestContent": "{{REQUEST_CONTENT}}"
    },
    "PROMPT_STEP_ENRICHMENT_JSON": {
        "loopai_project_id": "RedRobot",
        "loopai_project_description": "Enterprise cloud computing analysis enhancement",
        "writing_mode": "cloud industry context expansion",
        "request": """Enhance cloud computing content using enterprise research methods:
        1. Multi-cloud strategy analysis and adoption patterns  
        2. Cloud provider competitive positioning (AWS vs Azure vs GCP)      
        3. Enterprise migration challenges and success factors
        4. Cloud infrastructure innovation assessment      Professional Standards:
        - Multiple source verification from industry reports
        - Enterprise case study integration
        - Market share and spending analysis
        - Technical capability comparisons
        CRITICAL: Return ONLY valid JSON format. No additional text or markdown.""",
        "language": "professional business English",
        "requestContent": "{{REQUEST_CONTENT}}",
        "json_structure": {
            "original_brief": "string: The original cloud computing content",
            "enriched_brief": "string: Enterprise-focused analysis with strategic cloud context",
            "market_analysis": "string: Cloud provider competitive landscape and market dynamics",
            "enterprise_implications": "string: Business impact and adoption recommendations"
        },
        "response": {
            "original_brief": "{{REQUEST_CONTENT}}",
            "enriched_brief": "Enterprise-focused analysis with strategic cloud context",
            "market_analysis": "Cloud provider competitive landscape and market dynamics",
            "enterprise_implications": "Business impact and adoption recommendations"
        }
    }
}

SYSTEM_CONTENT_TEMPLATES = {
    "SYSTEM_CONTENT_STEP_1": {
        "role": "system",
        "content": "You are a senior cloud infrastructure analyst at a prestigious publication like Forbes or Financial Times, specializing in enterprise cloud computing, multi-cloud strategies, and infrastructure technology.\n      Focus on AWS, Azure, Google Cloud market dynamics, enterprise adoption patterns, and technological innovations.\n      Avoid hype words; maintain professional, data-driven analysis of cloud economics and enterprise implications.\n      CRITICAL: Your answer must be ONLY valid JSON format for API use. Follow the user's prompt template strictly.\n      Do not include <a href> in article body. Do not wrap JSON in ```. Return only pure JSON."
    },
    "SYSTEM_CONTENT_STEP_TASKS": {
        "role": "system",
        "content": "You are a chief editor at an enterprise technology publication, focusing on cloud infrastructure, multi-cloud strategies, and enterprise digital transformation.\n      CRITICAL: Answer only in valid JSON format as specified in the user prompt. No additional text."
    },
    "SYSTEM_CONTENT_STEP_2": {
        "role": "system",
        "content": "You are a technology visualization expert creating professional cloud computing illustrations for enterprise publications. Focus on clean, conceptual representations of cloud architecture, data flows, and infrastructure concepts. Be creative, you are inspired by S.Dali, Picasso, DaVinci, J.Bosch, Van Eik"
    },
    "SYSTEM_CONTENT_STEP_DE": {
        "role": "system",
        "content": "Sie sind Senior Editor und Cloud-Experte bei einer prestigeträchtigen Publikation wie Forbes oder Financial Times, spezialisiert auf Enterprise Cloud Computing und Infrastruktur-Technologie.\n      Vermeiden Sie Hype-Wörter; halten Sie die Analyse professionell, datengestützt und auf Enterprise-Implikationen ausgerichtet.\n      Ihre Antwort ist immer ein JSON-String für die API-Nutzung. Folgen Sie der Benutzervorlage streng.\n      Fügen Sie kein <a href> in den Artikeltext ein. Schließen Sie JSON nicht in ``` ein. Geben Sie nur einen validen JSON-String zurück."
    },
    "SYSTEM_CONTENT_STEP_ENRICHMENT": {
        "role": "system",
        "content": "You're an experienced cloud industry analyst at an enterprise technology outlet. Your role is to add depth, market context, and strategic analysis to cloud computing content.\n      Focus on enterprise adoption patterns, multi-cloud strategies, and competitive dynamics between major cloud providers.\n      CRITICAL: Response must be valid JSON without wrapping symbols or additional text."
    }
}

CREATE_TASK_CSV_FIELDNAMES=["title", "brief"]
CREATE_TASK_CSV_MAPPING={"title":"title", "brief":"brief"}
