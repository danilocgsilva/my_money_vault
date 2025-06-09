from src.Repositories.RepositoryInterface import RepositoryInterface
from src.Models.State import State
from src.Exceptions.ModelDataValidationException import ModelDataValidationException
from typing import List
from typing import Optional
import mysql.connector
from src.MySQLConnectorWrapper import MySQLConnectorWrapper

class StateRepository(RepositoryInterface):
    def __init__(self, mysql_connector: MySQLConnectorWrapper):
        self.mysql_connector = mysql_connector
        
    def create(self, state: State) -> State:
        if not state.validate():
            raise ModelDataValidationException("Can't create state.")
        
        query = """
        INSERT INTO states (account_id, balance, date)
        VALUES (%s, %s, %s)
        """
        try:
            cursor =  self.mysql_connector.cursor()
            cursor.execute(query, (state.account_id, state.balance, state.date, ))
            self.mysql_connector.commit()
            state.id = cursor.lastrowid
            return state
        except:
            raise
        finally:
            if self.mysql_connector:
                self.mysql_connector.close()
    
    def find_by_id(self, state_id: int) -> Optional[State]:
        query = """
        SELECT id, account_id, balance, date
        FROM states
        WHERE id = %s
        """
        
        cursor = self.mysql_connector.cursor(dictionary=True)
        cursor.execute(query, (state_id, ))
        result = cursor.fetchone()
        if result:
            state = State()
            state.id = result['id']
            state.account_id = result['account_id']
            state.balance = result['balance']
            state.date = result['date']
            return state
        return None
    
    def find_states_by_account(self, account_id: int):
        query = """
        SELECT id, account_id, balance, date
        FROM states
        WHERE account_id = %s
        """
        try:
            cursor = self.mysql_connector.cursor(dictionary=True)
            cursor.execute(query, (account_id, ))
            results = cursor.fetchall()
            states_list = []
            for row in results:
                state = State()
                state.id = row['id']
                state.account_id = row['account_id']
                state.balance = row['balance']
                state.date = row['date']
                states_list.append(state)
            return states_list
        finally:
            if self.mysql_connector:
                self.mysql_connector.close()
    
    def find_all(self) -> List[State]:
        query = """
        SELECT id, account_id, balance, date
        FROM states
        """
        try:
            cursor = self.mysql_connector.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
            states_list = []
            for row in results:
                state = State()
                state.id = row['id']
                state.account_id = row['account_id']
                state.balance = row['balance']
                state.date = row['date']
                states_list.append(state)
            return states_list
        finally:
            if self.mysql_connector:
                self.mysql_connector.close()
        
    def update(self, state: State) -> State:
        if not state.validate():
            raise ModelDataValidationException("Can't proceed to change the State.")
        query = """
        UPDATE states
        SET account_id = %s,
        balance = %s,
        date = %s
        WHERE id = %s
        """
        
        try:
            cursor = self.mysql_connector.cursor()
            cursor.execute(query, (state.account_id, state.balance, state.date, state.id, ))
            if cursor.rowcount == 0:
                raise ValueError(f"State with id {state.id} not found.")
            self.mysql_connector.commit()
            
            return self.find_by_id(state.id)
        except mysql.connector.Error as err:
            raise
        finally:
            if self.mysql_connector:
                self.mysql_connector.close()
    
    def delete(self, state_id: int) -> bool:
        query = """
        DELETE FROM states WHERE id = %s 
        """
        
        try:
            cursor = self.mysql_connector.cursor()
            cursor.execute(query, (state_id, ))
            self.mysql_connector.commit()
            return cursor.rowcount > 0
        finally:
            if self.mysql_connector:
                self.mysql_connector.close()
