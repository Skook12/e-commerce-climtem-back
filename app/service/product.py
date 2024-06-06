from datetime import datetime
from psycopg2._psycopg import connection
import base64
from app.db import RepoI

class ProductService(RepoI):
    __table = "product"

    def __init__(self, db: connection):
        self.__conn = db

    def insert(self, values) -> int:
        cursor = self.__conn.cursor()
        try:
            query = f"""
                INSERT INTO {self.__table} (ID_Brand, ID_Category, name, description, value, discount, highl, quantity)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING ID_Product
            """
            cursor.execute(query, values)
            inserted_id = cursor.fetchone()[0]
            self.__conn.commit()
        except Exception as e:
            self.__conn.rollback()
            print(f'\n===================\n[Error]({datetime.now()}):{e}\n===================\n')
            return e, 500
        cursor.close()
        return inserted_id
    
    def select(self, search:str=None):
        """param: 
            - search: search query complement

            SELECT * FROM Table WHERE (Complement);
        """
        cursor = self.__conn.cursor()
        query = f"SELECT * FROM {self.__table};"

        if search != None:
            query = f"SELECT * FROM {self.__table} {search};"

        try:
            cursor.execute(query)
            results = cursor.fetchall()
            if search != None and search.find('image') != -1:
                r = [{
                    'id': row[0],
                    'brand': row[12] if search.find('Brand') != -1 else row[1],
                    'category': row[10] if search.find('Category') != -1 else row[2],
                    'name': row[3],
                    'description': row[4],
                    'value': float(row[5]),
                    'discount': float(row[6]),
                    'higlight': row[7],
                    'quantity': row[8],
                    'path': row[15] if search.find('Category') != -1 else row[11],
                    'image': base64.b64encode(open(row[15] if search.find('Category') != -1 else row[11], "rb").read()).decode('utf-8')
                } for row in results]
            else:
                r = [{
                    'id': row[0],
                    'brand_id': row[1],
                    'category_id': row[2],
                    'name': row[3],
                    'description': row[4],
                    'value': float(row[5]),
                    'discount': float(row[6]),
                    'highlight': row[7]
                } for row in results]
                        
        except Exception as e:
            self.__conn.rollback()
            print(f'\n===================\n[Error]({datetime.now()}):{e}\n===================\n')
        
        cursor.close()
        return r

    def update(self, column, condition, value):
        cursor = self.__conn.cursor()
        try:
            if type(value) == str:
                value = f'\'{value}\''

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

    def delete(self, id):
        cursor = self.__conn.cursor()
        try:
            query = f"""
                DELETE FROM {self.__table} WHERE ID_Product = {id}
            """
            cursor.execute(query)
            self.__conn.commit()
        
        except Exception as e:
            self.__conn.rollback()
            print(f'\n===================\n[Error]({datetime.now()}):{e}\n===================\n')
        
        cursor.close()
