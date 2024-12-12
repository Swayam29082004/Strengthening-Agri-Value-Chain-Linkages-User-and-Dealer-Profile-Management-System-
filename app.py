import os
import json
import hashlib
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'  # Ensure this is a strong, unique key in production
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Ensure the upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('data', exist_ok=True)

# File paths for JSON data
USERS_JSON = 'data/users.json'
DEALERS_JSON = 'data/dealers.json'

# Load users and dealers from JSON files
def load_data():
    if os.path.exists(USERS_JSON):
        with open(USERS_JSON, 'r') as file:
            users = json.load(file)
    else:
        users = {}

    if os.path.exists(DEALERS_JSON):
        with open(DEALERS_JSON, 'r') as file:
            dealers = json.load(file)
    else:
        dealers = {}

    return users, dealers

# Save users and dealers to JSON files
def save_data(users, dealers):
    with open(USERS_JSON, 'w') as file:
        json.dump(users, file, indent=4)

    with open(DEALERS_JSON, 'w') as file:
        json.dump(dealers, file, indent=4)

# Load initial data
users, dealers = load_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        login_type = request.form.get('login_type')  # Determine login type

        if login_type == 'user':
            user = users.get(username)
            if user and user['password'] == hashlib.sha256(password.encode()).hexdigest():
                session['username'] = username
                session['profile_type'] = 'user'
                if not user.get('profile_complete', False):
                    return redirect(url_for('complete_profile'))
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password.')

        elif login_type == 'dealer':
            dealer = dealers.get(username)
            if dealer and dealer['password'] == hashlib.sha256(password.encode()).hexdigest():
                session['username'] = username
                session['profile_type'] = 'dealer'
                if not dealer.get('profile_complete', False):
                    return redirect(url_for('complete_profile'))
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password.')
    
    return render_template('login.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        profile_type = request.form.get('profile_type')

        # Validate inputs
        if not username or not password or not confirm_password or not profile_type:
            flash('All fields are required.')
            return redirect(url_for('create_account'))

        if password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('create_account'))

        # Check if the username already exists
        if username in users or username in dealers:
            flash('Username already exists.')
            return redirect(url_for('create_account'))

        # Hash the password before storing
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Initialize profile data with product_rate included
        profile_data = {
            'full_name': '',
            'email': '',
            'phone': '',
            'address': '',
            'farm_size': '',
            'products': '',
            'product_rate': '',  # Added for both users and dealers
            'organization_name': '',
            'organization_address': '',
            'location': '',
            'business_type': '',
            'products_interested': '',
            'gst_no': '',
            'profile_picture': 'uploads/default.jpg',
            'certified_documents': None
        }

        # Create the account based on the selected profile type
        if profile_type == 'user':
            users[username] = {
                'password': hashed_password,
                'profile_type': 'user',
                'profile_complete': False,
                'profile': profile_data
            }
        elif profile_type == 'dealer':
            dealers[username] = {
                'password': hashed_password,
                'profile_type': 'dealer',
                'profile_complete': False,
                'profile': profile_data
            }
        else:
            flash('Invalid profile type.')
            return redirect(url_for('create_account'))

        # Save the data to the appropriate JSON file
        save_data(users, dealers)

        flash('Account created successfully! Please log in.')
        return redirect(url_for('login'))

    return render_template('create_account.html')


