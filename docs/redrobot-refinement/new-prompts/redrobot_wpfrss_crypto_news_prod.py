PROMPT_TEMPLATES = {
    "PROMPT_STEP_1_JSON": {
        "loopai_project_id": "RedRobot",
        "loopai_project_description": "Cryptocurrency markets and digital asset analysis",
        "writing_mode": "analytical crypto market intelligence",
        "request": "Write an analytical article on the cryptocurrency topic described in 'requestContent'. Focus on market dynamics, regulatory developments, and technological innovations in blockchain and digital assets. Use real facts from credible sources like industry reports, official announcements, or reputable publications. Incorporate quotations from experts, executives, or analysts, specifying their names, affiliations, and context.\n        When citing announcements, specify exactly who (e.g., company CEO, project founder, or regulatory official), where (e.g., press release, court filing, conference), and include verifiable details. Add exact dates only if known and relevant, in format DD Month YYYY. Do not invent dates, events, or URLs.\n        Do not refer to non-existent sources. Explicitly reference information sources: e.g., 'according to a CoinGecko report,' 'as stated in the SEC filing,' or 'Binance announced in their quarterly update.'\n        Check conceptual plausibility of any market claims or technical assertions. Consider current date for timeliness and relevance to crypto market cycles.\n        Focus on Bitcoin, Ethereum, DeFi protocols, NFT markets, regulatory developments, and institutional adoption trends.\n        Maintain objective, professional tone akin to Forbes or Financial Times: balanced, insightful, data-driven. Include quantitative data, market statistics, and on-chain metrics.\n        CRITICAL: Return ONLY valid JSON format with no additional text, markdown, or explanations. Ensure all strings are properly quoted.",
        "restrictions": "1. No invented sources or events 2. Maintain professional market analysis tone 3. Avoid price speculation and investment advice 4. Return ONLY JSON format",
        "special_instructions": "For cryptocurrency articles, add analytical context about:\n        - Market structure and institutional adoption patterns\n        - Regulatory developments and policy implications\n        - Technological innovations and protocol upgrades\n        - On-chain metrics and network activity analysis\n        Structure with professional crypto market sections using <h3> tags",
        "language": "professional business English",
        "requestContent": "{{REQUEST_CONTENT}}",
        "region": "Global",
        "format": "json",
        "json_structure": {
            "title": "string: Professional headline - see detailed instructions below",
            "summary": "string: 25-35 word executive summary highlighting market implications",
            "tags": "string: 6-8 crypto industry tags (Bitcoin, DeFi, Regulation, etc)",
            "category": "Crypto, News",
            "lead_paragraph": "string: Context-setting opening with market or regulatory context",
            "illustration": "Professional visualization - be creative, make specifications for interesting and glossy surrealstic image which will be created by another AI. You are inspired by modern arts",
            "article_body": "string: Sophisticated analysis with market focus, using HTML tags for structure"
        },
        "response": {
            "title": """HEADLINE INSTRUCTIONS - Use ONE of these structures (rotate across articles):

STRUCTURE 1 - Direct Action News (40% usage):
Pattern: [Company/Entity] + [Action Verb] + [Object/Amount]
Examples:
- "Binance reports $2.4B in institutional BTC inflows during Q4"
- "Ethereum Foundation announces Pectra upgrade timeline"
- "BlackRock files for tokenized treasury ETF with SEC"

STRUCTURE 2 - Impact-First News (30% usage):
Pattern: [Effect/Outcome] + as/after + [Cause/Event]
Examples:
- "Bitcoin ETF outflows hit $800M as Fed signals rate pause"
- "DeFi TVL surges 40% following Ethereum gas fee reduction"
- "Crypto exchanges face scrutiny after cross-border compliance gap"

STRUCTURE 3 - Causal Investigation (20% usage):
Pattern: [Data/Event] + signals/reveals/shows + [Deeper Trend]
Examples:
- "ETF flow reversals reveal institutional de-risking in volatile markets"
- "On-chain metrics signal whale accumulation near support levels"
- "Regulatory filings expose institutional custody demand surge"

STRUCTURE 4 - By-The-Numbers (10% usage):
Pattern: [Specific Metric] + [Context]
Examples:
- "Bitcoin mining difficulty reaches all-time high of 73.2T"
- "Ethereum gas fees drop 85% post-Dencun upgrade"
- "Stablecoin market cap crosses $180B milestone"

CRITICAL RULES:
- Use standard capitalization (only first word and proper nouns)
- 7-13 words maximum
- Include specific numbers, protocol names, or entities
- NO WORDS: reshapes, transforms, revolutionizes, accelerates, intensifies, drives
- NO FORMULAS: "X Reshapes Y Amid Z" or "X: Driving Y and Z"
- NO VAGUE ADJECTIVES: major, significant, key, critical, unprecedented
- Choose ONLY ONE structure per article
- Vary structure from previous articles""",
            "summary": "25-35 word executive summary highlighting market implications",
            "tags": "6-8 crypto industry tags separated by commas",
            "category": "Crypto, News",
            "lead_paragraph": "Context-setting opening with market or regulatory context",
            "illustration": "Professional visualization - be creative, make specifications for interesting and glossy surrealstic image which will be created by another AI. You are inspired by modern arts",
            "article_body": "Sophisticated analysis with market focus, using HTML tags for structure"
        }
    },

    "PROMPT_STEP_DE_JSON": {
        "loopai_project_id": "RedRobot",
        "loopai_project_description": "Kryptowährungsmärkte und digitale Asset-Analyse",
        "writing_mode": "analytische Krypto-Marktanalyse",
        "request": "Übersetzen Sie den 'requestContent' in diesem JSON. Verwenden Sie echte Fakten aus seriösen Quellen wie Branchenberichten, offiziellen Ankündigungen oder angesehenen Veröffentlichungen.\n        Wenn Sie schreiben, dass jemand etwas angekündigt hat, geben Sie genau an, wer (z.B. Projektgründer, Firmen-CEO oder Regulierungsbeamter), wo (z.B. in einer Pressemitteilung, Gerichtsakte oder Konferenz) und fügen Sie überprüfbare Details hinzu. Erfinden Sie keine URLs. Beziehen Sie sich nicht auf Quellen, die nicht existieren.\n        Beziehen Sie sich explizit auf die Herkunft der Informationen: z.B. 'laut einer Pressemitteilung von Company X', 'wie in einem aktuellen CoinGecko-Bericht berichtet' oder 'Analysten bei Messari stellten in ihrer neuesten Studie fest.'\n        Überprüfen Sie Links konzeptionell auf Plausibilität und fügen Sie keine fehlerhaften oder hypothetischen URLs in hrefs ein.\n        Halten Sie die Feldnamen genau wie in 'response' - diese Felder sind erforderlich. Erstellen Sie keinen unvollständigen JSON.\n        Ihre Antwort sollte ein gültiges JSON sein.\n        Strenge ANSI-Symbole, beachten Sie JSON-Regeln.",
        "restrictions": "Beziehen Sie sich nicht auf Bloomberg. Erstellen Sie keine Links im Text. Verwenden Sie kein <a href>",
        "language": "Deutsch",
        "requestContent": "{{REQUEST_CONTENT}}",
        "region": "Global",
        "format": "json",
        "response": {
            "title": """ÜBERSCHRIFTEN-ANWEISUNGEN - Verwenden Sie EINE dieser Strukturen (rotieren Sie zwischen Artikeln):

STRUKTUR 1 - Direkte Aktion (40%):
Muster: [Unternehmen/Entität] + [Aktionsverb] + [Objekt/Betrag]
Beispiele:
- "Binance meldet $2,4Mrd institutionelle BTC-Zuflüsse im Q4"
- "Ethereum Foundation kündigt Pectra-Upgrade-Zeitplan an"

STRUKTUR 2 - Impact-First (30%):
Muster: [Effekt/Ergebnis] + nach/als + [Ursache/Ereignis]
Beispiele:
- "Bitcoin-ETF-Abflüsse erreichen $800M nach Fed-Zinspause-Signal"
- "DeFi-TVL steigt um 40% nach Ethereum-Gasgebühren-Senkung"

STRUKTUR 3 - Kausal-Untersuchung (20%):
Muster: [Daten/Ereignis] + signalisiert/zeigt + [Tieferer Trend]
Beispiele:
- "ETF-Fluss-Umkehrungen zeigen institutionelles De-Risking"
- "On-Chain-Metriken signalisieren Wal-Akkumulation"

STRUKTUR 4 - Nach Zahlen (10%):
Muster: [Spezifische Metrik] + [Kontext]
Beispiele:
- "Bitcoin-Mining-Schwierigkeit erreicht Allzeithoch von 73,2T"
- "Ethereum-Gasgebühren fallen um 85% nach Dencun-Upgrade"

KRITISCHE REGELN:
- Nur Großschreibung des ersten Wortes und Eigennamen
- 7-13 Wörter maximum
- Spezifische Zahlen, Protokollnamen oder Entitäten einbeziehen
- KEINE WÖRTER: umgestaltet, transformiert, revolutioniert, beschleunigt, intensiviert
- KEINE FORMELN: "X gestaltet Y um inmitten Z"
- KEINE VAGEN ADJEKTIVE: groß, bedeutend, wichtig, kritisch
- NUR EINE Struktur pro Artikel wählen
- Struktur von vorherigen Artikeln variieren""",
            "summary": "Kurzfassung des Artikels 20-30 Wörter",
            "tags": "8 durch Kommas getrennte Tags für WordPress",
            "category": "Crypto, News",
            "lead_paragraph": "nicht länger als 50 Wörter. Der Lead-Paragraph sollte nicht die Zusammenfassung kopieren. Er sollte andere Wörter enthalten und mit Details und Fakten interessanter sein",
            "illustration": "Hier die Aufgabenbeschreibung für einen KI-gestützten Bildgenerator einfügen",
            "article_body": "Vollständiger Artikeltext mindestens 2000 Wörter. Strukturieren Sie professionell: verwenden Sie <h3> Unterüberschriften für Abschnitte (3-5 insgesamt), <p> für Absätze, <strong> oder <em> sparsam für Hervorhebungen. Fügen Sie Datenpunkte, Zitate und Analysen ein. Sicherstellen Sie einen logischen Fluss: Einleitung, Hauptteil mit Beweisen, Schlussfolgerung mit Implikationen.\n          Verwenden Sie keine Umbrüche mit Escape-Symbolen. Teilen Sie den Text in kleinere Fragmente auf und verwenden Sie Unterüberschriften h3. Bitte verwenden Sie HTML-Tags!!!\n          Verwenden Sie HTML, um Wichtiges hervorzuheben oder Unterüberschriften zu erstellen, aber nicht mehr als 3-4. Erstellen Sie Absätze zwischen den Absätzen"
        }
    },
    "PROMPT_STEP_GENERATE_IMG": {
        "request": "Create a professional illustration for cryptocurrency blog content based on the description in 'requestContent'.\n      Style: Modern blockchain and financial technology aesthetic with clean lines, cryptocurrency symbols, and market data visualization. Suitable for Forbes or FT-style publications: conceptual, professional, and finance-focused.",
        "requestContent": "{{REQUEST_CONTENT}}"
    },
    "PROMPT_STEP_TASKS_JSON": {
        "loopai_project_id": "RedRobot",
        "loopai_project_description": "Cryptocurrency markets and digital asset analysis",
        "writing_mode": "strategic crypto topic development",
        "request": "Based on cryptocurrency content in 'requestContent', select 3 most important, insightful topics for in-depth articles exploring:\n       - Bitcoin and Ethereum market dynamics and protocol developments\n       - DeFi ecosystem growth and institutional adoption\n       - NFT markets and digital collectibles evolution\n       - Regulatory developments and policy implications\n       - Layer 2 solutions and blockchain scalability\n       - Stablecoin markets and payment infrastructure\n       Focus on subjects with broad market impact and technological significance.\n       Ensure topics are current and relevant to crypto market cycles.\n       Provide detailed analytical frameworks for each topic with emphasis on:\n       - Market structure and institutional flow analysis\n       - Regulatory impact assessment and compliance trends\n       - Technological innovation and protocol competition\n       - Economic implications and market sentiment analysis\n       CRITICAL: Return ONLY valid JSON format. No additional text or explanations.",
        "json_structure": [{
            "title": "string: Professional cryptocurrency topic title",
            "brief": "string: 400-600 word analytical framework with market focus"
        }],
        "requestContent": "{{REQUEST_CONTENT}}"
    },
    "PROMPT_STEP_ENRICHMENT_JSON": {
        "loopai_project_id": "RedRobot",
        "loopai_project_description": "Cryptocurrency market analysis enhancement",
        "writing_mode": "crypto market context expansion",
        "request": "Enhance cryptocurrency content using market research methods:\n        \n        1. Market structure analysis and institutional adoption patterns\n        2. Regulatory developments and policy impact assessment\n        3. On-chain metrics and network activity analysis\n        4. Protocol competition and technological innovation assessment\n        \n        Professional Standards:\n        - Multiple source verification from industry reports\n        - Market data and on-chain metric integration\n        - Regulatory framework analysis\n        - Institutional adoption trend assessment\n        \n        CRITICAL: Return ONLY valid JSON format. No additional text or markdown.",
        "language": "professional business English",
        "requestContent": "{{REQUEST_CONTENT}}",
        "json_structure": {
            "original_brief": "string: The original cryptocurrency content",
            "enriched_brief": "string: Market-focused analysis with strategic crypto context",
            "market_analysis": "string: Market structure, institutional flows, and regulatory landscape",
            "strategic_implications": "string: Market impact and adoption trajectory analysis"
        },
        "response": {
            "original_brief": "{{REQUEST_CONTENT}}",
            "enriched_brief": "Market-focused analysis with strategic crypto context",
            "market_analysis": "Market structure, institutional flows, and regulatory landscape",
            "strategic_implications": "Market impact and adoption trajectory analysis"
        }
    }
}

