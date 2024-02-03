import os
import sqlite3

import click
from flask import Flask, current_app, g

import bcrypt


def get_db():
    """Get the db connection, open a new connection if one does not exist."""
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'],
                               detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """Close the db connection."""
    db = g.pop('db', None)

    if db is not None:
        db.close()


def register_admin(db):
    username = 'admin'
    password = b'admin'
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password, salt)
    db.execute('INSERT INTO user (username, password) VALUES (?, ?)',
               (username, password_hash))
    db.execute('INSERT INTO role (name) VALUES ("admin")')
    db.commit()
    db.execute('INSERT INTO user_role (uid, rid) SELECT '
               '(SELECT id FROM user WHERE username = "admin") as uid, '
               '(SELECT id FROM role WHERE name = "admin") as rid')
    db.commit()


def init_db():
    """Initialize a new db with the sql/init.sql script."""
    db = get_db()

    with current_app.open_resource('sql/init.sql', 'r') as f:
        db.executescript(f.read())

    register_admin(db)


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app: Flask):
    """Setup app context teardown for closing db."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
