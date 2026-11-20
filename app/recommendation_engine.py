import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.decomposition import TruncatedSVD
import joblib
import os
from app import db
from app.models import User, Song, UserInteraction, PlaylistSong
from typing import List, Dict, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SongRecommendationEngine:
    def __init__(self):
        self.content_similarity_matrix = None
        self.collaborative_model = None
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=0.95)  # Keep 95% of variance
        self.is_trained = False
        
    def get_audio_features(self) -> pd.DataFrame:
        """Extract audio features for all songs"""
        songs = Song.query.all()
        features = []
        
        for song in songs:
            if all([song.danceability is not None, song.energy is not None, 
                   song.valence is not None, song.tempo is not None]):
                features.append({
                    'song_id': song.id,
                    'danceability': song.danceability,
                    'energy': song.energy,
                    'valence': song.valence,
                    'tempo': song.tempo,
                    'acousticness': song.acousticness or 0,
                    'instrumentalness': song.instrumentalness or 0,
                    'liveness': song.liveness or 0,
                    'speechiness': song.speechiness or 0,
                    'popularity': song.popularity or 0
                })
        
        return pd.DataFrame(features)
    
    def get_user_interactions(self) -> pd.DataFrame:
        """Get user interaction data for collaborative filtering"""
        interactions = UserInteraction.query.all()
        data = []
        
        for interaction in interactions:
            # Weight different interaction types
            weight = {
                'like': 5,
                'play': 3,
                'skip': -1,
                'add_to_playlist': 4
            }.get(interaction.interaction_type, 1)
            
            data.append({
                'user_id': interaction.user_id,
                'song_id': interaction.song_id,
                'rating': weight,
                'timestamp': interaction.timestamp
            })
        
        return pd.DataFrame(data)
    
    def train_content_based_model(self):
        """Train content-based recommendation model"""
        logger.info("Training content-based model...")
        
        # Get audio features
        features_df = self.get_audio_features()
        
        if features_df.empty:
            logger.warning("No audio features found. Cannot train content-based model.")
            return
        
        # Prepare features (exclude song_id)
        feature_columns = [col for col in features_df.columns if col != 'song_id']
        features = features_df[feature_columns].values
        
        # Normalize features
        features_scaled = self.scaler.fit_transform(features)
        
        # Apply PCA for dimensionality reduction
        features_pca = self.pca.fit_transform(features_scaled)
        
        # Compute cosine similarity matrix
        self.content_similarity_matrix = cosine_similarity(features_pca)
        
        # Store song IDs for mapping
        self.song_ids = features_df['song_id'].values
        
        logger.info(f"Content-based model trained with {len(self.song_ids)} songs")
    
    def train_collaborative_model(self):
        """Train collaborative filtering model using matrix factorization"""
        logger.info("Training collaborative filtering model...")
        
        # Get user interactions
        interactions_df = self.get_user_interactions()
        
        if interactions_df.empty:
            logger.warning("No user interactions found. Cannot train collaborative model.")
            return
        
        # Create user-item matrix
        user_item_matrix = interactions_df.pivot_table(
            index='user_id', 
            columns='song_id', 
            values='rating', 
            fill_value=0
        )
        
        # Use TruncatedSVD for matrix factorization
        self.collaborative_model = TruncatedSVD(n_components=min(50, user_item_matrix.shape[1]-1), random_state=42)
        self.user_factors = self.collaborative_model.fit_transform(user_item_matrix)
        self.item_factors = self.collaborative_model.components_
        
        # Store user and item mappings
        self.user_ids = user_item_matrix.index.values
        self.song_ids_collab = user_item_matrix.columns.values
        
        logger.info(f"Collaborative model trained with {len(self.user_ids)} users and {len(self.song_ids_collab)} songs")
    
    def train_models(self):
        """Train both recommendation models"""
        self.train_content_based_model()
        self.train_collaborative_model()
        self.is_trained = True
        
        # Save models
        self.save_models()
    
    def get_content_based_recommendations(self, song_id: int, n_recommendations: int = 10) -> List[Dict]:
        """Get content-based recommendations for a song"""
        if not self.is_trained or self.content_similarity_matrix is None:
            return []
        
        try:
            # Find song index
            song_idx = np.where(self.song_ids == song_id)[0]
            if len(song_idx) == 0:
                return []
            
            song_idx = song_idx[0]
            
            # Get similarity scores
            similarities = self.content_similarity_matrix[song_idx]
            
            # Get top similar songs (excluding the input song)
            similar_indices = np.argsort(similarities)[::-1][1:n_recommendations+1]
            
            recommendations = []
            for idx in similar_indices:
                if similarities[idx] > 0.1:  # Only include songs with meaningful similarity
                    recommendations.append({
                        'song_id': int(self.song_ids[idx]),
                        'similarity_score': float(similarities[idx])
                    })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error in content-based recommendations: {e}")
            return []
    
    def get_collaborative_recommendations(self, user_id: int, n_recommendations: int = 10) -> List[Dict]:
        """Get collaborative filtering recommendations for a user"""
        if not self.is_trained or self.collaborative_model is None or not hasattr(self, 'user_ids'):
            return []
        
        try:
            # Find user index
            user_idx = np.where(self.user_ids == user_id)[0]
            if len(user_idx) == 0:
                return []
            
            user_idx = user_idx[0]
            
            # Get user's interaction history
            user_interactions = UserInteraction.query.filter_by(user_id=user_id).all()
            interacted_song_ids = {interaction.song_id for interaction in user_interactions}
            
            # Calculate predicted ratings for all songs
            user_vector = self.user_factors[user_idx]
            predicted_ratings = np.dot(self.item_factors.T, user_vector)
            
            # Get song indices and ratings
            predictions = []
            for i, song_id in enumerate(self.song_ids_collab):
                if song_id not in interacted_song_ids:
                    predictions.append({
                        'song_id': int(song_id),
                        'predicted_rating': float(predicted_ratings[i])
                    })
            
            # Sort by predicted rating and return top recommendations
            predictions.sort(key=lambda x: x['predicted_rating'], reverse=True)
            
            return predictions[:n_recommendations]
            
        except Exception as e:
            logger.error(f"Error in collaborative recommendations: {e}")
            return []
    
    def get_hybrid_recommendations(self, user_id: int, n_recommendations: int = 10) -> List[Dict]:
        """Get hybrid recommendations combining content-based and collaborative filtering"""
        # Get collaborative recommendations
        collab_recs = self.get_collaborative_recommendations(user_id, n_recommendations * 2)
        
        # Get user's recent interactions for content-based recommendations
        recent_interactions = UserInteraction.query.filter_by(user_id=user_id)\
            .order_by(UserInteraction.timestamp.desc()).limit(5).all()
        
        content_recs = []
        for interaction in recent_interactions:
            song_recs = self.get_content_based_recommendations(interaction.song_id, 3)
            content_recs.extend(song_recs)
        
        # Combine and rank recommendations
        combined_recs = {}
        
        # Add collaborative recommendations with weight 0.6
        for rec in collab_recs:
            song_id = rec['song_id']
            combined_recs[song_id] = combined_recs.get(song_id, 0) + rec['predicted_rating'] * 0.6
        
        # Add content-based recommendations with weight 0.4
        for rec in content_recs:
            song_id = rec['song_id']
            combined_recs[song_id] = combined_recs.get(song_id, 0) + rec['similarity_score'] * 0.4
        
        # Sort by combined score
        sorted_recs = sorted(combined_recs.items(), key=lambda x: x[1], reverse=True)
        
        # Return top recommendations with song details
        recommendations = []
        for song_id, score in sorted_recs[:n_recommendations]:
            song = Song.query.get(song_id)
            if song:
                recommendations.append({
                    'song_id': song_id,
                    'title': song.title,
                    'artist': song.artist,
                    'album': song.album,
                    'score': score,
                    'spotify_id': song.spotify_id
                })
        
        return recommendations
    
    def get_trending_songs(self, n_songs: int = 10) -> List[Dict]:
        """Get trending songs based on recent interactions"""
        from sqlalchemy import func, desc
        from datetime import datetime, timedelta
        
        # Get songs with most interactions in the last 7 days
        week_ago = datetime.utcnow() - timedelta(days=7)
        
        trending = db.session.query(
            Song.id,
            Song.title,
            Song.artist,
            Song.album,
            Song.spotify_id,
            func.count(UserInteraction.id).label('interaction_count')
        ).join(UserInteraction)\
         .filter(UserInteraction.timestamp >= week_ago)\
         .group_by(Song.id)\
         .order_by(desc('interaction_count'))\
         .limit(n_songs).all()
        
        return [{
            'song_id': song.id,
            'title': song.title,
            'artist': song.artist,
            'album': song.album,
            'spotify_id': song.spotify_id,
            'interaction_count': song.interaction_count
        } for song in trending]
    
    def save_models(self):
        """Save trained models to disk"""
        try:
            os.makedirs('models', exist_ok=True)
            
            if self.content_similarity_matrix is not None:
                joblib.dump(self.content_similarity_matrix, 'models/content_similarity.pkl')
                joblib.dump(self.song_ids, 'models/song_ids.pkl')
                joblib.dump(self.scaler, 'models/scaler.pkl')
                joblib.dump(self.pca, 'models/pca.pkl')
            
            if self.collaborative_model is not None:
                joblib.dump(self.collaborative_model, 'models/collaborative_model.pkl')
                # Save collaborative filtering attributes
                if hasattr(self, 'user_factors'):
                    joblib.dump(self.user_factors, 'models/user_factors.pkl')
                if hasattr(self, 'item_factors'):
                    joblib.dump(self.item_factors, 'models/item_factors.pkl')
                if hasattr(self, 'user_ids'):
                    joblib.dump(self.user_ids, 'models/user_ids.pkl')
                if hasattr(self, 'song_ids_collab'):
                    joblib.dump(self.song_ids_collab, 'models/song_ids_collab.pkl')
            
            logger.info("Models saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving models: {e}")
    
    def load_models(self):
        """Load trained models from disk"""
        try:
            if os.path.exists('models/content_similarity.pkl'):
                self.content_similarity_matrix = joblib.load('models/content_similarity.pkl')
                self.song_ids = joblib.load('models/song_ids.pkl')
                self.scaler = joblib.load('models/scaler.pkl')
                self.pca = joblib.load('models/pca.pkl')
            
            if os.path.exists('models/collaborative_model.pkl'):
                self.collaborative_model = joblib.load('models/collaborative_model.pkl')
                # Load collaborative filtering attributes if they exist
                if os.path.exists('models/user_factors.pkl'):
                    self.user_factors = joblib.load('models/user_factors.pkl')
                if os.path.exists('models/item_factors.pkl'):
                    self.item_factors = joblib.load('models/item_factors.pkl')
                if os.path.exists('models/user_ids.pkl'):
                    self.user_ids = joblib.load('models/user_ids.pkl')
                if os.path.exists('models/song_ids_collab.pkl'):
                    self.song_ids_collab = joblib.load('models/song_ids_collab.pkl')
            
            self.is_trained = True
            logger.info("Models loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            self.is_trained = False

# Global recommendation engine instance
recommendation_engine = SongRecommendationEngine()
