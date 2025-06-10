import unittest
from src.Repositories.StateRepository import StateRepository
from src.MySQLConnectorWrapper import MySQLConnectorWrapper
from src.CredentialsBag import CredentialsBag
import os
from tests.helpers.DatabaseHelper import DatabaseHelper
from decimal import *
import math

class test_StateRepository(unittest.TestCase):
    
    def setUp(self):
        self.mysql_connector = MySQLConnectorWrapper(self.__get_crecential_bag()).connector
        self.database_helper = DatabaseHelper(self.mysql_connector)
    
    def test_find_all(self):
        self.database_helper.reset_database()
        self.__create_institutions(1, 'Test Institution')
        self.__create_accounts(1, 1, 'Test Account')
        self.__create_states(1, 1, 223.11, '2025-03-01 00:00:00')
        state_repository = StateRepository(self.mysql_connector)
        states = state_repository.find_all()
        self.assertEqual(1, len(states))
        
    def test_find_all_two_elements(self):
        self.database_helper.reset_database()
        self.__create_institutions(1, 'Test Institution')
        self.__create_accounts(1, 1, 'Test Account')
        self.__create_states(1, 1, 223.11, '2025-03-01 00:00:00')
        self.__create_states(2, 1, 100.00, '2025-02-25 00:00:00')
        state_repository = StateRepository(self.mysql_connector)
        states = state_repository.find_all()
        self.assertEqual(2, len(states))

    def test_find_all_states_from_single_account(self):
        self.database_helper.reset_database()
        self.__create_institutions(1, 'Test Institution')
        self.__create_accounts(1, 1, 'First Account From Institution')
        self.__create_accounts(2, 1, 'Second Account From Institution')
        self.__create_states(1, 1, 223.11, '2025-03-01 00:00:00')
        self.__create_states(2, 2, 100.00, '2025-02-25 00:00:00')
        state_repository = StateRepository(self.mysql_connector)
        states = state_repository.find_states_by_account(1)
        self.assertEqual(1, len(states))
        
    def test_check_date_properties(self):
        self.database_helper.reset_database()
        self.__create_institutions(id=1, name='Test Institution')
        self.__create_accounts(id=1, account_id=1, account_name='Test Account')
        self.__create_states(id=1, account_id=1, balance=223.11, date='2025-03-01 00:00:00')
        state_repository = StateRepository(self.mysql_connector)
        states = state_repository.find_all()
        self.assertEqual('2025-03-01 00:00:00', states[0].date_string)
        self.assertEqual(math.isclose(223.11, states[0].balance), True)
        
    def __get_crecential_bag(self) -> CredentialsBag:
        credential_bag = CredentialsBag(
            host=os.environ.get('MYSQL_HOST_TEST'),
            user=os.environ.get('MYSQL_USER_TEST'),
            password=os.environ.get('MYSQL_PASSWORD_TEST'),
            database=os.environ.get('MYSQL_DATABASE_TEST'),
            port=int(os.environ.get('MYSQL_PORT_TEST', 3306))
        )
        return credential_bag
    
    def __create_accounts(self, id: str, account_id: str, account_name: str):
        query = "INSERT INTO accounts (id, institution_id, name) VALUES ({}, {}, '{}')"
        self.database_helper.write(query.format(id, account_id, account_name), self.mysql_connector)
        
    def __create_institutions(self, id: str, name: str):
        query = "INSERT INTO institutions (id, name) VALUES ({}, '{}')"
        self.database_helper.write(query.format(id, name), self.mysql_connector)
        
    def __create_states(self, id, account_id, balance, date):
        query = "INSERT INTO states (id, account_id, balance, date) VALUES ({}, {}, {}, '{}');"
        self.database_helper.write(query.format(id, account_id, balance, date), self.mysql_connector)
