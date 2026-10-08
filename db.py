import os
from dotenv import load_dotenv
import mysql.connector

class MysqlConfig:

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
    
    @classmethod
    def get_connection(cls) -> mysql.connector.CMySQLConnection:
        return mysql.connector.connect(**cls.CONFIG)