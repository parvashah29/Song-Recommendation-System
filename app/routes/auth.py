from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app import db
from app.services.spotify_service import spotify_service

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('recommendations.index'))
        flash('Invalid username or password')
    return render_template('auth/login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('auth.register'))
            
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('auth.register'))
            
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route('/spotify-login')
@login_required
def spotify_login():
    try:
        auth_url = spotify_service.get_user_auth_url(str(current_user.id))
        return redirect(auth_url)
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for('recommendations.index'))

@bp.route('/callback')
def spotify_callback():
    code = request.args.get('code')
    error = request.args.get('error')
    
    if error:
        flash('Failed to connect to Spotify')
        return redirect(url_for('recommendations.index'))
    
    if current_user.is_authenticated and code:
        access_token = spotify_service.get_user_token(str(current_user.id), code)
        
        if access_token:
            current_user.spotify_token = access_token
            db.session.commit()
            flash('Successfully connected to Spotify!')
            return redirect(url_for('recommendations.index'))
    
    flash('Failed to connect to Spotify')
    return redirect(url_for('recommendations.index')) 