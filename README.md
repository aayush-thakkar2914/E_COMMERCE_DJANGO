# 🛒 E-Commerce Web Application (Django + Tailwind CSS)

This is a full-featured e-commerce web application built using Django, integrating core shopping features like product browsing, cart management, order placement, and authentication. Tailwind CSS is used for a modern and responsive UI.

---

## 🚀 Features

- ✅ User Authentication (Login, Signup, Logout)
- 🛍️ Browse Products
- 🔍 Product Detail View
- 🧺 Add to Cart / Remove from Cart
- 📦 Place Orders
- 🧾 Order Summary
- 🚫 Out of Stock Indication
- 🎨 Clean UI using Tailwind CSS

---

## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, Tailwind CSS
- **Database**: SQLite (can be replaced with PostgreSQL/MySQL)
- **Authentication**: Django's built-in auth system

---

## 📁 Project Structure

E_Comm_Django/
├── E_Comm_Django/               # Main project settings directory
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py              # Project settings
│   ├── urls.py                  # Root URL configuration
│   └── wsgi.py

├── E_comm/                      # Main app directory
│   ├── __init__.py
│   ├── admin.py                 # Admin interface setup
│   ├── apps.py
│   ├── forms.py                 # Django forms
│   ├── models.py                # Database models
│   ├── tests.py
│   ├── urls.py                  # App-specific URL configuration
│   ├── views/                   # Views folder (contains view logic)
│   │   └── __init__.py
│   ├── migrations/              # Database migrations
│   └── templates/               # HTML templates (Django templates)

├── media/products/              # Uploaded product images

├── static/                      # Static files (CSS, JS, etc.)

├── theme/                       # (Optional) Additional UI-related files

├── db.sqlite3                   # SQLite database

└── manage.py                    # Django's command-line utility

## ⚙️ Setup Instructions

--- 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ecomm-django.git
cd ecomm-django  

--- 2. Create and Activate Virtual Environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

--- 3. Install Dependencies

pip install -r requirements.txt

--- 4. Apply Migrations

python manage.py makemigrations
python manage.py migrate

--- 5. Create Superuser (for admin panel)

python manage.py createsuperuser

--- 6. Run the Server

python manage.py runserver

🧼 Additional Enhancements (TODOs)
-- ✅ Product Image Upload

-- ⏳ Payment Integration 

-- 🧾 Order History for Users

-- 📧 Email Confirmation

-- 🔐 Password Reset

👨‍💻 Developed By: Aayush Thakkar
GitHub: @aayush-thakkar2914