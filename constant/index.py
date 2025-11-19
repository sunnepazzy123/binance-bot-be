from enum import Enum
import os

from dotenv import load_dotenv
# Load env file
load_dotenv()

# Define an Enum
class Role(Enum):
    CUSTOMER = 1
    ACCOUNT_MANAGER = 2
    ADMIN = 3
    SUPER_ADMIN = 4
    
    
    
# Get environment variables (no defaults)
DB_NAME = os.environ["DB_NAME"] or None
DB_USER = os.environ["DB_USER"] or None
DB_PASSWORD = os.environ["DB_PASSWORD"] or None
DB_HOST = os.environ["DB_HOST"] or None
DB_PORT = os.environ["DB_PORT"] or None

SMTP_SERVER = os.environ["SMTP_SERVER"] or None
SMTP_PORT = os.environ["SMTP_PORT"] or None
SMTP_USERNAME = os.environ["SMTP_USERNAME"] or None
SMTP_PASSWORD = os.environ["SMTP_PASSWORD"] or None