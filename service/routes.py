"""
Customer Service

Paths:
------
GET /customers - Returns a list all of all Customers
GET /customers/{id} - Returns the Customer with a given id number
POST /customers - creates a new Customer record in the database
PUT /customers/{id} - updates a Customer record in the database
DELETE /customers/{id} - deletes a Customer record in the database
"""

import os
import sys
import logging
from functools import wraps
import json
from werkzeug.exceptions import NotFound
from flask import Flask, jsonify, request, url_for, make_response, abort, render_template
from flask_restx import Api, Resource, fields, reqparse, inputs
from . import status  # HTTP Status Codes

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Address, Customer, DataValidationError

# Import Flask application
from . import app

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    app.logger.info("Request for Root URL")
    return app.send_static_file("index.html")

######################################################################
# Configure Swagger before initializing it
######################################################################
api = Api(app,
          version='1.0.0',
          title='Customer Demo REST API Service',
          description='This is a sample server Customer Catalog server.',
          default='customers',
          default_label='Customer Catalog operations',
          doc='/apidocs', # default also could use doc='/apidocs/'
          prefix='/' # /api if doesn't work
         )

# Define the model so that the docs reflect what can be sent
create_addr_model = api.model('Address', {
    'street': fields.String(required=True,
                          description='The first name of the Customer'),
    'city': fields.String(required=True,
                          description='The last name of the Customer'),
    'state': fields.String(required=False,
                              description='The userid of the Customer'),
    'postal_code': fields.String(required=False,
                                description='The password of the Customer'),
})

address_model = api.inherit(
    'AddressModel', 
    create_addr_model,
    {
        'id': fields.Integer(readOnly=True,
                            description='The unique id assigned internally by service'),
        'customer_id': fields.Integer(readOnly=True,
                            description='The unique customer id foreign key assigned internally by service'),
    }
)

# Define the model so that the docs reflect what can be sent
create_model = api.model('Customer', {
    'first_name': fields.String(required=True,
                          description='The first name of the Customer'),
    'last_name': fields.String(required=True,
                          description='The last name of the Customer'),
    'userid': fields.String(required=False,
                              description='The userid of the Customer'),
    'password': fields.String(required=False,
                                description='The password of the Customer'),
    'active': fields.Boolean(required=False,
                                description='The status of the Customer Account (active/inactive)'),
    "addresses": fields.List(fields.Nested(address_model)),
})

customer_model = api.inherit(
    'CustomerModel', 
    create_model,
    {
        'id': fields.Integer(readOnly=True,
                            description='The unique id assigned internally by service'),
    }
)

# query string arguments
customer_args = reqparse.RequestParser()
customer_args.add_argument('first_name', type=str, required=False, help='List Customers by first name')
customer_args.add_argument('last_name', type=str, required=False, help='List Customers by last name')
customer_args.add_argument('userid', type=str, required=False, help='List Customers by user id')
#customer_args.add_argument('active', type=inputs.boolean, required=False, help='List Customers by active status')

######################################################################
#  PATH: /customers/{id}
######################################################################
@api.route('/customers/<customer_id>')
@api.param('customer_id', 'The Customer identifier')
class CustomerResource(Resource):
    """
    CustomerResource class
    Allows the manipulation of a single Customer
    GET /customer{id} - Returns a Customer with the id
    PUT /customer{id} - Update a Customer with the id
    DELETE /customer{id} -  Deletes a Customer with the id
    """
    #------------------------------------------------------------------
    # RETRIEVE A CUSTOMER
    #------------------------------------------------------------------
    @api.doc('get_customers')
    @api.response(404, 'Customer not found')
    @api.marshal_with(customer_model)
    def get(self, customer_id):
        """
        Retrieve a single customer

        This endpoint will return a Customer based on it's id
        """
        app.logger.info("Request for customer with id: %s", customer_id)
        customer = Customer.find(customer_id)
        if not customer:
            abort(status.HTTP_404_NOT_FOUND, "Customer with id '{}' was not found.".format(customer_id))

        app.logger.info("Returning customer: %s", customer.first_name)
        return customer.serialize(), status.HTTP_200_OK
    
    #------------------------------------------------------------------
    # UPDATE AN EXISTING Customer
    #------------------------------------------------------------------
    @api.doc('update_customers')
    @api.response(404, 'Customer not found')
    @api.response(400, 'The posted Customer data was not valid')
    @api.expect(customer_model)
    @api.marshal_with(customer_model)
    def put(self, customer_id):
        """
        Update a Customer
        This endpoint will update a Customer based the body that is posted
        """
        app.logger.info("Requesting to update a customer")
        customer = Customer.find(customer_id)
        # if not customer:
        #     abort(status.HTTP_404_NOT_FOUND, "Customer with id '{}' was not found.".format(customer_id))
        
        app.logger.debug('Payload = %s', api.payload)
        data = api.payload
        customer.deserialize(data)
        customer.id = customer_id
        customer.update()
        app.logger.info("Updated customer with id %s", customer.id)
        
        return customer.serialize(), status.HTTP_200_OK
    
    #------------------------------------------------------------------
    # DELETE A CUSTOMER
    #------------------------------------------------------------------
    @api.doc('delete_customers')
    @api.response(204, 'Customer deleted')
    def delete(self, customer_id):
        """
        Delete a Customer

        This endpoint will delete a Customer based the id specified in the path
        """
        app.logger.info("Request to delete customer with id: %s", customer_id)
        customer = Customer.find(customer_id)
        if customer:
            for addr in customer.addresses:
                address_id = addr.id
                address = Address.find(address_id)
                if address:
                    address.delete()
            customer.delete()

        app.logger.info("Customer with ID [%s] delete complete.", customer_id)
        return '', status.HTTP_204_NO_CONTENT

