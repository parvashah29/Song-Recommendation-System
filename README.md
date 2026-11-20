# 🎵 Song Recommendation System

A modern, AI-powered music recommendation system built with Flask and machine learning. Discover your next favorite song with personalized recommendations based on your listening habits and music preferences.

## ✨ Features

- **🤖 AI-Powered Recommendations**: Uses both collaborative filtering and content-based filtering
- **🎧 Spotify Integration**: Connect your Spotify account for seamless music discovery
- **📊 User Analytics**: Track your listening habits and get insights
- **🔥 Trending Songs**: Discover what's popular right now
- **📱 Modern UI**: Beautiful, responsive interface built with Bootstrap
- **👥 User Management**: Secure authentication and user profiles
- **📋 Playlist Management**: Create and manage your music playlists

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Spotify Developer Account (for API access)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd song-recommendation
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Spotify API credentials:
   ```env
   SECRET_KEY=your-secret-key-here
   SPOTIFY_CLIENT_ID=your-spotify-client-id
   SPOTIFY_CLIENT_SECRET=your-spotify-client-secret
   SPOTIFY_REDIRECT_URI=http://localhost:5000/callback
   ```

5. **Get Spotify API Credentials**
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Create a new app
   - Copy your Client ID and Client Secret
   - Add `http://localhost:5000/callback` to your app's redirect URIs

6. **Initialize the database and seed sample data**
   ```bash
   python seed_data.py
   ```

7. **Run the application**
   ```bash
   python run.py
   ```

8. **Open your browser**
   Navigate to `http://localhost:5000`

## 🎯 How It Works

### Recommendation Algorithms

1. **Content-Based Filtering**
   - Analyzes audio features (tempo, energy, danceability, etc.)
   - Finds songs similar to your favorites
   - Uses cosine similarity on normalized feature vectors

2. **Collaborative Filtering**
   - Finds users with similar taste
   - Recommends songs liked by similar users
   - Uses SVD (Singular Value Decomposition) algorithm

3. **Hybrid Approach**
   - Combines both methods for better accuracy
   - Weights collaborative filtering at 60% and content-based at 40%
   - Continuously learns from user interactions

### User Interaction Tracking

The system tracks various user interactions to improve recommendations:
- **Likes**: Songs you heart ❤️
- **Plays**: Songs you listen to ▶️
- **Skips**: Songs you skip ⏭️
- **Playlist additions**: Songs you add to playlists 📋

## 🏗️ Project Structure

```
song-recommendation/
├── app/
│   ├── __init__.py              # Flask app initialization
│   ├── models/                  # Database models
│   │   ├── user.py             # User model
│   │   ├── song.py             # Song model
│   │   ├── playlist.py         # Playlist models
│   │   └── user_interaction.py # Interaction tracking
│   ├── routes/                 # API routes
│   │   ├── auth.py            # Authentication
│   │   ├── songs.py           # Song management
│   │   ├── playlists.py       # Playlist management
│   │   └── recommendations.py # Recommendation API
│   ├── services/              # Business logic
│   │   └── spotify_service.py # Spotify integration
│   ├── templates/             # HTML templates
│   │   ├── base.html         # Base template
│   │   ├── auth/             # Auth templates
│   │   ├── songs/            # Song templates
│   │   └── recommendations/  # Recommendation templates
│   └── recommendation_engine.py # ML recommendation engine
├── config.py                  # Configuration
├── run.py                     # Application entry point
├── seed_data.py              # Database seeding script
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Flask secret key | Yes |
| `DATABASE_URL` | Database connection string | No (defaults to SQLite) |
| `SPOTIFY_CLIENT_ID` | Spotify API client ID | Yes |
| `SPOTIFY_CLIENT_SECRET` | Spotify API client secret | Yes |
| `SPOTIFY_REDIRECT_URI` | Spotify OAuth redirect URI | No (defaults to localhost:5000/callback) |

### Database

The application uses SQLite by default for development. For production, consider using PostgreSQL:

```env
DATABASE_URL=postgresql://username:password@localhost/song_recommender
```

## 📊 Sample Data

The seeding script creates:
- 6 sample users (including admin)
- 10 popular songs with audio features
- Random user interactions
- Sample playlists
- Trained recommendation models

### Sample Users
- **admin** / admin123
- **alice** / password123
- **bob** / password123
- **charlie** / password123
- **diana** / password123
- **eve** / password123

## 🎨 Customization

### Adding New Features

1. **New Recommendation Algorithms**
   - Extend `SongRecommendationEngine` class
   - Add new methods for different algorithms
   - Update the hybrid recommendation logic

2. **Additional User Interactions**
   - Add new interaction types to `UserInteraction` model
   - Update the recommendation engine to use new interactions
   - Modify the frontend to capture new interactions

3. **Enhanced Spotify Integration**
   - Extend `SpotifyService` class
   - Add new API endpoints
   - Implement real-time playback controls

### Styling

The application uses Bootstrap 5 with custom CSS variables. Main colors:
- Primary: `#1db954` (Spotify Green)
- Secondary: `#191414` (Spotify Black)
- Accent: `#1ed760` (Spotify Light Green)

## 🚀 Deployment

### Heroku Deployment

1. **Create a Heroku app**
   ```bash
   heroku create your-app-name
   ```

2. **Set environment variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set SPOTIFY_CLIENT_ID=your-client-id
   heroku config:set SPOTIFY_CLIENT_SECRET=your-client-secret
   heroku config:set SPOTIFY_REDIRECT_URI=https://your-app-name.herokuapp.com/callback
   ```

3. **Deploy**
   ```bash
   git push heroku main
   ```

4. **Run migrations and seed data**
   ```bash
   heroku run python seed_data.py
   ```

### Docker Deployment

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 5000
   CMD ["python", "run.py"]
   ```

2. **Build and run**
   ```bash
   docker build -t song-recommender .
   docker run -p 5000:5000 song-recommender
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Spotify Web API](https://developer.spotify.com/documentation/web-api/) for music data
- [Spotipy](https://spotipy.readthedocs.io/) for Python Spotify integration
- [Surprise](https://surpriselib.com/) for collaborative filtering
- [Scikit-learn](https://scikit-learn.org/) for machine learning algorithms
- [Bootstrap](https://getbootstrap.com/) for the UI framework

## 📞 Support

If you have any questions or need help, please:
- Open an issue on GitHub
- Check the documentation
- Review the sample data and configuration

---

**Happy Music Discovery! 🎵**
