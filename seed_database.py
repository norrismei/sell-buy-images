"""Script to seed database"""

import os
import server
import model

from flask_sqlalchemy import SQLAlchemy

def reset_db():
    """Drops existing database and creates new one with current model"""
    os.system('dropdb imgstore')
    os.system('createdb imgstore')

    model.connect_to_db(server.app)
    model.db.create_all()

    print('Reset db complete!')