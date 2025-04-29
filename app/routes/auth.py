from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash

def auth_routes(app, mysql):
    @app.route('/')
    def home():
        return redirect(url_for('login'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cur.fetchone()
            cur.close()

            if user and check_password_hash(user['password_hash'], password):
                session['username'] = user['username']
                return redirect(url_for('dashboard'))
            else:
                flash('Email ou senha incorretos!')
                return redirect(url_for('login'))

        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            email = request.form['email']
            username = request.form['username']
            password = request.form['password']
            hashed_password = generate_password_hash(password)

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (email, username, password_hash) VALUES (%s, %s, %s)", (email, username, hashed_password))
            mysql.connection.commit()
            cur.close()

            flash('Usuário registrado com sucesso!')
            return redirect(url_for('login'))

        return render_template('register.html')

    @app.route('/logout')
    def logout():
        session.pop('username', None)
        return redirect(url_for('login'))

    @app.route('/dashboard')
    def dashboard():
        if 'username' not in session:
            return redirect(url_for('login'))
        return render_template('dashboard.html', username=session['username'])
