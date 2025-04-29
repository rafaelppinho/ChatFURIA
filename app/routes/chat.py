from flask import render_template, request, redirect, url_for, session, flash

def chat_routes(app, mysql):
    @app.route('/chat', methods=['GET', 'POST'])
    def chat():
        if 'username' not in session:
            flash("Você precisa estar logado para acessar o chat.")
            return redirect(url_for('login'))

        if request.method == 'POST':
            content = request.form['content']
            username = session['username']

            if content.strip():
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO messages (username, content) VALUES (%s, %s)", (username, content))
                mysql.connection.commit()
                cur.close()
            return redirect(url_for('chat'))

        cur = mysql.connection.cursor()
        cur.execute("SELECT username, content, timestamp FROM messages ORDER BY timestamp DESC LIMIT 50")
        messages = cur.fetchall()
        cur.close()

        return render_template('chat.html', messages=messages)
