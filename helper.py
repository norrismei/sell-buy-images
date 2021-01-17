import crud
import model
from decimal import Decimal

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

def format_price(amt):
    """Takes in float and returns with Decimal number rounded to two decimal places"""

    decimal_amt = Decimal(amt)
    rounded = round(decimal_amt, 2)

    return rounded

def format_expiration_date(exp_mo, exp_yr):
    """Takes in MM and YY and returns date in 'YYYY-MM' format"""

    formatted_exp = f"20{exp_yr}-{exp_mo}"
    print(formatted_exp)

    return formatted_exp