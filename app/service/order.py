from datetime import datetime
from psycopg2._psycopg import connection
import base64
from app.db import RepoI

class OrderService(RepoI):
    __table = "user_order"

    def __init__(self, db: connection):
        self.__conn = db

    def insert(self, values):
        cursor = self.__conn.cursor()
        try:
            query = f"""
                INSERT INTO {self.__table} (ID_User, buy_date, status, payment_type, expiration, total_bought, track_id, transport_name, estimated_time, freight_value)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING ID_Order
            """
            cursor.execute(query, values)
            inserted_id = cursor.fetchone()[0]
            self.__conn.commit()
        
        except Exception as e:
            self.__conn.rollback()
            print(f'\n===================\n[Error]({datetime.now()}):{e}\n===================\n')
            return e
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
        
        except Exception as e:
            self.__conn.rollback()
            print(f'\n===================\n[Error]({datetime.now()}):{e}\n===================\n')
        
        cursor.close()
        return [{
            'id': row[0],
            'user_id': row[1],
            'buy_date': row[2],
            'status': row[3],
            'payment_type': row[4],
            'expiration': row[5],
            'total_bought': row[6],
            'track_id': row[7],
            'transport_name': row[8],
            'estimated_time': row[9],
            'freight_value': row[10],
            'quantity': row[14],
            'name': row[18],
            'image':  base64.b64encode(open(row[30], "rb").read()).decode('utf-8'),
            'user_name':  row[32],
            'user_email':  row[33],
            'user_cpf':  row[35],
            'user_phone':  row[36],
            'user_num':  row[40],
            'user_complement':  row[41],
            'user_cep':  row[42],
            'user_city':  row[43],
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
        return value

class ShoppingCarService(RepoI):
    __table = "products_order"

    def __init__(self, db: connection):
        self.__conn = db

    def insert(self, values):
        cursor = self.__conn.cursor()
        try:
            query = f"""
                INSERT INTO {self.__table} (ID_Order, ID_Product, quantity)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, values)
            self.__conn.commit()
        
        except Exception as e:
            self.__conn.rollback()
            print(f'\n===================\n[Error]({datetime.now()}):{e}\n===================\n')
            return e
        cursor.close()
        return 201
    
    def select(self, search:str=None):
        """param: 
            - search: search query complement

            SELECT * FROM Table WHERE (Complement);
        """
        cursor = self.__conn.cursor()
        query = f"SELECT * FROM {self.__table};"

        if search != None:
            query = f"SELECT * FROM {self.__table} WHERE {search};"

        try:
            cursor.execute(query)
            results = cursor.fetchall()
        
        except Exception as e:
            self.__conn.rollback()
            print(f'\n===================\n[Error]({datetime.now()}):{e}\n===================\n')
        
        cursor.close()
        return [{'id': row[0], 'user_id': row[1], 'buy_date': row[2], 'status': row[3]} for row in results]
    
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
