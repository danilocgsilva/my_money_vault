from src.Repositories.RepositoryInterface import RepositoryInterface
from src.Models.State import State
from src.Exceptions.ModelDataValidationException import ModelDataValidationException
from typing import List
from typing import Optional

class StateRepository(RepositoryInterface):
    def __init__(self, mysql_connector):
        self.mysql_connector = mysql_connector
        
    def create(self, state: State) -> State:
        if not state.validate():
            raise ModelDataValidationException("Can't create state.")
        
        query = """
        INSERT INTO states (account_id, balance, date)
        VALUES (%s, %s)
        """
        try:
            cursor =  self.mysql_connector.cursor()
            cursor.execute(query, ())
        
    
    def find_by_id(self, institution_id: int) -> Optional[State]:
        pass
        
    def find_all(self) -> List[State]:
        pass
        
    def find_all_with_accounts_counts(self) -> List[State]:
        pass

    def update(self, institution: State) -> State:
        pass
    
    def delete(self, institution_id: int) -> bool:
        pass