######################################################################
#  PATH: /customers
######################################################################
@api.route('/customers', strict_slashes=False)
class CustomerCollection(Resource):
    """ Handles all interactions with collections of Customers """
    #------------------------------------------------------------------
    # LIST ALL CUSTOMERS
    #------------------------------------------------------------------
    @api.doc('list_customers')
    @api.expect(customer_args, validate=True)
    @api.marshal_list_with(customer_model)
    def get(self):
        """Returns all of the customer"""
        app.logger.info("Request for Customer list")
        customers = []
        args = customer_args.parse_args()
        if args['first_name']:
            app.logger.info('Filtering by first name: %s', args['first_name'])
            customers = Customer.find_by_first_name(args['first_name'])
        elif args['last_name']:
            app.logger.info('Filtering by last name: %s', args['last_name'])
            customers = Customer.find_by_last_name(args['last_name'])
        elif args['userid']:
            app.logger.info('Filtering by userid: %s', args['userid'])
            customers = Customer.find_by_userid(args['userid'])
        else:
            app.logger.info('Returning unfiltered list.')
            customers = Customer.all()

        app.logger.info('[%s] Customers returned', len(customers))
        results = [customer.serialize() for customer in customers]
        return results, status.HTTP_200_OK
    
    #------------------------------------------------------------------
    # ADD A NEW CUSTOMER
    #------------------------------------------------------------------
    @api.doc('create_customers')
    @api.response(415, 'The posted data has unsupported media type')
    @api.response(400, 'The posted data was not valid')
    @api.expect(create_model)
    @api.marshal_with(customer_model, code=201)
    def post(self):
        """
        Creates a Customer
        This endpoint will create a Customer based the data in the body that is posted
        """
        app.logger.info("Request to create a customer")
        customer = Customer()
        app.logger.debug('Payload = %s', api.payload)
        customer.deserialize(api.payload)
        customer.create()
        app.logger.info("Customer with ID [%s] created.", customer.id)
        location_url = api.url_for(CustomerResource, customer_id=customer.id, _external=True)
        return customer.serialize(), status.HTTP_201_CREATED, {"Location": location_url}
    
######################################################################
#  PATH: /customers/{id}/activate
######################################################################
@api.route('/customers/<customer_id>/activate')
@api.param('customer_id', 'The Customer identifier')
class ActivateResource(Resource):
    @api.doc('activate_customer')
    @api.response(404, 'Customer not found')
    def put(self, customer_id):
        """
        Activate an existing Customer
        This endpoint will update a Customer's active field
        """

        app.logger.info("Requesting to update a customer")
        customer = Customer.find(customer_id)
        if not customer:
            abort(status.HTTP_404_NOT_FOUND, "Customer with id '{}' was not found.".format(customer_id))
        customer.active = True
        customer.update()
        app.logger.info("Updated customer with id %s", customer.id)
        
        return customer.serialize(), status.HTTP_200_OK
