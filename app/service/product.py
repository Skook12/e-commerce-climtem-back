from datetime import datetime
from psycopg2._psycopg import connection
from app.db import RepoI

class ProductService(RepoI):
    __table = "produto"

    def __init__(self, db: connection):
        self.__conn = db

    def insert(self, values):
        cursor = self.__conn.cursor()
        try:
            query = f"""
                INSERT INTO {self.__table} (nome_produto, ID_Marca, ID_Categoria, descricao, valor, desconto)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, values)
            self.__conn.commit()
        
        except Exception as e:
            self.__conn.rollback()
            print(f'\n===================\n[Error]({datetime.now()}):{e}\n===================\n')
            return e
        cursor.close()
        return 201
    
    def select(self, id=None):
        cursor = self.__conn.cursor()
        query = f"SELECT * FROM {self.__table};"

        if id != None:
            query = f"SELECT * FROM {self.__table} WHERE ID_Produto = {id};"

        try:
            cursor.execute(query)
            results = cursor.fetchall()
        
        except Exception as e:
            self.__conn.rollback()
            print(f'\n===================\n[Error]({datetime.now()}):{e}\n===================\n')
        
        cursor.close()
        return results
    
    def update(self, column, condition, value):
        cursor = self.__conn.cursor()
        try:
            query = f"""
                UPDATE {self.__table}
                SET {column} = {value}
                WHERE {condition};
            """
            cursor.execute(query)
            self.__conn.commit()
        
        except Exception as e:
            self.__conn.rollback()
            print(f'\n===================\n[Error]({datetime.now()}):{e}\n===================\n')
        
        cursor.close()
