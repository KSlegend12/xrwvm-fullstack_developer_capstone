import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import CarMake, CarModel, Dealership, Review
from .populate import initiate


class DealershipAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        initiate()

    def test_car_make_and_model_creation(self):
        """Test CarMake and CarModel models and __str__ representations"""
        make = CarMake.objects.get(name="Toyota")
        self.assertEqual(str(make), "Toyota")
        model = CarModel.objects.filter(car_make=make, name="Camry").first()
        self.assertIsNotNone(model)
        self.assertEqual(model.type, "SEDAN")
        self.assertIn("Toyota Camry", str(model))

    def test_dealership_and_kansas(self):
        """Test Dealership retrieval including Kansas state dealer"""
        dealer = Dealership.objects.filter(state="Kansas").first()
        self.assertIsNotNone(dealer)
        self.assertEqual(dealer.id, 8)
        self.assertEqual(dealer.city, "Topeka")
        self.assertEqual(dealer.st, "KS")

    def test_api_get_all_dealers(self):
        """Test GET /djangoapp/get_dealers"""
        response = self.client.get('/djangoapp/get_dealers')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 200)
        self.assertGreater(len(data['dealers']), 0)

    def test_api_get_dealers_by_state_kansas(self):
        """Test GET /djangoapp/get_dealers/Kansas and /djangoapp/get_dealers/KS"""
        res_kansas = self.client.get('/djangoapp/get_dealers/Kansas')
        self.assertEqual(res_kansas.status_code, 200)
        data_kansas = res_kansas.json()
        self.assertEqual(data_kansas['status'], 200)
        self.assertTrue(any(d['id'] == 8 for d in data_kansas['dealers']))

        res_ks = self.client.get('/djangoapp/get_dealers/KS')
        self.assertEqual(res_ks.status_code, 200)
        data_ks = res_ks.json()
        self.assertEqual(data_ks['status'], 200)
        self.assertTrue(any(d['id'] == 8 for d in data_ks['dealers']))

    def test_api_get_dealer_by_id(self):
        """Test GET /djangoapp/dealer/8"""
        response = self.client.get('/djangoapp/dealer/8')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['dealer'][0]['id'], 8)
        self.assertEqual(data['dealer'][0]['city'], 'Topeka')

    def test_api_get_dealer_reviews(self):
        """Test GET /djangoapp/reviews/dealer/8"""
        response = self.client.get('/djangoapp/reviews/dealer/8')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 200)
        self.assertGreater(len(data['reviews']), 0)
        self.assertIn('sentiment', data['reviews'][0])

    def test_api_get_cars(self):
        """Test GET /djangoapp/get_cars"""
        response = self.client.get('/djangoapp/get_cars')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('CarModels', data)
        self.assertGreater(len(data['CarModels']), 0)
        first_car = data['CarModels'][0]
        self.assertIn('CarMake', first_car)
        self.assertIn('CarModel', first_car)

    def test_api_registration_and_login_logout(self):
        """Test user registration, login, and logout endpoints"""
        reg_payload = {
            "userName": "testdriver99",
            "password": "Password99!",
            "firstName": "Test",
            "lastName": "Driver",
            "email": "testdriver99@example.com"
        }
        reg_res = self.client.post(
            '/djangoapp/register',
            data=json.dumps(reg_payload),
            content_type='application/json'
        )
        self.assertEqual(reg_res.status_code, 200)
        reg_data = reg_res.json()
        self.assertEqual(reg_data['userName'], "testdriver99")
        self.assertEqual(reg_data['status'], "Authenticated")

        # Test duplicate registration rejection
        dup_res = self.client.post(
            '/djangoapp/register',
            data=json.dumps(reg_payload),
            content_type='application/json'
        )
        self.assertEqual(dup_res.status_code, 400)
        self.assertEqual(dup_res.json()['error'], "Already Registered")

        # Test logout
        logout_res = self.client.get('/djangoapp/logout')
        self.assertEqual(logout_res.status_code, 200)
        self.assertEqual(logout_res.json()['status'], "Logged out")

        # Test login
        login_payload = {
            "userName": "testdriver99",
            "password": "Password99!"
        }
        login_res = self.client.post(
            '/djangoapp/login',
            data=json.dumps(login_payload),
            content_type='application/json'
        )
        self.assertEqual(login_res.status_code, 200)
        self.assertEqual(login_res.json()['status'], "Authenticated")

    def test_sentiment_analysis_endpoint(self):
        """Test sentiment analysis of 'Fantastic services'"""
        response = self.client.get('/djangoapp/analyze/Fantastic%20services')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('sentiment', data)
        self.assertEqual(data['sentiment'], 'positive')

    def test_add_review_endpoint(self):
        """Test submitting a review via /djangoapp/add_review"""
        review_payload = {
            "name": "Jordan Smith",
            "dealership": 8,
            "review": "Fantastic services, smooth transaction and polite representatives.",
            "purchase": True,
            "purchase_date": "2023-08-15",
            "car_make": "Toyota",
            "car_model": "Camry",
            "car_year": 2022
        }
        res = self.client.post(
            '/djangoapp/add_review',
            data=json.dumps(review_payload),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['status'], 200)
        self.assertTrue(Review.objects.filter(name="Jordan Smith", dealership=8).exists())
