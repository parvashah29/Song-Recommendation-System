import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from flask import current_app, session, url_for
import os
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class SpotifyService:
    def __init__(self):
        try:
            self.client_id = current_app.config.get('SPOTIFY_CLIENT_ID')
            self.client_secret = current_app.config.get('SPOTIFY_CLIENT_SECRET')
            self.redirect_uri = current_app.config.get('SPOTIFY_REDIRECT_URI')
            
            # Client credentials flow for app-level access
            if self.client_id and self.client_secret:
                self.client_credentials_manager = SpotifyClientCredentials(
                    client_id=self.client_id,
                    client_secret=self.client_secret
                )
                self.spotify = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)
            else:
                self.spotify = None
        except RuntimeError:
            # Working outside of application context
            self.client_id = None
            self.client_secret = None
            self.redirect_uri = None
            self.spotify = None
    
    def get_user_auth_url(self, user_id: str) -> str:
        """Get Spotify authorization URL for user"""
        if not self.client_id or not self.client_secret:
            raise ValueError("Spotify credentials not configured. Please add SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET to your .env file.")
        
        scope = "user-read-recently-played user-top-read user-library-read playlist-read-private playlist-modify-public playlist-modify-private user-read-playback-state user-modify-playback-state"
        
        sp_oauth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=scope,
            cache_path=f".cache-{user_id}"
        )
        
        return sp_oauth.get_authorize_url()
    
    def get_user_token(self, user_id: str, code: str) -> Optional[str]:
        """Exchange authorization code for access token"""
        try:
            sp_oauth = SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
                cache_path=f".cache-{user_id}"
            )
            
            token_info = sp_oauth.get_access_token(code)
            return token_info['access_token']
            
        except Exception as e:
            logger.error(f"Error getting user token: {e}")
            return None
    
    def get_user_spotify(self, access_token: str) -> spotipy.Spotify:
        """Get Spotify client with user access token"""
        return spotipy.Spotify(auth=access_token)
    
    def search_songs(self, query: str, limit: int = 20) -> List[Dict]:
        """Search for songs on Spotify"""
        try:
            results = self.spotify.search(q=query, type='track', limit=limit)
            songs = []
            
            for track in results['tracks']['items']:
                song_data = {
                    'spotify_id': track['id'],
                    'title': track['name'],
                    'artist': ', '.join([artist['name'] for artist in track['artists']]),
                    'album': track['album']['name'],
                    'duration': track['duration_ms'],
                    'popularity': track['popularity'],
                    'preview_url': track['preview_url'],
                    'external_urls': track['external_urls'],
                    'album_artwork': track['album']['images'][0]['url'] if track['album']['images'] else None
                }
                songs.append(song_data)
            
            return songs
            
        except Exception as e:
            logger.error(f"Error searching songs: {e}")
            return []
    
    def get_audio_features(self, spotify_id: str) -> Optional[Dict]:
        """Get audio features for a specific track"""
        try:
            features = self.spotify.audio_features(spotify_id)[0]
            if features:
                return {
                    'danceability': features['danceability'],
                    'energy': features['energy'],
                    'valence': features['valence'],
                    'tempo': features['tempo'],
                    'acousticness': features['acousticness'],
                    'instrumentalness': features['instrumentalness'],
                    'liveness': features['liveness'],
                    'speechiness': features['speechiness']
                }
        except Exception as e:
            logger.error(f"Error getting audio features for {spotify_id}: {e}")
        
        return None
    
    def get_user_top_tracks(self, access_token: str, time_range: str = 'medium_term', limit: int = 50) -> List[Dict]:
        """Get user's top tracks"""
        try:
            sp = self.get_user_spotify(access_token)
            results = sp.current_user_top_tracks(time_range=time_range, limit=limit)
            
            tracks = []
            for track in results['items']:
                track_data = {
                    'spotify_id': track['id'],
                    'title': track['name'],
                    'artist': ', '.join([artist['name'] for artist in track['artists']]),
                    'album': track['album']['name'],
                    'duration': track['duration_ms'],
                    'popularity': track['popularity'],
                    'preview_url': track['preview_url'],
                    'external_urls': track['external_urls'],
                    'album_artwork': track['album']['images'][0]['url'] if track['album']['images'] else None
                }
                tracks.append(track_data)
            
            return tracks
            
        except Exception as e:
            logger.error(f"Error getting user top tracks: {e}")
            return []
    
    def get_user_recently_played(self, access_token: str, limit: int = 50) -> List[Dict]:
        """Get user's recently played tracks"""
        try:
            sp = self.get_user_spotify(access_token)
            results = sp.current_user_recently_played(limit=limit)
            
            tracks = []
            for item in results['items']:
                track = item['track']
                track_data = {
                    'spotify_id': track['id'],
                    'title': track['name'],
                    'artist': ', '.join([artist['name'] for artist in track['artists']]),
                    'album': track['album']['name'],
                    'duration': track['duration_ms'],
                    'popularity': track['popularity'],
                    'preview_url': track['preview_url'],
                    'external_urls': track['external_urls'],
                    'album_artwork': track['album']['images'][0]['url'] if track['album']['images'] else None,
                    'played_at': item['played_at']
                }
                tracks.append(track_data)
            
            return tracks
            
        except Exception as e:
            logger.error(f"Error getting recently played tracks: {e}")
            return []
    
    def get_recommendations(self, access_token: str, seed_tracks: List[str], limit: int = 20) -> List[Dict]:
        """Get Spotify recommendations based on seed tracks"""
        try:
            sp = self.get_user_spotify(access_token)
            results = sp.recommendations(seed_tracks=seed_tracks, limit=limit)
            
            tracks = []
            for track in results['tracks']:
                track_data = {
                    'spotify_id': track['id'],
                    'title': track['name'],
                    'artist': ', '.join([artist['name'] for artist in track['artists']]),
                    'album': track['album']['name'],
                    'duration': track['duration_ms'],
                    'popularity': track['popularity'],
                    'preview_url': track['preview_url'],
                    'external_urls': track['external_urls'],
                    'album_artwork': track['album']['images'][0]['url'] if track['album']['images'] else None
                }
                tracks.append(track_data)
            
            return tracks
            
        except Exception as e:
            logger.error(f"Error getting recommendations: {e}")
            return []
    
    def create_playlist(self, access_token: str, user_id: str, name: str, description: str = "") -> Optional[str]:
        """Create a new playlist for the user"""
        try:
            sp = self.get_user_spotify(access_token)
            playlist = sp.user_playlist_create(
                user=user_id,
                name=name,
                description=description,
                public=False
            )
            return playlist['id']
            
        except Exception as e:
            logger.error(f"Error creating playlist: {e}")
            return None
    
    def add_tracks_to_playlist(self, access_token: str, playlist_id: str, track_ids: List[str]) -> bool:
        """Add tracks to a playlist"""
        try:
            sp = self.get_user_spotify(access_token)
            sp.playlist_add_items(playlist_id, track_ids)
            return True
            
        except Exception as e:
            logger.error(f"Error adding tracks to playlist: {e}")
            return False
    
    def get_track_details(self, spotify_id: str) -> Optional[Dict]:
        """Get detailed information about a track"""
        try:
            track = self.spotify.track(spotify_id)
            
            return {
                'spotify_id': track['id'],
                'title': track['name'],
                'artist': ', '.join([artist['name'] for artist in track['artists']]),
                'album': track['album']['name'],
                'duration': track['duration_ms'],
                'popularity': track['popularity'],
                'preview_url': track['preview_url'],
                'external_urls': track['external_urls'],
                'album_artwork': track['album']['images'][0]['url'] if track['album']['images'] else None,
                'release_date': track['album']['release_date'],
                'genres': track['album'].get('genres', [])
            }
            
        except Exception as e:
            logger.error(f"Error getting track details for {spotify_id}: {e}")
            return None

# Global Spotify service instance
spotify_service = SpotifyService()
