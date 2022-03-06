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
    userid = db.Column(db.String(63))
    password = db.Column(db.String(63))
    addresses = db.Column(db.ARRAY(db.String(63)))

    def __repr__(self):
        return "<Customer %r id=[%s]>" % (self.name, self.id)

    def create(self):
        """
        Creates a Customer to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Customer to the database
        """
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """ Removes a Customer from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
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
            self.first_name = data["first_name"]
            self.last_name = data["last_name"]
            self.userid = data["userid"]
            self.password = data["password"]
            self.addresses = data["addresses"]
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
        """ Finds a Customer by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_or_404(cls, by_id):
        """ Find a Customer by it's id """
        logger.info("Processing lookup or 404 for id %s ...", by_id)
        return cls.query.get_or_404(by_id)

    @classmethod
    def find_by_first_name(cls, first_name):
        """Returns all Customer with the given first name

        Args:
            name (string): the name of the Customer you want to match
        """
        logger.info("Processing first name query for %s ...", first_name)
        return cls.query.filter(cls.first_name == first_name)

    @classmethod
    def find_by_last_name(cls, last_name):
        """Returns all Customer with the given last name

        Args:
            name (string): the name of the Customer you want to match
        """
        logger.info("Processing last name query for %s ...", last_name)
        return cls.query.filter(cls.last_name == last_name)

    @classmethod
    def find_by_userid(cls, userid):
        """Returns all Customer with the given userid

        Args:
            name (string): the name of the Customer you want to match
        """
        logger.info("Processing user id query for %s ...", userid)
        return cls.query.filter(cls.userid == userid)
