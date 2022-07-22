from flask import render_template, url_for, flash, redirect, request
from WebPage import app, db, bcrypt
from WebPage.Forms import RegistrationForm, LoginForm, UpdateAccountForm, EmployeeForm
from WebPage.models import User, Employee
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
from WebPage.quiz import PopQuiz
import secrets
import os

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    form = PopQuiz()
    if form.validate_on_submit():
        return redirect(url_for('passed'))
    return render_template('quiz.html', form=form, title='Quiz')

@app.route('/passed')
@login_required
def passed():
    return render_template('passed.html')

@app.route('/training_hub')
@login_required
def training_hub():
    return render_template('training_hub.html', title='Training Hub')

@app.route('/quick_links')
@login_required
def quick_links():
    return render_template('links.html', title='Quick Links')

@app.route('/excel_files')
@login_required
def excel_files():
    return render_template('excel_files.html', title='Excel Files')

@app.route('/employee_list')
@login_required
def employee_list():
    employees = Employee.query.all()
    return render_template('employee_list.html', title='Employee List', employees = employees)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! Please login!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (100, 100)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    return picture_fn

@app.route('/account', methods = ['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.image_file = picture_file
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route('/truck_train')
def truck_train():
    return render_template('TruckTraining.html', title='Truck')

@app.route('/employee/new', methods = ['GET', 'POST'])
@login_required
def new_employee():
    form = EmployeeForm()
    if form.validate_on_submit():
        employee = Employee(name = form.name.data, address = form.address.data, phone_number = form.phone_number.data, hire_date = form.hire_date.data, license_ = form.license_.data, medical = form.medical.data)
        db.session.add(employee)
        db.session.commit()
        flash('This employee has been added!', 'success')
        return redirect(url_for('employee_list'))
    return render_template('create_employee.html', title='New Employee', form=form)