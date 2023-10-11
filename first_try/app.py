import mysql.connector
from flask import Flask, redirect, render_template, request, url_for
from flask import session
from fileinput import filename
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

# Debug code : 291-145-463
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

conn = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'bhiravha_chits'
)


UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

@app.route('/')
def form():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        pwd = request.form['pwd']
        if name and pwd != '':
            session['name'] = request.form['name']
            session['pwd'] = request.form['pwd']
            return redirect(url_for('success'))
        else:
            return redirect(url_for('form'))
    else:
        return f'No User Found'

@app.route('/success')
def success():
    if 'name' in session:
        name = session['name']
        pwd  = session['pwd']
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_creation")
        result = cursor.fetchall()

        for row in result:
            user_name = row[1]
        return render_template('success.html', uname=name, password=pwd, user_name = user_name)
    else:
        return redirect(url_for('form'))

@app.route('/logout')
def logout():
    if 'name' in session:
        session.clear()
        return redirect(url_for('form'))
    else:
        # return f'404'
        return f''' 
        <h3>Logout</h3>
        <a href='/'><button>login</button></a>
        '''
@app.route('/upload')
def Upload():
    return render_template('upload_file.html')

@app.route('/upload_file',methods=['POST'])
def upload_file():
    if request.method=='POST':
        # single file upload
        f = request.files['file']
        #  multiple file upload
        mf = request.files.getlist('multifile')
        for file in mf:
            file.save('Multiple-' + file.filename)
        filename = secure_filename(f.filename)
        upload_file = f.save(app.config['UPLOAD_FOLDER'] + filename)
        return 'Files Uploaded Successfully'
    
if __name__ == ('__main__'):
    app.run(debug=True)

