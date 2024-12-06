from flask import Flask, render_template, request, redirect, url_for
import hashlib
import os
import datetime

app = Flask(__name__)

# Путь к файлу для хранения хеша пароля
password_file = 'password.txt'

with open('ban.txt', 'w') as mvfdvfd:
    mvfdvfd = mvfdvfd.write('')

 
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_password = request.form['password']
        hashed_password = hash_password(user_password)

        with open(password_file, 'w') as file:
            file.write(hashed_password)

        return redirect(url_for('check_password'))

    return render_template('index.html', value=datetime.datetime.now())


@app.route('/')
def card():
    return render_template('card.html')


@app.route('/check', methods=['GET', 'POST'])
def check_password():
    if request.method == 'POST':
        input_password = request.form['password']
        hashed_input_password = hash_password(input_password)

        with open('ban.txt', 'r') as ban_password_file:
            ban_password_file = ban_password_file.read()

        if ban_password_file == 'ban':
            return render_template('ban.html')
            
        else:
            if os.path.exists(password_file):
                with open(password_file, 'r') as file:
                    stored_hashed_password = file.read().strip()

                if hashed_input_password == stored_hashed_password:
                    with open('yes_or_no.txt', 'w') as yes:
                        yes = yes.write('Yes')
                    return render_template('yes.html')
                
                else:
                    with open('ban.txt', 'w') as ban_file:
                        ban_file = ban_file.write('ban')
                    return render_template('no.html')
            else:
                return render_template('dont_have_password.html')

    return render_template('check.html')


@app.route('/remove')
def remove():
    if os.path.exists(password_file):
        return render_template('remove.html', value=os.remove('password.txt'))
    
    else:
        return render_template('FileNotFoundError.html')
    

@app.route('/comp')
def comp():
    return render_template('Comp.html')

if __name__ == '__main__':
    app.run(debug=True)