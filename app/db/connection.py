import psycopg2

def getConnection(config: dict):
    conn = psycopg2.connect(
        dbname=config['db'],
        user=config['user'],
        password=config['pass'],
        host = config.get('host', 'localhost'),
        port = config.get('port', '5432')
    )

    return conn