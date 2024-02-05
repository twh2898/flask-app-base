
from flask import (Blueprint, current_app, flash, g, redirect, render_template,
                   request, session, url_for)

from ..auth import login_required, role_required
from ..db import get_db
from .role import bp as role_bp

bp = Blueprint('admin', __name__, url_prefix='/admin')
bp.register_blueprint(role_bp)


@bp.route('/')
@login_required
@role_required('admin')
def index():
    return render_template('page/admin/index.html')


@bp.route('/users')
@login_required
@role_required('admin')
def users():
    return render_template('page/admin/users.html')
