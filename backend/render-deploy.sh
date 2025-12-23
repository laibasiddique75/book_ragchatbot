#!/bin/bash
# render-deploy.sh - Deployment script for Render

# This script is for local testing only. For actual deployment to Render:
# 1. Push this code to a Git repository (GitHub, GitLab, or Bitbucket)
# 2. Connect your repository to Render
# 3. Set the environment variables in Render dashboard

# To run locally for testing:
# 1. Make sure you have Python 3.11 and the required packages installed
# 2. Set your environment variables in a .env file
# 3. Run: bash render-deploy.sh local

if [ "$1" = "local" ]; then
    echo "Starting the application locally for testing..."
    python main.py
else
    echo "This script is for documentation purposes."
    echo "For Render deployment:"
    echo "1. Push your code to a Git repository"
    echo "2. Create a new Web Service on Render"
    echo "3. Set the build command to: pip install -r requirements.txt"
    echo "4. The start command is already in the Procfile"
    echo "5. Set your environment variables in the Render dashboard"
fi