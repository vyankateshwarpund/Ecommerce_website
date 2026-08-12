# 🌐 PythonAnywhere Live Deployment Guide for SPCart

Follow these step-by-step instructions to launch your **SPCart** website live on **PythonAnywhere** (`https://yourusername.pythonanywhere.com`).

---

## 📋 Pre-Deployment Checklist
Before beginning, ensure you have:
1. A free or paid account at [PythonAnywhere.com](https://www.pythonanywhere.com/).
2. Your PythonAnywhere **username** (e.g. `spcartdemo`).
3. Your Git repository URL (GitHub/GitLab) where this codebase is stored.

---

## 🚀 Step 1: Open Bash Console on PythonAnywhere
1. Log in to [PythonAnywhere Dashboard](https://www.pythonanywhere.com/user/).
2. Click on **Consoles** → **Bash**.
3. Clone your GitHub repository:
   ```bash
   git clone https://github.com/YOUR_GITHUB_USERNAME/ECommers_Project.git
   cd ECommers_Project
   ```

---

## 📦 Step 2: Run 1-Click Deployment Script
Inside the PythonAnywhere Bash console, run:
```bash
bash deploy_pythonanywhere.sh
```
This script will automatically:
- Create virtual environment (`venv`)
- Install all dependencies (`requirements.txt`, `gunicorn`, `whitenoise`)
- Collect static files into `staticfiles/`
- Run database migrations (`manage.py migrate`)

---

## 🔑 Step 3: Create Superuser Account (Admin)
Inside the Bash console, run:
```bash
source venv/bin/activate
python manage.py createsuperuser
```
Follow the prompts to set your Admin Username, Email, and Password.

---

## 🌐 Step 4: Configure Web Tab in PythonAnywhere Dashboard

1. Go to the **Web** tab in PythonAnywhere header.
2. Click **Add a new web app**.
3. Choose **Manual configuration** → Select **Python 3.10** (or 3.11).
4. Fill in the following directory paths:

### 📂 Directory Paths:
| Field | Value on PythonAnywhere |
|---|---|
| **Source code** | `/home/YOUR_USERNAME/ECommers_Project` |
| **Working directory** | `/home/YOUR_USERNAME/ECommers_Project` |
| **Virtualenv** | `/home/YOUR_USERNAME/ECommers_Project/venv` |

---

## 📄 Step 5: Update WSGI Configuration File

1. Under the **Web** tab → **Code** section, click the link to **WSGI configuration file** (e.g. `/var/www/YOUR_USERNAME_pythonanywhere_com_wsgi.py`).
2. Delete all default content and paste the following:

```python
import os
import sys

# Replace 'YOUR_USERNAME' with your exact PythonAnywhere username
path = '/home/YOUR_USERNAME/ECommers_Project'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'ecommerce_project.settings.prod'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
3. Click **Save** (top right).

---

## 🎨 Step 6: Configure Static & Media Files Mappings

Under the **Web** tab → **Static files** section, add the following 2 URL mappings:

| URL | Path |
|---|---|
| `/static/` | `/home/YOUR_USERNAME/ECommers_Project/staticfiles` |
| `/media/` | `/home/YOUR_USERNAME/ECommers_Project/media` |

---

## 🔄 Step 7: Reload & Launch Web App!

1. Click the green **Reload YOUR_USERNAME.pythonanywhere.com** button at the top of the Web tab.
2. Open your live website in browser: **`https://YOUR_USERNAME.pythonanywhere.com`**
3. Open Admin Panel: **`https://YOUR_USERNAME.pythonanywhere.com/dashboard/`**

---

### 🎉 Congratulations! Your SPCart E-Commerce Platform is Live!
