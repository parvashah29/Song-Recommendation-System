# 🚀 Installation Guide

## Quick Setup (Recommended)

1. **Run the setup script**
   ```bash
   python setup.py
   ```

2. **Edit .env file**
   Add your Spotify API credentials to the `.env` file

3. **Run the application**
   ```bash
   python run.py
   ```

## Manual Setup

### Step 1: Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Spotify API Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Copy your Client ID and Client Secret
4. Add `http://localhost:5000/callback` to redirect URIs

### Step 3: Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your credentials
# SECRET_KEY=your-secret-key-here
# SPOTIFY_CLIENT_ID=your-spotify-client-id
# SPOTIFY_CLIENT_SECRET=your-spotify-client-secret
# SPOTIFY_REDIRECT_URI=http://localhost:5000/callback
```

### Step 4: Database Setup

```bash
# Seed the database with sample data
python seed_data.py
```

### Step 5: Run Application

```bash
python run.py
```

## Troubleshooting

### Common Issues

1. **Import errors for surprise/implicit**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **Spotify API errors**
   - Check your Client ID and Secret
   - Ensure redirect URI matches exactly
   - Verify your Spotify app is not in development mode restrictions

3. **Database errors**
   ```bash
   # Delete existing database and recreate
   rm instance/song_recommender.db
   python seed_data.py
   ```

4. **Port already in use**
   ```bash
   # Kill process on port 5000
   lsof -ti:5000 | xargs kill -9
   ```

### Dependencies Issues

If you encounter issues with specific packages:

```bash
# For macOS with M1/M2 chips
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# For Windows
pip install --upgrade pip
pip install -r requirements.txt

# For Linux
sudo apt-get update
sudo apt-get install python3-dev
pip install -r requirements.txt
```

## Verification

After installation, verify everything works:

1. **Check application starts**
   ```bash
   python run.py
   # Should see: Running on http://127.0.0.1:5000
   ```

2. **Test login**
   - Go to http://localhost:5000
   - Login with: admin / admin123
   - Should see the dashboard

3. **Test recommendations**
   - Click "Get My Recommendations"
   - Should see personalized song recommendations

4. **Test Spotify integration**
   - Click "Connect Spotify"
   - Should redirect to Spotify authorization

## Production Deployment

### Environment Variables for Production

```env
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:pass@localhost/song_recommender
SPOTIFY_CLIENT_ID=your-spotify-client-id
SPOTIFY_CLIENT_SECRET=your-spotify-client-secret
SPOTIFY_REDIRECT_URI=https://yourdomain.com/callback
FLASK_ENV=production
```

### Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Use strong database credentials
- [ ] Enable HTTPS in production
- [ ] Set up proper CORS policies
- [ ] Use environment variables for all secrets
- [ ] Enable database connection pooling
- [ ] Set up monitoring and logging

## Support

If you encounter issues:

1. Check the [README.md](README.md) for detailed documentation
2. Review the error logs in the console
3. Ensure all dependencies are installed correctly
4. Verify your Spotify API credentials
5. Check that the database was seeded properly

## Next Steps

After successful installation:

1. **Explore the features**
   - Try different user accounts
   - Test the recommendation system
   - Connect your Spotify account

2. **Customize the system**
   - Modify recommendation algorithms
   - Add new features
   - Customize the UI

3. **Deploy to production**
   - Set up a production database
   - Configure environment variables
   - Deploy to your preferred platform

Happy music discovery! 🎵
