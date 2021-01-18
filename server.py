"Server for app to sell/buy images"

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from jinja2 import StrictUndefined

import os
import requests

import model
import crud
import helper
import charge_credit_card

import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

cloud_name = os.environ["CLOUD_NAME"]
cloudinary_api_key = os.environ["CLOUDINARY_API_KEY"]
cloudinary_api_secret = os.environ["CLOUDINARY_API_SECRET"]

cloudinary.config(
    cloud_name = cloud_name,
    api_key = cloudinary_api_key,
    api_secret = cloudinary_api_secret
)

@app.route('/')
def homepage():
    """View homepage of app"""

    return redirect('/admin')

@app.route('/upload', methods=['POST'])
def upload_image():
    """Uploads user's image to Cloudinary"""

    user_file = request.files.get('new-image-upload')
    filename = request.form['new-image-name']
    price = request.form['new-image-price']

    response = cloudinary.uploader.upload(user_file)
    image_url = response['secure_url']

    new_image = crud.create_image(name=filename, url=image_url, price=price)

    if new_image:
        flash("Image uploaded")
        return redirect('/admin')


@app.route('/admin')
def manage_inventory():
    """View page to manage inventory"""

    images = crud.get_for_sale_images_desc()

    return render_template('inventory.html', images=images)


@app.route('/store')
def view_store():
    """View public view of store"""

    images = crud.get_for_sale_images_desc()
    
    cart_size = ""
    image_ids = []

    if 'cart' in session:
        cart = session['cart']
        cart_size = str(len(cart))
        image_ids = list(cart.keys())

    return render_template('store.html', images=images, cart_size=cart_size, image_ids=image_ids)


@app.route('/cart')
def view_cart():
    """View items in shopping cart, total, and checkout"""
    
    cart_items = {}
    subtotal = ""

    if 'cart' in session:
        cart_items = session['cart']
        subtotal = helper.get_subtotal(cart_items)

    return render_template('cart.html', cart_items=cart_items, subtotal=subtotal)


@app.route('/api/update-image', methods=['POST'])
def update_image():
    """Updates image data per user's edits"""

    id = request.form.get("id")
    name = request.form.get("name")
    price = request.form.get("price")

    return helper.update_image(id, name, price)


@app.route('/api/hide-image', methods=['POST'])
def hide_image():
    """Changes image's status to REMOVED so it no longer appears in the app"""

    id = request.form.get("id")
    hidden_image = crud.hide_image(id)

    return {"id": hidden_image.id}


@app.route('/api/add-to-cart', methods=['POST'])
def add_to_cart():
    """Creates cart if user hasn't started one. Adds item to cart, stored in Flask session"""

    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']

    id = request.form.get("id")
    name = request.form.get("name")
    price = float(request.form.get("price"))
    url = request.form.get("url")

    cart[id] = [name, price, url]
    cart_size = str(len(cart))
    
    # Save the updated cart dictionary to session
    session['cart'] = cart

    return {'cart_size': cart_size}

@app.route('/api/remove-from-cart', methods=["POST"])
def remove_from_cart():
    """Removes existing item from cart stored in Flask session"""

    cart = session['cart']

    id = request.form.get("image_id")

    # Remove item from cart by its ID
    del cart[id]
    cart_size = str(len(cart))

    # Save the updated cart dictionary to session
    session['cart'] = cart

    return {'cart_size': cart_size}

@app.route('/api/process-order', methods=['POST'])
def process_order():
    """Processes order after user submits payment info"""

    card_number = request.form.get("order-user-card-no")
    expiration_mo = request.form.get("order-user-card-exp-mo")
    expiration_yr = request.form.get("order-user-card-exp-yr")
    exp_date = helper.format_expiration_date(expiration_mo, expiration_yr)
    cart_items = session['cart']
    amt = helper.get_subtotal(cart_items)
    rounded_amt = helper.format_price(amt)

    charged = charge_credit_card.charge(card_number, exp_date, rounded_amt)

    if charged:
        fname = request.form.get("order-user-fname")
        lname = request.form.get("order-user-lname")
        email = request.form.get("order-user-email")
        user = crud.create_user(fname, lname, email)

        order = crud.create_order(user.id)
        order_items = session['cart']
        helper.record_order_items(order.id, order_items)

        del session['cart']
        flash("Mock payment processed. Order complete")
        return redirect('/store')
    else:
        flash("There was a problem with your payment. Please check payment details.")
        return redirect('/cart')

if __name__ == '__main__':
    model.connect_to_db(app)

    # to run Flask app in dev environment
    app.run(host='0.0.0.0', debug=True)

    # # to run Flask app in prod environment
    # app.run()