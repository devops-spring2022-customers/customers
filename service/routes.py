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
import json
from werkzeug.exceptions import NotFound
from flask import Flask, jsonify, request, url_for, make_response, abort
from . import status  # HTTP Status Codes

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Customer, DataValidationError

# Import Flask application
from . import app

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    app.logger.info("Request for Root URL")
    return (
        jsonify(
            name="Customer Demo REST API Service",
            version="1.0",
            #paths=url_for("list_customers", _external=True),
        ),
        status.HTTP_200_OK,
    )

######################################################################
# LIST ALL CUSTOMERS
######################################################################
@app.route("/customers", methods=["GET"])
def list_customers():
    """Returns all of the customer"""
    app.logger.info('Request to list Customers...')
    customer = Customer.all()
    customer_list = [x.serialize() for x in customer]
    new_dict = {}
    for item in customer_list:
        name = item['id']
        new_dict[name] = item
    return new_dict, status.HTTP_200_OK

    #return None


######################################################################
# RETRIEVE A CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customers(customer_id):
    """
    Retrieve a single customer

    This endpoint will return a Customer based on it's id
    """
    app.logger.info("Request for customer with id: %s", customer_id)
    customer = Customer.find(customer_id)
    if not customer:
        raise NotFound("Customer with id '{}' was not found.".format(customer_id))

    app.logger.info("Returning customer: %s", customer.first_name)
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)

######################################################################
# ADD A NEW CUSTOMER
######################################################################
@app.route("/customers", methods=["POST"])
def create_customers():
    """
    Creates a Customer
    This endpoint will create a Customer based the data in the body that is posted
    """
    app.logger.info("Request to create a customer")
    check_content_type("application/json")
    customer = Customer()
    customer.deserialize(request.get_json())
    customer.create()
    message = customer.serialize()
    location_url = url_for("get_customers", customer_id=customer.id, _external=True)

    app.logger.info("Customer with ID [%s] created.", customer.id)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )


######################################################################
# UPDATE AN EXISTING CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>", methods=["PUT"])
def update_customers(customer_id):
    """
    Update a Customer
    This endpoint will update a Customer based the body that is posted
    """

    app.logger.info("Requesting to update a customer")
    check_content_type("application/json")
    customer = Customer.find(customer_id)
    customer.deserialize(request.get_json())
    customer.customer_id = customer_id
    customer.update()
    app.logger.info("Updated customer with id %s", customer.customer_id)
    
    
    return customer.serialize(), status.HTTP_200_OK

######################################################################
# DELETE A CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customers(customer_id):
    """
    Delete a Customer

    This endpoint will delete a Customer based the id specified in the path
    """
    app.logger.info("Request to delete customer with id: %s", customer_id)
    customer = Customer.find(customer_id)
    if customer:
        customer.delete()

    app.logger.info("Customer with ID [%s] delete complete.", customer_id)
    return make_response("", status.HTTP_204_NO_CONTENT)

'''
'''
######################################################################
# RETRIEVE A CUSTOMER'S ADDRESSES
######################################################################
@app.route("/customers/<int:customer_id>/addresses", methods=["GET"])
def get_customers_addresses(customer_id):
    """
    Retrieve a single customer's addresses

    This endpoint will return a Customer's addresses based on it's id
    """
    app.logger.info("Request for addresses with id: %s", customer_id)
    customer = Customer.find(customer_id)
    if not customer:
        raise NotFound("Customer with id '{}' was not found.".format(customer_id))

    app.logger.info("Returning addresses of customer: %s, %s with addresses: %s", customer.first_name,customer.last_name, customer.addresses)
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE A CUSTOMER'S ADDRESS
######################################################################
@app.route("/customers/<int:customer_id>/addresses", methods=["DELETE"])
def delete_customers_addresses(customer_id):
    """
    DELETE a Customer's address

    This endpoint will delete a Customer's address based the id and address 
    specified in the path and the body that is posted
    """

    app.logger.info("Request to delete customer address with id: %s", customer_id)
    customer = Customer.find(customer_id)
    if customer:
        customer.delete_addresses()

    app.logger.info("Customer with ID [%s] 's addresses delete complete.", customer_id)
    return make_response("", status.HTTP_204_NO_CONTENT)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    Customer.init_db(app)

def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "Content-Type must be {}".format(media_type),
    )
