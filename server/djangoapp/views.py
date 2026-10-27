from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import logging
import json

from .models import CarMake, CarModel, Dealership, Review
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review

logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    """Handle sign in request"""
    try:
        data = json.loads(request.body)
        username = data.get('userName', '')
        password = data.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({
                "userName": username,
                "status": "Authenticated",
                "firstName": user.first_name,
                "lastName": user.last_name
            })
        else:
            return JsonResponse({
                "userName": username,
                "status": "Failed",
                "error": "Invalid credentials"
            }, status=401)
    except Exception as e:
        logger.error(f"Login error: {e}")
        return JsonResponse({"status": "Failed", "error": str(e)}, status=400)


def logout_request(request):
    """Handle sign out request"""
    logout(request)
    return JsonResponse({"userName": "", "status": "Logged out"})


@csrf_exempt
def registration(request):
    """Handle sign up request"""
    try:
        data = json.loads(request.body)
        username = data.get('userName', '')
        password = data.get('password', '')
        first_name = data.get('firstName', '')
        last_name = data.get('lastName', '')
        email = data.get('email', '')

        if User.objects.filter(username=username).exists():
            return JsonResponse({"userName": username, "error": "Already Registered"}, status=400)

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )
        login(request, user)
        return JsonResponse({
            "userName": username,
            "status": "Authenticated",
            "firstName": first_name,
            "lastName": last_name
        })
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return JsonResponse({"error": str(e)}, status=400)


def get_cars(request):
    """Return all car makes and models"""
    if CarMake.objects.count() == 0:
        initiate()
    car_models = CarModel.objects.select_related('car_make').all()
    cars = []
    for cm in car_models:
        cars.append({
            "CarModel": cm.name,
            "CarMake": cm.car_make.name,
            "Type": cm.type,
            "Year": cm.year
        })
    return JsonResponse({"CarModels": cars})


def get_dealerships(request, state="All"):
    """Get all dealerships or dealerships by state"""
    dealers = None
    if state == "All":
        endpoint = "/fetchDealers"
        dealers = get_request(endpoint)
    else:
        endpoint = f"/fetchDealers/{state}"
        dealers = get_request(endpoint)

    if dealers is not None and isinstance(dealers, list):
        return JsonResponse({"status": 200, "dealers": dealers})

    # Fallback to local SQLite database
    if Dealership.objects.count() == 0:
        initiate()

    if state == "All":
        qs = Dealership.objects.all()
    else:
        qs = Dealership.objects.filter(Q(state__iexact=state) | Q(st__iexact=state))

    local_dealers = []
    for d in qs:
        local_dealers.append({
            "id": d.id,
            "city": d.city,
            "state": d.state,
            "st": d.st,
            "address": d.address,
            "zip": d.zip,
            "lat": d.lat,
            "long": d.long,
            "short_name": d.short_name,
            "full_name": d.full_name
        })
    return JsonResponse({"status": 200, "dealers": local_dealers})


def get_dealer_details(request, dealer_id):
    """Get dealer details by ID"""
    endpoint = f"/fetchDealer/{dealer_id}"
    dealer = get_request(endpoint)
    if dealer is not None:
        if isinstance(dealer, dict):
            dealer = [dealer]
        return JsonResponse({"status": 200, "dealer": dealer})

    # Local fallback
    if Dealership.objects.count() == 0:
        initiate()

    try:
        d = Dealership.objects.get(id=dealer_id)
        local_dealer = [{
            "id": d.id,
            "city": d.city,
            "state": d.state,
            "st": d.st,
            "address": d.address,
            "zip": d.zip,
            "lat": d.lat,
            "long": d.long,
            "short_name": d.short_name,
            "full_name": d.full_name
        }]
        return JsonResponse({"status": 200, "dealer": local_dealer})
    except Dealership.DoesNotExist:
        return JsonResponse({"status": 404, "message": "Dealer not found"}, status=404)


def get_dealer_reviews(request, dealer_id):
    """Get reviews for a particular dealer and evaluate sentiment"""
    endpoint = f"/fetchReviews/dealer/{dealer_id}"
    reviews = get_request(endpoint)

    if reviews is None or len(reviews) == 0:
        # Local fallback
        if Review.objects.count() == 0:
            initiate()
        qs = Review.objects.filter(dealership=dealer_id)
        reviews = []
        for r in qs:
            reviews.append({
                "id": r.id,
                "name": r.name,
                "dealership": r.dealership,
                "review": r.review,
                "purchase": r.purchase,
                "purchase_date": r.purchase_date,
                "car_make": r.car_make,
                "car_model": r.car_model,
                "car_year": r.car_year,
                "sentiment": r.sentiment
            })

    # Attach sentiment analysis for each review
    for rev in reviews:
        if not rev.get('sentiment') or rev.get('sentiment') == 'neutral':
            senti_res = analyze_review_sentiments(rev['review'])
            if senti_res and 'sentiment' in senti_res:
                rev['sentiment'] = senti_res['sentiment']

    return JsonResponse({"status": 200, "reviews": reviews})


@csrf_exempt
def add_review(request):
    """Submit a dealer review"""
    if request.user.is_authenticated or request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Forward to microservice if running
            post_review(data)

            # Persist in local database
            rev_name = data.get('name')
            if not rev_name or rev_name == 'null null' or 'null' in rev_name:
                rev_name = request.user.username if request.user.is_authenticated else "Verified Driver"

            rev_text = data.get('review', '')
            senti_res = analyze_review_sentiments(rev_text)
            sentiment_val = senti_res.get('sentiment', 'positive') if senti_res else 'positive'

            Review.objects.create(
                name=rev_name,
                dealership=int(data.get('dealership', 1)),
                review=rev_text,
                purchase=data.get('purchase', True),
                purchase_date=data.get('purchase_date', ''),
                car_make=data.get('car_make', ''),
                car_model=data.get('car_model', ''),
                car_year=data.get('car_year'),
                sentiment=sentiment_val
            )
            return JsonResponse({"status": 200, "message": "Review posted successfully"})
        except Exception as e:
            logger.error(f"Add review error: {e}")
            return JsonResponse({"status": 400, "message": f"Error inserting review: {e}"}, status=400)
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"}, status=403)


def analyze_sentiment(request, input_txt):
    """Direct sentiment analysis endpoint for verification and tests"""
    res = analyze_review_sentiments(input_txt)
    return JsonResponse(res)
