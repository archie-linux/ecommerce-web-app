## Create virtualenv

- python3 -m venv myvenv
- source myvenv/bin/activate

## Install Dependencies

- pip3 install -r requirements.txt

## Setup Database

- export FLASK_APP=app

- flask shell

- from app import db

- from models import User

- db.create_all()

- User.query.all() // returns []```

## Run App

- python3 app.py

## Run Selenium Tests:

- pytest -v

## To run in development mode:

- flask run --reload

## On user registration, run the following commands to get the otp

- flask shell

- from models import User

- User.query.all()[-1].otp


## Web App Screenshots


# Login

<img src="./screenshots/login.png" alt="drawing" width="400"/>

# Register

<img src="./screenshots/register.png" alt="drawing" width="400"/>

# Enter OTP

<img src="./screenshots/enter_otp.png" alt="drawing" width="400"/>


# Email Confirmed

<img src="./screenshots/email_confirmed.png" alt="drawing" width="400"/>

# Products Dashboard

<img src="./screenshots/all_products.png" alt="drawing" width="400"/>

# Filter Products View By Categories

<img src="./screenshots/filter_view_by_categories.png" alt="drawing" width="400"/>

# Search Products

<img src="./screenshots/search_products.png" alt="drawing" width="400"/>

# View Cart Items

<img src="./screenshots/view_cart.png" alt="drawing" width="400"/>

# Checkout

<img src="./screenshots/checkout.png" alt="drawing" width="400"/>
