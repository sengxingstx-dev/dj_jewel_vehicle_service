import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set default DJANGO_ENV to 'dev' if not specified in .env
DJANGO_ENV = os.getenv('DJANGO_ENV', 'dev')

if DJANGO_ENV == 'prod':
    from .prod import *
else:
    from .dev import *
