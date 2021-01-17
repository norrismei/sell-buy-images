import crud
import model

def update_image(id, name, price):
    """Updates image in database and returns update as dictionary"""

    updated = crud.update_image(id, name, price)

    return {
        "id": updated.id,
        "name": updated.name,
        "price": updated.price
    }

def get_subtotal(cart):
    """Receives cart items and adds up prices"""

    # Cart format: {image_id: [name, price, url]}
    subtotal = sum([item_data[1] for item_data in cart.values()])

    return subtotal

