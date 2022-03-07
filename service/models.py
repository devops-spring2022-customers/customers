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
    addresses = db.Column(db.ARRAY(db.String(63)), nullable=False)

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

    '''
    # To be implemented

    def update(self):
        """
        Updates a Customer to the database
        """

    def delete(self):
        """ Removes a Customer from the data store """
    '''

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
            
            self.userid = data["userid"]
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
    '''
    # To be implemented
    @classmethod
    def find_or_404(cls, by_id):
        """ Find a Customer by its id """

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
