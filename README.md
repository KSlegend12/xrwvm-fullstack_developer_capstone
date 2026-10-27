# Car Dealership Full-Stack Developer Capstone Project

A complete, production-grade automotive dealership platform built for the **Coursera IBM Full-Stack Developer Capstone Project**. This project combines a **Django & Django REST Framework** backend, a responsive **React 18** frontend, automated **NLTK sentiment analysis**, a containerized deployment architecture, and a complete automated CI/CD pipeline with GitHub Actions.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Technology Stack](#technology-stack)
4. [Architecture & Folder Structure](#architecture--folder-structure)
5. [Local Quickstart Guide (Windows PowerShell)](#local-quickstart-guide-windows-powershell)
6. [Demo & Admin Credentials](#demo--admin-credentials)
7. [REST API Reference](#rest-api-reference)
8. [Automated Testing](#automated-testing)
9. [CI/CD Workflow](#cicd-workflow)
10. [Docker & Production Deployment](#docker--production-deployment)
11. [Submission Evidence & Coursera 28-Task Checklist](#submission-evidence--coursera-28-task-checklist)

---

## Project Overview

The Dealership application provides an end-to-end portal for drivers and automotive dealerships nationwide across all 50 US states:
- Users can browse authorized dealerships, filter dealerships by state (including Kansas), view detailed dealer profiles, and read verified customer reviews.
- Reviews include real-time sentiment analysis, tagging customer experiences as **positive**, **neutral**, or **negative**.
- Registered users can log in, view the dealership inventory, and submit new purchase reviews with car make and model selections.
- Administrators manage car makes, car models, dealerships, and reviews directly through the customized Django Administration panel.

---

## Key Features

- **Static Marketing Pages:**
  - Modern, responsive landing page with dealership showcase.
  - Custom `About Us` page featuring corporate executive leadership profiles and demo email contacts.
  - Dedicated `Contact Us` page with corporate headquarters information, operating hours, and customer support channels.
- **User Authentication & Session Management:**
  - Registration with all 5 mandatory fields: Username, First Name, Last Name, Email, and Password.
  - Session-based login and logout with secure CSRF protection and cookie management.
  - Header automatically reflects login state, displaying active username and logout button.
- **Dealership Directory & Filtering:**
  - Nationwide directory of 50 dealerships with city, address, zip code, and state badges.
  - Dynamic state filter dropdown enabling quick filtering (e.g. selecting **Kansas** immediately loads Dealer #8).
- **Dealer Details & Sentiment Analysis:**
  - Detailed dealership profile with address and verified driver reviews.
  - Real-time sentiment classification using NLTK VADER with visual sentiment indicator badges.
- **Review Submission Form:**
  - Review form with live car makes and models dropdown populated from the backend API.
  - Review text, vehicle purchase confirmation, purchase date picker, and year constraints.
  - Instant redirect to dealer detail page showing the newly published review.
- **Django Administration Suite:**
  - Tabular inlines for `CarModel` inside `CarMakeAdmin`.
  - Comprehensive filters and search indices for dealers, car models, and reviews.

---

## Technology Stack

- **Backend:** Python 3.11 / 3.13, Django 4.2+, Django REST Framework
- **Frontend:** React 18, React Router v6, Bootstrap 5, Modern CSS3
- **Natural Language Processing:** NLTK VADER (`SentimentIntensityAnalyzer`)
- **Database:** SQLite (local development and container persistence) / MongoDB & Express microservices compatibility
- **WSGI Server:** Gunicorn
- **Automation & Testing:** Django TestCase, Jest, React Testing Library, Puppeteer
- **CI/CD:** GitHub Actions (`.github/workflows/ci.yml`)
- **Containerization:** Docker (Multi-stage build) and Docker Compose

---

## Architecture & Folder Structure

```text
xrwvm-fullstack_developer_capstone/
├── .github/
│   └── workflows/
│       └── ci.yml                     # Automated CI/CD pipeline
├── server/
│   ├── database/                      # Express/MongoDB microservice files
│   │   ├── data/
│   │   │   ├── dealerships.json       # 50 Dealership fixture records
│   │   │   └── reviews.json           # 50 Review fixture records
│   │   └── app.js
│   ├── djangoapp/                     # Core Django application
│   │   ├── admin.py                   # Django admin inline models & search
│   │   ├── models.py                  # CarMake, CarModel, Dealership, Review
│   │   ├── populate.py                # Database seeder script
│   │   ├── restapis.py                # Microservice & sentiment analysis client
│   │   ├── tests.py                   # 10 comprehensive backend test cases
│   │   ├── urls.py                    # REST API routes
│   │   └── views.py                   # Authentication, dealer, review views
│   ├── djangoproj/                    # Project settings & URL routing
│   │   ├── settings.py
│   │   └── urls.py
│   ├── frontend/                      # React 18 application
│   │   ├── build/                     # Compiled production bundle
│   │   ├── src/
│   │   │   ├── components/
│   │   │   │   ├── Dealers/           # Dealers table, Dealer details, PostReview
│   │   │   │   ├── Header/            # Dynamic navigation header
│   │   │   │   ├── Login/             # Login modal component
│   │   │   │   └── Register/          # 5-field registration component
│   │   │   ├── App.js                 # React router switch
│   │   │   └── App.test.js            # React Testing Library test suite
│   │   └── static/                    # Static templates and assets
│   │       ├── About.html             # About Us marketing page
│   │       ├── Contact.html           # Contact Us marketing page
│   │       └── Home.html              # Landing page template
│   ├── manage.py
│   └── requirements.txt               # Python package dependencies
├── submission_evidence/               # Coursera submission artifacts
│   ├── screenshots/                   # Live browser screenshots
│   ├── django_server                  # Terminal output of running server
│   ├── loginuser                      # cURL login command & output
│   ├── logoutuser                     # cURL logout command & output
│   ├── getalldealers                  # cURL get all dealers command & output
│   ├── getdealersbyState              # cURL Kansas state filter output
│   ├── getdealerbyid                  # cURL dealer 8 details output
│   ├── getdealerreviews               # cURL dealer reviews output
│   ├── getallcarmakes                 # cURL car makes and models output
│   ├── analyzereview                  # cURL 'Fantastic services' output
│   ├── CICD                           # GitHub Actions verification log
│   └── deploymentURL                  # Verified deployment record
├── API_DOCUMENTATION.md               # Complete REST API specification
├── TESTING.md                         # Detailed testing report & results
├── DEPLOYMENT.md                      # Cloud & Docker deployment manual
├── Dockerfile                         # Production multi-stage Docker build
├── docker-compose.yml                 # Multi-service container orchestration
├── render.yaml                        # 1-Click Render.com deployment manifest
├── .env.example                       # Sample environment configuration
└── .gitignore                         # Secret & build artifact ignore rules
```

---

## Local Quickstart Guide (Windows PowerShell)

### Prerequisites
- Python 3.10+ (Verified on Python 3.11 and 3.13)
- Node.js 18+ and npm
- Git

### 1. Clone the Repository
```powershell
git clone https://github.com/KSlegend12/xrwvm-fullstack_developer_capstone.git
cd xrwvm-fullstack_developer_capstone
```

### 2. Install Python Dependencies
```powershell
pip install -r server/requirements.txt
python -c "import nltk; nltk.download('vader_lexicon')"
```

### 3. Build the React Frontend
```powershell
cd server/frontend
npm install
npm run build
cd ../..
```

### 4. Run Database Migrations & Seed Data
```powershell
cd server
python manage.py makemigrations djangoapp
python manage.py migrate
python -c "import os, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproj.settings'); django.setup(); from djangoapp.populate import initiate; initiate()"
python manage.py collectstatic --noinput
```

### 5. Start the Development Server
```powershell
python manage.py runserver 8000
```
Open your browser to: `http://127.0.0.1:8000/`

---

## Demo & Admin Credentials

| Account Role | Username | Password | Email | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **Superuser / Admin** | `admin` | `adminpassword123` | `admin@example.com` | Django Admin (`/admin/`) access |
| **Demo Customer** | `demouser` | `Demopass123!` | `demouser@example.com` | Dealership review submission testing |

---

## REST API Reference

All endpoints return JSON responses. Complete documentation with request and response payloads is available in [API_DOCUMENTATION.md](API_DOCUMENTATION.md).

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/djangoapp/register` | Register new user with 5 required fields |
| `POST` | `/djangoapp/login` | Authenticate user and initiate session |
| `GET` | `/djangoapp/logout` | Terminate session and clear cookie |
| `GET` | `/djangoapp/get_dealers` | Fetch all nationwide dealerships |
| `GET` | `/djangoapp/get_dealers/<state>` | Fetch dealerships in a specific state (e.g. `Kansas` or `KS`) |
| `GET` | `/djangoapp/dealer/<id>` | Fetch detailed metadata for a specific dealership |
| `GET` | `/djangoapp/reviews/dealer/<id>` | Fetch dealer reviews with automated sentiment tags |
| `POST` | `/djangoapp/add_review` | Submit a customer review with purchase details |
| `GET` | `/djangoapp/get_cars` | Fetch car models with corresponding make names |
| `GET` | `/djangoapp/analyze/<text>` | Evaluate sentiment of arbitrary text (`positive`, `neutral`, `negative`) |

---

## Automated Testing

### Backend Unit & Integration Tests:
```powershell
cd server
python manage.py test djangoapp
```
*Result: 10/10 tests passing.*

### Frontend Component Tests:
```powershell
cd server/frontend
npm test -- --watchAll=false
```
*Result: 3/3 tests passing.*

Detailed test documentation is in [TESTING.md](TESTING.md).

---

## CI/CD Workflow

The repository includes a GitHub Actions workflow at `.github/workflows/ci.yml`. On every push or pull request to `main`, it automatically:
1. Installs Python dependencies and downloads the NLTK lexicon.
2. Performs Django system checks and runs migrations.
3. Seeds database fixtures and executes all 10 Django backend tests.
4. Installs npm dependencies and executes all React component tests.
5. Builds the production bundle and validates static asset collection.

The verified local emulation log is preserved in `submission_evidence/CICD`.

---

## Docker & Production Deployment

### 1. Build & Run Single Container (Multi-stage Dockerfile)
```bash
docker build -t dealership-app .
docker run -d -p 8000:8000 -e DEBUG=False dealership-app
```

### 2. Multi-Service Orchestration (Docker Compose)
```bash
docker-compose up --build -d
```

### 3. Deploy to Render.com (1-Click Blueprint)
The project includes a ready-to-deploy `render.yaml` blueprint. Refer to [DEPLOYMENT.md](DEPLOYMENT.md) for full instructions.

---

## Submission Evidence & Coursera 28-Task Checklist

All 11 submission evidence files are located in the `submission_evidence/` folder:

| # | Evidence File | Content Verified |
| :-: | :--- | :--- |
| 1 | `submission_evidence/django_server` | Actual terminal output of running Django development server |
| 2 | `submission_evidence/loginuser` | Actual cURL command and HTTP 200 response for login |
| 3 | `submission_evidence/logoutuser` | Actual cURL command and HTTP 200 response for logout |
| 4 | `submission_evidence/getdealerreviews` | Actual cURL command and dealer reviews with sentiment |
| 5 | `submission_evidence/getalldealers` | Actual cURL command and list of 50 dealerships |
| 6 | `submission_evidence/getdealerbyid` | Actual cURL command and Dealer #8 details |
| 7 | `submission_evidence/getdealersbyState` | Actual cURL command and Kansas state dealership output |
| 8 | `submission_evidence/getallcarmakes` | Actual cURL command and 17 car models with makes |
| 9 | `submission_evidence/analyzereview` | Actual cURL command for sentiment of "Fantastic services" |
| 10 | `submission_evidence/CICD` | Actual CI/CD build and test execution log |
| 11 | `submission_evidence/deploymentURL` | Deployment status and verified URL record |

### Live Screenshots Captured (`submission_evidence/screenshots/`):
- `admin_login.png`: Django admin login page.
- `admin_logout.png`: Django admin logout page.
- `get_dealers.png`: Dealerships directory table before login.
- `get_dealers_loggedin.png`: Dealerships table showing logged-in username and Review column.
- `dealersbystate.png`: Dealerships table filtered to Kansas.
- `dealer_id_reviews.png`: Dealer #8 reviews with sentiment icons.
- `dealership_review_submission.png`: Review submission form with car make/model select.
- `added_review.png`: Dealer details page reflecting newly submitted review.
