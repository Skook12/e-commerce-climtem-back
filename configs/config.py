import os
import dotenv

dotenv.load_dotenv()

class Config:
    PSQL_SETTINGS = {
        'db': os.environ['PSQL_DB'],
        'host': os.environ['PSQL_HOST'],
        'port': os.getenv('PSQL_PORT', '5432'),
        'user': os.environ['PSQL_USER'],
        'pass': os.environ['PSQL_PASSWORD'],
    }
