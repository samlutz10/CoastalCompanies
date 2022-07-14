from flask import Flask, render_template, url_for, flash, redirect
from Forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = '1169c4ddf749979a0b760b49ddbe9e11'

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/training_hub')
def training_hub():
    return render_template('training_hub.html', title='Training Hub')

@app.route('/excel_files')
def excel_files():
    return render_template('excel_files.html', title='Excel Files')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account Created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@coastalcompaniesri.com' and form.password.data == 'Coastal1':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
    app.run(debug=True)
    app.run(debug=True, host= '192.168.8.103')