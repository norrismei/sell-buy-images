"Server for app to sell/buy images"

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)

from jinja2 import StrictUndefined

import model

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View homepage of app"""

    return render_template('homepage.html')

if __name__ == '__main__':
    model.connect_to_db(app)

    # to run Flask app in dev environment
    app.run(host='0.0.0.0', debug=True)

    # # to run Flask app in prod environment
    # app.run()