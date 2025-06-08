import mysql.connector
import os
from typing import Optional
from src.CredentialsBag import CredentialsBag

class MySQLConnectorWrapper:
    
    connector: Optional[mysql.connector] = None
    
    def __init__(self, credentials: Optional[CredentialsBag] = None):
        if credentials:
            self.connector = mysql.connector.connect(
                host=credentials.host,
                user=credentials.user,
                password=credentials.password,
                database=credentials.database,
                port=credentials.port
            )
        else:
            self._initialize_from_env()
            
        self.connector = mysql.connector.connect(
            host=os.environ.get("MYSQL_HOST"),
            user=os.environ.get("MYSQL_USER"),
            password=os.environ.get("MYSQL_PASSWORD"),
            database=os.environ.get("MYSQL_DATABASE")
        )
    