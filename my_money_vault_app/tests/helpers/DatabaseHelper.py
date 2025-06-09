class DatabaseHelper:
    def __init__(self, connector):
        self.connector = connector
        
    def reset_database(self):
        self.__delete_states()
        self.__delete_accounts()
        self.__delete_institutions()
        
    def write(self, query, connector):
        cursor = connector.cursor()
        cursor.execute(query)
        self.connector.commit()
        
    def __delete_accounts(self):
        query = "DELETE FROM accounts;"
        self.__write(query)
        
    def __delete_institutions(self):
        query = "DELETE FROM institutions;"
        self.__write(query)
        
    def __delete_states(self):
        query = "DELETE FROM states;"
        self.__write(query)
        
    def __write(self, query: str):
        cursor = self.connector.cursor()
        cursor.execute(query)
        self.connector.commit()
    