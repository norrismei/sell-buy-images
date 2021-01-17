"Server for app to sell/buy images"

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from jinja2 import StrictUndefined

import os
import requests

import model
import crud
import helper

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

    if 'cart' in session:
        del session['cart']

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
        print('image ids', image_ids)

    return render_template('store.html', images=images, cart_size=cart_size, image_ids=image_ids)


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

    id = request.form.get('id')
    name = request.form.get("name")
    price = float(request.form.get("price"))

    cart[id] = [name, price]
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


if __name__ == '__main__':
    model.connect_to_db(app)

    # to run Flask app in dev environment
    app.run(host='0.0.0.0', debug=True)

    # # to run Flask app in prod environment
    # app.run()