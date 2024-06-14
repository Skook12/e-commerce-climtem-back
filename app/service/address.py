from datetime import datetime
from psycopg2._psycopg import connection
from app.db import RepoI

class AddressService(RepoI):
    __table = "user_address"

    def __init__(self, db: connection):
        self.__conn = db

    def insert(self, values):
        cursor = self.__conn.cursor()
        try:
            query = f"""
                INSERT INTO {self.__table} (id_user, num, complement, cep, city)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, values)
            self.__conn.commit()
        
        except Exception as e:
            self.__conn.rollback()
            print(f'\n===================\n[Error]({datetime.now()}):{e}\n===================\n')
            return e
        cursor.close()
        return 201
    
    def select(self, search:str):
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
        return [{'id': row[0], 'id_user': row[1], 'num': row[2], 'complement': row[3], 'cep': row[4], 'city': row[5]} for row in results]
    
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
