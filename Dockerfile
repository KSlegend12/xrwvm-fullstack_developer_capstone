# Stage 1: Build React Frontend
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY server/frontend/package*.json ./
RUN npm install
COPY server/frontend ./
RUN npm run build

# Stage 2: Django Backend & Production Server
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY server/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN python -c "import nltk; nltk.download('vader_lexicon')"

# Copy backend code
COPY server/ ./server/
COPY --from=frontend-builder /app/frontend/build /app/server/frontend/build

WORKDIR /app/server

# Run Django setup, migrations, and static asset collection
RUN python manage.py migrate --noinput
RUN python -c "import os, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproj.settings'); django.setup(); from djangoapp.populate import initiate; initiate()"
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "djangoproj.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
