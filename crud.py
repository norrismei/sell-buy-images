"""CRUD operations"""

from model import (db, connect_to_db, Image)

def create_image(name, url, price):
    image = Image(name=name, url=url, price=price)

    db.session.add(image)
    db.session.commit()

    return image

def query_public_images():
    """Returns base query for all public images"""

    public_images = db.session.query(Image).filter_by(public=True)

    return public_images


def get_public_images_desc():
    """Returns public images, in descending order by ID"""

    images = query_public_images()

    return images.order_by(Image.id.desc()).all()


def get_image_by_id(id):
    """Returns single image that matches ID"""

    image = Image.query.get(id)

    return image


def update_image(id, name, price):
    """Makes changes to image in database and returns updated object"""

    image = get_image_by_id(id)
    image.name = name
    image.price = price
    db.session.commit()

    return image

if __name__ == '__main__':
    from server import app
    connect_to_db(app)