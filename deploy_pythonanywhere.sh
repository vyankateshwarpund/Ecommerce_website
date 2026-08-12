#!/bin/bash
# ============================================================
# SPCart — PythonAnywhere Automated Deployment Script
# Run this inside PythonAnywhere Bash Console:
# bash deploy_pythonanywhere.sh
# ============================================================

echo "🚀 Starting SPCart Deployment on PythonAnywhere..."

# 1. Create Virtual Environment
echo "📦 Setting up Python Virtual Environment..."
python3 -m venv venv
source venv/bin/activate

# 2. Upgrade pip & Install Dependencies
echo "📥 Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn whitenoise

# 3. Create .env File if not exists
if [ ! -f .env ]; then
    echo "📄 Creating default .env file..."
    cp .env.example .env
fi

# 4. Collect Static Files
echo "🎨 Collecting static files for WhiteNoise..."
python manage.py collectstatic --noinput

# 5. Database Migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

echo "=========================================================="
echo "✅ SPCart Deployment Script Completed Successfully!"
echo "Next: Configure Web Tab in PythonAnywhere Dashboard."
echo "=========================================================="
