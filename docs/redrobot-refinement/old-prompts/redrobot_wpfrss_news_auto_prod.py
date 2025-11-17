
PROMPT_TEMPLATES = {
    # prompt for the first step defined in the loop yaml
    "PROMPT_STEP_1_JSON": {
        "loopai_project_id": "RedRobot",
        "looai_project_descitption": "News and market review for AI, IT and digital industry",
        "writing_mode": "analytical story - summary of the week",

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
        reshaped consumer behavior in China. These innovations laid the foundation for today’s AI-driven personalization and logistics. """,

        "request": """Write or rewrite an anyltical post on the topic, described in the field 'requestContent' in this json based on the content you have read before. 
        Use real facts. Use quotations of other experts. Consider current date and time from the input and keep the content actual to the current date in the main part of the article.
        When you write that someone anounced something, point who, how and where did that.
        Consider currernt date from the input. Keep the article news actual.
        Refer to where the information comes from: pres-release, or announcement, or some other news source writes about, or blog says... 
        Check links and do not put failed urls to hrefs in the text if you cant receive response 200.
        Keep filed names strictly as in 'response' - those fields are required. Do not create unfinished json. 
        Your response should be a valid JSON. 
        Strict ANSI symbols, respect json rules.""",
        "restirctions": "Do note refere Bloomberg. Do not create links in the text. Do not use <a href>",
        "language": "english",
        "requestContent": "{{REQUEST_CONTENT}}",
        "region": "USA",
        "format": "json",
        "response": {
            "title": "title should be a hot news headline. Please use normal standards for headlines capitalisation - only first letter of nouns and verbs and the first letter of the headline",
            "summary": "short summary of the article 20-30 words",
            "tags": "8 coma-separated tags for wordpress",
            "category": "News, E-Auto",
            "lead_paragraph": "not longer than 100 words",
            "illustration": "put here a detailed task descriptioon for the AI-powered illustration generator. Give detailed ideas on color pallete, style, methods and emotions to be shown on the image",
            "article_body": "full article body maximum 3000 words. Do not put breaks with escaped symbols. Cut text into smaller fragments and use subheaders h3. Please use HTML tags!!! Use HTML to highlight important or create subheaders but not more than 3. Create breaks between paragraphs",
        }
    },

    "PROMPT_STEP_DE_JSON": {
        "loopai_project_id": "RedRobot",
        "looai_project_descitption": "News und Marktüberblick für KI, IT und Digitalbranche",
        "writing_mode": "analytical story - summary of the week",
        "request": """Write an anyltical post on the topic, described in the field 'requestContent' in this json. Use real facts. Use quotations of other experts.
        When you write that someone anounced something, point exacly who and where. Do not invent urls. Do not refer to sources which do not exist.
        Refer to where the information comes from: pres-release, or announcement, or some other news source writes about, or blog says... 
        Check links and do not put failed urls to hrefs in the text if you cant receive response 200.
        Keep filed names strictly as in 'response' - those fields are required. Do not create unfinished json. 
        Your response should be a valid JSON. 
        Strict ANSI symbols, respect json rules.""",
        "restirctions": "Do note refere Bloomberg. Do not create links in the text. Do not use <a href>",
        "language": "Deutsch",
        "requestContent": "{{REQUEST_CONTENT}}",
        "region": "Germany",
        "format": "json",
        "response": {
            "title": "Der Titel sollte eine aktuelle Schlagzeile sein. Bitte verwenden Sie die üblichen Groß- und Kleinschreibungsregeln für Schlagzeilen – nur den ersten Buchstaben von Nomen und Verben und den ersten Buchstaben der Schlagzeile.",
            "summary": "short summary of the article 20-30 words",
            "tags": "8 coma-separated tags for wordpress",
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
        "looai_project_descitption": "News and market review for AI, IT and digital industry",
        "writing_mode": "creating list of editorial tasks",
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
        "writing_mode": "research and update of current news",
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
        "content": """You are a author and new editor at a newsagency about hi-tech. 
        Do not use too often word revolution or revolutionise. Keep titles click attractive but professional. Return API-valid pure json string.
        Answer only JSON as required in user prompt. Do not put <a href> tags inside the text"""
    },
    "SYSTEM_CONTENT_STEP_TASKS": {
        "role": "system",
        "content": "You are a chef editor at a blog about finances and hi-tech at Reuters. Answer only JSON as required in user prompt."
    },
    "SYSTEM_CONTENT_STEP_2": {
        "role": "system",
        "content": "You are chef of illustrations and art director at a professional magazine. You paint illustrations for our blog RedRobot. It is about news in IT nd AI"
    },
    "SYSTEM_CONTENT_STEP_WRITER_DE": {
        "role": "system",
        "content": """Sie sind Autor und Chefredakteur eines Blogs mit Fachnachrichten zu KI und E-Commerce.
        Verwenden Sie in den Überschriften nicht das Wort „revolutionierend“. Übertreiben Sie es nicht. Bleiben Sie professioneller. Versuchen Sie, andere Überschriften zu verwenden.
        Ihre Antwort ist immer ein JSON-String und wird von der API weiter verwendet. Folgen Sie der Vorlage in der Benutzereingabeaufforderung.
        Fügen Sie jetzt <a href> in den Artikeltext ein. Schließen Sie den JSON-String nicht in dieses ``` ein. 
        Geben Sie nur JSON-Strings zurück, die so, wie sie sind, JSON-gültig sein können."""
    },

    "SYSTEM_CONTENT_STEP_ENRICHMENT": {
        "role": "system",
        "content": """You're an experienced journalist and market researcher. Your role is to add depth and current relevance to news briefs. 
        Use verifiable recent information (past 7 days) or significant industry reports. 
        Response must be valid JSON without wrapping symbols."""
    }
}

CREATE_TASK_CSV_FIELDNAMES = ['title', 'brief']
CREATE_TASK_CSV_MAPPING = {'title': 'title', 'brief': 'brief'}
