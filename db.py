import os
from dotenv import load_dotenv
import mysql.connector

class MysqlConnector:

    load_dotenv()
    
    HOST = os.getenv("DB_HOST")
    PORT = os.getenv("DB_PORT")
    USER = os.getenv("DB_USER")
    PASSWORD = os.getenv("DB_PASSWORD")
    DATABASE = os.getenv("DB_DATABASE")

    CONFIG = {
        'host': HOST,
        'port': PORT,
        'user': USER,
        'password': PASSWORD,
        'database': DATABASE
    }
    
    def get_connection(self) -> mysql.connector.CMySQLConnection:
            return mysql.connector.connect(**self.CONFIG)
    
class MysqlTransaction:
    def __init__(self, connection: mysql.connector.CMySQLConnection):
        self. connection = connection
        
    def start_transaction(self):
        self.connection.start_transaction()
        
    def commit(self):
        self.connection.commit()
        
    def rollback(self):
        self.connection.rollback()