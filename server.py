"Server for app to sell/buy images"

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from jinja2 import StrictUndefined

import os
import requests

import model
import crud

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

    return render_template('homepage.html', image="")

@app.route('/upload', methods=['POST'])
def upload_image():
    """Uploads user's image to Cloudinary"""

    user_file = request.files.get('new-image-upload')
    filename = request.form['new-image-name']
    price = request.form['new-image-price']

    response = cloudinary.uploader.upload(user_file)
    image_url = response['secure_url']

    crud.create_image(name=filename, url=image_url, price=price)

    return render_template('homepage.html', image=image_url)

@app.route('/inventory')
def manage_inventory():
    """View page to manage inventory"""

    return render_template('inventory.html')

@app.route('/store')
def view_store():
    """View public view of store"""

    return render_template('store.html')

if __name__ == '__main__':
    model.connect_to_db(app)

    # to run Flask app in dev environment
    app.run(host='0.0.0.0', debug=True)

    # # to run Flask app in prod environment
    # app.run()