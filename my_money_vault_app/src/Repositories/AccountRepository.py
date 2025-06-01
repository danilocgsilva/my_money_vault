from typing import List, Optional
from src.Repositories.RepositoryInterface import RepositoryInterface
from src.Models.Account import Account
import mysql.connector

class AccountRepository(RepositoryInterface):
    
    def __init__(self, mysql_connector):
        self.mysql_connector = mysql_connector
        self.get_institution = False
    
    def create(self, account: Account) -> Account:
        account.validate()
        
        query = """
        INSERT INTO accounts (institution_id, name)
        VALUES (%s, %s)
        """
        try:
            cursor = self.mysql_connector.cursor()
            cursor.execute(query, (account.institution_id, account.name))
            self.mysql_connector.commit()
            account.id = cursor.lastrowid
            return account
        except mysql.connector.Error as err:
            raise
        finally:
            if self.mysql_connector:
                self.mysql_connector.close()
    
    def find_by_id(self, account_id: int) -> Optional[Account]:
        
        if self.get_institution:
            query = """
            SELECT
                a.id as account_id,
                a.institution_id as account_institution_id,
                a.name as account_name
            FROM accounts a
            LEFT JOIN institutiona i ON i.id = a.institution_id
            WHERE id = %s
            """
            try:
                cursor = self.mysql_connector.cursor(dictionary=True)
                cursor.execute(query, (account_id,))
                result = cursor.fetchone()
                if result:
                    account = Account()
                    
                    account.id = result['account_id']
                    account.institution_id = result['account_institution_id']
                    account.name = result['account_name']
        else:
            query = """
            SELECT
                id as account_id, 
                institution_id as account_institution_id, 
                name as account_name
            FROM accounts
            WHERE id = %s
            """
            try:
                cursor = self.mysql_connector.cursor(dictionary=True)
                cursor.execute(query, (account_id,))
                result = cursor.fetchone()
                
                if result:
                    account = Account()
                    account.id = result['account_id']
                    account.institution_id = result['account_institution_id']
                    account.name = result['account_name']
                    return account
                return None
            finally:
                if self.mysql_connector:
                    self.mysql_connector.close()

    def find_all(self) -> List[Account]:
        query = """
        SELECT id, institution_id, name
        FROM accounts
        """
        try:
            cursor = self.mysql_connector.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
            accounts_list = []
            for row in results:
                account = Account()
                account.id = row['id']
                account.institution_id = row['institution_id']
                account.name = row['name']
                
                accounts_list.append(account)
            
            return accounts_list
        finally:
            if self.mysql_connector:
                self.mysql_connector.close()
    
    def update(self, account: Account) -> Account:
        account.validate()
        
        query = """
        UPDATE accounts
        SET institution_id = %s, name = %s
        WHERE id = %s
        """
        try:
            cursor = self.mysql_connector.cursor()
            cursor.execute(query, (account.institution_id, account.name, account.id))
            if cursor.rowcount == 0:
                raise ValueError(f"Account with id {account.id} not found")
            self.mysql_connector.commit()
            
            return self.find_by_id(account.id)
        except mysql.connector.Error as err:
            if err.errno == 1062:
                raise ValueError(f"Account with name '{account.name}' already exists") from err
            raise
        finally:
            if self.mysql_connector:
                self.mysql_connector.close()
    
    def delete(self, account_id: int) -> bool:
        query = """
        DELETE FROM accounts
        WHERE id = %s
        """
        try:
            cursor = self.mysql_connector.cursor()
            cursor.execute(query, (account_id,))
            self.mysql_connector.commit()
            return cursor.rowcount > 0
        finally:
            if self.mysql_connector:
                self.mysql_connector.close()
    
    def find_by_name(self, name: str) -> Optional[Account]:
        query = """
        SELECT id, institution_id, name
        FROM accounts
        WHERE name = %s
        """
        try:
            cursor = self.mysql_connector.cursor(dictionary=True)
            cursor.execute(query, (name,))
            result = cursor.fetchone()
            
            if result:
                account = Account()
                account.id = result['id']
                account.institution_id = result['institution_id']
                account.name = result['name']
                
                return account
                
            return None
        finally:
            if self.mysql_connector:
                self.mysql_connector.close()
                
    def prepareWithInstitution(self):
        self.get_institution = True
