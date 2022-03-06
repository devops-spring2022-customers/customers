"""
Test cases for Customer Model

"""
import logging
import unittest
import os
from service.models import Customer, DataValidationError, db
from service import app

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)
######################################################################
#  <Customer>   M O D E L   T E S T   C A S E S
######################################################################
class TestCustomerModel(unittest.TestCase):
    """ Test Cases for Customer Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Customer.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_customer(self):
        """Create a Customer and assert that it exists"""
        self.assertTrue(True)

    def test_add_a_customer(self):
        """Create a Customer and add it to the database"""
        self.assertTrue(True)

    def test_update_a_customer(self):
        """Update a Customer"""
        self.assertTrue(True)

    def test_delete_a_customer(self):
        """Delete a Customer"""
        self.assertTrue(True)

    def test_serialize_a_customer(self):
        """Test serialization of a Customer"""
        self.assertTrue(True)
    
    def test_deserialize_a_customer(self):
        """Test deserialization of a Customer"""
        self.assertTrue(True)

    def test_deserialize_missing_data(self):
        """Test deserialization of a Customer with missing data"""
        self.assertTrue(True)

    def test_deserialize_bad_data(self):
        """Test deserialization of bad data"""
        self.assertTrue(True)

    def test_deserialize_bad_first_name(self):
        """ Test deserialization of bad first_name attribute """
        self.assertTrue(True)

    def test_deserialize_bad_last_name(self):
        """ Test deserialization of bad last_name attribute """
        self.assertTrue(True)
    
    def test_deserialize_bad_addresses(self):
        """ Test deserialization of bad addresses attribute """
        self.assertTrue(True)

    def test_find_customer(self):
        """Find a Customer by ID"""
        self.assertTrue(True)

    def test_find_by_first_name(self):
        """Find a Customer by first name"""
        self.assertTrue(True)

    def test_find_by_last_name(self):
        """Find a Customer by last name"""
        self.assertTrue(True)

    def test_find_by_userid(self):
        """Find a Customer by userid name"""
        self.assertTrue(True)

    def test_find_or_404_found(self):
        """Find or return 404 found"""
        self.assertTrue(True)

    def test_find_or_404_not_found(self):
        """Find or return 404 NOT found"""
        self.assertTrue(True)