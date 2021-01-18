"""CRUD operations"""

from model import (db, connect_to_db, InventoryImage, User, Order, OrderItem)

def create_image(name, url, price):
    """Creates new row in inventory_images table and returns new image"""
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

def create_user(fname, lname, email):
    """Creates new row in users table and returns new user"""

    user = User(first_name=fname, last_name=lname, email=email)

    db.session.add(user)
    db.session.commit()

    return user

def create_order(user_id, discount=None):
    """Creates new row in orders table once payment is successful. Returns order"""

    order = Order(user_id=user_id, discount=discount)

    db.session.add(order)
    db.session.commit()

    return order

def create_order_item(order_id, image_id):
    """Creates and returns new abstract Order Item"""

    order_item = OrderItem(order_id=order_id, image_id=image_id)

    db.session.add(order_item)
    db.session.commit()

    return order_item

if __name__ == '__main__':
    from server import app
    connect_to_db(app)