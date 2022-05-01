"""
Models for Customer

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """

    pass
######################################################################
#  P E R S I S T E N T   B A S E   M O D E L
######################################################################
class PersistentBase():
    """ Base class added persistent methods """

    def create(self):
        """
        Creates a Customer to the database
        """
        logger.info("Creating %s", self.first_name)
        self.id = None  # id must be none to generate next primary key
        if self.active is None: # default active when created
            self.active = True
    
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise DataValidationError(
                "Userid already exists!"
            )
            # error, there already is a customer with this userid

    def update(self):
        """
        Updates a Customer to the database
        """
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise DataValidationError(
                "Userid already exists!"
            )
            # error, there already is a customer with this userid
    def delete(self):
        """ Removes a Customer from the data store """
        #logger.info("Deleting %s", self.first_name)
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
#  A D D R E S S   M O D E L
######################################################################
class Address(db.Model,PersistentBase):
    """
    Class that represents an Address
    """

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    street = db.Column(db.String(64))
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))
    postal_code = db.Column(db.String(64))

    # def __repr__(self):
    #     return "<Address %r id=[%s] customer[%s]>" % (self.name, self.id, self.customer_id)

    # def __str__(self):
    #     return "%s " % (self.address)
        
    def serialize(self):
        """ Serializes a Address into a dictionary """
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "street": self.street,
            "city": self.city,
            "state": self.state,
            "postal_code": self.postal_code,
        }

    def deserialize(self, data):
        """
        Deserializes a Address from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.street = data["street"]
            self.city = data["city"]
            self.state = data["state"]
            self.postal_code = data["postal_code"]
        except KeyError as error:
            raise DataValidationError("Invalid Address: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Address: body of request contained" "bad or no data"
            )
        return self

######################################################################
#  C U S T O M E R  M O D E L
######################################################################

class Customer(db.Model, PersistentBase):
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
    userid = db.Column(db.String(63), nullable=True, unique=True)
    password = db.Column(db.String(63), nullable=True)
    active = db.Column(db.Boolean(), nullable=False)
    addresses = db.relationship('Address', backref='customer', lazy=True)  

    def __repr__(self):
        return "<Customer %r id=[%s]>" % (self.first_name, self.id)
    
    def serialize(self):
        """ Serializes a Customer into a dictionary """
        customer = {
            "id": self.id, 
            "first_name": self.first_name,
            "last_name": self.last_name,
            "userid": self.userid,
            "password": self.password,
            "active": self.active,
            "addresses": []
        }
        for address in self.addresses:
            customer["addresses"].append(address.serialize())
        
        return customer

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
            
            self.userid = data.get("userid")
            self.password = data.get("password")

            self.active = data.get("active")

            #address_list = data.get("addresses", [])
            address_list = data.get("addresses")
            for json_address in address_list:
                address = Address()
                address.deserialize(json_address)
                self.addresses.append(address)

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
    def find_by_id(cls, id):
        """ Returns all Customer with the given unique id """
        logger.info("Processing lookup for id %s ...", id)
        return cls.query.filter(cls.id == id)

    @classmethod
    def find_by_first_name(cls, first_name):
        """ Returns all Customer with the given first name """
        logger.info("Processing lookup for first_name %s ...", first_name)
        return cls.query.filter(cls.first_name == first_name)

    @classmethod
    def find_by_last_name(cls, last_name):
        """ Returns all Customer with the given last name """
        logger.info("Processing lookup for last_name %s ...", last_name)
        return cls.query.filter(cls.last_name == last_name)

    @classmethod
    def find_by_userid(cls, userid):
        """ Returns all Customer with the given userid """
        logger.info("Processing lookup for userid %s ...", userid)
        return cls.query.filter(cls.userid == userid)