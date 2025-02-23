# app_global_config.py
import json
import os
import sys
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

POSTGRESQL_DB_HOST = os.getenv('POSTGRESQL_DB_HOST')
POSTGRESQL_DB_NAME = os.getenv('POSTGRESQL_DB_NAME')
POSTGRESQL_DB_PORT = os.getenv('POSTGRESQL_DB_PORT')
POSTGRESQL_DB_USER = os.getenv('POSTGRESQL_DB_USER')
POSTGRESQL_DB_PASSWORD = os.getenv('POSTGRESQL_DB_PASSWORD')

LOOPAI_ROOT = os.getenv('LOOPAI_ROOT')
LOOPAI_SINGLE_FILESYSTEM_PATH = os.getenv('LOOPAI_SINGLE_FILESYSTEM_PATH')
LOOPAI_WEB_USERS_FILESYSTEM_PATH = os.getenv('LOOPAI_WEB_USERS_FILESYSTEM_PATH')

DATABASE_URL = f"postgresql://{POSTGRESQL_DB_USER}:{POSTGRESQL_DB_PASSWORD}@{POSTGRESQL_DB_HOST}:{POSTGRESQL_DB_PORT}/{POSTGRESQL_DB_NAME}"

GLOBAL_USER_ID = ''
GLOBAL_LOOP_ID = ''
WEB_SESSION_ID = ''
GLOBAL_PROJECT_ID = ''

RUNNING_CRON = os.getenv('RUNNING_CRON', False)

# if len(sys.argv) > 0 and sys.argv[0].endswith('.py') and RUNNING_CRON == False:
#     WEB_OR_CLI = 'cli'
# else:
WEB_OR_CLI = os.getenv('WEB_OR_CLI', 'web')

# Constants
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-openai-api-key')
ASSISTANT_1_API_KEY = os.getenv('ASSISTANT_1_API_KEY', 'your-assistant-api-key')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', 'your-google-youtube-api-key')
DALLE_API_URL = "your-dalle-api-url"


######## global functions #######
def is_valid_json(response):
    try:
        json.loads(response)
        return True
    except ValueError:
        return False
    pass
