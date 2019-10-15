# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy import Column, String, Integer, Boolean, Date, Table, ForeignKey
from datetime import date


### Declare Mapping
# We use declarative base to define the mapping of classes/objects to database tables
Base = declarative_base()

### creates a linkage between posts and authors
# posts_authors_association = Table(
#     'posts_authors', Base.metadata,
#     Column('user_id', Integer, ForeignKey('users.id')),
#     Column('post_id', Integer, ForeignKey('posts.id'))
# )

class Post(Base):
     #Here is where we map this class to a tablename
    __tablename__ = 'posts'
     #Here we define the attributes of the class
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    content = Column(String)
    # author = relationship("User", secondary=posts_authors_association)
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship("User", back_populates="posts")
    
    def __init__(self, name, description, content, author_id):
        self.name = name
        self.description = description
        self.content = content
        self.author_id = author_id


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    bio = Column(String(10000))
    email = Column(String(100))
    password = Column(String)
    # posts = relationship("Post", secondary=posts_authors_association)
    posts = relationship("Post", back_populates="author")
    authenticated = Column(Boolean, default=False)

    def __init__(self, name, bio, email, password):
        self.name = name
        self.bio = bio
        self.email = email
        self.password = password
        self.authenticated = False
    
    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated
 
    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True
 
    @property
    def is_anonymous(self):
        """Always False, as anonymous users aren't supported."""
        return False
 
    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        """Requires use of Python 3"""
        return str(self.id)
 
    def __repr__(self):
        return '<User {0}>'.format(self.name)

    def get_id(self):
        return self.id


engine = create_engine('sqlite:///blog.db')
Base.metadata.create_all(engine)
