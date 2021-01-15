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