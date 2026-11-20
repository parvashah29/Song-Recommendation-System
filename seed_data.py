#!/usr/bin/env python3
"""
Data seeding script for the Song Recommendation System
This script populates the database with sample data for demonstration purposes.
"""

import os
import sys
import random
from datetime import datetime, timedelta

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Song, UserInteraction, Playlist, PlaylistSong
from app.recommendation_engine import recommendation_engine

def create_sample_users():
    """Create sample users"""
    print("Creating sample users...")
    
    users_data = [
        {'username': 'admin', 'email': 'admin@example.com', 'password': 'admin123'},
        {'username': 'alice', 'email': 'alice@example.com', 'password': 'password123'},
        {'username': 'bob', 'email': 'bob@example.com', 'password': 'password123'},
        {'username': 'charlie', 'email': 'charlie@example.com', 'password': 'password123'},
        {'username': 'diana', 'email': 'diana@example.com', 'password': 'password123'},
        {'username': 'eve', 'email': 'eve@example.com', 'password': 'password123'},
    ]
    
    for user_data in users_data:
        if not User.query.filter_by(username=user_data['username']).first():
            user = User(
                username=user_data['username'],
                email=user_data['email']
            )
            user.set_password(user_data['password'])
            db.session.add(user)
    
    db.session.commit()
    print(f"Created {len(users_data)} users")

def create_sample_songs():
    """Create sample songs with audio features"""
    print("Creating sample songs...")
    
    # Sample songs with realistic audio features
    songs_data = [
        {
            'spotify_id': '4iV5W9uYEdYUVa79Axb7Rh',
            'title': 'Blinding Lights',
            'artist': 'The Weeknd',
            'album': 'After Hours',
            'duration': 200040,
            'popularity': 95,
            'danceability': 0.514,
            'energy': 0.730,
            'valence': 0.334,
            'tempo': 171.005,
            'acousticness': 0.00123,
            'instrumentalness': 0.00000665,
            'liveness': 0.0929,
            'speechiness': 0.0302
        },
        {
            'spotify_id': '0VjIjW4WU0z4DpB5SSW1X3',
            'title': 'Watermelon Sugar',
            'artist': 'Harry Styles',
            'album': 'Fine Line',
            'duration': 174000,
            'popularity': 88,
            'danceability': 0.736,
            'energy': 0.525,
            'valence': 0.778,
            'tempo': 95.977,
            'acousticness': 0.182,
            'instrumentalness': 0.00000165,
            'liveness': 0.159,
            'speechiness': 0.0321
        },
        {
            'spotify_id': '6f3Slt0GbA2bPZlz0aIFXN',
            'title': 'Levitating',
            'artist': 'Dua Lipa',
            'album': 'Future Nostalgia',
            'duration': 203000,
            'popularity': 92,
            'danceability': 0.730,
            'energy': 0.578,
            'valence': 0.804,
            'tempo': 103.000,
            'acousticness': 0.0534,
            'instrumentalness': 0.00000165,
            'liveness': 0.165,
            'speechiness': 0.0362
        },
        {
            'spotify_id': '1mea3bSkSGXuIRvnydlB5b',
            'title': 'Good 4 U',
            'artist': 'Olivia Rodrigo',
            'album': 'SOUR',
            'duration': 178000,
            'popularity': 90,
            'danceability': 0.586,
            'energy': 0.778,
            'valence': 0.456,
            'tempo': 166.969,
            'acousticness': 0.0102,
            'instrumentalness': 0.00000165,
            'liveness': 0.204,
            'speechiness': 0.0302
        },
        {
            'spotify_id': '3n3Ppam7vgaVa1iaRUpq9s',
            'title': 'Stay',
            'artist': 'The Kid LAROI, Justin Bieber',
            'album': 'F*CK LOVE 3: OVER YOU',
            'duration': 141000,
            'popularity': 89,
            'danceability': 0.680,
            'energy': 0.463,
            'valence': 0.464,
            'tempo': 169.980,
            'acousticness': 0.414,
            'instrumentalness': 0.00000165,
            'liveness': 0.111,
            'speechiness': 0.0302
        },
        {
            'spotify_id': '4cOdK2wGLETKBW3PvgPWqT',
            'title': 'Industry Baby',
            'artist': 'Lil Nas X, Jack Harlow',
            'album': 'MONTERO',
            'duration': 212000,
            'popularity': 87,
            'danceability': 0.748,
            'energy': 0.696,
            'valence': 0.808,
            'tempo': 150.040,
            'acousticness': 0.0102,
            'instrumentalness': 0.00000165,
            'liveness': 0.204,
            'speechiness': 0.0302
        },
        {
            'spotify_id': '0tZ3mElWcr74OOhKEiNz1x',
            'title': 'Heat Waves',
            'artist': 'Glass Animals',
            'album': 'Dreamland',
            'duration': 238000,
            'popularity': 85,
            'danceability': 0.761,
            'energy': 0.525,
            'valence': 0.641,
            'tempo': 80.870,
            'acousticness': 0.414,
            'instrumentalness': 0.00000165,
            'liveness': 0.111,
            'speechiness': 0.0302
        },
        {
            'spotify_id': '1rqqCSm0Qe4I9rUvWncaom',
            'title': 'Peaches',
            'artist': 'Justin Bieber, Daniel Caesar, Giveon',
            'album': 'Justice',
            'duration': 198000,
            'popularity': 84,
            'danceability': 0.677,
            'energy': 0.696,
            'valence': 0.808,
            'tempo': 90.030,
            'acousticness': 0.182,
            'instrumentalness': 0.00000165,
            'liveness': 0.159,
            'speechiness': 0.0321
        },
        {
            'spotify_id': '2VxeLyX666F8uXCJ0dZF8B',
            'title': 'Kiss Me More',
            'artist': 'Doja Cat, SZA',
            'album': 'Planet Her',
            'duration': 208000,
            'popularity': 86,
            'danceability': 0.748,
            'energy': 0.525,
            'valence': 0.641,
            'tempo': 111.087,
            'acousticness': 0.0534,
            'instrumentalness': 0.00000165,
            'liveness': 0.165,
            'speechiness': 0.0362
        },
        {
            'spotify_id': '3YRCqOhFifThpSRFJ1VWFM',
            'title': 'Montero',
            'artist': 'Lil Nas X',
            'album': 'MONTERO',
            'duration': 137000,
            'popularity': 83,
            'danceability': 0.586,
            'energy': 0.778,
            'valence': 0.456,
            'tempo': 166.969,
            'acousticness': 0.0102,
            'instrumentalness': 0.00000165,
            'liveness': 0.204,
            'speechiness': 0.0302
        }
    ]
    
    for song_data in songs_data:
        if not Song.query.filter_by(spotify_id=song_data['spotify_id']).first():
            song = Song(**song_data)
            db.session.add(song)
    
    db.session.commit()
    print(f"Created {len(songs_data)} songs")

