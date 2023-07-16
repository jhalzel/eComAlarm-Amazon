import os
from dotenv import load_dotenv

load_dotenv()

REFRESH_TOKEN = os.environ.get('SP_API_REFRESH_TOKEN')   
LWA_APP_ID = os.environ.get('LWA_APP_ID')
LWA_CLIENT_SECRET = os.environ.get('LWA_CLIENT_SECRET')
SP_API_ACCESS_KEY = os.environ.get('SP_API_ACCESS_KEY')
SP_API_SECRET_KEY = os.environ.get('SP_API_SECRET_KEY')
SP_API_ROLE_ARN = os.environ.get('SP_API_ROLE_ARN')

GMAIL_USERNAME = os.environ.get('GMAIL_USERNAME')
GMAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD')