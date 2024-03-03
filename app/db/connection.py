import psycopg2

def getConnection(config: dict):
    '''
    Starts a connection with postgresql\n
    Parameters:\n
    - config: Postgres's configuration, the main attributes are db, user, password, host and port;
    '''
    conn = psycopg2.connect(
        dbname=config['db'],
        user=config['user'],
        password=config['pass'],
        host = config.get('host', 'localhost'),
        port = config.get('port', '5432')
    )

    return conn