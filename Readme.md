## Create virtualenv
python3 -m venv myvenv
source myvenv/bin/activate

# Install Dependencies
pip install flask-sqlalchemy Flask-WTF Flask-Migrate Flask-Script email_validator

# Setup Database
export FLASK_APP=app
flask shell

// Import Database object
from app import db

// Import models
from model.user import User

// Create tables
db.create_all()

// Verify User table got created
User.query.all() // returns []

# Run App
python3 app.py

App Url: http://127.0.0.1:5000

# Setup DB Migration

flask db init
flask db migrate -m "Initial Migration"
flask db upgrade