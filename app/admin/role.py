
from flask import (Blueprint, Response, current_app, flash, g, redirect,
                   render_template, request, session, url_for)

from ..auth import login_required, role_required
from ..db import get_db

bp = Blueprint('role', __name__, url_prefix='/role')


def _get_roles():
    db = get_db()
    cur = db.execute('SELECT id, name FROM role')
    rows = cur.fetchall()
    roles = []
    for row in rows:
        id_, name = row['id'], row['name']
        cur = db.execute('SELECT id FROM user_role WHERE rid=?', (id_,))
        users = cur.fetchall()
        user_count = len(users)
        roles.append({
            'id': id_,
            'name': name,
            'user_count': user_count,
        })
    return roles


@bp.route('/')
@login_required
@role_required('admin')
def index():
    return render_template('page/admin/roles.html', roles=_get_roles())


@bp.route('/view/table', methods=('GET',))
@login_required
@role_required('admin')
def table():
    return render_template('page/admin/role/table.html', roles=_get_roles())


@bp.route('/add')
@login_required
@role_required('admin')
def add():
    return render_template('page/admin/role/role_add.html')


@bp.route('/edit', methods=('GET', 'POST', 'PUT', 'DELETE'))
@login_required
@role_required('admin')
def edit():
    db = get_db()
    roles = _get_roles()

    if request.method == "POST":
        name = request.form.get('name', None)

        if name is None:
            return render_template('page/admin/role/role_add.html', error='Missing name')

        name = name.strip()

        if len(name) == 0:
            return render_template('page/admin/role/role_add.html', error='Missing name')

        cur = db.execute('SELECT * FROM role WHERE name=?', (name,))
        exist = cur.fetchall()
        if len(exist) > 0:
            return render_template('page/admin/role/role_add.html', error='Name already exists')

        db.execute('INSERT INTO role (name) VALUES (?)', (name,))
        db.commit()

        resp = Response(add())
        resp.headers['HX-Trigger'] = 'newRole'
        return resp

    key = request.args.get('role', None, type=int)

    if key is None:
        return 'Missing key', 400

    roles_id = [role['id'] for role in roles]
    if key not in roles_id:
        print('Key', key, 'not found in', roles_id)
        return 'Key does not exist', 400

    if request.method == "PUT":
        name = request.form.get('role', None)

        if name is None:
            return 'Missing new name', 400

        name = name.strip()

        if len(name) == 0:
            return 'Missing name', 400

        db.execute('UPDATE role SET name=? WHERE id=?', (name, key))
        db.commit()

        roles = _get_roles()
        role = None
        for role in roles:
            if role['id'] == key:
                break

        else:
            return 'Failed to update role', 500

        return render_template('page/admin/role/.html', id=role['id'],
                               name=role['name'])

    if request.method == "DELETE":
        db.execute('DELETE FROM role WHERE id=?', (key,))
        db.commit()
        return ''

    cur = db.execute('SELECT id, name FROM role WHERE id=?', (key,))
    role = cur.fetchone()

    return render_template('page/admin/role/row_edit.html',
                           id=role['id'],
                           name=role['name'])


@bp.route('/view')
@login_required
@role_required('admin')
def view():
    key = request.args.get('role', None, type=int)
    if key is None:
        return 'Missing key', 400

    roles = _get_roles()
    roles_id = [role['id'] for role in roles]
    print(roles_id)
    if key not in roles_id:
        return 'Key not found', 400

    cur = get_db().execute('SELECT id, name FROM role WHERE id=?', (key,))
    role = cur.fetchone()

    return render_template('page/admin/role/row_view.html', id=role['id'], name=role['name'])
