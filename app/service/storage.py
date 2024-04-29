from datetime import datetime
from psycopg2._psycopg import connection
from app.db import RepoI
from werkzeug.datastructures.file_storage import FileStorage
from werkzeug.utils import secure_filename

class StorageService(RepoI):
    __table = "product_image"
    __parentpath = "/app/app/content/"

    def __init__(self, db: connection):
        self.__conn = db

    def loadFile(self, file: FileStorage, path: str = None):
        """Assert file typo and add into filesystem"""

        if file.filename == '':
            return 'No selected file'
        
        if path == None:
            path = ''

        if file.content_type not in ['image/jpeg', 'image/png', 'image/jpg']:
            return f'Invalid Format {file.content_type}'

        filename = secure_filename(f'{datetime.now()}_{file.filename}')
        file.save(f'{self.__parentpath + path}{filename}')

        return f'{self.__parentpath + path}{filename}'

    def insert(self, values):
        cursor = self.__conn.cursor()
        try:
            query = f"""
                INSERT INTO {self.__table} (ID_Product, path)
                VALUES (%s, %s)
            """
            cursor.execute(query, values)
            self.__conn.commit()
        
        except Exception as e:
            self.__conn.rollback()
            print(f'\n===================\n[Error]({datetime.now()}):{e}\n===================\n')
            return e
        cursor.close()
        return 201
    
    def select(self, product_id=None):
        cursor = self.__conn.cursor()
        query = f"SELECT * FROM {self.__table};"

        if product_id != None:
            query = f"SELECT * FROM {self.__table} WHERE ID_Product = {product_id};"

        try:
            cursor.execute(query)
            results = cursor.fetchall()
        
        except Exception as e:
            self.__conn.rollback()
            print(f'\n===================\n[Error]({datetime.now()}):{e}\n===================\n')
        
        cursor.close()
        return [{'id': row[0], 'product_id': row[1], 'path': row[2]} for row in results]

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
