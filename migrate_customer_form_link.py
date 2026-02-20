#!/usr/bin/env python3
"""
Migration script to add CustomerFormLink table
"""

import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, CustomerFormLink

def migrate():
    """Add CustomerFormLink table to the database"""
    with app.app_context():
        # Create the new table
        CustomerFormLink.__table__.create(db.engine, checkfirst=True)
        print("CustomerFormLink table created successfully!")

if __name__ == '__main__':
    migrate()
