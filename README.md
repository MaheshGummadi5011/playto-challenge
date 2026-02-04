# 🚀 Playto Engineering Challenge

### A Full-Stack Social Feed with High-Performance Optimization

![Status](https://img.shields.io/badge/Status-Complete-success)
![Stack](https://img.shields.io/badge/Tech-React_%7C_Django_%7C_SQL-blue)

## 📋 Overview
This project is a prototype of a Reddit-style community feed built to demonstrate solutions to complex backend engineering problems. It features threaded comments, real-time leaderboard aggregation, and concurrency-safe voting.

**Key Engineering Highlights:**
* **N+1 Optimization:** Solved nested comment loading using an O(n) in-memory reconstruction algorithm.
* **Concurrency Safety:** Implemented atomic transactions and database locking to prevent race conditions on votes.
* **Complex Aggregation:** Dynamic "Last 24h" leaderboard calculation without denormalized counters.

---

## 🛠️ Tech Stack
* **Frontend:** React 18, Vite, Tailwind CSS v4
* **Backend:** Python 3.x, Django 5, Django Rest Framework (DRF)
* **Database:** SQLite (Prototyping)

---

## ⚡ Full Setup Guide

Follow these steps to run the project locally.

### 1. Prerequisites
Ensure you have the following installed:
* Node.js (v18 or higher)
* Python (v3.10 or higher)
* Git

### 2. Frontend Setup (React)
Open a terminal window and navigate to the `client` folder.

```bash
# 1. Navigate to the frontend directory
cd client

# 2. Install Node packages
npm install

# 3. Start the development server
npm run dev
```
### 3. Backend Setup (Django)
Open a terminal in the project root directory.

```bash
# 1. Create a virtual environment
python -m venv venv

# 2. Activate the virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate

# 3. Install dependencies
pip install django djangorestframework django-cors-headers

# 4. Apply database migrations
python manage.py migrate

# 5. Create a superuser (for Admin panel access)
python manage.py createsuperuser

# 6. Run the server
python manage.py runserver
