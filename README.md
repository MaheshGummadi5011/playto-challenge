# 🚀 Playto Engineering Challenge

### A Full-Stack Social Feed with High-Performance Optimization

![Status](https://img.shields.io/badge/Status-Complete-success)
![Stack](https://img.shields.io/badge/Tech-Django_%7C_React_%7C_SQL-blue)

## 📋 Overview
This project is a prototype of a Reddit-style community feed built to demonstrate solutions to complex backend engineering problems. It features threaded comments, real-time leaderboard aggregation, and concurrency-safe voting.

**Key Engineering Highlights:**
* **N+1 Optimization:** Solved nested comment loading using an O(n) in-memory reconstruction algorithm.
* **Concurrency Safety:** Implemented atomic transactions and database locking to prevent race conditions on votes.
* **Complex Aggregation:** Dynamic "Last 24h" leaderboard calculation without denormalized counters.

---

## 🛠️ Tech Stack
* **Backend:** Python, Django Rest Framework (DRF)
* **Frontend:** React (Vite), Tailwind CSS v4
* **Database:** SQLite (Prototyping), extensible to PostgreSQL

---

## ⚡ Setup Guide

### 1. Backend (Django)
```bash
# Navigate to the root folder
cd playto_challenge

# Activate Virtual Environment (Windows)
venv\Scripts\activate

# Install Dependencies
pip install django djangorestframework django-cors-headers

# Run the Server
python manage.py runserver
