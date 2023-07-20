from flask import Flask, render_template, url_for, \
    request, flash, session, redirect, abort
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)

menu = [{"name": "Установка", "url": "install-flask"},
        {"name": "Первое приложение", "url": "first-app"},
        {"name": "Обратная связь", "url": "contact"}]


@app.route("/")
def index():
    print(url_for('index'))
    return render_template('index.html', menu=menu)


@app.route("/about")
def about():
    print(url_for('about'))
    return render_template('about.html', title="О сайте", menu=menu)


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == 'POST':
        if len(request.form.get('username', default={})) > 2:
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправки', category='error')

    return render_template('contact.html', title="Обратная связь", menu=menu)


@app.errorhandler(404)
def pageNotFount(error):
    return render_template('page404.html', title="Страница не найдена", menu=menu), 404


@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)

    return f'Профиль пользователя: {username}'


@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session.get('userLogged', default='user')))
    elif request.method == 'POST' and request.form.get('username') == "vvvdanilsss" and request.form.get('psw') == "1234":
        session['userLogged'] = request.form.get('username')
        return redirect(url_for('profile', username=session.get('userLogged')))

    return render_template('login.html', title="Авторизация", menu=menu)


if __name__ == '__main__':
    app.run()
