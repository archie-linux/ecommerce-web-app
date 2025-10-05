from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask_migrate import Migrate
from models import User, Product
from forms import RegistrationForm, LoginForm
from models import db
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__)) + '/'
app.config['SECRET_KEY'] = 'secret'  # Replace with your secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +  basedir + 'users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route("/")
def index():
    return redirect('/register')

@app.route("/dashboard")
def dashboard():
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect('/login')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect('/dashboard')
        else:
            return 'Invalid email or password'

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()

    return redirect('/login')

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = request.form.get('quantity')

    # Retrieve the product from the database
    product = Product.query.get(product_id)

    # Check if the product exists
    if product:
        cart_item = {
            'product_id': product_id,
            'quantity': quantity,
            'name': product.name,
            'price': product.price
        }

        cart = session.get('cart', {})
        cart[product_id] = cart_item
        session['cart'] = cart
        print(session['cart'])
        return redirect('/dashboard')
    else:
        return 'Product not found'

@app.route('/update-cart', methods=['POST'])
def update_cart():
    cart_items = session.get('cart', {})

    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity'))
    item = cart_items[product_id]

    if quantity > 0:
        item['quantity'] = str(quantity)
    else:
        cart_items.pop(product_id)

    session['cart'] = cart_items
    return redirect(url_for('view_cart'))

@app.route('/view-cart', methods=['GET'])
def view_cart():
    cart = session.get('cart', {})
    return render_template('cart.html', cart=cart)

if __name__ == '__main__':
    app.run(port=5001)