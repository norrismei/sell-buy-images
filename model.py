"""Models for app to sell/buy images"""

from flask_sqlalchemy import SQLAlchemy 
import os

db = SQLAlchemy()

def connect_to_db(flask_app, db_uri='postgresql:///imgstore', echo=False):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')

class Image(db.Model):
    """An image uploaded to repository"""

    __tablename__ = "images"

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)
    name = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    public = db.Column(db.Boolean, default=True, nullable=False)

if __name__ == '__main__':
    from server import app

    connect_to_db(app)
