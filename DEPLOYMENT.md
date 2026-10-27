# Production Deployment Guide

This guide details how to build, containerize, and deploy the Car Dealership Full-Stack Developer Capstone project to production environments.

---

## Architecture Overview
The application consists of:
- **Backend:** Python 3.11+ and Django 4.2 with Django REST Framework.
- **Frontend:** React 18 single-page application compiled to static production bundles served via Django.
- **Database:** SQLite for persistent, zero-configuration storage, or containerized PostgreSQL / MongoDB.
- **Static Assets:** Collected via `python manage.py collectstatic` into `server/static`.
- **WSGI Server:** Gunicorn for production concurrency.

---

## Option 1: Render.com Cloud Deployment (Recommended & Free Tier Compatible)

Render offers free hosting for web services with automatic builds from your GitHub repository.

### Step-by-Step Deployment:
1. **Push your code to GitHub:**
   Ensure your repository `https://github.com/KSlegend12/xrwvm-fullstack_developer_capstone` is up to date on branch `main`.
2. **Sign up or Log in to [Render.com](https://render.com).**
3. **Create New Web Service:**
   - Click **New +** -> **Web Service**.
   - Connect your GitHub repository `xrwvm-fullstack_developer_capstone`.
4. **Configure Service Settings:**
   - **Name:** `fullstack-car-dealership-capstone`
   - **Region:** Oregon (US West) or closest region
   - **Branch:** `main`
   - **Root Directory:** Leave empty (or `.`)
   - **Environment:** `Python 3`
   - **Build Command:**
     ```bash
     pip install -r server/requirements.txt && python -c "import nltk; nltk.download('vader_lexicon')" && cd server/frontend && npm install && npm run build && cd ../.. && python server/manage.py migrate --noinput && python -c "import os, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproj.settings'); django.setup(); from djangoapp.populate import initiate; initiate()" && python server/manage.py collectstatic --noinput
     ```
   - **Start Command:**
     ```bash
     cd server && gunicorn djangoproj.wsgi:application --bind 0.0.0.0:$PORT
     ```
5. **Set Environment Variables:**
   - `DEBUG` = `False`
   - `SECRET_KEY` = `[Click 'Generate' on Render for a 256-bit secure key]`
   - `PYTHON_VERSION` = `3.11.9`
6. **Deploy:**
   - Click **Create Web Service**.
   - Render will build the React frontend, apply migrations, seed the database, and launch Gunicorn.
   - Once deployed, copy your live public URL (e.g. `https://fullstack-car-dealership-capstone.onrender.com`) and paste it into `submission_evidence/deploymentURL`.

---

## Option 2: Docker Container Deployment

The project includes a root `Dockerfile` using a multi-stage build:
1. Node.js 18 builds the React application.
2. Python 3.11 slim runs the backend with Gunicorn.

### Building and Running the Docker Image:
```bash
# Build the production image
docker build -t dealership-capstone .

# Run the container
docker run -d -p 8000:8000 --name dealership_app -e DEBUG=False dealership-capstone
```

### Accessing the Container:
Open your browser to `http://localhost:8000`.

---

## Option 3: Full Microservices Multi-Container (Docker Compose)

To launch the full microservices topology (Django application, Flask sentiment analyzer, MongoDB, and Express API):

```bash
docker-compose up --build -d
```

### Services launched:
- **Django Main App:** `http://localhost:8000`
- **Flask Sentiment Analyzer:** `http://localhost:5050`
- **Node/Express Backend:** `http://localhost:3030`
- **MongoDB Database:** `localhost:27017`

---

## Production Security & Settings Checklist

- [x] `SECRET_KEY` pulled from environment variable with fallback for development.
- [x] `DEBUG` set to `False` in production.
- [x] `ALLOWED_HOSTS` includes wildcard or custom domains (`.onrender.com`, `localhost`).
- [x] `CSRF_TRUSTED_ORIGINS` configured for HTTPS domains.
- [x] Passwords hashed using Django's standard PBKDF2 algorithm.
- [x] Session cookies flagged with `HttpOnly` and `SameSite=Lax`.
- [x] SQLite database and `.env` credentials excluded from Git via `.gitignore`.