######################################################################
#  PATH: /customers/{id}/deactivate
######################################################################
@api.route('/customers/<customer_id>/deactivate')
@api.param('customer_id', 'The Customer identifier')
class DeactivateResource(Resource):
    @api.doc('deactivate_customer')
    @api.response(404, 'Customer not found')
    def put(self, customer_id):
        """
        Dectivate an existing Customer
        This endpoint will update a Customer's active field
        """

        app.logger.info("Requesting to update a customer")
        customer = Customer.find(customer_id)
        if not customer:
            abort(status.HTTP_404_NOT_FOUND, "Customer with id '{}' was not found.".format(customer_id))
        customer.active = False
        customer.update()
        app.logger.info("Updated customer with id %s", customer.id)
        
        return customer.serialize(), status.HTTP_200_OK


######################################################################
#  PATH: /customers/{customer_id}/addresses/{address_id}
######################################################################
@api.route('/customers/<customer_id>/addresses/<address_id>')
@api.param('customer_id', 'The Customer identifier')
@api.param('address_id', 'The Address identifier')
class AddressResource(Resource):
    """
    AddressResource class
    Allows the manipulation of a single Address
    GET /customer{id}/address{id} - Returns an address with the id
    PUT /customer{id}/address{id} - Update an address with the id
    DELETE /customer{id}/address{id} -  Deletes an address with the id
    """
    #------------------------------------------------------------------
    # RETRIEVE AN ADDRESS
    #------------------------------------------------------------------
    @api.doc('get_addresses')
    @api.response(404, 'Address not found')
    @api.marshal_with(address_model)
    def get(self, customer_id, address_id):
        """
        Retrieve a single customer's addresses

        This endpoint will return a Customer's addresses based on it's id
        """

        app.logger.info("Request for customer with id: %s", customer_id)
        customer = Customer.find(customer_id)
        if not customer:
            abort(status.HTTP_404_NOT_FOUND, "Customer with id '{}' was not found.".format(customer_id))

        app.logger.info("Request to get an address with id: %s", address_id)
        address = Address.find_or_404(address_id)
        return address.serialize(), status.HTTP_200_OK
    
    #------------------------------------------------------------------
    # UPDATE AN EXISTING Customer
    #------------------------------------------------------------------
    @api.doc('update_addresses')
    @api.response(404, 'Address not found')
    @api.response(400, 'The posted Address data was not valid')
    @api.expect(address_model)
    @api.marshal_with(address_model)
    def put(self, customer_id, address_id):
        """
        Update an Address
        This endpoint will update an Address based the body that is posted
        """
        app.logger.info("Request for customer with id: %s", customer_id)
        customer = Customer.find(customer_id)
        if not customer:
            abort(status.HTTP_404_NOT_FOUND, "Customer with id '{}' was not found.".format(customer_id))

        app.logger.info("Request to update address with id: %s", address_id)
        address = Address.find_or_404(address_id)
        app.logger.debug('Payload = %s', api.payload)
        data = api.payload
        address.deserialize(data)
        address.id = address_id
        address.update()
        app.logger.info("Updated address with id %s", address.id)
        
        return address.serialize(), status.HTTP_200_OK
    
    #------------------------------------------------------------------
    # DELETE A CUSTOMER
    #------------------------------------------------------------------
    @api.doc('delete_addresses')
    @api.response(204, 'Address deleted')
    def delete(self, customer_id, address_id):
        """
        Delete an Address
        This endpoint will delete an Address based the id specified in the path
        """
        app.logger.info("Request for customer with id: %s", customer_id)
        customer = Customer.find(customer_id)
        if not customer:
            abort(status.HTTP_404_NOT_FOUND, "Customer with id '{}' was not found.".format(customer_id))

        app.logger.info("Request to delete address with id: %s", address_id)
        address = Address.find(address_id)
        if address:
            address.delete()
        return make_response("", status.HTTP_204_NO_CONTENT)

######################################################################
#  PATH: /customers/{customer_id}/addresses
######################################################################
@api.route('/customers/<customer_id>/addresses', strict_slashes=False)
class AddressCollection(Resource):
    """ Handles all interactions with collections of Customers """
    #------------------------------------------------------------------
    # LIST ALL CUSTOMERS
    #------------------------------------------------------------------
    @api.doc('list_addresses')
    @api.marshal_list_with(address_model)
    def get(self, customer_id):
        """ Returns all of the Addresses for a customer """
        app.logger.info("Request for Customer Addresses...")
        customer = Customer.find_or_404(customer_id)
        results = [address.serialize() for address in customer.addresses]
        return results, status.HTTP_200_OK
    
    #------------------------------------------------------------------
    # ADD A NEW CUSTOMER
    #------------------------------------------------------------------
    @api.doc('create_addresses')
    @api.response(415, 'The posted data has unsupported media type')
    @api.response(400, 'The posted data was not valid')
    @api.expect(create_addr_model)
    @api.marshal_with(address_model, code=201)
    def post(self, customer_id):
        """
        Create an Address on a Customer
        This endpoint will add an address to a customer
        """
        app.logger.info("Request to add an address to a customer")
        customer = Customer.find_or_404(customer_id)
        address = Address()
        app.logger.debug('Payload = %s', api.payload)
        address.deserialize(api.payload)
        customer.addresses.append(address)
        customer.update()
        message = address.serialize()
        return address.serialize(), status.HTTP_201_CREATED

