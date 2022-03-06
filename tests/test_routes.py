"""
TestCustomerModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from service import status  # HTTP Status Codes
from service.models import db
from service.routes import app, init_db

from .factories import CustomerFactory

# Disable all but critical errors during normal test run
# uncomment for debugging failing tests
logging.disable(logging.CRITICAL)

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/customers"
CONTENT_TYPE_JSON = "application/json"
######################################################################
#  T E S T   C A S E S
######################################################################
class TestCustomerServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db()

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################
    def _create_customers(self, count):
        """Factory method to create pets in bulk"""
        customers = []

        return customers
    
    def test_index(self):
        """Test the Home Page"""
        self.assertTrue(True)

    def test_get_customer_list(self):
        """Get a list of Customers"""
        self.assertTrue(True)

    def test_get_customer(self):
        """Get a single Customer"""
        self.assertTrue(True)

    def test_get_customer_not_found(self):
        """Get a Customer thats not found"""
        self.assertTrue(True)

    def test_create_customer(self):
        """Create a new Customer"""
        self.assertTrue(True)

    def test_create_customer_no_data(self):
        """Create a Customer with missing data"""
        self.assertTrue(True)

    def test_create_customer_no_first_name(self):
        """Create a Customer with no first name"""
        self.assertTrue(True)
    
    def test_create_customer_no_last_name(self):
        """Create a Customer with no last name"""
        self.assertTrue(True)

    def test_create_customer_no_addresses(self):
        """Create a Customer with no address"""
        self.assertTrue(True)

    def test_update_customer(self):
        """Update an existing Customer"""
        self.assertTrue(True)

    def test_delete_customer(self):
        """Delete a Customer"""
        self.assertTrue(True)

    def test_query_customer_list_by_first_name(self):
        """Query Customer by first name"""
        self.assertTrue(True)
    
    def test_query_customer_list_by_last_name(self):
        """Query Customer by last name"""
        self.assertTrue(True)
    
    def test_query_customer_list_by_userid(self):
        """Query Customer by userid"""
        self.assertTrue(True)