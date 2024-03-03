from abc import ABC, abstractmethod
from psycopg2._psycopg import connection

class RepoI(ABC):
    def __init__(self, db: connection):
        pass
    
    @abstractmethod
    def insert(self):
        pass

    @abstractmethod
    def select(self):
        pass

    @abstractmethod
    def update(self):
        pass
