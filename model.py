"""Models for app to sell/buy images"""

from flask_sqlalchemy import SQLAlchemy 
import os
import enum

db = SQLAlchemy()

def connect_to_db(flask_app, db_uri='postgresql:///imgstore', echo=False):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')

class InventoryStatus(enum.Enum):
    """Pre-defined set of inventory statuses an inventory image can have"""
    FOR_SALE = enum.auto()
    REMOVED = enum.auto()   

class InventoryImage(db.Model):
    """An image uploaded for sale"""

    __tablename__ = "inventory_images"

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)
    name = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum(InventoryStatus), nullable=False, default="FOR_SALE")
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())


if __name__ == '__main__':
    from server import app

    connect_to_db(app)
