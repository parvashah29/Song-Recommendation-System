from app import db
from datetime import datetime

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(100), unique=True)
    title = db.Column(db.String(200), nullable=False)
    artist = db.Column(db.String(200))
    album = db.Column(db.String(200))
    duration = db.Column(db.Integer)  # Duration in milliseconds
    popularity = db.Column(db.Integer)
    danceability = db.Column(db.Float)
    energy = db.Column(db.Float)
    tempo = db.Column(db.Float)
    valence = db.Column(db.Float)
    acousticness = db.Column(db.Float)
    instrumentalness = db.Column(db.Float)
    liveness = db.Column(db.Float)
    speechiness = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    playlist_songs = db.relationship('PlaylistSong', backref='song', lazy=True) 