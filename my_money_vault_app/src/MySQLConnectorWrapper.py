import mysql.connector
import os
from typing import Optional


class MySQLConnectorWrapper:
    
    connector: Optional[mysql.connector] = None
    
    def __init__(self):
        self.connector = mysql.connector.connect(
            host=os.environ.get("MYSQL_HOST"),
            user=os.environ.get("MYSQL_USER"),
            password=os.environ.get("MYSQL_PASSWORD"),
            database=os.environ.get("MYSQL_DATABASE")
        )
    