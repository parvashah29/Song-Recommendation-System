from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Song, UserInteraction
from app.recommendation_engine import recommendation_engine
from datetime import datetime
import logging

bp = Blueprint('recommendations', __name__, url_prefix='/recommendations')
logger = logging.getLogger(__name__)

@bp.route('/')
@login_required
def index():
    """Main recommendations page"""
    return render_template('recommendations/index.html')

@bp.route('/api/personalized')
@login_required
def get_personalized_recommendations():
    """Get personalized recommendations for the current user"""
    try:
        n_recommendations = request.args.get('limit', 10, type=int)
        
        # Get hybrid recommendations
        recommendations = recommendation_engine.get_hybrid_recommendations(
            current_user.id, n_recommendations
        )
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'user_id': current_user.id
        })
        
    except Exception as e:
        logger.error(f"Error getting personalized recommendations: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get recommendations'
        }), 500

@bp.route('/api/trending')
def get_trending_songs():
    """Get trending songs"""
    try:
        n_songs = request.args.get('limit', 10, type=int)
        trending = recommendation_engine.get_trending_songs(n_songs)
        
        return jsonify({
            'success': True,
            'trending_songs': trending
        })
        
    except Exception as e:
        logger.error(f"Error getting trending songs: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get trending songs'
        }), 500

@bp.route('/api/similar/<int:song_id>')
def get_similar_songs(song_id):
    """Get songs similar to a given song"""
    try:
        n_recommendations = request.args.get('limit', 10, type=int)
        
        # Get content-based recommendations
        recommendations = recommendation_engine.get_content_based_recommendations(
            song_id, n_recommendations
        )
        
        # Add song details
        similar_songs = []
        for rec in recommendations:
            song = Song.query.get(rec['song_id'])
            if song:
                similar_songs.append({
                    'song_id': song.id,
                    'title': song.title,
                    'artist': song.artist,
                    'album': song.album,
                    'spotify_id': song.spotify_id,
                    'similarity_score': rec['similarity_score']
                })
        
        return jsonify({
            'success': True,
            'similar_songs': similar_songs
        })
        
    except Exception as e:
        logger.error(f"Error getting similar songs: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get similar songs'
        }), 500

@bp.route('/api/interact', methods=['POST'])
@login_required
def record_interaction():
    """Record user interaction with a song"""
    try:
        data = request.get_json()
        
        song_id = data.get('song_id')
        interaction_type = data.get('interaction_type')
        context = data.get('context', 'unknown')
        duration_played = data.get('duration_played', 0)
        
        if not song_id or not interaction_type:
            return jsonify({
                'success': False,
                'error': 'Missing required fields'
            }), 400
        
        # Validate interaction type
        valid_types = ['like', 'play', 'skip', 'add_to_playlist']
        if interaction_type not in valid_types:
            return jsonify({
                'success': False,
                'error': 'Invalid interaction type'
            }), 400
        
        # Check if song exists
        song = Song.query.get(song_id)
        if not song:
            return jsonify({
                'success': False,
                'error': 'Song not found'
            }), 404
        
        # Create interaction record
        interaction = UserInteraction(
            user_id=current_user.id,
            song_id=song_id,
            interaction_type=interaction_type,
            context=context,
            duration_played=duration_played
        )
        
        db.session.add(interaction)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Interaction recorded successfully'
        })
        
    except Exception as e:
        logger.error(f"Error recording interaction: {e}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to record interaction'
        }), 500

@bp.route('/api/retrain', methods=['POST'])
@login_required
def retrain_models():
    """Retrain recommendation models (admin only)"""
    try:
        # Check if user is admin (you can implement admin role later)
        if not current_user.username == 'admin':  # Simple admin check
            return jsonify({
                'success': False,
                'error': 'Unauthorized'
            }), 403
        
        # Retrain models in background
        recommendation_engine.train_models()
        
        return jsonify({
            'success': True,
            'message': 'Models retrained successfully'
        })
        
    except Exception as e:
        logger.error(f"Error retraining models: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrain models'
        }), 500

@bp.route('/api/stats')
@login_required
def get_recommendation_stats():
    """Get recommendation statistics for the user"""
    try:
        # Get user's interaction count
        interaction_count = UserInteraction.query.filter_by(user_id=current_user.id).count()
        
        # Get user's liked songs count
        liked_count = UserInteraction.query.filter_by(
            user_id=current_user.id, 
            interaction_type='like'
        ).count()
        
        # Get user's play count
        play_count = UserInteraction.query.filter_by(
            user_id=current_user.id, 
            interaction_type='play'
        ).count()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_interactions': interaction_count,
                'liked_songs': liked_count,
                'played_songs': play_count,
                'user_id': current_user.id
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting recommendation stats: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get stats'
        }), 500
