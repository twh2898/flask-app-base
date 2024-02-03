import functools

import bcrypt
from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for, current_app)

from .auth import login_required
from .db import get_db

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/')
def index():
    return redirect(url_for('auth.login'))


@bp.route('/profile')
@login_required
def profile():
    return render_template('page/user/profile.html')
