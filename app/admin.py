import functools

import bcrypt
from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for, current_app)

from .auth import login_required, role_required
from .db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/')
@login_required
@role_required('admin')
def index():
    return render_template('page/admin/index.html')


@bp.route('/roles')
@login_required
@role_required('admin')
def roles():
    return render_template('page/admin/roles.html')


@bp.route('/users')
@login_required
@role_required('admin')
def users():
    return render_template('page/admin/users.html')
