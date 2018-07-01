from app.routes.auth import auth
from flask import redirect, url_for


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return redirect(url_for('user.login'))


@auth.route('/logout')
def logout():
    return redirect(url_for('user.logout'))


@auth.route('/authenticated')
def authenticated():
    return redirect(url_for('main.user_home'))
