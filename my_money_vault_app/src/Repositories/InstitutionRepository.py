from typing import List, Optional
from src.Repositories.RepositoryInterface import RepositoryInterface
from src.Models.Institution import Institution
from src.Models.Account import Account
import mysql.connector

class InstitutionRepository(RepositoryInterface):
    
    def __init__(self, mysql_connector):
        self.mysql_connector = mysql_connector
    
    def create(self, institution: Institution) -> Institution:
        institution.validate()
        
        query = """
        INSERT INTO institutions (name, description)
        VALUES (%s, %s)
        """
        try:
            cursor = self.mysql_connector.cursor()
            cursor.execute(query, (institution.name, institution.description))
            self.mysql_connector.commit()
            institution.id = cursor.lastrowid
            return institution
        except mysql.connector.Error as err:
            raise
        finally:
            if self.mysql_connector:
                self.mysql_connector.close()
    
    def find_by_id(self, institution_id: int) -> Optional[Institution]:
        query = """
        SELECT id, name, description
        FROM institutions
        WHERE id = %s
        """
            
        cursor = self.mysql_connector.cursor(dictionary=True)
        cursor.execute(query, (institution_id,))
        result = cursor.fetchone()
        
        if result:
            institution = Institution()
            institution.id = result['id']
            institution.name = result['name']
            institution.description = result['description']
            return institution
        return None
    
    def find_all(self) -> List[Institution]:
        query = """
        SELECT id, name, description
        FROM institutions
        """
        try:
            cursor = self.mysql_connector.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
            institutions_list = []
            for row in results:
                
                institution = Institution()
                institution.id = row['id']
                institution.name = row['name']
                institution.description = row['description']
                
                institutions_list.append(institution)
            
            return institutions_list
        finally:
            if self.mysql_connector:
                self.mysql_connector.close()
    
    def update(self, institution: Institution) -> Institution:
        institution.validate()
        
        query = """
        UPDATE institutions
        SET name = %s, description = %s
        WHERE id = %s
        """
        try:
            cursor = self.mysql_connector.cursor()
            cursor.execute(query, (institution.name, institution.description, institution.id))
            if cursor.rowcount == 0:
                raise ValueError(f"Institution with id {institution.id} not found")
            self.mysql_connector.commit()
            
            return self.find_by_id(institution.id)
        except mysql.connector.Error as err:
            if err.errno == 1062:
                raise ValueError(f"Institution with name '{institution.name}' already exists") from err
            raise
        finally:
            if self.mysql_connector:
                self.mysql_connector.close()
    
    def delete(self, institution_id: int) -> bool:
        query = """
        DELETE FROM institutions
        WHERE id = %s
        """
        try:
            cursor = self.mysql_connector.cursor()
            cursor.execute(query, (institution_id,))
            self.mysql_connector.commit()
            return cursor.rowcount > 0
        finally:
            if self.mysql_connector:
                self.mysql_connector.close()
    
    def find_by_name(self, name: str) -> Optional[Institution]:
        query = """
        SELECT id, name, description
        FROM institutions
        WHERE name = %s
        """
        try:
            cursor = self.mysql_connector.cursor(dictionary=True)
            cursor.execute(query, (name,))
            result = cursor.fetchone()
            
            if result:
                return Institution(
                    id=result['id'],
                    name=result['name'],
                    description=result['description']
                )
            return None
        finally:
            if self.mysql_connector:
                self.mysql_connector.close()
                
    def fill_accounts(self, institution: Institution):
        query = """
        SELECT id, institution_id, name
        FROM accounts
        WHERE institution_id = %s
        """
        try:
            cursor = self.mysql_connector.cursor(dictionary=True)
            cursor.execute(query, (institution.id,))
            results = cursor.fetchall()
            accounts_list = []
            for row in results:
                
                account = Account()
                account.id = row['id']
                account.institution_id = row['institution_id']
                account.name = row['name']
                
                accounts_list.append(account)
            
            institution.accounts = accounts_list
        finally:
            if self.mysql_connector:
                self.mysql_connector.close()
                