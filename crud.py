"""CRUD operations"""

from model import (db, connect_to_db, InventoryImage)

def create_image(name, url, price):
    image = InventoryImage(name=name, url=url, price=price)

    db.session.add(image)
    db.session.commit()

    return image

def query_for_sale_images():
    """Returns base query for all images for sale"""

    public_images = db.session.query(InventoryImage).filter_by(status="FOR_SALE")

    return public_images


def get_for_sale_images_desc():
    """Returns images for sale, in descending order by ID"""

    images = query_for_sale_images()

    return images.order_by(InventoryImage.id.desc()).all()


def get_image_by_id(id):
    """Returns single image that matches ID"""

    image = InventoryImage.query.get(id)

    return image


def update_image(id, name, price):
    """Makes changes to image in database and returns updated object"""

    image = get_image_by_id(id)
    image.name = name
    image.price = price
    db.session.commit()

    return image


def hide_image(id):
    """Changes image's status to REMOVED and returns object"""

    image = get_image_by_id(id)
    image.status = "REMOVED"
    db.session.commit()

    return image


if __name__ == '__main__':
    from server import app
    connect_to_db(app)