# ######################################################################
# # LIST ALL CUSTOMERS
# ######################################################################
# @app.route("/customers", methods=["GET"])
# def list_customers():
#     """Returns all of the customer"""
#     app.logger.info("Request for Customer list")
#     customers = []
#     id = request.args.get("id")
#     first_name = request.args.get("first_name")
#     last_name = request.args.get("last_name")
#     userid = request.args.get("userid")
#     if id:
#         customers = Customer.find_by_id(id)
#     elif first_name:
#         customers = Customer.find_by_first_name(first_name)
#     elif last_name:
#         customers = Customer.find_by_last_name(last_name)
#     elif userid:
#         customers = Customer.find_by_userid(userid)
#     else:
#         customers = Customer.all()

#     results = [customer.serialize() for customer in customers]
#     return make_response(jsonify(results), status.HTTP_200_OK)


# ######################################################################
# # RETRIEVE A CUSTOMER
# ######################################################################
# @app.route("/customers/<int:customer_id>", methods=["GET"])
# def get_customers(customer_id):
#     """
#     Retrieve a single customer

#     This endpoint will return a Customer based on it's id
#     """
#     app.logger.info("Request for customer with id: %s", customer_id)
#     customer = Customer.find(customer_id)
#     if not customer:
#         raise NotFound("Customer with id '{}' was not found.".format(customer_id))

#     app.logger.info("Returning customer: %s", customer.first_name)
#     return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)

######################################################################
# ADD A NEW CUSTOMER
######################################################################
# @app.route("/customers", methods=["POST"])
# def create_customers():
#     """
#     Creates a Customer
#     This endpoint will create a Customer based the data in the body that is posted
#     """
#     app.logger.info("Request to create a customer")
#     check_content_type("application/json")
#     customer = Customer()
#     request_body = request.get_json()
#     customer.deserialize(request_body)
#     customer.create()
#     message = customer.serialize()
#     location_url = url_for("get_customers", customer_id=customer.id, _external=True)

#     app.logger.info("Customer with ID [%s] created.", customer.id)
#     return make_response(
#         jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
#     )


# ######################################################################
# # UPDATE AN EXISTING CUSTOMER
# ######################################################################
# @app.route("/customers/<int:customer_id>", methods=["PUT"])
# def update_customers(customer_id):
#     """
#     Update a Customer
#     This endpoint will update a Customer based the body that is posted
#     """

#     app.logger.info("Requesting to update a customer")
#     check_content_type("application/json")
#     customer = Customer.find(customer_id)
#     if not customer:
#         raise NotFound("Customer with id '{}' was not found.".format(customer_id))
#     customer.deserialize(request.get_json())
#     customer.customer_id = customer_id
#     customer.update()
#     app.logger.info("Updated customer with id %s", customer.customer_id)
    
    
#     return customer.serialize(), status.HTTP_200_OK

# ######################################################################
# # ACTIVATE AN EXISTING CUSTOMER
# ######################################################################
# @app.route("/customers/<int:customer_id>/activate", methods=["PUT"])
# def activate_customers(customer_id):
#     """
#     Activate an existing Customer
#     This endpoint will update a Customer's active field
#     """

#     app.logger.info("Requesting to update a customer")
#     check_content_type("application/json")
#     customer = Customer.find(customer_id)
#     #customer.deserialize(request.get_json())
#     if not customer:
#         raise NotFound("Customer with id '{}' was not found.".format(customer_id))
#     customer.customer_id = customer_id
#     customer.active = True
#     customer.update()
#     app.logger.info("Updated customer with id %s", customer.customer_id)
    
    
#     return customer.serialize(), status.HTTP_200_OK

# ######################################################################
# # DEACTIVATE AN EXISTING CUSTOMER
# ######################################################################
# @app.route("/customers/<int:customer_id>/deactivate", methods=["PUT"])
# def deactivate_customers(customer_id):
#     """
#     Deactivate an existing Customer
#     This endpoint will update a Customer's active field
#     """

