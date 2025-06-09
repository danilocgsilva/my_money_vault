import mysql.connector
import os
from typing import Optional
from src.CredentialsBag import CredentialsBag

class MySQLConnectorWrapper:
    
    connector: Optional[mysql.connector] = None
    
    def __init__(self, credentialsBag: Optional[CredentialsBag] = None):
        if credentialsBag:
            self.connector = mysql.connector.connect(
                host=credentialsBag.host,
                user=credentialsBag.user,
                password=credentialsBag.password,
                database=credentialsBag.database,
                port=credentialsBag.port
            )
        else:
            self.connector = mysql.connector.connect(
                host=os.environ.get("MYSQL_HOST"),
                user=os.environ.get("MYSQL_USER"),
                password=os.environ.get("MYSQL_PASSWORD"),
                database=os.environ.get("MYSQL_DATABASE"),
                port=int(os.environ.get("MYSQL_PORT", 3306))
            )
    