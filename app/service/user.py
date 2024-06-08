from datetime import datetime
from psycopg2._psycopg import connection
from app.db import RepoI

class UserService(RepoI):
    __table = "usertable"

    def __init__(self, db: connection):
        self.__conn = db

    def insert(self, values):
        cursor = self.__conn.cursor()
        try:
            query = f"""
                INSERT INTO {self.__table} (name, email, password, cpf, phone, adm)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING ID_User
            """
            cursor.execute(query, values)
            inserted_id = cursor.fetchone()[0]
            self.__conn.commit()
        except Exception as e:
            self.__conn.rollback()
            raise e
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
        if search != None and search.find('User_Address') != -1:
            r = [{
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'cpf': f'{row[4][:3]}.{row[4][3:6]}.{row[4][6:9]}-{row[4][9:]}',
                'phone': f'({str(row[5])[:2]}) {str(row[5])[2:3]} {str(row[5])[3:7]}-{str(row[5])[7:]}',
                'num': row[9],
                'complement': row[10],
                'cep': f'{row[11][:5]}-{row[11][5:]}',
                'city': row[12]
            } for row in results]
        else:
            r = [{'id': row[0], 'name': row[1], 'email': row[2], 'phone': row[5], 'adm': row[6]} for row in results]
        return r if len(results) != 0 else None 
    
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
