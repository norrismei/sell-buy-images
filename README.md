## App Overview
For this backend-focused project centered on building an image repository, I wanted to mimic creating a store where digital images can be uploaded and purchased.

In seller view, the user can upload images, as well as manage, edit, and remove inventory.

In buyer view, the user can see all images available for sale, add and remove from cart, and submit credit card details to process order.

To facilitate testing the app routes and visualizing the app features and requirements, I built a basic, unstyled frontend, which is by no means what a production-quality frontend would look like.

## About Me
When I first learned Python, I discovered coding was not unlike learning the rules and strategy to a game, solving escape room puzzles, and editing — all activities that I enjoy. I doubled down on my decision to switch careers by attending Hackbright Academy, a full-stack software engineering program with a mission to #changetheratio in tech. I'm thrilled to combine my skills, talent, and interests into my new path as a software engineer.

## Contents
* [Tech Stack](#tech-stack)
* [Features](#features)
* [Installation](#install)

## <a name="tech-stack"></a>Tech Stack
* Python
* Flask
* Jinja2
* Javascript
* jQuery
* PostgreSQL
* SQLAlchemy ORM
* HTML
* (A tiny bit) CSS

## <a name="features"></a>Features

#### Seller View: Upload An Image
Select file from your computer and add a name and price. Once submitted, the asset will be uploaded and stored in Cloudinary, and the public URL saved to the database.

#### Seller View: Manage Inventory
Images appear in descending order, starting with most recently added. If a field is clicked on or highlighted, a button to save changes will appear. When either the Save or Remove button is clicked, the individual row will update itself. Note that removing an image will mark an image as removed in the database but the row will still exist. I did it this way to lay groundwork for possible future feature where an image can be removed from the store but still exist for seller to add back to the store without uploading the asset to Cloudinary again.

#### Buyer View: View Store | Add/Remove Items to Cart
Each image can be added to the cart once. The View Cart link will update its count to show how many images are in the cart. Note that all information for the cart is stored in a Flask session to allow for quick adding/removing without making calls to the database.

#### Buyer View: View Cart | Submit Order
When there's at least one item in the cart, user can enter their information to submit the order. For the payment information, it's okay to use fake information when testing but use these best practices to avoid being flagged:
* Authorize.net may flag any credit cards that are suspicious. For testing, try '4111111111111111' for the credit card number.
* For the expiration date, enter a MM/YY that hasn't expired yet. If it's expired, the payment will fail to process.
* Charge only small amounts of money. Even though it's a test transaction, a large amount of money may get flagged as a suspicious transaction.
* When the mock payment is approved, you will get a confirmation at the email you used to register for the Authorize.net developer account.

## <a name="install"></a>Installation
To run this project on your machine:

Clone or fork this repo:
```
https://github.com/norrismei/sell-buy-images
```

Create and activate a virtual environment inside your directory:
```
virtualenv env
source env/bin/activate
```

Install the dependencies:
```
pip install -r requirements.txt
```

Sign up to use the [Cloudinary API](https://cloudinary.com/documentation/image_upload_api_reference) for uploading images to a cloud server.

Sign up for a free developer [Authorize.net](https://developer.authorize.net/) account for charging credit cards.

Store your Cloudinary and Authorize.net API keys and other sensitive information in:

```
secrets.sh
```

Set up the database:

```
createdb imgstore
python3 model.py
python3 -i seed_database.py
reset_db()
```

Run the app:

```
source secrets.sh
python3 server.py
```

You can now navigate to 'http://0.0.0.0:5000/' in your browser to interact with the app.