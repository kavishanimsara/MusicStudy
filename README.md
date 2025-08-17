# MusicStudy

A simple, student-friendly web app that uses **music to support focus, wellness, and productivity**. Built with **Django + Bootstrap**.

Goal: help learners quickly pick music, start a focus timer, and track study sessions — without distractions.

---

## Features

- **User Accounts** – Sign up/in, profile basics.
- **Music Categories** – Curated categories (e.g., Classical, Ambient, Chill, Instrumental, Focus) with images.
- **Focus / Study Timer** – Manually set a duration, start the timer, and get an **alarm sound + completion message**.
- **Favorites & History** – Save preferred categories; basic session history.
- **Clean UI** – Responsive Bootstrap styling with a study-friendly color theme.
- **Simple Admin** – Manage content via Django Admin.

Note: This is an educational project. Some features may be minimal by design and easy to extend.

---

## Tech Stack

- **Backend:** Django (Python)
- **Frontend:** Bootstrap 5, HTML, CSS, JavaScript
- **Database:** SQLite (dev), PostgreSQL/MySQL supported
- **Auth:** Django built-in auth

---

## Project Structure

```text
MusicStudy/
├─ manage.py
├─ requirements.txt
├─ .env.example
├─ README.md
├─ musicstudy/                  # Django project settings
│  ├─ __init__.py
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py / asgi.py
├─ app/                          # Main app (views, models, templates, static)
│  ├─ migrations/
│  ├─ models.py
│  ├─ views.py
│  ├─ urls.py
│  ├─ templates/
│  │  ├─ base.html
│  │  ├─ home.html
│  │  ├─ login.html / signup.html
│  │  ├─ categories.html
│  │  ├─ timer.html
│  │  └─ about.html
│  └─ static/
│     └─ images/ (Classical.jpeg, Ambient.jpeg, etc.)
└─ db.sqlite3
```

---

## Getting Started (Local)

### 1) Prerequisites

- Python **3.10+**
- Git
- (Optional) `virtualenv` or `conda`

### 2) Clone & Setup

```bash
# clone
git clone https://github.com/kavishanimsara/MusicStudy.git
cd MusicStudy

# create & activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt
```

### 3) Environment Variables

Create a `.env` file (or export variables) using the template below. If you don’t have a `.env.example`, copy this:

```env
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3
```

### 4) Database & Admin

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5) Run the Server

```bash
python manage.py runserver
```

Visit: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Usage Guide

1. Register / Log in to unlock favorites and session history.
2. Browse Music Categories and pick one.
3. Open the Study Timer, set your custom time, and start.
4. When the timer finishes, you’ll hear an alarm and see a completion message.
5. Mark categories as favorites and review your recent study sessions.

---

## Screenshots

Add images to `/app/static/images/` and reference them here:

- Home: `![Home](/app/static/images/home.png)`
- Categories: `![Categories](/app/static/images/categories.png)`
- Timer: `![Timer](/app/static/images/timer.png)`
- About: `![About](/app/static/images/about.png)`

---

## Deployment Notes

- Collect static files for production:

```bash
python manage.py collectstatic
```

- For production (DEBUG=False), set `ALLOWED_HOSTS` and use a production database.
- When deploying on Render, Railway, or Heroku:
  - Configure environment variables (SECRET\_KEY, DEBUG, ALLOWED\_HOSTS, DATABASE\_URL).
  - Add `gunicorn` to `requirements.txt`.
  - Use `whitenoise` or cloud storage for static files.

---

## Tests

If tests are present:

```bash
pytest
```

Or Django’s test runner:

```bash
python manage.py test
```

## Contact

- GitHub: [@kavishanimsara](https://github.com/kavishanimsara)

