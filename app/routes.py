from flask import Flask
from .resource import teste
from .db import connection

PREFX_API = '/api/v1/'


def create_server(config):
    '''Starts flask server'''
    app = Flask(__name__)
    app.register_blueprint(teste.get_blueprint(), url_prefix=PREFX_API)
    db = connection.getConnection(config.PSQL_SETTINGS)
    cur = db.cursor()
    # try:
    #     # Define the INSERT INTO statement
    #     sql = """
    #         INSERT INTO Produto (nome_produto, descricao, valor, desconto)
    #         VALUES (%s, %s, %s, %s)
    #     """

    #     # Define the values to be inserted
    #     values = ('Product B', 'Description of Product B', 100.0, 0.1)

    #     # Execute the INSERT INTO statement
    #     cur.execute(sql, values)

    #     # Commit the transaction
    #     db.commit()

    #     print("Data inserted into Produto table successfully!")

    # except psycopg2.Error as e:
    #     # Rollback the transaction in case of error
    #     db.rollback()

    #     print("Error inserting data into Produto table:", e)


    return app 