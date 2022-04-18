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

from .factories import AddressFactory, CustomerFactory

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
        """Factory method to create customers in bulk"""
        customers = []
        for _ in range(count):
            test_customer = CustomerFactory()
            test_customer.userid = "userid{}".format(_)
            resp = self.app.post(
                BASE_URL, json=test_customer.serialize(), content_type=CONTENT_TYPE_JSON
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test customer"
            )
            new_customer = resp.get_json()
            test_customer.id = new_customer["id"]
            customers.append(test_customer)
        return customers

    # def test_index(self):
    #     """Test the Home Page"""
    #     resp = self.app.get("/")
    #     self.assertEqual(resp.status_code, status.HTTP_200_OK)
    #     data = resp.get_json()
    #     self.assertEqual(data["name"], "Customer Demo REST API Service")

    def test_get_customer_not_found(self):
        """Get a Customer thats not found"""
        resp = self.app.get("/customers/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_post_customer_by_id_not_allowed(self):
        """Post a Customer by id (Not allowed method)"""
        resp = self.app.post("/customers/0")
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_customer(self):
        """Create a new Customer"""
        test_customer = CustomerFactory()
        logging.debug(test_customer)
        resp = self.app.post(
            BASE_URL, json=test_customer.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)
        # Check the data is correct
        new_customer = resp.get_json()
        self.assertEqual(new_customer["first_name"], test_customer.first_name, "First name does not match")
        self.assertEqual(new_customer["last_name"], test_customer.last_name, "Last name does not match")
        self.assertEqual(new_customer["userid"], test_customer.userid, "Userid does not match")
        self.assertEqual(new_customer["password"], test_customer.password, "Password does not match")
        self.assertEqual(new_customer["addresses"], test_customer.addresses, "Addresses does not match")
        # Check that the location header was correct
        resp = self.app.get(location, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_customer = resp.get_json()
        self.assertEqual(new_customer["first_name"], test_customer.first_name, "First name does not match")
        self.assertEqual(new_customer["last_name"], test_customer.last_name, "Last name does not match")
        self.assertEqual(new_customer["userid"], test_customer.userid, "Userid does not match")
        self.assertEqual(new_customer["password"], test_customer.password, "Password does not match")
        self.assertEqual(new_customer["addresses"], test_customer.addresses, "Addresses does not match")

    def test_create_customer_no_data(self):
        """Create a Customer with missing data"""
        resp = self.app.post(BASE_URL, json={}, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_customer_no_content_type(self):
        """Create a Customer with no content type"""
        resp = self.app.post(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_customer_bad_first_name(self):
        """ Create a Customer with bad first name """
        test_customer = CustomerFactory()
        logging.debug(test_customer)
        # change available to a string
        test_customer.first_name = 123
        resp = self.app.post(
            BASE_URL, json=test_customer.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_customer_bad_last_name(self):
        """ Create a Customer with bad last name """
        test_customer = CustomerFactory()
        logging.debug(test_customer)
        # change available to a string
        test_customer.last_name = True
        resp = self.app.post(
            BASE_URL, json=test_customer.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_customer_bad_url(self):
        """Create a Customer with wrong url"""
        test_customer = CustomerFactory()
        logging.debug(test_customer)
        resp = self.app.post(
            BASE_URL+"s", json=test_customer.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update(self):
        """Update a customer's firstname"""

        random_customers = CustomerFactory()
        resp = self.app.post(
            BASE_URL, json=random_customers.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        
        new_customer = resp.get_json()
        new_customer["first_name"] = "Jash"

        resp = self.app.put("/customers/{}".format(new_customer["id"]), json = new_customer, content_type = CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        updated_customer  = resp.get_json()
        self.assertEqual(new_customer["id"],updated_customer["id"])
        self.assertEqual(new_customer["first_name"], updated_customer["first_name"])
    
    def test_bad_request(self):
        """ Send wrong parameters in json """
        customer = CustomerFactory()
        resp = self.app.post(
            "/customers", 
            json={"name": "not enough data"}, 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsupported_media_type(self):
        """ Send wrong media type """
        customer = CustomerFactory()
        resp = self.app.post(
            "/customers", 
            json=customer.serialize(), 
            content_type="test/html"
        )
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_method_not_allowed(self):
        """ Make an illegal method call """
        resp = self.app.put(
            "/customers", 
            json={"not": "today"}, 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_all(self):
        """Get all customers"""
        self._create_customers(3)
        res = self.app.get(BASE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = res.get_json()
        self.assertEqual(len(res_data),3)

    def test_delete_customer(self):
        """Delete a customer"""
        test_customer = self._create_customers(1)[0]
        resp = self.app.delete(
            "{0}/{1}".format(BASE_URL, test_customer.id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get(
            "{0}/{1}".format(BASE_URL, test_customer.id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_address_list(self):
        """ Get a list of Addresses """
        # add two addresses to customer
        customer = self._create_customers(1)[0]
        address_list = AddressFactory.create_batch(2)

        # Create address 1
        resp = self.app.post(
            "/customers/{}/addresses".format(customer.id), 
            json=address_list[0].serialize(), 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Create address 2
        resp = self.app.post(
            "/customers/{}/addresses".format(customer.id), 
            json=address_list[1].serialize(), 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # get the list back and make sure there are 2
        resp = self.app.get(
            "/customers/{}/addresses".format(customer.id), 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        self.assertEqual(len(data), 2)

    def test_add_address(self):
        """ Add an address to a customer """
        customer = self._create_customers(1)[0]
        address = AddressFactory()
        resp = self.app.post(
            "/customers/{}/addresses".format(customer.id), 
            json=address.serialize(), 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["customer_id"], customer.id)
        self.assertEqual(data["street"], address.street)
        self.assertEqual(data["city"], address.city)
        self.assertEqual(data["state"], address.state)
        self.assertEqual(data["postal_code"], address.postal_code)

    def test_get_address(self):
        """ Get an address from a customer """
        # create a known address
        customer = self._create_customers(1)[0]
        address = AddressFactory()
        resp = self.app.post(
            "/customers/{}/addresses".format(customer.id), 
            json=address.serialize(), 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        data = resp.get_json()
        logging.debug(data)
        address_id = data["id"]

        # retrieve it back
        resp = self.app.get(
            "/customers/{}/addresses/{}".format(customer.id, address_id), 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["customer_id"], customer.id)
        self.assertEqual(data["street"], address.street)
        self.assertEqual(data["city"], address.city)
        self.assertEqual(data["state"], address.state)
        self.assertEqual(data["postal_code"], address.postal_code)

    def test_update_address(self):
        """ Update an address on a customer """
        # create a known address
        customer = self._create_customers(1)[0]
        address = AddressFactory()
        resp = self.app.post(
            "/customers/{}/addresses".format(customer.id), 
            json=address.serialize(), 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        data = resp.get_json()
        logging.debug(data)
        address_id = data["id"]
        data["street"] = "XXXX"

        # send the update back
        resp = self.app.put(
            "/customers/{}/addresses/{}".format(customer.id, address_id), 
            json=data, 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # retrieve it back
        resp = self.app.get(
            "/customers/{}/addresses/{}".format(customer.id, address_id), 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["id"], address_id)
        self.assertEqual(data["customer_id"], customer.id)
        self.assertEqual(data["street"], "XXXX")

    def test_delete_address(self):
        """ Delete an Address """
        customer = self._create_customers(1)[0]
        address = AddressFactory()
        resp = self.app.post(
            "/customers/{}/addresses".format(customer.id), 
            json=address.serialize(), 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        logging.debug(data)
        address_id = data["id"]

        # send delete request
        resp = self.app.delete(
            "/customers/{}/addresses/{}".format(customer.id, address_id),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        # retrieve it back and make sure address is not there
        resp = self.app.get(
            "/customers/{}/addresses/{}".format(customer.id, address_id), 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_activate_existing_customer(self):
        """Activate existing customer"""

        random_customers = CustomerFactory()
        random_customers.active = False
        resp = self.app.post(
            BASE_URL, json=random_customers.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        
        new_customer = resp.get_json()
        self.assertEqual(new_customer["active"], False)

        resp = self.app.put("/customers/{}/activate".format(new_customer["id"]), json = {}, content_type = CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        updated_customer  = resp.get_json()
        self.assertEqual(new_customer["id"],updated_customer["id"])
        self.assertEqual(new_customer["first_name"], updated_customer["first_name"])
        self.assertEqual(updated_customer["active"], True)

    def test_activate_non_existing_customer(self):
        """Activate non existing customer"""

        random_customers = CustomerFactory()
        random_customers.active = False
        resp = self.app.post(
            BASE_URL, json=random_customers.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        
        new_customer = resp.get_json()
        self.assertEqual(new_customer["active"], False)

        resp = self.app.put("/customers/{}/activate".format("123"), json = {}, content_type = CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_deactivate_existing_customer(self):
        """Deactivate existing customer"""

        random_customers = CustomerFactory()
        random_customers.active = True
        resp = self.app.post(
            BASE_URL, json=random_customers.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        
        new_customer = resp.get_json()
        self.assertEqual(new_customer["active"], True)

        resp = self.app.put("/customers/{}/deactivate".format(new_customer["id"]), json = {}, content_type = CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        updated_customer  = resp.get_json()
        self.assertEqual(new_customer["id"],updated_customer["id"])
        self.assertEqual(new_customer["first_name"], updated_customer["first_name"])
        self.assertEqual(updated_customer["active"], False)

        