SYSTEM_CONTENT_TEMPLATES = {
    "SYSTEM_CONTENT_STEP_1": {
        "role": "system",
        "content": """You are a senior cryptocurrency analyst at a prestigious publication like Forbes or Financial Times, specializing in digital assets, blockchain technology, and crypto markets.
      Focus on Bitcoin, Ethereum, DeFi protocols, NFT markets, regulatory developments, and institutional adoption patterns.
      Avoid hype words and price speculation; maintain professional, data-driven analysis of market structure and technological developments.

      HEADLINE DIVERSITY REQUIREMENTS:
      1. Vary structure across articles—never repeat the same formula
      2. Follow the specific headline style rotation provided in the user prompt
      3. Use active, specific verbs (announces, reports, launches, reaches—NOT reshapes, drives, transforms)
      4. Include concrete numbers, protocol names, or entities
      5. Keep factual and direct—avoid interpretive buzzwords
      6. Standard capitalization only (first word + proper nouns)
      7. If you catch yourself writing "X Reshapes Y" or "X: Driving Y", stop and rewrite with a different structure
      8. Track your last 3 headlines mentally and ensure current one uses different opening words and structure

      CRITICAL: Your answer must be ONLY valid JSON format for API use. Follow the user's prompt template strictly.
      Do not include <a href> in article body. Do not wrap JSON in ```. Return only pure JSON."""
    },
    "SYSTEM_CONTENT_STEP_TASKS": {
        "role": "system",
        "content": "You are a chief editor at a cryptocurrency and digital assets publication, focusing on market structure, regulatory developments, and blockchain innovation.\n      CRITICAL: Answer only in valid JSON format as specified in the user prompt. No additional text."
    },
    "SYSTEM_CONTENT_STEP_2": {
        "role": "system",
        "content": "You are an art director at a fintech glossy online magazine. Focus on surrealistic, conceptual representations - the colors are from classical paintings of impressionists"
    },
    "SYSTEM_CONTENT_STEP_DE": {
        "role": "system",
        "content": """Sie sind Senior Editor und Krypto-Experte bei einer prestigeträchtigen Publikation wie Forbes oder Financial Times, spezialisiert auf digitale Assets, Blockchain-Technologie und Kryptomärkte.
      Vermeiden Sie Hype-Wörter und Preisspekulation; halten Sie die Analyse professionell, datengestützt und auf Marktstruktur ausgerichtet.

      ÜBERSCHRIFTEN-DIVERSITÄT:
      1. Variieren Sie Strukturen zwischen Artikeln
      2. Folgen Sie der bereitgestellten Rotationsanweisung
      3. Verwenden Sie spezifische Verben (kündigt an, meldet, startet—NICHT umgestaltet, treibt an)
      4. Fügen Sie konkrete Zahlen und Namen ein
      5. Vermeiden Sie interpretative Schlagworte
      6. Nur Großschreibung des ersten Wortes und Eigennamen

      Ihre Antwort ist immer ein JSON-String für die API-Nutzung. Folgen Sie der Benutzervorlage streng.
      Fügen Sie kein <a href> in den Artikeltext ein. Schließen Sie JSON nicht in ``` ein. Geben Sie nur einen validen JSON-String zurück."""
    },
    "SYSTEM_CONTENT_STEP_ENRICHMENT": {
        "role": "system",
        "content": "You're an experienced cryptocurrency market analyst at a financial technology outlet. Your role is to add depth, market context, and strategic analysis to crypto content.\n      Focus on market structure, institutional adoption patterns, regulatory developments, and on-chain metrics analysis.\n      CRITICAL: Response must be valid JSON without wrapping symbols or additional text."
    }
}


CREATE_TASK_CSV_FIELDNAMES = ["title", "brief"]
CREATE_TASK_CSV_MAPPING = {"title": "title", "brief": "brief"}
