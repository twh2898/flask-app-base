import functools

import bcrypt
from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for, current_app)

from .auth import login_required
from .db import get_db

bp = Blueprint('debug', __name__, url_prefix='/debug')


@bp.route('/')
@login_required
def index():
    return render_template('page/debug.html')
