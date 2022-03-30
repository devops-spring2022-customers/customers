"""
Test cases for Customer Model

"""
from ast import Add
import logging
import unittest
import os
from service.models import Customer, Address, DataValidationError, db
from service import app
from .factories import CustomerFactory, AddressFactory

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
#  H E L P E R   M E T H O D S
######################################################################

    def _create_customer(self, addresses):
        """ Creates an customer from a Factory """
        fake_customer = CustomerFactory()
        fake_customer.addresses=addresses
        return fake_customer

    def _create_address(self):
        """ Creates fake addresses from factory """
        fake_address = AddressFactory()
        address = Address(
            street=fake_address.street,
            city=fake_address.city,
            state=fake_address.state,
            postal_code=fake_address.postal_code
        )
        self.assertTrue(address != None)
        self.assertEqual(address.id, None)
        return fake_address

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_customer(self):
        """Create a customer and assert that it exists"""
        customer = Customer(first_name="allen", last_name="zhang",
                            userid="allenzhang", password="devops2022")
        self.assertTrue(customer != None)
        self.assertEqual(customer.id, None)
        self.assertEqual(customer.first_name, "allen")
        self.assertEqual(customer.last_name, "zhang")
        self.assertEqual(customer.userid, "allenzhang")
        self.assertEqual(customer.password, "devops2022")
    
        customer = Customer(first_name="allen", last_name="zhang",
                            userid="devops2022", password="customers2022")
                            
        self.assertEqual(customer.userid, "devops2022")
        self.assertEqual(customer.password, "customers2022")
    
    def test_add_a_customer(self):
        """Create a customer and add it to the database"""

        customers = Customer.all()
        self.assertEqual(customers, [])
        customer = Customer(first_name="allen", last_name="zhang",
                            userid="allenzhang", password="devops2022", addresses=[])
        self.assertTrue(customer != None)
        self.assertEqual(customer.id, None)
        customer.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(customer.id, 1)
        customers = Customer.all()
        self.assertEqual(len(customers), 1)
        # Check for an additional customer
        customer = Customer(first_name="allen", last_name="zhang",
                            userid="allenzhang2", password="devops2022", addresses=[])
        self.assertTrue(customer != None)
        self.assertEqual(customer.id, None)
        customer.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(customer.id, 2)
        customers = Customer.all()
        self.assertEqual(len(customers), 2)

    def test_serialize_a_customer(self):
        """Test serialization of a Customer"""
        address = self._create_address()
        customer = self._create_customer(addresses=[address])
        data = customer.serialize()
        # Customer assertions
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
        self.assertEqual(len(data['addresses']), 1)

        # Address assertions
        addresses = data["addresses"]

        self.assertIn("addresses", data)
        self.assertEqual(addresses[0]['id'], address.id)
        self.assertEqual(addresses[0]['customer_id'], address.customer_id)
        self.assertEqual(addresses[0]['street'], address.street)
        self.assertEqual(addresses[0]['city'], address.city)
        self.assertEqual(addresses[0]['state'], address.state)
        self.assertEqual(addresses[0]['postal_code'], address.postal_code)
    
    def test_deserialize_a_customer(self):
        """Test deserialization of a Customer"""
        address = self._create_address()
        customer = self._create_customer(addresses=[address])
        serial_customer = customer.serialize()
        new_customer = Customer()
        new_customer.deserialize(serial_customer)

        # Assertions for testing
        self.assertNotEqual(new_customer, None)
        self.assertEqual(new_customer.id, None)
        self.assertEqual(new_customer.first_name, customer.first_name)
        self.assertEqual(new_customer.last_name, customer.last_name)
        self.assertEqual(new_customer.userid, customer.userid)
        self.assertEqual(new_customer.password, customer.password)
        self.assertEqual(new_customer.addresses[0].street, address.street)
        self.assertEqual(new_customer.addresses[0].city, address.city)
        self.assertEqual(new_customer.addresses[0].state, address.state)
        self.assertEqual(new_customer.addresses[0].postal_code, address.postal_code)
        self.assertEqual(len(new_customer.addresses), 1)
        #self.assertEqual(new_customer.addresses[0].id, address.id)
        self.assertEqual(new_customer.addresses[0].customer_id, address.customer_id)

    def test_deserialize_missing_data(self):
        """Test deserialization of a Customer with missing data"""
        data = {
            "id": 1,
            "first_name": "allen",
            "userid": "allenzhang",
            "password": "devops2022",
            "addresses": [],
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

    def test_deserialize_bad_addresses_list_type(self):
        """ Test deserialization of bad addresses list type attribute """
        test_customer = CustomerFactory()
        data = test_customer.serialize()
        data["addresses"] = [True, 123]
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, data)
    
    def test_deserialize_bad_addresses_type(self):
        """ Test deserialization of bad addresses type attribute """
        test_customer = CustomerFactory()
        data = test_customer.serialize()
        data["addresses"] = "abc"
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, data)

    def test_deserialize_with_key_error(self):
        """ Deserialize an customer with a KeyError """
        customer = CustomerFactory()
        self.assertRaises(DataValidationError, customer.deserialize, {})
    
    def test_deserialize_with_type_error(self):
        """ Deserialize an customer with a TypeError """
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, [])
    
    def test_deserialize_address_key_error(self):
        """ Deserialize an address with a KeyError """
        address = AddressFactory()
        self.assertRaises(DataValidationError, address.deserialize, {})
    
    def test_deserialize_address_type_error(self):
        """ Deserialize an address with a TypeError """
        address = AddressFactory()
        self.assertRaises(DataValidationError, address.deserialize, [])

    def test_update_a_customer(self):
        """Update or return 404 NOT FOUND"""
        test_customer = Customer(first_name="Jash", last_name="Doshi",
                            userid="jashdoshi07", password="devops2022", addresses=[])
        test_customer.create()
        self.assertEqual(test_customer.id, 1)
        test_customer.first_name = "Jash T"
        test_customer.update()
        cust = Customer.find(1)
        self.assertEqual(cust.first_name, "Jash T")

    def test_list_all(self):
        """Test case to list all customers"""
        customers = CustomerFactory.create_batch(3)
        customers[0].userid = "firstid"
        customers[1].userid = "secondid"
        customers[2].userid = "thirdid"
        for customer in customers:
            customer.create()
        self.assertEqual(len(Customer.all()), 3)
        self.assertEqual(len(Customer.all()), 3)

    def test_find(self):
        """ Find or throw 404 error """
        customer = CustomerFactory()
        customer.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(customer.id, 1)

        # Fetch it back
        customer = Customer.find(customer.id)
        self.assertEqual(customer.id, 1)

    def test_find_or_404(self):
        """ Find or throw 404 error """
        customer = CustomerFactory()
        customer.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(customer.id, 1)

        # Fetch it back
        customer = Customer.find_or_404(customer.id)
        self.assertEqual(customer.id, 1)
    
    def test_find_by_first_name(self):
        """ Find by first_name """
        customer = CustomerFactory()
        customer.create()

        # Fetch it back by name
        same_customer = Customer.find_by_first_name(customer.first_name)[0]
        self.assertEqual(same_customer.id, customer.id)
        self.assertEqual(same_customer.first_name, customer.first_name)

    def test_find_by_last_name(self):
        """ Find by last_name """
        customer = CustomerFactory()
        customer.create()

        # Fetch it back by name
        same_customer = Customer.find_by_last_name(customer.last_name)[0]
        self.assertEqual(same_customer.id, customer.id)
        self.assertEqual(same_customer.last_name, customer.last_name)

    def test_delete_a_customer(self):
        """Delete a Customer"""
        test_customer = CustomerFactory()
        test_customer.create()
        self.assertEqual(len(test_customer.all()), 1)
        # delete the customer and make sure it isn't in the database
        test_customer.delete()
        self.assertEqual(len(test_customer.all()), 0)

    def test_add_customer_address(self):
        """ Create a customer with an address and add it to the database """
        customers = Customer.all()
        self.assertEqual(customers, [])
        customer = CustomerFactory()
        address = AddressFactory()
        customer.addresses.append(address)
        customer.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(customer.id, 1)
        customers = Customer.all()
        self.assertEqual(len(customers), 1)

        new_customer = Customer.find(customer.id)
        self.assertEqual(new_customer.addresses[0].street, address.street)
        self.assertEqual(new_customer.addresses[0].city, address.city)
        self.assertEqual(new_customer.addresses[0].state, address.state)
        self.assertEqual(new_customer.addresses[0].postal_code, address.postal_code)

        address2 = AddressFactory()
        customer.addresses.append(address2)
        customer.update()

        new_customer = Customer.find(customer.id)
        self.assertEqual(len(new_customer.addresses), 2)
        self.assertEqual(new_customer.addresses[1].street, address2.street)
        self.assertEqual(new_customer.addresses[1].city, address2.city)
        self.assertEqual(new_customer.addresses[1].state, address2.state)
        self.assertEqual(new_customer.addresses[1].postal_code, address2.postal_code)

    def test_update_customer_address(self):
        """ Update a customers address """
        customers = Customer.all()
        self.assertEqual(customers, [])

        address = AddressFactory()
        customer = CustomerFactory()
        customer.addresses.append(address)
        customer.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(customer.id, 1)
        customers = Customer.all()
        self.assertEqual(len(customers), 1)

        # Fetch it back
        customer = Customer.find(customer.id)
        old_address = customer.addresses[0]
        self.assertEqual(old_address.street, address.street)
        self.assertEqual(old_address.city, address.city)
        self.assertEqual(old_address.state, address.state)
        self.assertEqual(old_address.postal_code, address.postal_code)

        old_address.street = "XX"
        customer.update()

        # Fetch it back again
        customer = Customer.find(customer.id)
        address = customer.addresses[0]
        self.assertEqual(address.street, "XX")

    def test_delete_customer_address(self):
        """ Delete an customers address """
        customers = Customer.all()
        self.assertEqual(customers, [])

        address = AddressFactory()
        customer = CustomerFactory()
        customer.addresses.append(address)
        customer.create()

        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(customer.id, 1)
        customers = Customer.all()
        self.assertEqual(len(customers), 1)

        # Fetch it back
        customer = Customer.find(customer.id)
        old_address = customer.addresses[0]
        address.delete()
        customer.update()

        # Fetch it back again
        customer = Customer.find(customer.id)
        self.assertEqual(len(customer.addresses), 0)
    
    def test_create_customer_same_userid(self):
        """Create customer with same userid"""
        customer = Customer(first_name="allen", last_name="zhang",
                            userid="allenzhang", password="devops2022")
        self.assertTrue(customer != None)
        self.assertEqual(customer.id, None)
        self.assertEqual(customer.first_name, "allen")
        self.assertEqual(customer.last_name, "zhang")
        self.assertEqual(customer.userid, "allenzhang")
        self.assertEqual(customer.password, "devops2022")
        customer.create()
        customer = Customer(first_name="allen", last_name="zhang",
                            userid="allenzhang", password="customers2022")
        self.assertRaises(DataValidationError, customer.create)

    def test_update_a_customer_to_existing_userid(self):
        """Update customer userid to existing userid"""

        customer = Customer(first_name="allen", last_name="zhang",
                            userid="allenzhang", password="devops2022")
        self.assertTrue(customer != None)
        self.assertEqual(customer.id, None)
        self.assertEqual(customer.first_name, "allen")
        self.assertEqual(customer.last_name, "zhang")
        self.assertEqual(customer.userid, "allenzhang")
        self.assertEqual(customer.password, "devops2022")
        customer.create()
        customer = Customer(first_name="allen", last_name="zhang",
                            userid="allenzhang2", password="customers2022")
        self.assertTrue(customer != None)
        self.assertEqual(customer.id, None)
        self.assertEqual(customer.first_name, "allen")
        self.assertEqual(customer.last_name, "zhang")
        self.assertEqual(customer.userid, "allenzhang2")
        self.assertEqual(customer.password, "customers2022")
        customer.create()
        customer.userid="allenzhang"
        self.assertRaises(DataValidationError, customer.update)