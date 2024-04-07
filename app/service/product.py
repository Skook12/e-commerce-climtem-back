from datetime import datetime
from psycopg2._psycopg import connection
from app.db import RepoI

class ProductService(RepoI):
    __table = "product"

    def __init__(self, db: connection):
        self.__conn = db

    def insert(self, values):
        cursor = self.__conn.cursor()
        try:
            query = f"""
                INSERT INTO {self.__table} (ID_Brand, ID_Category, name, description, value, discount)
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
            query = f"SELECT * FROM {self.__table} WHERE ID_Product = {id};"

        try:
            cursor.execute(query)
            results = cursor.fetchall()
        
        except Exception as e:
            self.__conn.rollback()
            print(f'\n===================\n[Error]({datetime.now()}):{e}\n===================\n')
        
        cursor.close()
        return [
            {
                'id': row[0],
                'brand_id': row[1],
                'category_id': row[2],
                'name': row[3],
                'description': row[4],
                'value': row[5],
                'discount': row[6]
            } for row in results]
    
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
