"""CRUD operations"""

from model import (db, connect_to_db, Image)

def create_image(name, url, price):
    image = Image(name=name, url=url, price=price)

    db.session.add(image)
    db.session.commit()

    return image

if __name__ == '__main__':
    from server import app
    connect_to_db(app)