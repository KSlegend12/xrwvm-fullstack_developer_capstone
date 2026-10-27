# Dealership Application API Reference & Documentation

This document provides a comprehensive specification of all REST endpoints implemented in the Car Dealership Full-Stack Developer Capstone application. All endpoints return standard JSON responses and adhere to Coursera and IBM Developer Skills Network project requirements.

---

## Base URLs
- **Local Django Backend:** `http://127.0.0.1:8000`
- **Container / Docker Compose:** `http://localhost:8000`
- **Express Microservice (Optional backend):** `http://localhost:3030`
- **Sentiment Analyzer Flask Microservice (Optional backend):** `http://localhost:5050`

---

## 1. Authentication & User Management

### 1.1 User Registration
- **Method:** `POST`
- **Path:** `/djangoapp/register` (also aliased at `/djangoapp/registration`)
- **Description:** Registers a new customer account with username, first name, last name, email, and password. Automatically logs in the user upon successful creation.
- **Authentication Required:** No
- **Request Body (JSON):**
  ```json
  {
    "userName": "testdriver99",
    "password": "Password99!",
    "firstName": "Test",
    "lastName": "Driver",
    "email": "testdriver99@example.com"
  }
  ```
- **Success Response (`200 OK`):**
  ```json
  {
    "userName": "testdriver99",
    "status": "Authenticated",
    "firstName": "Test",
    "lastName": "Driver"
  }
  ```
- **Error Response (`400 Bad Request`):**
  ```json
  {
    "userName": "testdriver99",
    "error": "Already Registered"
  }
  ```
- **Windows PowerShell Example:**
  ```powershell
  $body = @{
    userName = "john_doe"
    password = "SecurePassword123!"
    firstName = "John"
    lastName = "Doe"
    email = "john@example.com"
  } | ConvertTo-Json

  Invoke-RestMethod -Uri "http://127.0.0.1:8000/djangoapp/register" -Method Post -Body $body -ContentType "application/json"
  ```
- **cURL Example:**
  ```bash
  curl -i -X POST http://127.0.0.1:8000/djangoapp/register \
    -H "Content-Type: application/json" \
    -d '{"userName":"john_doe","password":"SecurePassword123!","firstName":"John","lastName":"Doe","email":"john@example.com"}'
  ```

---

### 1.2 User Login
- **Method:** `POST`
- **Path:** `/djangoapp/login`
- **Description:** Authenticates user credentials and establishes a Django session with session cookie.
- **Authentication Required:** No
- **Request Body (JSON):**
  ```json
  {
    "userName": "demouser",
    "password": "Demopass123!"
  }
  ```
- **Success Response (`200 OK`):**
  ```json
  {
    "userName": "demouser",
    "status": "Authenticated",
    "firstName": "Demo",
    "lastName": "Driver"
  }
  ```
- **Error Response (`401 Unauthorized`):**
  ```json
  {
    "userName": "demouser",
    "status": "Failed",
    "error": "Invalid credentials"
  }
  ```
- **Windows PowerShell Example:**
  ```powershell
  $body = @{ userName = "demouser"; password = "Demopass123!" } | ConvertTo-Json
  Invoke-RestMethod -Uri "http://127.0.0.1:8000/djangoapp/login" -Method Post -Body $body -ContentType "application/json" -SessionVariable mySession
  ```
- **cURL Example:**
  ```bash
  curl -i -X POST http://127.0.0.1:8000/djangoapp/login \
    -H "Content-Type: application/json" \
    -d '{"userName":"demouser","password":"Demopass123!"}' \
    -c cookies.txt
  ```

---

### 1.3 User Logout
- **Method:** `GET`
- **Path:** `/djangoapp/logout`
- **Description:** Terminates the current authenticated session and clears session cookies.
- **Authentication Required:** Yes (via session cookie)
- **Success Response (`200 OK`):**
  ```json
  {
    "userName": "",
    "status": "Logged out"
  }
  ```
- **Windows PowerShell Example:**
  ```powershell
  Invoke-RestMethod -Uri "http://127.0.0.1:8000/djangoapp/logout" -Method Get -WebSession $mySession
  ```
- **cURL Example:**
  ```bash
  curl -i -X GET http://127.0.0.1:8000/djangoapp/logout -b cookies.txt
  ```

---

## 2. Dealership Endpoints

