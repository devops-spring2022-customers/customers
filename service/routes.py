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
            paths=url_for("list_customers", _external=True),
        ),
        status.HTTP_200_OK,
    )

######################################################################
# LIST ALL CUSTOMERS
######################################################################
@app.route("/customers", methods=["GET"])
def list_customers():
    """Returns all of the customer"""

    return None


######################################################################
# RETRIEVE A CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customers(customer_id):
    """
    Retrieve a single customer

    This endpoint will return a Customer based on it's id
    """
    
    return None

######################################################################
# ADD A NEW CUSTOMER
######################################################################
@app.route("/customers", methods=["POST"])
def create_customers():
    """
    Creates a Customer
    This endpoint will create a Customer based the data in the body that is posted
    """
    
    return None


######################################################################
# UPDATE AN EXISTING CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>", methods=["PUT"])
def update_customers(customer_id):
    """
    Update a Customer

    This endpoint will update a Customer based the body that is posted
    """
    
    return None


######################################################################
# DELETE A CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customers(customer_id):
    """
    Delete a Customer

    This endpoint will delete a Customer based the id specified in the path
    """
    
    return None

######################################################################
# RETRIEVE A CUSTOMER'S ADDRESSES
######################################################################
@app.route("/customers/<int:customer_id>/addresses", methods=["GET"])
def get_customers_addresses(customer_id):
    """
    Retrieve a single customer's addresses

    This endpoint will return a Customer's addresses based on it's id
    """
    
    return None

######################################################################
# UPDATE A CUSTOMER'S ADDRESSES
######################################################################
@app.route("/customers/<int:customer_id>/addresses", methods=["PUT"])
def update_customers_addresses(customer_id):
    """
    Update a Customer's addresses

    This endpoint will update a Customer's addresses based the body that is posted
    """
    
    return None

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
    
    return None


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    Customer.init_db(app)
