from flask import Blueprint, render_template, jsonify, request, current_app
from flask_login import login_required, current_user
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from app.models.song import Song
from app import db
from config import Config

bp = Blueprint('songs', __name__)

def get_spotify_client():
    if current_user.spotify_token:
        return spotipy.Spotify(auth=current_user.spotify_token)
    return None

@bp.route('/')
@login_required
def index():
    return render_template('songs/index.html')

@bp.route('/search')
@login_required
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    sp = get_spotify_client()
    if not sp:
        return jsonify({'error': 'Please connect to Spotify first'}), 401
    
    results = sp.search(q=query, type='track', limit=10)
    tracks = []
    
    for track in results['tracks']['items']:
        # Store track in database if not exists
        song = Song.query.filter_by(spotify_id=track['id']).first()
        if not song:
            song = Song(
                spotify_id=track['id'],
                title=track['name'],
                artist=track['artists'][0]['name'],
                album=track['album']['name'],
                duration=track['duration_ms'],
                popularity=track['popularity']
            )
            db.session.add(song)
            db.session.commit()
        
        tracks.append({
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'album': song.album,
            'spotify_id': song.spotify_id
        })
    
    return jsonify(tracks)

@bp.route('/recommendations')
@login_required
def get_recommendations():
    sp = get_spotify_client()
    if not sp:
        return jsonify({'error': 'Please connect to Spotify first'}), 401
    
    # Get user's top tracks
    top_tracks = sp.current_user_top_tracks(limit=5)
    seed_tracks = [track['id'] for track in top_tracks['items']]
    
    # Get recommendations based on top tracks
    recommendations = sp.recommendations(
        seed_tracks=seed_tracks[:5],
        limit=10
    )
    
    tracks = []
    for track in recommendations['tracks']:
        song = Song.query.filter_by(spotify_id=track['id']).first()
        if not song:
            song = Song(
                spotify_id=track['id'],
                title=track['name'],
                artist=track['artists'][0]['name'],
                album=track['album']['name'],
                duration=track['duration_ms'],
                popularity=track['popularity']
            )
            db.session.add(song)
            db.session.commit()
        
        tracks.append({
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'album': song.album,
            'spotify_id': song.spotify_id
        })
    
    return jsonify(tracks) 