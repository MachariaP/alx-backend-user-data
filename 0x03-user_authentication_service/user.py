#!/usr/bin/env python3
""" SQLAlchemy model for the users table.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    SQLAlchemy model for the users table.

    Attributes:
        id (int): The primary key.
        email (str): The email of the user, non-nullable.
        hashed_password (str): The hashed password of the user, non-nullable.
        session_id (str): The session ID of the user, nullable.
        reset_token (str): The reset token of the user, nullable.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
