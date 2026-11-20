from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from app.models.playlist import Playlist, PlaylistSong
from app.models.song import Song
from app import db

bp = Blueprint('playlists', __name__)

@bp.route('/')
@login_required
def index():
    playlists = Playlist.query.filter_by(user_id=current_user.id).all()
    return render_template('playlists/index.html', playlists=playlists)

@bp.route('/create', methods=['POST'])
@login_required
def create():
    name = request.form.get('name')
    description = request.form.get('description')
    
    playlist = Playlist(
        name=name,
        description=description,
        user_id=current_user.id
    )
    db.session.add(playlist)
    db.session.commit()
    
    return jsonify({
        'id': playlist.id,
        'name': playlist.name,
        'description': playlist.description
    })

@bp.route('/<int:playlist_id>')
@login_required
def view(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    if playlist.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    songs = []
    for playlist_song in playlist.songs:
        song = playlist_song.song
        songs.append({
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'album': song.album,
            'spotify_id': song.spotify_id
        })
    
    return render_template('playlists/view.html', playlist=playlist, songs=songs)

@bp.route('/<int:playlist_id>/add-song', methods=['POST'])
@login_required
def add_song(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    if playlist.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    song_id = request.form.get('song_id')
    song = Song.query.get_or_404(song_id)
    
    # Check if song is already in playlist
    existing = PlaylistSong.query.filter_by(
        playlist_id=playlist_id,
        song_id=song_id
    ).first()
    
    if existing:
        return jsonify({'error': 'Song already in playlist'}), 400
    
    # Add song to playlist
    playlist_song = PlaylistSong(
        playlist_id=playlist_id,
        song_id=song_id,
        position=len(playlist.songs)
    )
    db.session.add(playlist_song)
    db.session.commit()
    
    return jsonify({
        'id': song.id,
        'title': song.title,
        'artist': song.artist,
        'album': song.album
    })

@bp.route('/<int:playlist_id>/remove-song', methods=['POST'])
@login_required
def remove_song(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    if playlist.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    song_id = request.form.get('song_id')
    playlist_song = PlaylistSong.query.filter_by(
        playlist_id=playlist_id,
        song_id=song_id
    ).first_or_404()
    
    db.session.delete(playlist_song)
    db.session.commit()
    
    return jsonify({'success': True}) 