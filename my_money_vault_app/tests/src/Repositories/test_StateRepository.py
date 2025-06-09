import unittest
from src.Repositories.StateRepository import StateRepository
from src.MySQLConnectorWrapper import MySQLConnectorWrapper
from src.CredentialsBag import CredentialsBag
import os
from tests.helpers.DatabaseHelper import DatabaseHelper

class test_StateRepository(unittest.TestCase):
    
    def setUp(self):
        self.mysql_connector = MySQLConnectorWrapper(self.__get_crecential_bag()).connector
        self.database_helper = DatabaseHelper(self.mysql_connector)
    
    def test_find_all(self):
        self.database_helper.reset_database()
        self.__create_institutions()
        self.__create_accounts()
        self.__create_states(1, 1, 223.11, '2025-03-01 00:00:00')
        state_repository = StateRepository(self.mysql_connector)
        states = state_repository.find_all()
        self.assertEqual(1, len(states))
        
    def test_find_all_two_elements(self):
        self.database_helper.reset_database()
        self.__create_institutions()
        self.__create_accounts()
        self.__create_states(1, 1, 223.11, '2025-03-01 00:00:00')
        self.__create_states(2, 1, 100.00, '2025-02-25 00:00:00')
        state_repository = StateRepository(self.mysql_connector)
        states = state_repository.find_all()
        self.assertEqual(2, len(states))
        
    def __get_crecential_bag(self) -> CredentialsBag:
        credential_bag = CredentialsBag(
            host=os.environ.get('MYSQL_HOST_TEST'),
            user=os.environ.get('MYSQL_USER_TEST'),
            password=os.environ.get('MYSQL_PASSWORD_TEST'),
            database=os.environ.get('MYSQL_DATABASE_TEST'),
            port=int(os.environ.get('MYSQL_PORT_TEST', 3306))
        )
        return credential_bag
    
    def __create_accounts(self):
        query = "INSERT INTO accounts (id, institution_id, name) VALUES (1, 1, 'Test Account')"
        self.database_helper.write(query, self.mysql_connector)
        
    def __create_institutions(self):
        query = "INSERT INTO institutions (id, name) VALUES (1, 'Test Institution')"
        self.database_helper.write(query, self.mysql_connector)
        
    def __create_states(self, id, account_id, balance, date):
        query = "INSERT INTO states (id, account_id, balance, date) VALUES ({}, {}, {}, '{}');"
        self.database_helper.write(query.format(id, account_id, balance, date), self.mysql_connector)

