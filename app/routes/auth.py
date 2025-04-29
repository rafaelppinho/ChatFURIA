from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint('auth', __name__)

def init_auth_routes(app, mysql):
    # Aqui conectamos o Blueprint ao app
    app.register_blueprint(auth_bp)

    # Adicionamos a variável mysql ao Blueprint
    auth_bp.mysql = mysql


@auth_bp.route('/')
def home():
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        print("Dados recebidos:", email, password)

        try:
            cur = auth_bp.mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cur.fetchone()
            cur.close()
            print("Usuário encontrado:", user)
        except Exception as e:
            flash(f"Erro ao acessar o banco: {e}")
            return redirect(url_for('auth.login'))

        if user and check_password_hash(user['password_hash'], password):
            session['username'] = user['username']
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Email ou senha incorretos!')
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        try:
            cur = auth_bp.mysql.connection.cursor()
            cur.execute(
                "INSERT INTO users (email, username, password_hash) VALUES (%s, %s, %s)",
                (email, username, hashed_password)
            )
            auth_bp.mysql.connection.commit()
            cur.close()
            print("Usuário registrado:", username)
        except Exception as e:
            flash(f"Erro ao registrar usuário: {e}")
            return redirect(url_for('auth.register'))

        flash('Usuário registrado com sucesso!')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('auth.login'))

@auth_bp.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html', username=session['username'])