def create_sample_interactions():
    """Create sample user interactions"""
    print("Creating sample user interactions...")
    
    users = User.query.all()
    songs = Song.query.all()
    
    if not users or not songs:
        print("No users or songs found. Please run user and song creation first.")
        return
    
    interaction_types = ['like', 'play', 'skip', 'add_to_playlist']
    contexts = ['recommendation', 'search', 'playlist', 'trending']
    
    # Create interactions for each user
    for user in users:
        # Each user interacts with 5-15 random songs
        num_interactions = random.randint(5, 15)
        user_songs = random.sample(songs, min(num_interactions, len(songs)))
        
        for song in user_songs:
            # Create multiple interactions for some songs
            num_song_interactions = random.randint(1, 3)
            
            for _ in range(num_song_interactions):
                interaction_type = random.choice(interaction_types)
                context = random.choice(contexts)
                
                # Create interaction with random timestamp in the last 30 days
                days_ago = random.randint(0, 30)
                hours_ago = random.randint(0, 23)
                minutes_ago = random.randint(0, 59)
                
                timestamp = datetime.utcnow() - timedelta(
                    days=days_ago, 
                    hours=hours_ago, 
                    minutes=minutes_ago
                )
                
                interaction = UserInteraction(
                    user_id=user.id,
                    song_id=song.id,
                    interaction_type=interaction_type,
                    context=context,
                    timestamp=timestamp,
                    duration_played=random.randint(30, song.duration // 1000) if interaction_type == 'play' else 0
                )
                
                db.session.add(interaction)
    
    db.session.commit()
    print("Created sample user interactions")

def create_sample_playlists():
    """Create sample playlists"""
    print("Creating sample playlists...")
    
    users = User.query.all()
    songs = Song.query.all()
    
    if not users or not songs:
        print("No users or songs found.")
        return
    
    playlist_names = [
        'My Favorites',
        'Workout Mix',
        'Chill Vibes',
        'Party Hits',
        'Road Trip',
        'Study Music',
        'Summer Playlist',
        'Throwback Thursday'
    ]
    
    for user in users:
        # Each user gets 2-4 playlists
        num_playlists = random.randint(2, 4)
        user_playlist_names = random.sample(playlist_names, min(num_playlists, len(playlist_names)))
        
        for playlist_name in user_playlist_names:
            playlist = Playlist(
                name=playlist_name,
                description=f"{user.username}'s {playlist_name}",
                user_id=user.id
            )
            db.session.add(playlist)
            db.session.flush()  # Get the playlist ID
            
            # Add 3-8 songs to each playlist
            num_songs = random.randint(3, 8)
            playlist_songs = random.sample(songs, min(num_songs, len(songs)))
            
            for i, song in enumerate(playlist_songs):
                playlist_song = PlaylistSong(
                    playlist_id=playlist.id,
                    song_id=song.id,
                    position=i + 1
                )
                db.session.add(playlist_song)
    
    db.session.commit()
    print("Created sample playlists")

def train_recommendation_models():
    """Train the recommendation models with the sample data"""
    print("Training recommendation models...")
    
    try:
        recommendation_engine.train_models()
        print("Models trained successfully!")
    except Exception as e:
        print(f"Error training models: {e}")

def main():
    """Main seeding function"""
    print("Starting data seeding...")
    
    # Create Flask app context
    app = create_app()
    
    with app.app_context():
        # Create all database tables
        db.create_all()
        
        # Seed data
        create_sample_users()
        create_sample_songs()
        create_sample_interactions()
        create_sample_playlists()
        
        # Train models
        train_recommendation_models()
        
        print("\n" + "="*50)
        print("Data seeding completed successfully!")
        print("="*50)
        print("\nSample users created:")
        print("- admin / admin123")
        print("- alice / password123")
        print("- bob / password123")
        print("- charlie / password123")
        print("- diana / password123")
        print("- eve / password123")
        print("\nYou can now run the application with: python run.py")

if __name__ == '__main__':
    main()
