# 🛍️ ShopSphere — Production-Level E-Commerce Platform

**ShopSphere** is a full-featured, scalable, production-ready e-commerce web application built using Python, Django, MySQL, Bootstrap 5, and JavaScript.

---

## 🛠️ Technology Stack

- **Backend:** Python 3.14+, Django 5.x
- **Frontend:** HTML5, CSS3 (Vanilla + Custom Tokens), Bootstrap 5, JavaScript (ES6+)
- **Database:** MySQL 8.x
- **Storage:** Cloudinary (Optional) / Local Media
- **Email:** Brevo API / SMTP
- **Deployment:** Render + Gunicorn + WhiteNoise

---

## 🚀 Quick Setup

### 1. Clone Repository & Setup Virtual Environment
```bash
git clone https://github.com/your-username/ShopSphere.git
cd ShopSphere

python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your MySQL credentials:
```ini
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=shopsphere_db
DB_USER=shopsphere_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

### 3. Run Migrations & Start Server
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000` in your browser.

---

## 📄 License
Designed and Developed by Saurav Pund.
