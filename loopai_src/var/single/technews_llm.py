PROMPT_STEP_1_MAX_TOKENS = 50
PROMPT_STEP_2_MAX_TOKENS = 50
PROMPT_STEP_3_MAX_TOKENS = 50
PROMPT_STEP_4_MAX_TOKENS = 50

ARTICLE_EXAMPLE = ""

PROMPT_TEMPLATES = {
    #prompt for the first step defined in the loop yaml
    "PROMPT_STEP_1_JSON": {
        "request":"Write an article about the topic, described in the field 'requestContent' in this json. Keep filed names strictlyas in 'REPSONSE'. Always use artilce_body and lead_paragraph with the underscors symbol. Do not create unfinished json. Your response should be a valid JSON maximum 300 tokens. Strict ANSI symbols, respect json rules.",
        "language":"english",
        "requestContent":"{{REQUEST_CONTENT}}",
        "region":"USA",
        "format":"json",
        "REPSONSE":{
            "TITLE": "text",
            "SUMMARY": "short summary of the article 10 words",
            "TAGS": "5 coma-separated tags for wordpress",
            "CATEGORY": "<gpt: put here category on your choice>",
            "LEAD_PARAGRAPH": "not longer than 10 words",
            "ARTICLE_BODY": "full article body maximum 300 words"
        }
    },

    #prompt for second step
    "PROMPT_STEP_2_JSON": "Generate a vibrant realistic image for our blog. This is the description: {{DESCRIPTION}}",
    
    "PROMPT_STEP_TASKS_JSON": {
      "request":"""Based on the list of headers in the field 'requestContent' in the current JSON create a response.
       Generate only three topics for the blog, which cover the main trends and most important, and put htem in the field 'response' as text to be saved as list of dicts [{"title":"value", "brief":"value"}, {"title":"value2", "brief":"value2"}]in strict json format.
       ---> important! do not keep requestContent in your response. !!!!!DO NOT ESCAPE "-SYMBOLS!!!!!. Do not put into quotes lists and dicts in json. Send me only json with the field response which contains the list of the tasks as text which will be parsed as CSV """,
      "response":"",
      "requestContent":"{{REQUEST_CONTENT}}",
    },
    "TECH_NEWS_SOURCES_1": {'fin'}
}

SYSTEM_CONTENT_TEMPLATES = {
    "SYSTEM_CONTENT_STEP_1": {
        "role": "system",
        "content": "You are chef editor at a blog about finances and hi-tech."
    },
    "SYSTEM_CONTENT_STEP_TASKS": {
        "role": "system",
        "content": "You are chef editor at a blog about finances and hi-tech."
    },
    "SYSTEM_CONTENT_STEP_2": {
        "role": "system",
        "content": "You are an image editor and an artist who works as an art director"
    },
    "TECH_NEWS_SOURCES_S":['crypto_gpt']
}

CREATE_TASK_CSV_FIELDNAMES=['title', 'brief']
CREATE_TASK_CSV_MAPPING={'title':'title', 'brief':'brief'}

TECH_NEWS_SOURCES_S=['crypto_gpt']