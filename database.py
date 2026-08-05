import os
import json
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

RESTAURANTS_FILE = os.path.join(DATA_DIR, "restaurants.json")
NGOS_FILE = os.path.join(DATA_DIR, "ngos.json")
DONATIONS_FILE = os.path.join(DATA_DIR, "donations.json")

def init_db():
    """Initializes the database directory and seeds sample JSON files if they do not exist."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    # 1. Seed Restaurants if not exists
    if not os.path.exists(RESTAURANTS_FILE) or os.path.getsize(RESTAURANTS_FILE) == 0:
        sample_restaurants = [
            {
                "id": "R1",
                "name": "Green Garden Bistro",
                "cuisine": "Healthy & Salads",
                "phone": "+91 98765 43210",
                "latitude": 12.9716,
                "longitude": 77.5946,
                "joined_date": "2026-06-15"
            },
            {
                "id": "R2",
                "name": "The Pizza Haven",
                "cuisine": "Italian & Fast Food",
                "phone": "+91 98765 43211",
                "latitude": 12.9698,
                "longitude": 77.6123,
                "joined_date": "2026-07-02"
            },
            {
                "id": "R3",
                "name": "Spice Symphony Restaurant",
                "cuisine": "Indian Fine Dine",
                "phone": "+91 98765 43212",
                "latitude": 12.9782,
                "longitude": 77.6405,
                "joined_date": "2026-07-10"
            },
            {
                "id": "R4",
                "name": "Sweet Treats Bakery",
                "cuisine": "Bakery & Desserts",
                "phone": "+91 98765 43213",
                "latitude": 12.9591,
                "longitude": 77.5721,
                "joined_date": "2026-07-25"
            }
        ]
        with open(RESTAURANTS_FILE, 'w') as f:
            json.dump(sample_restaurants, f, indent=4)

    # 2. Seed NGOs if not exists
    if not os.path.exists(NGOS_FILE) or os.path.getsize(NGOS_FILE) == 0:
        sample_ngos = [
            {
                "id": "N1",
                "name": "Robin Hood Army - Central",
                "focus_area": "Cooked Meals Redistribution",
                "phone": "+91 91234 56780",
                "latitude": 12.9750,
                "longitude": 77.6000,
                "capacity_kg": 500,
                "joined_date": "2026-05-10"
            },
            {
                "id": "N2",
                "name": "No Food Waste - Indiranagar",
                "focus_area": "Surplus Groceries & Produce",
                "phone": "+91 91234 56781",
                "latitude": 12.9710,
                "longitude": 77.6320,
                "capacity_kg": 300,
                "joined_date": "2026-06-01"
            },
            {
                "id": "N3",
                "name": "Feed The Needy - Jayanagar",
                "focus_area": "Fresh Produce & Breads",
                "phone": "+91 91234 56782",
                "latitude": 12.9550,
                "longitude": 77.5800,
                "capacity_kg": 250,
                "joined_date": "2026-06-18"
            },
            {
                "id": "N4",
                "name": "Hope Foundation - Malleshwaram",
                "focus_area": "All Food Types (Cooked/Dry)",
                "phone": "+91 91234 56783",
                "latitude": 12.9850,
                "longitude": 77.5850,
                "capacity_kg": 400,
                "joined_date": "2026-07-05"
            }
        ]
        with open(NGOS_FILE, 'w') as f:
            json.dump(sample_ngos, f, indent=4)

    # 3. Seed Donations if not exists
    if not os.path.exists(DONATIONS_FILE) or os.path.getsize(DONATIONS_FILE) == 0:
        base_time = datetime.now()
        sample_donations = [
            {
                "id": "D1",
                "restaurant_id": "R1",
                "restaurant_name": "Green Garden Bistro",
                "food_category": "Produce",
                "quantity_kg": 12.5,
                "prep_time": (base_time - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M"),
                "storage_condition": "Refrigerated",
                "detected_food": "Fresh Garden Salad",
                "confidence_score": 94.6,
                "freshness_score": 94.4,
                "safe_hours_remaining": 212.0,
                "priority": "LOW 🟢",
                "nearest_ngo_id": "N1",
                "nearest_ngo_name": "Robin Hood Army - Central",
                "nearest_ngo_distance": 0.72,
                "carbon_saved_kg": 31.25,
                "status": "Collected",
                "timestamp": (base_time - timedelta(days=2)).strftime("%Y-%m-%d %H:%M")
            },
            {
                "id": "D2",
                "restaurant_id": "R2",
                "restaurant_name": "The Pizza Haven",
                "food_category": "Cooked Meals",
                "quantity_kg": 25.0,
                "prep_time": (base_time - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M"),
                "storage_condition": "Ambient",
                "detected_food": "Cheese Pizza",
                "confidence_score": 91.2,
                "freshness_score": 87.5,
                "safe_hours_remaining": 21.0,
                "priority": "HIGH ⚠️",
                "nearest_ngo_id": "N1",
                "nearest_ngo_name": "Robin Hood Army - Central",
                "nearest_ngo_distance": 1.48,
                "carbon_saved_kg": 62.5,
                "status": "Accepted",
                "timestamp": (base_time - timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
            },
            {
                "id": "D3",
                "restaurant_id": "R3",
                "restaurant_name": "Spice Symphony Restaurant",
                "food_category": "Cooked Meals",
                "quantity_kg": 18.0,
                "prep_time": (base_time - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"),
                "storage_condition": "Refrigerated",
                "detected_food": "Biryani & Curry",
                "confidence_score": 88.5,
                "freshness_score": 97.2,
                "safe_hours_remaining": 70.0,
                "priority": "LOW 🟢",
                "nearest_ngo_id": "N2",
                "nearest_ngo_name": "No Food Waste - Indiranagar",
                "nearest_ngo_distance": 1.22,
                "carbon_saved_kg": 45.0,
                "status": "Pending",
                "timestamp": base_time.strftime("%Y-%m-%d %H:%M")
            },
            {
                "id": "D4",
                "restaurant_id": "R4",
                "restaurant_name": "Sweet Treats Bakery",
                "food_category": "Bakery",
                "quantity_kg": 10.0,
                "prep_time": (base_time - timedelta(hours=12)).strftime("%Y-%m-%d %H:%M"),
                "storage_condition": "Ambient",
                "detected_food": "Chocolate Cake & Croissants",
                "confidence_score": 95.8,
                "freshness_score": 75.0,
                "safe_hours_remaining": 36.0,
                "priority": "MEDIUM ⏰",
                "nearest_ngo_id": "N3",
                "nearest_ngo_name": "Feed The Needy - Jayanagar",
                "nearest_ngo_distance": 0.99,
                "carbon_saved_kg": 25.0,
                "status": "Collected",
                "timestamp": (base_time - timedelta(days=3)).strftime("%Y-%m-%d %H:%M")
            },
            {
                "id": "D5",
                "restaurant_id": "R2",
                "restaurant_name": "The Pizza Haven",
                "food_category": "Cooked Meals",
                "quantity_kg": 15.0,
                "prep_time": (base_time - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M"),
                "storage_condition": "Ambient",
                "detected_food": "Garlic Bread & Pasta",
                "confidence_score": 82.4,
                "freshness_score": 79.2,
                "safe_hours_remaining": 19.0,
                "priority": "HIGH ⚠️",
                "nearest_ngo_id": "N1",
                "nearest_ngo_name": "Robin Hood Army - Central",
                "nearest_ngo_distance": 1.48,
                "carbon_saved_kg": 37.5,
                "status": "Pending",
                "timestamp": base_time.strftime("%Y-%m-%d %H:%M")
            }
        ]
        with open(DONATIONS_FILE, 'w') as f:
            json.dump(sample_donations, f, indent=4)

def load_restaurants():
    init_db()
    with open(RESTAURANTS_FILE, 'r') as f:
        return json.load(f)

def save_restaurants(data):
    init_db()
    with open(RESTAURANTS_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def add_restaurant(restaurant):
    restaurants = load_restaurants()
    restaurants.append(restaurant)
    save_restaurants(restaurants)

def load_ngos():
    init_db()
    with open(NGOS_FILE, 'r') as f:
        return json.load(f)

def save_ngos(data):
    init_db()
    with open(NGOS_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def add_ngo(ngo):
    ngos = load_ngos()
    ngos.append(ngo)
    save_ngos(ngos)

def load_donations():
    init_db()
    with open(DONATIONS_FILE, 'r') as f:
        return json.load(f)

def save_donations(data):
    init_db()
    with open(DONATIONS_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def add_donation(donation):
    donations = load_donations()
    donations.append(donation)
    save_donations(donations)

# Always initialize on load
init_db()
