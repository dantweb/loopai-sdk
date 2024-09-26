PROMPT_STEP_1_MAX_TOKENS = 50
PROMPT_STEP_2_MAX_TOKENS = 50
PROMPT_STEP_3_MAX_TOKENS = 50
PROMPT_STEP_4_MAX_TOKENS = 50


ARTICLE_EXAMPLE = ""

PROMPT_TEMPLATES = {
    #prompt for the first step defined in the loop yaml
    "PROMPT_STEP_1_JSON": {
        "request": "Write a short articles on the topics described in the field 'requestContent'. Return answer in json as shown in the field 'response'",
        "language": "english",
        "requestContent": "{{REQUEST_CONTENT}}",
        "region": "USA",
        "format": "json",
        "response": {
            "title": "text",
            "summary": "250 chars long text",
            "tags": "30 coma-separated tags for wordpress",
            "category": "Eat and drink",
            "lead_paragraph": "what solves the problem. not longer than 300 symbols",
            "article_body": "full article body minimum 3000 symbols",
            "part2": "Extend the article_body here with some extra facts and references. in the main 'article_body' and give  modern scientific exmplanation in 3-5 sentenses.",
            "part3": "Here goes the recipes with bulleted ingredients and step by step cooking. Use html to make the text nice looking. You can add some css styles, animation and hover effects as well. You may recommend or embed some relevant youtube videos here"
        }
    },

    #prompt for second step
    "PROMPT_STEP_2_JSON": "Generate a vibrant realistic image for our blog. Try to be original"
                          "description: {{DESCRIPTION}}"
}

SYSTEM_CONTENT_TEMPLATES = {
    "SYSTEM_CONTENT_STEP_1": {
        "role": "system",
        "content": "You are chef editor at a blog which focuses on topics such as healthcare and beauty. You have to "
                   "create content and headers. Each header or title should be unique. Your audience are readers "
                   " 18-50 y/o and each article is focused on some segment of age like 18-25 y/o, 25-30, 30-35, 35-40"
    },
    "SYSTEM_CONTENT_STEP_2": {
        "role": "system",
        "content": "You are an image editor and an artist who works as an art director "
                   "at a famous blog about health and beauty and psychologie"
    }
}