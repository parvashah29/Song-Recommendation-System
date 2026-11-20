from app import db
from datetime import datetime

class UserInteraction(db.Model):
    """Track user interactions with songs for recommendation learning"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    interaction_type = db.Column(db.String(20), nullable=False)  # 'like', 'play', 'skip', 'add_to_playlist'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Additional metadata
    context = db.Column(db.String(100))  # 'search', 'recommendation', 'playlist', etc.
    duration_played = db.Column(db.Integer)  # Duration in seconds
    
    # Relationships
    user = db.relationship('User', backref='interactions')
    song = db.relationship('Song', backref='interactions')
    
    def __repr__(self):
        return f'<UserInteraction {self.user_id} {self.interaction_type} {self.song_id}>'
