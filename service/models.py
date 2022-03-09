"""
Models for Customer

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """

    pass

######################################################################
#  A D D R E S S   M O D E L
######################################################################
class Address(db.Model):
    """
    Class that represents an Address
    """

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    address = db.Column(db.String(64))

    def __repr__(self):
        return "<Address %r id=[%s] account[%s]>" % (self.name, self.id, self.customer_id)

    def __str__(self):
        return "%s " % (self.address)
    def serialize(self):
        """ Serializes a Address into a dictionary """
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "address": self.address,
        }

    def deserialize(self, data):
        """
        Deserializes a Address from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.address = data["address"]
        except KeyError as error:
            raise DataValidationError("Invalid Address: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Address: body of request contained" "bad or no data"
            )
        return self
    
    def create(self):
        """
        Creates an Address to the database
        """
        logger.info("Creating %s", self.address)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates an address to the database
        """
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()
        
    def delete(self):
        """ Removes an Address from the data store """
        logger.info("Deleting %s", self.address)
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the records in the database """
        logger.info("Processing all records")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a record by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_or_404(cls, by_id):
        """ Find a record by it's id """
        logger.info("Processing lookup or 404 for id %s ...", by_id)
        return cls.query.get_or_404(by_id)

######################################################################
#  C U S T O M E R  M O D E L
######################################################################

class Customer(db.Model):
    """
    Class that represents a <your resource model name>
    """

    app = None

    ##################################################
    # Table Schema
    ##################################################
    # Unique id, first name, last name, optional userid and password, addresses
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(63), nullable=False)
    last_name = db.Column(db.String(63), nullable=False)
    userid = db.Column(db.String(63), nullable=True)
    password = db.Column(db.String(63), nullable=True)
    addresses = db.relationship('Address', backref='customer', lazy=True)  

    def __repr__(self):
        return "<Customer %r id=[%s]>" % (self.first_name, self.id)

    def create(self):
        """
        Creates a Customer to the database
        """
        logger.info("Creating %s", self.first_name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Customer to the database
        """
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()
        
    def delete(self):
        """ Removes a Customer from the data store """
        logger.info("Deleting %s, %s", self.first_name, self.last_name)
        db.session.delete(self)
        db.session.commit()
    
    def delete_addresses(self):
        """ Removes a Customer address from the data store """
        logger.info("Deleting %s, %s 's addresses", self.first_name, self.last_name)
        # db.session.delete(self.addresses)
        self.addresses = []
        db.session.commit()
    

    def serialize(self):
        """ Serializes a Customer into a dictionary """
        return {
            "id": self.id, 
            "first_name": self.first_name,
            "last_name": self.last_name,
            "userid": self.userid,
            "password": self.password,
            "addresses": self.addresses,
        }

    def deserialize(self, data):
        """
        Deserializes a Customer from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            if isinstance(data["first_name"], str):
                self.first_name = data["first_name"]
            else:
                raise DataValidationError(
                    "Invalid type for string [first_name]: "
                    + str(type(data["first_name"]))
                )
            if isinstance(data["last_name"], str):
                self.last_name = data["last_name"]
            else:
                raise DataValidationError(
                    "Invalid type for string [last_name]: "
                    + str(type(data["last_name"]))
                )    
            
            if "userid" in data:
                self.userid = data["userid"]
            if "password" in data:
                self.password = data["password"]

            if isinstance(data["addresses"], list):
                if len(data["addresses"]) > 0:
                    for addr in data["addresses"]:
                        if not isinstance(addr, str):
                            raise DataValidationError(
                                "Invalid type for address for string [addresses]: "
                                + str(type(data["addresses"]))
                            )
                    self.addresses = data["addresses"]
                else:
                    raise DataValidationError(
                        "Invalid number of addresses for list [addresses]: "
                        + str(type(data["addresses"]))
                    )
            else:
                raise DataValidationError(
                    "Invalid type for list [addresses]: "
                    + str(type(data["addresses"]))
                )     

        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0])
        except KeyError as error:
            raise DataValidationError("Invalid Customer: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Customer: body of request contained bad or no data " + str(error)
            )
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the Customer in the database """
        logger.info("Processing all Customer")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a Customer by its id """

        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)


  
    @classmethod
    def find_or_404(cls, by_id):
        """ Find a Customer by its id """

        cls.logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)


    '''
    @classmethod
    def find_by_first_name(cls, first_name):
        """Returns all Customer with the given first name

        Args:
            name (string): the name of the Customer you want to match
        """

    @classmethod
    def find_by_last_name(cls, last_name):
        """Returns all Customer with the given last name

        Args:
            name (string): the name of the Customer you want to match
        """

    @classmethod
    def find_by_userid(cls, userid):
        """Returns all Customer with the given userid

        Args:
            name (string): the name of the Customer you want to match
        """
    '''
