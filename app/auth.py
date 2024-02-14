import functools
from typing import List, Union

import bcrypt
from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)

from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/')
def index():
    return redirect(url_for('auth.login'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('userid')

    if user_id is None:
        g.user = None

    else:
        g.user = get_db().execute('SELECT * FROM user WHERE id = ?',
                                  (user_id,)).fetchone()
        user_roles = get_db().execute('''
            SELECT name FROM role WHERE
                id = (SELECT rid FROM user_role WHERE uid = ?)
            ''', (user_id,)).fetchall()
        g.user_roles = [role['name'] for role in user_roles]


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kw):
        if g.user is None:
            flash('Login is required to access this resource')
            return render_template('page/403.html'), 403

        return view(**kw)

    return wrapped_view


def _test_role(role):
    if isinstance(role, list):
        for option in role:
            if option in g.user_roles:
                return True

    elif role in g.user_roles:
        return True

    return False


def role_required(role: Union[str, List[str]]):
    def wrapper(view):
        @functools.wraps(view)
        def wrapped_view(**kw):
            if not _test_role(role):
                flash('User not authorized')
                return render_template('page/403.html'), 403

            return view(**kw)

        return wrapped_view

    return wrapper


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        db = get_db()
        error = None

        if not username:
            error = 'Username is required'

        elif not password:
            error = 'Password is required'

        else:
            try:
                password = password.encode()
                salt = bcrypt.gensalt()
                password_hash = bcrypt.hashpw(password, salt)
                db.execute(
                    'INSERT INTO user (username, password) VALUES (?, ?)',
                    (username, password_hash))
                db.commit()

            except db.IntegrityError:
                error = f'User {username} already registered.'

            else:
                return redirect(url_for('auth.login'))

        flash(error)

    return render_template('page/auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        db = get_db()
        error = None

        if not username or not password:
            error = 'Incorrect username or password'

        else:
            cur = db.execute(
                'SELECT * FROM user WHERE username = ?', (username,))
            user = cur.fetchone()

            if user is None:
                error = 'Incorrect username or password'

            elif not bcrypt.checkpw(password.encode(), user['password']):
                error = 'Incorrect username or password'

            if error is None:
                session.clear()
                session['userid'] = user['id']
                return redirect(url_for('index'))

        flash(error)

    return render_template('page/auth/login.html')


@bp.route('/change_pass', methods=('GET', 'POST'))
@login_required
def change_pass():
    if request.method == 'POST':
        password = request.form.get('password', None)
        new_password = request.form.get('new_password', None)
        db = get_db()
        error = None

        if not password or not new_password:
            error = 'Incorrect or invalid password'

        else:
            if not bcrypt.checkpw(password.encode(), g.user['password']):
                error = 'Incorrect or invalid password'

            if error is None:
                new_password = new_password.encode()
                salt = bcrypt.gensalt()
                password_hash = bcrypt.hashpw(new_password, salt)

                db.execute('UPDATE user SET password=? WHERE id=?',
                           (password_hash, g.user['id']))
                db.commit()
                return logout()

        flash(error)

    return render_template('page/auth/change_pass.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


@bp.route('/admin')
@login_required
def admin():
    cur = get_db().execute('SELECT username FROM user')
    rv = cur.fetchall()
    return [{'username': user['username']} for user in rv]
