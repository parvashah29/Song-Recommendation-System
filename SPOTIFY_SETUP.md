# 🎧 Spotify Integration Setup

## Quick Setup (Optional)

The song recommendation system works perfectly without Spotify integration! However, if you want to connect your Spotify account for enhanced features, follow these steps:

### 1. Get Spotify API Credentials

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Click "Create App"
4. Fill in the app details:
   - **App name**: Song Recommender (or any name you prefer)
   - **App description**: Music recommendation system
   - **Website**: http://localhost:5001 (or your domain)
   - **Redirect URI**: http://localhost:5001/callback
5. Click "Save"
6. Copy your **Client ID** and **Client Secret**

### 2. Update Environment Variables

Edit your `.env` file and replace the placeholder values:

```env
# Spotify API Configuration
SPOTIFY_CLIENT_ID=your-actual-client-id-here
SPOTIFY_CLIENT_SECRET=your-actual-client-secret-here
SPOTIFY_REDIRECT_URI=http://localhost:5001/callback
```

### 3. Restart the Application

After updating the `.env` file, restart your Flask application:

```bash
# Stop the current server (Ctrl+C)
# Then restart:
source venv/bin/activate
python -c "from app import create_app; app = create_app(); app.run(debug=True, port=5001)"
```

### 4. Test Spotify Integration

1. Go to http://localhost:5001
2. Login with any user account
3. Click "Connect Spotify" in the navigation
4. You should be redirected to Spotify for authorization
5. After authorization, you'll be redirected back to the app

## Features Available with Spotify Integration

- **Import your top tracks** from Spotify
- **Get recently played songs** from your Spotify history
- **Create playlists** directly in Spotify
- **Enhanced recommendations** based on your Spotify listening history

## Troubleshooting

### "No client_id" Error
- Make sure you've added the correct Client ID and Secret to your `.env` file
- Restart the application after updating the `.env` file

### Redirect URI Mismatch
- Ensure the redirect URI in your Spotify app settings matches exactly: `http://localhost:5001/callback`
- If you're using a different port, update both the Spotify app settings and the `.env` file

### Authorization Issues
- Make sure you're logged into the correct Spotify account
- Check that your Spotify app is not in "Development Mode" if you want to use it with other accounts

## Without Spotify Integration

The system works great without Spotify! You can still:
- ✅ Get AI-powered recommendations
- ✅ Like, play, and skip songs
- ✅ View trending songs
- ✅ Create and manage playlists
- ✅ Track your listening habits
- ✅ See personalized recommendations

The only difference is that you'll need to manually add songs to the database instead of importing them from Spotify.
