from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from models import User, Product
from forms import RegistrationForm, LoginForm
from models import db
from functools import wraps
import pyotp
import os
import base64

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__)) + '/'
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +  basedir + 'users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = '<your-mail-server>'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'your-email-address'
app.config['MAIL_PASSWORD'] = '<your-password>'


db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
bootstrap = Bootstrap(app)
mail = Mail(app)

# Decorator function to check if session exists
def check_session_exists(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            # Redirect to login page
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error_message="Page not found"), 404


@app.route("/")
def index():
    if session.get('user_id'):
        return redirect('/products')
    else:
        return redirect('/login')


def generate_otp():
    random_bytes = os.urandom(10)
    secret_key = base64.b32encode(random_bytes).decode('utf-8')
    otp = pyotp.TOTP(secret_key)
    return otp.now()


def send_otp_via_emai(otp, recepient):
    msg = Message('One-Time Password', sender='<sender-email-address>', recipients=[recepient])
    msg.body = f'Your OTP is: {otp}'

    mail.send(msg)

    return 'OTP sent successfully.'


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        otp = generate_otp()
        user = User(username=username, email=email, password=hashed_password, otp=otp)
        db.session.add(user)
        db.session.commit()

        # send_otp_via_emai(otp, user.email)

        return redirect(url_for('verify_email'))

    return render_template('register.html', form=form)


@app.route('/verify-email', methods=['GET', 'POST'])
def verify_email():
    if request.method == 'POST':
        email = request.form['email']
        otp = request.form['otp']

        user = User.query.filter_by(email=email).first()
        if otp == user.otp:
            user.email_confirmed = True
            db.session.commit()

            return render_template('email_confirmed.html')

        return render_template('error.html', error_message='Invalid OTP')  # OTP does not match

    return render_template('verify_email.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if not user:
            return render_template('error.html', error_message='User not found')

        if not user.email_confirmed:
            return render_template('error.html', error_message='Please verify your email!')

        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect('/products')
        else:
            return render_template('error.html', error_message='Invalid email or password')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    # Clear the session
    session.clear()

    return redirect(url_for('login'))


@app.route('/profile')
@check_session_exists
def user_profile():
    user = User.query.get(int(session.get('user_id')))
    return render_template('user_profile.html', user=user)


@app.route("/products")
@check_session_exists
def browse_products():
    products = Product.query.all()
    return render_template('products.html', products=products)


@app.route('/products/<category_id>')
@check_session_exists
def filter_products_by_category(category_id):
    if category_id:
        filtered_products = Product.query.filter_by(category_id=int(category_id)).all()
    else:
        filtered_products = Product.query.all()

    return render_template('products.html', products=filtered_products)


@app.route('/search')
@check_session_exists
def search():
    query = request.args.get('query')
    products = Product.query.filter(Product.name.ilike(f"%{query}%")).all()
    return render_template('products.html', products=products, query=query)


@app.route('/add-to-cart', methods=['POST'])
@check_session_exists
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = request.form.get(f"quantity_{product_id}")

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
        print(f"Cart Items: {session['cart']}")
        return redirect(url_for('browse_products'))
    else:
        return 'Product not found'


@app.route('/update-cart', methods=['POST'])
@check_session_exists
def update_cart():
    cart_items = session.get('cart', {})
    product_id = request.form.get('product_id')
    quantity = int(request.form.get(f"quantity_{product_id}"))
    item = cart_items[product_id]

    if quantity > 0:
        item['quantity'] = str(quantity)
    else:
        cart_items.pop(product_id)

    session['cart'] = cart_items
    return redirect(url_for('view_cart'))


@app.route('/view-cart', methods=['GET'])
@check_session_exists
def view_cart():
    cart = session.get('cart', {})
    return render_template('cart.html', cart=cart)


def calculate_total_amount(cart):
    total_amount = 0
    for _, item in cart.items():
        total_amount += item['price'] * int(item['quantity'])

    return round(total_amount, 2)


@app.route('/checkout')
@check_session_exists
def checkout():
    cart = session.get('cart', {})
    total_amount = calculate_total_amount(cart)
    return render_template('checkout.html', cart=cart, total_amount=total_amount)

@app.route('/place-order', methods=['POST'])
@check_session_exists
def place_order():
    name = request.form.get('name')
    address = request.form.get('address')
    payment = request.form.get('payment')

    # Clear the cart after the order is placed
    session.pop('cart', None)

    return render_template('order_confirmed.html')


if __name__ == '__main__':
    app.run(port=5000)