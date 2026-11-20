#!/usr/bin/env python3
"""
Setup script for the Song Recommendation System
This script helps with initial setup and installation.
"""

import os
import sys
import subprocess
import shutil

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def create_virtual_environment():
    """Create virtual environment"""
    if os.path.exists('venv'):
        print("📁 Virtual environment already exists")
        return True
    
    return run_command('python -m venv venv', 'Creating virtual environment')

def install_dependencies():
    """Install Python dependencies"""
    if os.name == 'nt':  # Windows
        pip_command = 'venv\\Scripts\\pip'
    else:  # Unix/Linux/macOS
        pip_command = 'venv/bin/pip'
    
    return run_command(f'{pip_command} install -r requirements.txt', 'Installing dependencies')

def create_env_file():
    """Create .env file from template"""
    if os.path.exists('.env'):
        print("📄 .env file already exists")
        return True
    
    if os.path.exists('.env.example'):
        shutil.copy('.env.example', '.env')
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env file and add your Spotify API credentials")
        return True
    else:
        print("❌ .env.example file not found")
        return False

def setup_database():
    """Set up database and seed data"""
    if os.name == 'nt':  # Windows
        python_command = 'venv\\Scripts\\python'
    else:  # Unix/Linux/macOS
        python_command = 'venv/bin/python'
    
    return run_command(f'{python_command} seed_data.py', 'Setting up database and seeding data')

def main():
    """Main setup function"""
    print("🎵 Song Recommendation System Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    # Setup database
    if not setup_database():
        print("⚠️  Database setup failed, but you can continue")
        print("   Run 'python seed_data.py' manually after setting up .env")
    
    print("\n" + "=" * 40)
    print("🎉 Setup completed successfully!")
    print("=" * 40)
    print("\nNext steps:")
    print("1. Edit .env file and add your Spotify API credentials")
    print("2. Get Spotify API credentials from: https://developer.spotify.com/dashboard")
    print("3. Run the application: python run.py")
    print("4. Open http://localhost:5000 in your browser")
    print("\nSample users:")
    print("- admin / admin123")
    print("- alice / password123")
    print("- bob / password123")
    print("- charlie / password123")
    print("- diana / password123")
    print("- eve / password123")

if __name__ == '__main__':
    main()
