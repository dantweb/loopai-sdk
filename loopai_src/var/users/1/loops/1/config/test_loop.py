PROMPT_STEP_1_MAX_TOKENS = 50
PROMPT_STEP_2_MAX_TOKENS = 50
PROMPT_STEP_3_MAX_TOKENS = 50
PROMPT_STEP_4_MAX_TOKENS = 50


ARTICLE_EXAMPLE = ""

PROMPT_TEMPLATES = {
    #prompt for the first step defined in the loop yaml
    "PROMPT_STEP_1_JSON": {
        "request": "Write an article about healthy eating. More precise the task is discribed in the field. Text data in your response should be base64 encoded",
        "language": "english",
        "requestContent": "{{REQUEST_CONTENT}}",
        "region": "USA",
        "format": "json",
        "response": {
            "title": "text",
            "summary": "24 words long",
            "tags": "30 coma-separated tags for wordpress",
            "category": "Eat and drink",
            "lead_paragraph": "what solves the problem. not longer than 12 words",
            "article_body": "full article body maximum 200 words",
            "part2": "details to the article body, i.e. some tabled structured data to support the article.",
            "part3": "sources of information for article_body"
        }
    },

    #prompt for second step
    "PROMPT_STEP_2_JSON": "Generate a vibrant realistic image for our blog. Try to be original description: {{DESCRIPTION}}"
}

SYSTEM_CONTENT_TEMPLATES = {
    "SYSTEM_CONTENT_STEP_1": {
        "role": "system",
        "content": "You are chef editor at a blog which focuses on topics such as healthcare and beauty"
    },
    "SYSTEM_CONTENT_STEP_2": {
        "role": "system",
        "content": "You are an image editor and an artist who works as an art director"
    }
}


CREATE_TASK_CSV_FIELDNAMES=['title']
CREATE_TASK_CSV_MAPPING={'title':'headerTitle'}