### 2.1 Get All Dealerships
- **Method:** `GET`
- **Path:** `/djangoapp/get_dealers`
- **Description:** Retrieves all nationwide dealerships across all 50 states.
- **Authentication Required:** No
- **Success Response (`200 OK`):**
  ```json
  {
    "status": 200,
    "dealers": [
      {
        "id": 1,
        "city": "El Paso",
        "state": "Texas",
        "st": "TX",
        "address": "3 Nova Court",
        "zip": "88563",
        "lat": 31.6948,
        "long": -106.3,
        "short_name": "Holdlamis",
        "full_name": "Holdlamis Car Dealership"
      },
      {
        "id": 8,
        "city": "Topeka",
        "state": "Kansas",
        "st": "KS",
        "address": "288 Larry Place",
        "zip": "66642",
        "lat": 39.0429,
        "long": -95.7697,
        "short_name": "Bytecard",
        "full_name": "Bytecard Car Dealership"
      }
    ]
  }
  ```
- **Windows PowerShell Example:**
  ```powershell
  Invoke-RestMethod -Uri "http://127.0.0.1:8000/djangoapp/get_dealers" -Method Get
  ```
- **cURL Example:**
  ```bash
  curl -i -X GET http://127.0.0.1:8000/djangoapp/get_dealers
  ```

---

### 2.2 Get Dealerships by State (Including Kansas)
- **Method:** `GET`
- **Path:** `/djangoapp/get_dealers/<state>` (e.g. `/djangoapp/get_dealers/Kansas` or `/djangoapp/get_dealers/KS`)
- **Description:** Filters dealerships by full state name or two-letter abbreviation.
- **Authentication Required:** No
- **Success Response (`200 OK`):**
  ```json
  {
    "status": 200,
    "dealers": [
      {
        "id": 8,
        "city": "Topeka",
        "state": "Kansas",
        "st": "KS",
        "address": "288 Larry Place",
        "zip": "66642",
        "lat": 39.0429,
        "long": -95.7697,
        "short_name": "Bytecard",
        "full_name": "Bytecard Car Dealership"
      }
    ]
  }
  ```
- **Windows PowerShell Example:**
  ```powershell
  Invoke-RestMethod -Uri "http://127.0.0.1:8000/djangoapp/get_dealers/Kansas" -Method Get
  ```
- **cURL Example:**
  ```bash
  curl -i -X GET http://127.0.0.1:8000/djangoapp/get_dealers/Kansas
  ```

---

### 2.3 Get Dealership Details by ID
- **Method:** `GET`
- **Path:** `/djangoapp/dealer/<id>` (e.g. `/djangoapp/dealer/8`)
- **Description:** Returns detailed metadata for a specific dealership.
- **Authentication Required:** No
- **Success Response (`200 OK`):**
  ```json
  {
    "status": 200,
    "dealer": [
      {
        "id": 8,
        "city": "Topeka",
        "state": "Kansas",
        "st": "KS",
        "address": "288 Larry Place",
        "zip": "66642",
        "lat": 39.0429,
        "long": -95.7697,
        "short_name": "Bytecard",
        "full_name": "Bytecard Car Dealership"
      }
    ]
  }
  ```
- **Windows PowerShell Example:**
  ```powershell
  Invoke-RestMethod -Uri "http://127.0.0.1:8000/djangoapp/dealer/8" -Method Get
  ```
- **cURL Example:**
  ```bash
  curl -i -X GET http://127.0.0.1:8000/djangoapp/dealer/8
  ```

---

## 3. Reviews & Sentiment Analysis Endpoints

### 3.1 Get Dealer Reviews
- **Method:** `GET`
- **Path:** `/djangoapp/reviews/dealer/<id>` (e.g. `/djangoapp/reviews/dealer/15`)
- **Description:** Fetches all customer reviews for the specified dealership, enriched with automated sentiment analysis (`positive`, `neutral`, or `negative`).
- **Authentication Required:** No
- **Success Response (`200 OK`):**
  ```json
  {
    "status": 200,
    "reviews": [
      {
        "id": 1,
        "name": "Berkly Shepley",
        "dealership": 15,
        "review": "Total grid-enabled service-desk",
        "purchase": true,
        "purchase_date": "07/11/2020",
        "car_make": "Audi",
        "car_model": "A6",
        "car_year": 2010,
        "sentiment": "neutral"
      },
      {
        "id": 37,
        "name": "Albrecht Collen",
        "dealership": 15,
        "review": "Pre-emptive heuristic solution",
        "purchase": true,
        "purchase_date": "10/10/2020",
        "car_make": "Lexus",
        "car_model": "IS F",
        "car_year": 2009,
        "sentiment": "positive"
      }
    ]
  }
  ```