@app.route('/complete_profile', methods=['GET', 'POST'])
def complete_profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    profile_type = session.get('profile_type')

    if request.method == 'POST':
        username = session['username']

        # Extract form data based on profile type
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        
        # Initialize fields that might not be relevant for both profiles
        address = farm_size = products = organization_name = organization_address = location = business_type = products_interested = gst_no = None

        if profile_type == 'user':
            address = request.form.get('address')
            farm_size = request.form.get('farm_size')
            products = request.form.get('products')
            products_rate = request.form.get('rate')
        elif profile_type == 'dealer':
            organization_name = request.form.get('organization_name')
            organization_address = request.form.get('organization_address')
            location = request.form.get('location')
            business_type = request.form.get('business_type')
            products_interested = request.form.get('products_interested')
            products_rate = request.form.get('rate')
            gst_no = request.form.get('gst_no')

        # Handling the profile picture upload
        profile_picture = request.files.get('profile_picture')
        if profile_picture and profile_picture.filename:
            # Sanitize the filename
            profile_picture_filename = secure_filename(profile_picture.filename)
            profile_picture_path = os.path.join(app.config['UPLOAD_FOLDER'], profile_picture_filename)
            profile_picture.save(profile_picture_path)
            profile_picture_url = f"uploads/{profile_picture_filename}"
        else:
            profile_picture_url = 'uploads/default.jpg'

        # Handling the certified documents upload (for dealer profile)
        certified_documents_url = None
        if profile_type == 'dealer':
            certified_documents = request.files.get('certified_documents')
            if certified_documents and certified_documents.filename:
                # Sanitize the filename
                certified_documents_filename = secure_filename(certified_documents.filename)
                certified_documents_path = os.path.join(app.config['UPLOAD_FOLDER'], certified_documents_filename)
                certified_documents.save(certified_documents_path)
                certified_documents_url = f"uploads/{certified_documents_filename}"

        # Store user or dealer profile data
        profile_data = {
            'full_name': full_name,
            'email': email,
            'phone': phone,
            'address': address,
            'farm_size': farm_size,
            'products': products,
            'products_rate': products_rate,
            'organization_name': organization_name,
            'organization_address': organization_address,
            'location': location,
            'business_type': business_type,
            'products_interested': products_interested,
            'gst_no': gst_no,
            'profile_picture': profile_picture_url,
            'certified_documents': certified_documents_url,
        }

        if profile_type == 'user':
            users[username]['profile_complete'] = True
            users[username]['profile'] = profile_data
        elif profile_type == 'dealer':
            dealers[username]['profile_complete'] = True
            dealers[username]['profile'] = profile_data

        save_data(users, dealers)

        flash('Profile completed successfully!')
        return redirect(url_for('dashboard'))

    # Render different templates based on profile type
    if profile_type == 'user':
        return render_template('complete_profile_user.html')
    elif profile_type == 'dealer':
        return render_template('complete_profile_dealer.html')


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    profile_type = session.get('profile_type')

    if profile_type == 'user':
        # Retrieve the user's profile
        user_profile = users.get(username, {}).get('profile', {})
        # Retrieve all dealer profiles
        dealer_profiles = [dealer for dealer in dealers.values() if dealer['profile_complete']]
        context = {
            'user_profile': user_profile,
            'dealers': dealer_profiles  # Provide dealer data for the user dashboard
        }
        # Render the user dashboard template
        return render_template('user_dashboard.html', **context)

    elif profile_type == 'dealer':
        # Retrieve the dealer's profile
        dealer_profile = dealers.get(username, {}).get('profile', {})
        # Retrieve all user profiles
        user_profiles = [user for user in users.values() if user['profile_complete']]
        context = {
            'dealer_profile': dealer_profile,
            'users': user_profiles  # Provide user data for the dealer dashboard if needed
        }
        # Render the dealer dashboard template
        return render_template('dealer_dashboard.html', **context)

    else:
        flash('Invalid profile type.')
        return redirect(url_for('login'))

def get_users():
    with open('data/users.json', 'r') as file:
        users = json.load(file)
    return users

def get_dealers():
    with open('data/dealers.json', 'r') as file:
        dealers = json.load(file)
    return dealers

def get_dealer_profile():
    with open('data/dealer_profile.json', 'r') as file:
        dealer_profile = json.load(file)
    return dealer_profile

@app.route('/dealer_dashboard')
def dealer_dashboard():
    users = get_users()
    dealers = get_dealers()
    dealer_profile = get_dealer_profile()
    return render_template('dealer_dashboard.html', users=users, dealers=dealers, dealer_profile=dealer_profile)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/dealer/<dealer_id>')
def get_dealer(dealer_id):
    with open('static/data/dealers.json', 'r') as file:
        dealers = json.load(file)
    
    # Find the specific dealer profile
    dealer_profile = next((dealer for dealer in dealers if dealer['id'] == dealer_id), None)
    
    if dealer_profile:
        return jsonify(dealer_profile)
    else:
        return jsonify({'error': 'Dealer not found'}), 404



