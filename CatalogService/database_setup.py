
import sys

# for creating the mapper code
from sqlalchemy import Column, ForeignKey, Integer, String

# for configuration and class code
from sqlalchemy.ext.declarative import declarative_base

# for creating foreign key relationship between the tables
from sqlalchemy.orm import relationship

# for configuration
from sqlalchemy import create_engine

# create declarative_base instance
Base = declarative_base()


# we create the class Book and extend it from the Base Class.
class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    topic = Column(String(250))
    stock = Column(Integer)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "topic": self.topic,
            "stock": self.stock,
        }        

# creates a create_engine instance at the bottom of the file
engine = create_engine('sqlite:///books-collection.db')

Base.metadata.create_all(engine)