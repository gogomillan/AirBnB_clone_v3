#!/usr/bin/python3
"""
Script for the database storage class for AirBnB clone
"""
import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """
    This class stores info into database (MySQL)

    Attributes:
        __engine (sqlalchemy.Engine): The working SQLAlchemy engine.
        __session (sqlalchemy.Session): The working SQLAlchemy session.
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Constructor method for DBStorage class
        """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(getenv('HBNB_MYSQL_USER'),
                                             getenv('HBNB_MYSQL_PWD'),
                                             getenv('HBNB_MYSQL_HOST'),
                                             getenv('HBNB_MYSQL_DB')))
        if getenv('HBNB_ENV') == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        On the curret database session get all objects of the given class.

        Args:
            cls (str): Name of object type. If None, queries all types of
                       objects.
        Return:
            Dict of queried classes <class name>.<obj id> = obj.
        """
        instances = {}
        ALL_CLS = ["State", "City", "User", "Place", "Review", "Amenity"]
        if cls is None:
            for cl in ALL_CLS:
                objs = self.__session.query(eval(cl))
                for obj in objs:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    instances[key] = obj
        else:
            if type(cls).__name__ == type(Base).__name__:
                objs = self.__session.query(cls).all()
                for obj in objs:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    instances[key] = obj

        return instances

    def get(self, cls, id):
        """
        On the curret database session get an object of the given class.

        Args:
            cls (str): Name of object type. If None, no queries.
            id (str): ID of object to query. If None, no queries.
        Return:
             The object based on the class name and its ID.
        """
        MY_CLASS = classes[cls.__name__]
        if MY_CLASS is None:
            return None
        for value in self.all(cls).values():
            if value.id == id:
                return value
        return None

    def new(self, obj):
        """
        Adds object to the current db session

        Args:
            obj (object): given object
        """
        self.__session.add(obj)

    def save(self):
        """
        Commit all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete an object from the current database session

        Args:
            obj (object): object to delete if not None
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        Reloads the database session
        """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        self.__session = Session

    def close(self):
        """
        Close the session by calling remove() method on the private session
        attribute.
        """
        self.__session.remove()

    def count(self, cls=None):
        """
        Returns the number of objects in storage according to the given class
        name. If name is None returns the count of all objects in storage.

        Args:
            cls (str): The name of the class of None for all.
        """
        if cls:
            return len(self.all(cls))
            MY_CLASS = classes[cls.__name__]
            if MY_CLASS is not None:
                return len(self.all(MY_CLASS))
        return len(self.all())
