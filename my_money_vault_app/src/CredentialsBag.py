class CredentialsBag:
    host: str
    user: str
    password: str
    database: str
    port: int = 3306
    
    def __init__(self, host: str, user: str, password: str, database: str, port: int = 3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
    