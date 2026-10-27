import json
import os
from .models import CarMake, CarModel, Dealership, Review


def initiate():
    # 1. Populate Car Makes
    car_make_data = [
        {"name": "NISSAN", "description": "Great cars. Japanese technology"},
        {"name": "Mercedes", "description": "Set the standard in luxury and engineering"},
        {"name": "Audi", "description": "Vorsprung durch Technik - German luxury and performance"},
        {"name": "Kia", "description": "Movement that inspires - Korean reliability"},
        {"name": "Toyota", "description": "Prioritizing durability, efficiency, and reliability"},
        {"name": "Ford", "description": "Built Ford Tough - American automotive power"},
    ]

    car_make_instances = []
    for data in car_make_data:
        make, _ = CarMake.objects.get_or_create(
            name=data['name'],
            defaults={'description': data['description']}
        )
        car_make_instances.append(make)

    # 2. Populate Car Models
    car_model_data = [
        {"name": "Pathfinder", "type": "SUV", "year": 2023, "car_make": car_make_instances[0]},
        {"name": "Qashqai", "type": "SUV", "year": 2023, "car_make": car_make_instances[0]},
        {"name": "X-Trail", "type": "SUV", "year": 2023, "car_make": car_make_instances[0]},
        {"name": "A-Class", "type": "SUV", "year": 2023, "car_make": car_make_instances[1]},
        {"name": "C-Class", "type": "SEDAN", "year": 2023, "car_make": car_make_instances[1]},
        {"name": "E-Class", "type": "SEDAN", "year": 2023, "car_make": car_make_instances[1]},
        {"name": "A4", "type": "SEDAN", "year": 2023, "car_make": car_make_instances[2]},
        {"name": "A5", "type": "SEDAN", "year": 2023, "car_make": car_make_instances[2]},
        {"name": "A6", "type": "SEDAN", "year": 2023, "car_make": car_make_instances[2]},
        {"name": "Sorrento", "type": "SUV", "year": 2023, "car_make": car_make_instances[3]},
        {"name": "Carnival", "type": "SUV", "year": 2023, "car_make": car_make_instances[3]},
        {"name": "Cerato", "type": "SEDAN", "year": 2023, "car_make": car_make_instances[3]},
        {"name": "Corolla", "type": "SEDAN", "year": 2023, "car_make": car_make_instances[4]},
        {"name": "Camry", "type": "SEDAN", "year": 2023, "car_make": car_make_instances[4]},
        {"name": "RAV4", "type": "SUV", "year": 2023, "car_make": car_make_instances[4]},
        {"name": "Explorer", "type": "SUV", "year": 2023, "car_make": car_make_instances[5]},
        {"name": "F-150", "type": "SUV", "year": 2023, "car_make": car_make_instances[5]},
    ]

    for data in car_model_data:
        CarModel.objects.get_or_create(
            name=data['name'],
            car_make=data['car_make'],
            defaults={'type': data['type'], 'year': data['year']}
        )

    # 3. Populate Dealerships from JSON fixture if empty
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dealers_json_path = os.path.join(base_dir, 'database', 'data', 'dealerships.json')
    if os.path.exists(dealers_json_path) and Dealership.objects.count() == 0:
        try:
            with open(dealers_json_path, 'r', encoding='utf-8') as f:
                dealers_data = json.load(f).get('dealerships', [])
                for d in dealers_data:
                    Dealership.objects.update_or_create(
                        id=d['id'],
                        defaults={
                            'city': d.get('city', ''),
                            'state': d.get('state', ''),
                            'st': d.get('st', ''),
                            'address': d.get('address', ''),
                            'zip': str(d.get('zip', '')),
                            'lat': d.get('lat'),
                            'long': d.get('long'),
                            'short_name': d.get('short_name', ''),
                            'full_name': d.get('full_name', '')
                        }
                    )
        except Exception as e:
            print(f"Error loading dealerships.json: {e}")

    # Ensure Kansas sample dealership exists
    Dealership.objects.update_or_create(
        id=8,
        defaults={
            'city': 'Topeka',
            'state': 'Kansas',
            'st': 'KS',
            'address': '288 Larry Place',
            'zip': '66642',
            'lat': 39.0429,
            'long': -95.7697,
            'short_name': 'Bytecard',
            'full_name': 'Bytecard Car Dealership'
        }
    )

    # 4. Populate Reviews from JSON fixture if empty
    reviews_json_path = os.path.join(base_dir, 'database', 'data', 'reviews.json')
    if os.path.exists(reviews_json_path) and Review.objects.count() == 0:
        try:
            with open(reviews_json_path, 'r', encoding='utf-8') as f:
                reviews_data = json.load(f).get('reviews', [])
                for r in reviews_data:
                    Review.objects.update_or_create(
                        id=r['id'],
                        defaults={
                            'name': r.get('name', 'Anonymous'),
                            'dealership': r.get('dealership', 1),
                            'review': r.get('review', ''),
                            'purchase': r.get('purchase', False),
                            'purchase_date': r.get('purchase_date', ''),
                            'car_make': r.get('car_make', ''),
                            'car_model': r.get('car_model', ''),
                            'car_year': r.get('car_year'),
                            'sentiment': r.get('sentiment', 'neutral')
                        }
                    )
        except Exception as e:
            print(f"Error loading reviews.json: {e}")

    # Seed sample review for Dealer 8 in Kansas if none exists
    if not Review.objects.filter(dealership=8).exists():
        Review.objects.create(
            name="Alice Walker",
            dealership=8,
            review="Fantastic services and helpful staff. Highly recommended dealership in Topeka!",
            purchase=True,
            purchase_date="05/12/2023",
            car_make="Toyota",
            car_model="Camry",
            car_year=2022,
            sentiment="positive"
        )

    print("Data population complete. Car makes, models, dealerships, and reviews are ready.")
