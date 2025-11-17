PROMPT_TEMPLATES = {
    "PROMPT_STEP_1_JSON":
    {
        "loopai_project_id": "RedRobot",
        "loopai_project_description": "Enterprise cloud computing and infrastructure analysis",
        "loopai_writing_mode": "analytical cloud industry analysis",
        "request": "Write an analytical article on the cloud computing topic described in 'requestContent'. Focus on enterprise implications, market dynamics, and technological innovations. Use real facts from credible sources like industry reports, official announcements, or reputable publications. Incorporate quotations from experts, executives, or analysts, specifying their names, affiliations, and context.\n        When citing announcements, specify exactly who (e.g., company CEO or spokesperson), where (e.g., press release, earnings call), and include verifiable details. Add exact dates only if known and relevant, in format DD Month YYYY. Do not invent dates, events, or URLs.\n        Do not refer to non-existent sources. Explicitly reference information sources: e.g., 'according to a Gartner report,' 'as stated in Microsoft's earnings call,' or 'AWS announced in their re:Invent keynote.'\n        Check conceptual plausibility of any technical claims. Consider current date for timeliness and relevance.\n        Focus on enterprise cloud adoption, multi-cloud strategies, AI infrastructure, and competitive dynamics between AWS, Azure, and Google Cloud.\n        Maintain objective, professional tone akin to Forbes or Financial Times: balanced, insightful, data-driven. Include quantitative data, market statistics, and enterprise adoption metrics.\n        CRITICAL: Return ONLY valid JSON format with no additional text, markdown, or explanations. Ensure all strings are properly quoted.",
        "restrictions": "1. No invented sources or events 2. Maintain enterprise focus 3. Avoid retail cloud services discussion 4. Return ONLY JSON format",
        "special_instructions": "For cloud computing articles, add analytical context about:\n        - Enterprise adoption trends and migration patterns\n        - Competitive positioning among cloud providers (AWS, Azure, GCP)\n        - Economic implications of cloud spending optimization\n        - Technical innovation timelines and market impact\n        Structure with professional cloud industry sections using <h3> tags",
        "language": "professional business English",
        "requestContent": "{{REQUEST_CONTENT}}",
        "region": "Global",
        "format": "json",
        "json_structure": {
            "title": "string: Professional headline - see detailed instructions below",
            "summary": "string: 25-35 word executive summary highlighting enterprise implications",
            "tags": "string: 6-8 cloud industry tags (multi-cloud, infrastructure, enterprise, etc)",
            "category": "Cloud, Hot Topic",
            "lead_paragraph": "string: Context-setting opening with market or technical context",
            "illustration": "Professional visualization - be creative, make specifications for interesting color pallete, inspired by classic barokko paintings. Sometimes surrealstic image which will be created by another AI",
            "article_body": "string: Sophisticated analysis with enterprise focus, using HTML tags for structure"
        },
        "response": {
            "title": """HEADLINE INSTRUCTIONS - Use ONE of these structures (rotate across articles for enterprise cloud content):

STRUCTURE 1 - Explanatory Analysis (20% usage):
Pattern: How/Why [Cloud Topic] + [Verb] + [Enterprise Outcome]
Examples:
- "How FinOps practices cut enterprise cloud costs by 30%"
- "Why multi-cloud strategies dominate enterprise IT roadmaps"
- "How GPU cloud infrastructure enables enterprise AI at scale"
- "Why Azure hybrid cloud wins government contract renewals"

STRUCTURE 2 - Comparative Analysis (20% usage):
Pattern: [Cloud Option A] vs. [Cloud Option B]: [Finding/Insight]
Examples:
- "AWS vs. Azure vs. GCP: Enterprise AI infrastructure showdown"
- "Multi-cloud vs. hybrid cloud: TCO analysis reveals 25% gap"
- "Public cloud vs. on-premise: Migration ROI reaches breakeven in 18 months"
- "Serverless vs. containers: Enterprise adoption patterns diverge"

STRUCTURE 3 - Direct Action News (15% usage):
Pattern: [Cloud Provider/Enterprise] + [Action Verb] + [Achievement/Launch]
Examples:
- "AWS launches new GPU instances for enterprise AI workloads"
- "Microsoft reports 30% Azure revenue growth in Q4"
- "Google Cloud secures $2B deal with Fortune 500 retailer"
- "Enterprise spending on multi-cloud surges 40% year-over-year"

STRUCTURE 4 - Technical Milestone (15% usage):
Pattern: [Cloud Technology/Service] + achieves/reaches + [Specific Metric]
Examples:
- "Azure OpenAI Service reaches 10,000 enterprise deployments"
- "AWS Graviton processors achieve 60% better price-performance"
- "Google Cloud TPU v5 delivers 2x training speed improvement"
- "Multi-cloud management tools reduce overhead by 40%"

STRUCTURE 5 - The Stakes Format (15% usage):
Pattern: What [Cloud Development] means for [Enterprise Stakeholder]
Examples:
- "What FinOps maturity means for enterprise cloud economics"
- "What sovereign cloud requirements mean for AWS and Azure strategy"
- "What GPU shortages mean for enterprise AI infrastructure plans"
- "What cloud repatriation trends mean for hybrid architecture"

STRUCTURE 6 - Thesis Statement (10% usage):
Pattern: [Cloud Topic]: [Specific Strategic Claim]
Examples:
- "Enterprise GPU cloud: Demand outpaces supply by 3:1 ratio"
- "FinOps adoption: Enterprises reclaim $40B in cloud waste"
- "Multi-cloud networking: Complexity costs exceed 20% of cloud spend"
- "Cloud AI infrastructure: NVIDIA partnerships reshape vendor landscape"

STRUCTURE 7 - Causal Investigation (5% usage):
Pattern: [Market Data/Trend] + signals/reveals/shows + [Strategic Implication]
Examples:
- "Cloud spending patterns reveal enterprise AI priorities"
- "Migration delays signal hybrid cloud as long-term state"
- "GPU instance pricing reveals infrastructure capacity constraints"
- "FinOps job postings surge 200%, indicating maturity shift"

CRITICAL RULES:
- Use standard capitalization (only first word and proper nouns)
- 7-15 words maximum
- Include specific provider names (AWS, Azure, GCP), metrics, or technologies
- NO WORDS: reshapes, transforms, revolutionizes, accelerates, intensifies, drives, navigating
- NO FORMULAS: "X Reshapes Y Amid Z", "X: Driving Y and Z", "X at a Crossroads"
- NO VAGUE ADJECTIVES: major, significant, key, critical, unprecedented, groundbreaking
- Choose ONLY ONE structure per article
- Ensure different opening word from previous 4 headlines
- Vary between competitive, strategic, and technical structures
- For market analysis, prefer Comparative Analysis or Thesis Statement
- For provider announcements, prefer Direct Action or Technical Milestone
- For enterprise strategy, prefer Explanatory Analysis or The Stakes Format
- For economic analysis, prefer Causal Investigation or Thesis Statement""",
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
        "loopai_writing_mode": "analytische Cloud-Branchenanalyse",
        "request": "Übersetzen Sie den 'requestContent' in diesem JSON. Verwenden Sie echte Fakten aus seriösen Quellen wie Branchenberichten, offiziellen Ankündigungen oder angesehenen Veröffentlichungen.\n        Wenn Sie schreiben, dass jemand etwas angekündigt hat, geben Sie genau an, wer (z.B. Firmen-CEO oder Sprecher), wo (z.B. in einer Pressemitteilung, Earnings Call oder Interview) und fügen Sie überprüfbare Details hinzu. Erfinden Sie keine URLs. Beziehen Sie sich nicht auf Quellen, die nicht existieren.\n        Beziehen Sie sich explizit auf die Herkunft der Informationen: z.B. 'laut einer Pressemitteilung von Company X', 'wie in einem aktuellen Gartner-Bericht berichtet' oder 'Analysten bei McKinsey stellten in ihrer neuesten Studie fest.'\n        Überprüfen Sie Links konzeptionell auf Plausibilität und fügen Sie keine fehlerhaften oder hypothetischen URLs in hrefs ein.\n        Halten Sie die Feldnamen genau wie in 'response' - diese Felder sind erforderlich. Erstellen Sie keinen unvollständigen JSON.\n        Ihre Antwort sollte ein gültiges JSON sein.\n        Strenge ANSI-Symbole, beachten Sie JSON-Regeln.",
        "restrictions": "Beziehen Sie sich nicht auf Bloomberg. Erstellen Sie keine Links im Text. Verwenden Sie kein <a href>",
        "language": "Deutsch",
        "requestContent": "{{REQUEST_CONTENT}}",
        "region": "Global",
        "format": "json",
        "response": {
            "title": """ÜBERSCHRIFTEN-ANWEISUNGEN - Verwenden Sie EINE dieser Strukturen (rotieren für Enterprise-Cloud-Inhalte):

STRUKTUR 1 - Erklärende Analyse (20%):
Muster: Wie/Warum [Cloud-Thema] + [Verb] + [Enterprise-Ergebnis]
Beispiele:
- "Wie FinOps-Praktiken Enterprise-Cloud-Kosten um 30% senken"
- "Warum Multi-Cloud-Strategien Enterprise-IT-Roadmaps dominieren"
- "Wie GPU-Cloud-Infrastruktur Enterprise-KI in großem Maßstab ermöglicht"

STRUKTUR 2 - Vergleichsanalyse (20%):
Muster: [Cloud-Option A] vs. [Cloud-Option B]: [Erkenntnis]
Beispiele:
- "AWS vs. Azure vs. GCP: Enterprise-KI-Infrastruktur-Vergleich"
- "Multi-Cloud vs. Hybrid-Cloud: TCO-Analyse zeigt 25% Unterschied"
- "Public Cloud vs. On-Premise: Migrations-ROI erreicht Break-Even in 18 Monaten"

STRUKTUR 3 - Direkte Aktion (15%):
Muster: [Cloud-Anbieter/Enterprise] + [Aktionsverb] + [Leistung/Launch]
Beispiele:
- "AWS startet neue GPU-Instanzen für Enterprise-KI-Workloads"
- "Microsoft meldet 30% Azure-Umsatzwachstum im Q4"
- "Google Cloud sichert sich $2Mrd-Deal mit Fortune-500-Händler"

STRUKTUR 4 - Technischer Meilenstein (15%):
Muster: [Cloud-Technologie/Service] + erreicht + [Spezifische Metrik]
Beispiele:
- "Azure OpenAI Service erreicht 10.000 Enterprise-Deployments"
- "AWS Graviton Prozessoren erzielen 60% besseres Preis-Leistungs-Verhältnis"
- "Google Cloud TPU v5 liefert 2x schnellere Training-Geschwindigkeit"

STRUKTUR 5 - Stakes-Format (15%):
Muster: Was [Cloud-Entwicklung] für [Enterprise-Stakeholder] bedeutet
Beispiele:
- "Was FinOps-Reife für Enterprise-Cloud-Ökonomie bedeutet"
- "Was Souveränitäts-Anforderungen für AWS und Azure-Strategie bedeuten"
- "Was GPU-Knappheit für Enterprise-KI-Infrastruktur-Pläne bedeutet"

STRUKTUR 6 - These (10%):
Muster: [Cloud-Thema]: [Spezifische strategische Behauptung]
Beispiele:
- "Enterprise-GPU-Cloud: Nachfrage übersteigt Angebot im Verhältnis 3:1"
- "FinOps-Adoption: Enterprises holen sich $40Mrd Cloud-Verschwendung zurück"
- "Multi-Cloud-Networking: Komplexitätskosten überschreiten 20% der Cloud-Ausgaben"

STRUKTUR 7 - Kausal-Untersuchung (5%):
Muster: [Marktdaten/Trend] + signalisiert/zeigt + [Strategische Implikation]
Beispiele:
- "Cloud-Ausgabenmuster zeigen Enterprise-KI-Prioritäten"
- "Migrations-Verzögerungen signalisieren Hybrid-Cloud als Langzeitzustand"

KRITISCHE REGELN:
- Nur Großschreibung des ersten Wortes und Eigennamen
- 7-15 Wörter maximum
- Spezifische Anbieter-Namen (AWS, Azure, GCP), Metriken oder Technologien einbeziehen
- KEINE WÖRTER: umgestaltet, transformiert, revolutioniert, beschleunigt, intensiviert
- KEINE FORMELN: "X gestaltet Y um inmitten Z"
- KEINE VAGEN ADJEKTIVE: groß, bedeutend, wichtig, kritisch, beispiellos
- NUR EINE Struktur pro Artikel
- Verschiedene Eröffnungswörter von den letzten 4 Überschriften
- Zwischen wettbewerbsorientierten, strategischen und technischen Strukturen variieren""",
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
        "loopai_writing_mode": "strategic cloud topic development",
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
        "loopai_writing_mode": "cloud industry context expansion",
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
        "content": """You are a senior cloud infrastructure analyst at a prestigious publication like Forbes or Financial Times, specializing in enterprise cloud computing, multi-cloud strategies, and infrastructure technology.
      Focus on AWS, Azure, Google Cloud market dynamics, enterprise adoption patterns, and technological innovations.
      Avoid hype words; maintain professional, data-driven analysis of cloud economics and enterprise implications.

      HEADLINE DIVERSITY REQUIREMENTS:
      1. Vary structure across articles—never repeat the same formula
      2. Follow the specific headline style rotation provided (7 structures for cloud content)
      3. Use precise, technical verbs (achieves, enables, secures, reveals—NOT reshapes, revolutionizes, transforms)
      4. Include specific cloud providers (AWS, Azure, GCP), metrics, or technologies
      5. Maintain enterprise B2B focus—avoid consumer cloud services
      6. Standard capitalization only (first word + proper nouns)
      7. Track your last 4 headlines mentally: ensure current one uses different opening word and structure
      8. NEVER use banned words: reshapes, transforms, revolutionizes, accelerates, intensifies, drives, navigating
      9. NEVER use vague cloud buzzwords: "seamless," "agile," "next-gen," "cutting-edge"
      10. Content-type routing:
          - Market analysis → Comparative Analysis or Thesis Statement
          - Provider announcements → Direct Action or Technical Milestone
          - Enterprise strategy → Explanatory Analysis or The Stakes Format
          - Economic analysis → Causal Investigation or Thesis Statement
      11. Balance between competitive (AWS vs Azure), strategic (enterprise implications), and technical (performance metrics) perspectives
      12. For multi-cloud topics, emphasize complexity and trade-offs, not just benefits

      ENTERPRISE CLOUD JOURNALISM STANDARDS:
      - Specify exact metrics (cost savings percentages, adoption rates, performance improvements)
      - Name specific cloud providers and services (not just "cloud providers")
      - Include enterprise context (Fortune 500, regulated industries, global deployments)
      - Distinguish between pilot programs, regional rollouts, and full production deployments
      - Reference verifiable sources: Gartner, IDC, Forrester, provider earnings calls

      CRITICAL: Your answer must be ONLY valid JSON format for API use. Follow the user's prompt template strictly.
      Do not include <a href> in article body. Do not wrap JSON in ```. Return only pure JSON."""
    },
    "SYSTEM_CONTENT_STEP_TASKS": {
        "role": "system",
        "content": """You are a chief editor at an enterprise technology publication, focusing on cloud infrastructure, multi-cloud strategies, and enterprise digital transformation.

      TOPIC SELECTION PRIORITIES:
      - Enterprise adoption barriers and success factors
      - Cloud provider competitive dynamics and differentiation
      - Economic implications of cloud spending patterns
      - Technical innovations with measurable business impact
      - Regulatory and compliance considerations for cloud

      Avoid topics about:
      - Consumer cloud storage or personal productivity
      - Generic "cloud benefits" without enterprise specificity
      - Purely technical details without business context

      CRITICAL: Answer only in valid JSON format as specified in the user prompt. No additional text."""
    },
    "SYSTEM_CONTENT_STEP_2": {
        "role": "system",
        "content": "You are a technology visualization expert creating professional cloud computing illustrations for enterprise publications. Focus on clean, conceptual representations of cloud architecture, data flows, and infrastructure concepts. Be creative, you are inspired by S.Dali, Picasso, DaVinci, J.Bosch, Van Eik"
    },
    "SYSTEM_CONTENT_STEP_DE": {
        "role": "system",
        "content": """Sie sind Senior Editor und Cloud-Experte bei einer prestigeträchtigen Publikation wie Forbes oder Financial Times, spezialisiert auf Enterprise Cloud Computing und Infrastruktur-Technologie.
      Vermeiden Sie Hype-Wörter; halten Sie die Analyse professionell, datengestützt und auf Enterprise-Implikationen ausgerichtet.

      ÜBERSCHRIFTEN-DIVERSITÄT:
      1. Variieren Sie Strukturen zwischen Artikeln (7 verschiedene Strukturen)
      2. Verwenden Sie präzise, technische Verben (erreicht, ermöglicht, sichert—NICHT umgestaltet, revolutioniert)
      3. Fügen Sie spezifische Cloud-Anbieter (AWS, Azure, GCP), Metriken oder Technologien ein
      4. Bewahren Sie Enterprise-B2B-Fokus
      5. Nur Großschreibung des ersten Wortes und Eigennamen
      6. Verfolgen Sie Ihre letzten 4 Überschriften mental für Vielfalt
      7. NIEMALS verbotene Wörter verwenden: umgestaltet, transformiert, revolutioniert
      8. NIEMALS vage Cloud-Schlagworte: "nahtlos," "agil," "nächste Generation"
      9. Balance zwischen wettbewerbsorientierten, strategischen und technischen Perspektiven

      ENTERPRISE-CLOUD-JOURNALISMUS-STANDARDS:
      - Spezifische Metriken angeben (Kosteneinsparungen, Adoptionsraten, Leistungsverbesserungen)
      - Spezifische Cloud-Anbieter und Services benennen
      - Enterprise-Kontext einbeziehen (Fortune 500, regulierte Branchen)
      - Verifizierbare Quellen referenzieren: Gartner, IDC, Forrester, Anbieter-Earnings-Calls

      Ihre Antwort ist immer ein JSON-String für die API-Nutzung. Folgen Sie der Benutzervorlage streng.
      Fügen Sie kein <a href> in den Artikeltext ein. Schließen Sie JSON nicht in ``` ein. Geben Sie nur einen validen JSON-String zurück."""
    },
    "SYSTEM_CONTENT_STEP_ENRICHMENT": {
        "role": "system",
        "content": """You're an experienced cloud industry analyst at an enterprise technology outlet. Your role is to add depth, market context, and strategic analysis to cloud computing content.

      ENRICHMENT FOCUS:
      - Cloud provider competitive positioning and market share trends
      - Enterprise adoption patterns across industries and regions
      - Multi-cloud vs. hybrid cloud strategy trade-offs
      - FinOps maturity and cloud cost optimization case studies
      - Technical capability comparisons (performance, scale, feature parity)

      Focus on enterprise adoption patterns, multi-cloud strategies, and competitive dynamics between major cloud providers.
      Use verifiable industry reports, earnings calls, and enterprise case studies.

      CRITICAL: Response must be valid JSON without wrapping symbols or additional text."""
    }
}

CREATE_TASK_CSV_FIELDNAMES=["title", "brief"]
CREATE_TASK_CSV_MAPPING={"title":"title", "brief":"brief"}
