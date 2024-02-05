
from flask import (Blueprint, current_app, flash, g, redirect, render_template,
                   request, session, url_for)

from ..auth import login_required, role_required
from ..db import get_db

bp = Blueprint('role', __name__, url_prefix='/role')


TMP_ROLES = [
    'admin',
    'one',
    'two',
    'three',
]


@bp.route('/')
@login_required
@role_required('admin')
def index():
    return render_template('page/admin/roles.html', roles=TMP_ROLES)


@bp.route('/edit', methods=('GET', 'PUT', 'DELETE'))
@login_required
@role_required('admin')
def edit():
    key = request.args.get('role', None)

    if request.method == "PUT":
        new_key = request.form.get('role', None)
        if new_key is None:
            print('Missing new key')
        if key not in TMP_ROLES:
            return 'Key does not exist', 403
        TMP_ROLES[TMP_ROLES.index(key)] = new_key
        return render_template('page/admin/role/row_view.html', role=new_key)

    elif request.method == "DELETE":
        if key not in TMP_ROLES:
            return 'Key does not exist', 403
        TMP_ROLES.remove(key)
        return ''

    return render_template('page/admin/role/row_edit.html', role=key)


@bp.route('/view', methods=('GET',))
@login_required
@role_required('admin')
def view():
    return render_template('page/admin/role/row_view.html', role='some edit name')
