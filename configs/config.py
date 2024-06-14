import os
import dotenv
import secrets, datetime

dotenv.load_dotenv()

class Config:
    PSQL_SETTINGS = {
        'db': os.environ['PSQL_DB'],
        'host': os.environ['PSQL_HOST'],
        'port': os.getenv('PSQL_PORT', '5432'),
        'user': os.environ['PSQL_USER'],
        'pass': os.environ['PSQL_PASSWORD'],
    }
    JWT_SETTINGS = {
        'SKey': secrets.token_urlsafe(32),
        'Expiretime': datetime.timedelta(minutes=60)
    }
    STMP_SETTINGS = {
        'email': os.environ['CLIMTEM_mail'],
        'p': os.environ['CLIMTEM_pass']
    }
    
    MEV_SETTINGS = os.environ['TOKEN']
    
