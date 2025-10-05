## Create virtualenv
```
python3 -m venv myvenv
source myvenv/bin/activate
```

## Install Dependencies
```pip install -r requirements.txt```

## Setup Database
```
export FLASK_APP=app
flask shell
```

## Import Database object

```from app import db```

## Import models
```from model.user import User```

## Create tables
```db.create_all()```

## Verify User table got created
```User.query.all() // returns []```

## Run App
```
python3 app.py

To run in development mode - `flask run --reload`
```

## Setup DB Migration
```
flask db init
flask db migrate -m "Initial Migration"
flask db upgrade
```