#     app.logger.info("Requesting to update a customer")
#     check_content_type("application/json")
#     customer = Customer.find(customer_id)
#     #customer.deserialize(request.get_json())
#     if not customer:
#         raise NotFound("Customer with id '{}' was not found.".format(customer_id))
#     customer.customer_id = customer_id
#     customer.active = False
#     customer.update()
#     app.logger.info("Updated customer with id %s", customer.customer_id)
    
#     return customer.serialize(), status.HTTP_200_OK

# ######################################################################
# # DELETE A CUSTOMER
# ######################################################################
# @app.route("/customers/<int:customer_id>", methods=["DELETE"])
# def delete_customers(customer_id):
#     """
#     Delete a Customer

#     This endpoint will delete a Customer based the id specified in the path
#     """
#     app.logger.info("Request to delete customer with id: %s", customer_id)
#     customer = Customer.find(customer_id)
#     if customer:
#         for addr in customer.addresses:
#             address_id = addr.id
#             address = Address.find(address_id)
#             if address:
#                 address.delete()
#         customer.delete()

#     app.logger.info("Customer with ID [%s] delete complete.", customer_id)
#     return make_response("", status.HTTP_204_NO_CONTENT)

# ######################################################################
# # LIST ADDRESSES
# ######################################################################
# @app.route("/customers/<int:customer_id>/addresses", methods=["GET"])
# def list_addresses(customer_id):
#     """ Returns all of the Addresses for a customer """
#     app.logger.info("Request for Customer Addresses...")
#     customer = Customer.find_or_404(customer_id)
#     results = [address.serialize() for address in customer.addresses]
#     return make_response(jsonify(results), status.HTTP_200_OK)

# ######################################################################
# # ADD AN ADDRESS TO CUSTOMER
# ######################################################################
# @app.route("/customers/<int:customer_id>/addresses", methods=["POST"])
# def post_customers_addresses(customer_id):
#     """
#     Create an Address on a Customer
#     This endpoint will add an address to a customer
#     """
#     app.logger.info("Request to add an address to a customer")
#     check_content_type("application/json")
#     customer = Customer.find_or_404(customer_id)
#     address = Address()
#     address.deserialize(request.get_json())
#     customer.addresses.append(address)
#     customer.update()
#     message = address.serialize()
#     return make_response(jsonify(message), status.HTTP_201_CREATED)

# ######################################################################
# # RETRIEVE A CUSTOMER'S ADDRESSES
# ######################################################################
# @app.route("/customers/<int:customer_id>/addresses/<int:address_id>", methods=["GET"])
# def get_customers_addresses(customer_id, address_id):
#     """
#     Retrieve a single customer's addresses

#     This endpoint will return a Customer's addresses based on it's id
#     """
#     app.logger.info("Request to get an address with id: %s", address_id)
#     address = Address.find_or_404(address_id)
#     return make_response(jsonify(address.serialize()), status.HTTP_200_OK)

# ######################################################################
# # UPDATE AN ADDRESS
# ######################################################################
# @app.route("/customers/<int:customer_id>/addresses/<int:address_id>", methods=["PUT"])
# def update_customers_addresses(customer_id, address_id):
#     """
#     Update an Address
#     This endpoint will update an Address based the body that is posted
#     """
#     app.logger.info("Request to update address with id: %s", address_id)
#     check_content_type("application/json")
#     address = Address.find_or_404(address_id)
#     address.deserialize(request.get_json())
#     address.id = address_id
#     address.update()
#     return make_response(jsonify(address.serialize()), status.HTTP_200_OK)

# ######################################################################
# # DELETE AN ADDRESS
# ######################################################################
# @app.route("/customers/<int:customer_id>/addresses/<int:address_id>", methods=["DELETE"])
# def delete_customers_addresses(customer_id, address_id):
#     """
#     Delete an Address
#     This endpoint will delete an Address based the id specified in the path
#     """
#     app.logger.info("Request to delete customer with id: %s", customer_id)
#     address = Address.find(address_id)
#     if address:
#         address.delete()
#     return make_response("", status.HTTP_204_NO_CONTENT)

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    Customer.init_db(app)

# def check_content_type(media_type):
#     """Checks that the media type is correct"""
#     content_type = request.headers.get("Content-Type")
#     if content_type and content_type == media_type:
#         return
#     app.logger.error("Invalid Content-Type: %s", content_type)
#     abort(
#         status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
#         "Content-Type must be {}".format(media_type),
#     )
