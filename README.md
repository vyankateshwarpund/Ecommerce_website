# 🛒 SPCart — Smart Shopping, Everyday.
> **Full-Stack Enterprise E-Commerce Platform Built with Django 6.1, MySQL 8.0, Razorpay, Brevo SMTP & Bootstrap 5**

---

## 🌟 Executive Overview
**SPCart** is a modern, production-grade e-commerce web application engineered for speed, security, and exceptional user experience. Built on Django 6.1 with a modular app architecture and MySQL 8.0 backend, SPCart includes end-to-end features for retail shoppers and staff administrators.

---

## 🚀 Key Features

### 🛍️ Customer Experience
- **Interactive Home Page & Dynamic Product Catalog:** Handpicked featured categories, best sellers, trending deals, and live stock count indicators.
- **Real-Time AJAX Search & Filter:** Instant autocomplete search bar (`/products/autocomplete/`) with multi-facet filters (Category, Brand, Price Range, In-Stock, Sort by Rating/Price/Newest).
- **Product Detail & Pincode Checker:** Multi-image gallery switcher, 6-digit Indian Pincode delivery estimator, technical specifications matrix, and verified buyer reviews.
- **Cart & Wishlist Engine:** Real-time quantity capping, instant AJAX add-to-cart & wishlist toggling without page reload, live top navbar badge updates, and coupon discount system.
- **Checkout & Multi-Payment Integration:** Integrated with **Razorpay Payment Gateway** (Credit/Debit, UPI, Net Banking) and **Cash on Delivery (COD)** with OTP order verification.
- **Order Lifecycle & Invoices:** Real-time order tracking timeline, automated PDF invoice generator, and in-app Notification Center with badge counter.
- **Automated Dual HTML Email Notifications:** Triggered upon Account Registration (Welcome), Order Confirmation, Order Shipping, Order Delivery, Order Cancellation, and Password Reset.

### 🛡️ Admin & Staff Control Panel (`/dashboard/`)
- **Executive Dashboard Analytics:** Stat cards (Revenue, Orders, Products, Customers), Chart.js visual charts (Monthly Revenue Line Chart & Order Status Doughnut Chart), and low stock alerts.
- **Product & Inventory Management:** 1-click stock quantity updates, product creation with main image & gallery uploads, brand CRUD, and category CRUD.
- **Customer Management:** Account list with lifetime spend metrics, 1-click **Block / Unblock** access toggle, customer creation, and deletion.
- **Order Processing:** Staff order management with status dropdown updates (Pending → Processing → Shipped → Delivered → Cancelled).
- **Review Moderation:** 1-click review **Approve / Hide / Delete** actions.
- **CSV Data Reports Export:** Downloadable CSV reports for Orders, Products, and Customers.

---

## 🏗️ Technology Stack

| Component | Technology / Library |
|---|---|
| **Backend Framework** | Django 6.1 (Python 3.14) |
| **Database Engine** | MySQL 8.0 (MySQLClient 2.2.7) |
| **Frontend UI** | HTML5, Vanilla CSS3 (Design Tokens), Bootstrap 5.3, FontAwesome 6 |
| **Payment Gateway** | Razorpay REST API SDK (`razorpay 1.4.2`) |
| **Email Service** | Gmail SMTP / Brevo (HTML Email Templates with inline CSS) |
| **Static File Compression** | WhiteNoise (`whitenoise 6.9.0`) |
| **WSGI Application Server** | Gunicorn (`gunicorn 23.0.0`) |
| **Environment Config** | django-environ (`django-environ 0.12.0`) |

---

## 📁 Modular Project Architecture

```text
ECommers_Project/
├── ecommerce_project/      # Main Project Settings & Routing
│   ├── settings/
│   │   ├── base.py         # Shared Settings & App Registrations
│   │   ├── dev.py          # Local Development Settings (DEBUG=True)
│   │   └── prod.py         # Production Settings (DEBUG=False, Security Headers)
│   ├── urls.py             # Top-Level Router & Custom Error Handlers (404, 403, 500)
│   └── wsgi.py             # WSGI Application Entrypoint
├── accounts/               # User Authentication, Profiles, Addresses, & OTP Verification
├── products/               # Product Catalog, Multi-Image Gallery, & Search Autocomplete
├── categories/             # Dynamic Category Models & Context Processors
├── cart/                   # Shopping Cart Engine & AJAX Badge Handlers
├── wishlist/               # Wishlist Management & Real-Time Counter
├── orders/                 # Checkout, Order Lifecycle, PDF Invoice Generation
├── payments/               # Razorpay Merchant Gateway Webhook & Verification
├── reviews/                # Verified Buyer Star Ratings & Average Auto-Calculation
├── notifications/          # Customer Notification Center & Global Navbar Bell Badge
├── dashboard/              # Staff Admin Control Panel & Chart.js Visual Analytics
├── core/                   # Home, About, Contact, HTML Email Utils, & Custom Error Views
├── static/                 # CSS Stylesheets (style.css), JS Logic (main.js), Brand Assets
├── templates/              # HTML Templates & Modular Includes
├── .env.example            # Deployment Environment Variables Template
├── Procfile                # Gunicorn Server Process Configuration
└── manage.py               # Django Management CLI
```

---

## ⚙️ Local Development Setup Guide

### 1. Clone & Setup Virtual Environment
```bash
git clone https://github.com/your-repo/spcart.git
cd ECommers_Project
python -m venv venv
venv\Scripts\activate      # On Windows
# source venv/bin/activate # On Linux/macOS
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure `.env` File
Create a `.env` file in the root project directory:
```env
DEBUG=True
SECRET_KEY=your-django-secret-key-here
ALLOWED_HOSTS=127.0.0.1,localhost

# Database Configuration
USE_MYSQL=True
DB_NAME=spcart_db
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=127.0.0.1
DB_PORT=3307

# Email SMTP Credentials
EMAIL_HOST_USER=pundsaurav@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Razorpay Test Keys
RAZORPAY_KEY_ID=rzp_test_TO6AddByUy1ngY
RAZORPAY_KEY_SECRET=x0DmYbAgeblxmKGjvQJDbouM
```

### 4. Database Migration & Superuser Setup
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Start Development Server
```bash
python manage.py runserver 127.0.0.1:8000
```
Visit `http://127.0.0.1:8000/` in your browser.

---

## 🌐 PythonAnywhere Deployment Guide

1. **Clone Code & Create Virtualenv on PythonAnywhere:**
   ```bash
   git clone https://github.com/your-repo/spcart.git
   cd spcart
   mkvirtualenv --python=/usr/bin/python3.10 spcart-venv
   pip install -r requirements.txt
   ```

2. **Configure Environment & Static Files:**
   ```bash
   cp .env.example .env
   # Edit .env with your PythonAnywhere MySQL credentials and SECRET_KEY
   python manage.py collectstatic --noinput
   python manage.py migrate
   ```

3. **Configure PythonAnywhere Web Tab:**
   - **Source code:** `/home/yourusername/spcart`
   - **Working directory:** `/home/yourusername/spcart`
   - **Virtualenv:** `/home/yourusername/.virtualenvs/spcart-venv`
   - **WSGI configuration file:** Point to `ecommerce_project.wsgi`
   - **Static Files mapping:**
     - `/static/` → `/home/yourusername/spcart/staticfiles/`
     - `/media/` → `/home/yourusername/spcart/media/`

4. **Reload Web App:** Click **Reload yourusername.pythonanywhere.com**.

---

## 🛡️ License & Credits
Developed with ❤️ by the **SPCart Engineering Team**.
All product images and brand placeholders belong to their respective copyright holders.
