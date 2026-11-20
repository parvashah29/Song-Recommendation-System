from flask import Blueprint, redirect, url_for
from flask_login import current_user

bp = Blueprint('home', __name__)

@bp.route('/')
def index():
    """Home route - redirect to appropriate page"""
    if current_user.is_authenticated:
        return redirect(url_for('recommendations.index'))
    else:
        return redirect(url_for('auth.login'))
