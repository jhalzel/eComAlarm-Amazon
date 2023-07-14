import os
from dotenv import load_dotenv

load_dotenv()

REFRESH_TOKEN = os.getenv('SP_API_REFRESH_TOKEN')   
LWA_APP_ID = os.getenv('LWA_APP_ID')
LWA_CLIENT_SECRET = os.getenv('LWA_CLIENT_SECRET')
SP_API_ACCESS_KEY = os.getenv('SP_API_ACCESS_KEY')
SP_API_SECRET_KEY = os.getenv('SP_API_SECRET_KEY')
SP_API_ROLE_ARN = os.getenv('SP_API_ROLE_ARN')