- **Windows PowerShell Example:**
  ```powershell
  Invoke-RestMethod -Uri "http://127.0.0.1:8000/djangoapp/reviews/dealer/15" -Method Get
  ```
- **cURL Example:**
  ```bash
  curl -i -X GET http://127.0.0.1:8000/djangoapp/reviews/dealer/15
  ```

---

### 3.2 Add a Review
- **Method:** `POST`
- **Path:** `/djangoapp/add_review`
- **Description:** Posts a customer review for a dealership. Automatically computes sentiment and saves to persistent storage.
- **Authentication Required:** Yes (or valid user details in request)
- **Request Body (JSON):**
  ```json
  {
    "name": "Jordan Smith",
    "dealership": 8,
    "review": "Fantastic services, smooth transaction and polite representatives.",
    "purchase": true,
    "purchase_date": "2023-08-15",
    "car_make": "Toyota",
    "car_model": "Camry",
    "car_year": 2022
  }
  ```
- **Success Response (`200 OK`):**
  ```json
  {
    "status": 200,
    "message": "Review posted successfully"
  }
  ```
- **Windows PowerShell Example:**
  ```powershell
  $body = @{
    name = "Jordan Smith"
    dealership = 8
    review = "Fantastic services, smooth transaction and polite representatives."
    purchase = $true
    purchase_date = "2023-08-15"
    car_make = "Toyota"
    car_model = "Camry"
    car_year = 2022
  } | ConvertTo-Json

  Invoke-RestMethod -Uri "http://127.0.0.1:8000/djangoapp/add_review" -Method Post -Body $body -ContentType "application/json"
  ```
- **cURL Example:**
  ```bash
  curl -i -X POST http://127.0.0.1:8000/djangoapp/add_review \
    -H "Content-Type: application/json" \
    -d '{"name":"Jordan Smith","dealership":8,"review":"Fantastic services!","purchase":true,"purchase_date":"2023-08-15","car_make":"Toyota","car_model":"Camry","car_year":2022}'
  ```

---

### 3.3 Sentiment Analysis
- **Method:** `GET`
- **Path:** `/djangoapp/analyze/<text>` (e.g. `/djangoapp/analyze/Fantastic%20services`)
- **Description:** Evaluates the sentiment polarity of any input text using NLTK VADER or the configured sentiment analyzer microservice.
- **Authentication Required:** No
- **Success Response (`200 OK`):**
  ```json
  {
    "sentiment": "positive"
  }
  ```
- **Windows PowerShell Example:**
  ```powershell
  Invoke-RestMethod -Uri "http://127.0.0.1:8000/djangoapp/analyze/Fantastic%20services" -Method Get
  ```
- **cURL Example:**
  ```bash
  curl -i -X GET "http://127.0.0.1:8000/djangoapp/analyze/Fantastic%20services"
  ```

---

## 4. Vehicle Inventory & Catalog Endpoints

### 4.1 Get All Car Makes and Models
- **Method:** `GET`
- **Path:** `/djangoapp/get_cars`
- **Description:** Retrieves all registered car makes and models configured in the database.
- **Authentication Required:** No
- **Success Response (`200 OK`):**
  ```json
  {
    "CarModels": [
      {
        "CarModel": "Pathfinder",
        "CarMake": "NISSAN",
        "Type": "SUV",
        "Year": 2023
      },
      {
        "CarModel": "Corolla",
        "CarMake": "Toyota",
        "Type": "SEDAN",
        "Year": 2023
      },
      {
        "CarModel": "Camry",
        "CarMake": "Toyota",
        "Type": "SEDAN",
        "Year": 2023
      }
    ]
  }
  ```
- **Windows PowerShell Example:**
  ```powershell
  Invoke-RestMethod -Uri "http://127.0.0.1:8000/djangoapp/get_cars" -Method Get
  ```
- **cURL Example:**
  ```bash
  curl -i -X GET http://127.0.0.1:8000/djangoapp/get_cars
  ```
