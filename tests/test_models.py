"""
Test cases for Customer Model

"""
import logging
import unittest
import os
from service.models import Customer, DataValidationError, db
from service import app
from .factories import CustomerFactory

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
        """Create a customer and assert that it exists"""
        customer = Customer(first_name="allen", last_name="zhang",
                            userid="allenzhang", password="devops2022", addresses=["2022 New York Street", "2022 Jersey Street"])
        self.assertTrue(customer != None)
        self.assertEqual(customer.id, None)
        self.assertEqual(customer.first_name, "allen")
        self.assertEqual(customer.last_name, "zhang")
        self.assertEqual(customer.userid, "allenzhang")
        self.assertEqual(customer.password, "devops2022")
        self.assertEqual(customer.addresses, ["2022 New York Street", "2022 Jersey Street"])

        customer = Customer(first_name="allen", last_name="zhang",
                            userid="devops2022", password="customers2022", addresses=["2022 devops road"])
        
        self.assertEqual(customer.userid, "devops2022")
        self.assertEqual(customer.password, "customers2022")
        self.assertEqual(customer.addresses, ["2022 devops road"])
    
    def test_add_a_customer(self):
        """Create a customer and add it to the database"""

        customers = Customer.all()
        self.assertEqual(customers, [])
        customer = Customer(first_name="allen", last_name="zhang",
                            userid="allenzhang", password="devops2022", addresses=["2022 New York Street", "2022 Jersey Street"])
        self.assertTrue(customer != None)
        self.assertEqual(customer.id, None)
        customer.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(customer.id, 1)
        customers = Customer.all()
        self.assertEqual(len(customers), 1)
        # Check for an additional customer
        customer = Customer(first_name="allen", last_name="zhang",
                            userid="allenzhang", password="devops2022", addresses=["2022 New York Street"])
        self.assertTrue(customer != None)
        self.assertEqual(customer.id, None)
        customer.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(customer.id, 2)
        customers = Customer.all()
        self.assertEqual(len(customers), 2)
        self.assertEqual(customers[0].addresses[1], "2022 Jersey Street")
        self.assertEqual(len(customers[1].addresses), 1)

    def test_serialize_a_customer(self):
        """Test serialization of a Customer"""
        customer = CustomerFactory()
        data = customer.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], customer.id)
        self.assertIn("first_name", data)
        self.assertEqual(data["first_name"], customer.first_name)
        self.assertIn("last_name", data)
        self.assertEqual(data["last_name"], customer.last_name)
        self.assertIn("userid", data)
        self.assertEqual(data["userid"], customer.userid)
        self.assertIn("password", data)
        self.assertEqual(data["password"], customer.password)
        self.assertIn("addresses", data)
        self.assertEqual(data["addresses"], customer.addresses)
    
    def test_deserialize_a_customer(self):
        """Test deserialization of a Customer"""
        data = {
            "id": 1,
            "first_name": "allen",
            "last_name": "zhang",
            "userid": "allenzhang",
            "password": "devops2022",
            "addresses": ["2022 New York Road"],
        }
        customer = Customer()
        customer.deserialize(data)
        self.assertNotEqual(customer, None)
        self.assertEqual(customer.id, None)
        self.assertEqual(customer.first_name, "allen")
        self.assertEqual(customer.last_name, "zhang")
        self.assertEqual(customer.userid, "allenzhang")
        self.assertEqual(customer.password, "devops2022")
        self.assertEqual(customer.addresses, ["2022 New York Road"])
        self.assertEqual(len(customer.addresses), 1)
        self.assertEqual(customer.addresses[0], "2022 New York Road")

    def test_deserialize_missing_data(self):
        """Test deserialization of a Customer with missing data"""
        data = {
            "id": 1,
            "first_name": "allen",
            "userid": "allenzhang",
            "password": "devops2022",
            "addresses": ["2022 New York Road"],
        } # Missing last name
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, data)

    def test_deserialize_bad_data(self):
        """Test deserialization of bad data"""
        data = "this is not a dictionary"
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, data)
    
    def test_deserialize_bad_first_name(self):
        """ Test deserialization of bad first name attribute """
        test_customer = CustomerFactory()
        data = test_customer.serialize()
        data["first_name"] = 123
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, data)
    
    def test_deserialize_bad_last_name(self):
        """ Test deserialization of bad last name attribute """
        test_customer = CustomerFactory()
        data = test_customer.serialize()
        data["last_name"] = True
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, data)

    def test_deserialize_bad_addresses__list_type(self):
        """ Test deserialization of bad addresses list type attribute """
        test_customer = CustomerFactory()
        data = test_customer.serialize()
        data["addresses"] = [True, 123]
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, data)
    
    def test_deserialize_bad_addresses_length(self):
        """ Test deserialization of bad addresses length """
        test_customer = CustomerFactory()
        data = test_customer.serialize()
        data["addresses"] = []
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, data)
    
    def test_deserialize_bad_addresses_type(self):
        """ Test deserialization of bad addresses type attribute """
        test_customer = CustomerFactory()
        data = test_customer.serialize()
        data["addresses"] = "abc"
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, data)
    
    def test_list_all(self):
        """Test case to list all customers"""
        customers = CustomerFactory.create_batch(3)
        for customer in customers:
            customer.create()
        self.assertEqual(len(Customer.all()), 3)
        self.assertEqual(len(Customer.all()), 3)

    def test_delete_a_customer(self):
        """Delete a Customer"""
        test_customer = CustomerFactory()
        test_customer.create()
        self.assertEqual(len(test_customer.all()), 1)
        # delete the customer and make sure it isn't in the database
        test_customer.delete()
        self.assertEqual(len(test_customer.all()), 0)

    def test_delete_customer_address(self):
        """Delete a Customer address"""
        test_customer = CustomerFactory()
        test_customer.create()
        test_customer.addresses = ["2022 New York Street"]
        self.assertEqual(len(test_customer.addresses), 1)

        # delete the customer and make sure it isn't in the database
        test_customer.delete_addresses()
