import random
import math

# Baseline shelf life in hours for various food categories under Ambient storage
BASELINE_SHELF_LIFE = {
    "Produce": 72.0,       # Fruits and vegetables can last ~3 days at room temp
    "Bakery": 48.0,        # Bread and pastries last ~2 days
    "Cooked Meals": 24.0,   # Cooked rice, curries, pizzas last ~24 hours
    "Dairy": 12.0,         # Milk, cottage cheese, yogurt goes bad quickly
    "Meat/Seafood": 6.0    # Extremely perishable
}

# Storage condition multipliers
STORAGE_MULTIPLIERS = {
    "Ambient": 1.0,
    "Refrigerated": 3.0,
    "Frozen": 10.0
}

# Carbon emissions saved factor (approx 2.5 kg CO2 saved per kg of food rescued)
CARBON_FACTOR_PER_KG = 2.5

def detect_food(filename="", category_hint=None):
    """
    Simulates rule-based AI food detection based on filename keywords or manual hints.
    """
    filename_lower = filename.lower() if filename else ""
    hint_lower = category_hint.lower() if category_hint else ""
    
    # Check for Pizza
    if "pizza" in filename_lower or "pizza" in hint_lower:
        name = "Classic Cheese & Veggie Pizza"
        category = "Cooked Meals"
    # Check for Salad
    elif "salad" in filename_lower or "salad" in hint_lower:
        name = "Garden Fresh Greens Salad"
        category = "Produce"
    # Check for Biryani / Rice
    elif "biryani" in filename_lower or "biryani" in hint_lower:
        name = "Vegetable Dum Biryani"
        category = "Cooked Meals"
    elif "rice" in filename_lower or "rice" in hint_lower:
        name = "Steamed Basmati Rice"
        category = "Cooked Meals"
    # Check for Bread/Bakery
    elif "bread" in filename_lower or "bread" in hint_lower or "croissant" in filename_lower:
        name = "Artisanal Wheat Bread & Croissants"
        category = "Bakery"
    elif "cake" in filename_lower or "cake" in hint_lower or "pastries" in filename_lower:
        name = "Assorted Cakes & Pastries"
        category = "Bakery"
    # Check for Fruits/Produce
    elif any(k in filename_lower or k in hint_lower for k in ["fruit", "apple", "banana", "orange", "mango"]):
        name = "Seasonal Fresh Fruit Basket"
        category = "Produce"
    # Check for Curries
    elif "curry" in filename_lower or "curry" in hint_lower or "gravy" in filename_lower:
        name = "Paneer Butter Masala & Gravy"
        category = "Cooked Meals"
    # Check for Dairy
    elif any(k in filename_lower or k in hint_lower for k in ["dairy", "milk", "cheese", "paneer"]):
        name = "Fresh Paneer (Cottage Cheese)"
        category = "Dairy"
    # Check for Meat
    elif any(k in filename_lower or k in hint_lower for k in ["meat", "chicken", "fish", "egg"]):
        name = "Roasted Garlic Chicken"
        category = "Meat/Seafood"
    # Defaults
    else:
        candidates = [
            ("Assorted Vegetable Stir-Fry", "Cooked Meals"),
            ("Lentil Soup (Yellow Dal)", "Cooked Meals"),
            ("Whole Wheat Roti & Naan", "Bakery"),
            ("Mixed Berry Bowl", "Produce"),
            ("Veg Hakka Noodles", "Cooked Meals"),
            ("Fresh Yogurt Cups", "Dairy")
        ]
        name, category = random.choice(candidates)

    confidence = round(random.uniform(85.0, 98.8), 1)
    return {
        "detected_food": name,
        "food_category": category,
        "confidence_score": confidence
    }

def predict_freshness(food_category, prep_time_hours, storage_condition):
    """
    Computes freshness stats using baseline shelf life and storage conditions.
    """
    baseline = BASELINE_SHELF_LIFE.get(food_category, 24.0)
    multiplier = STORAGE_MULTIPLIERS.get(storage_condition, 1.0)
    
    total_shelf_life = baseline * multiplier
    safe_hours_remaining = total_shelf_life - prep_time_hours
    
    # Calculate freshness score percentage
    if safe_hours_remaining <= 0:
        freshness_score = 0.0
        safe_hours_remaining = 0.0
        priority = "UNSAFE 🛑"
    else:
        freshness_score = round((safe_hours_remaining / total_shelf_life) * 100.0, 1)
        
        # Priority mapping based on remaining safe hours
        if safe_hours_remaining <= 4.0:
            priority = "CRITICAL 🚨"
        elif safe_hours_remaining <= 12.0:
            priority = "HIGH ⚠️"
        elif safe_hours_remaining <= 24.0:
            priority = "MEDIUM ⏰"
        else:
            priority = "LOW 🟢"
            
    return {
        "freshness_score": freshness_score,
        "safe_hours_remaining": round(safe_hours_remaining, 1),
        "priority": priority
    }

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculates Euclidean distance between two coordinate points, 
    scaled to approximate kilometers (~111km per degree).
    """
    try:
        lat1, lon1, lat2, lon2 = float(lat1), float(lon1), float(lat2), float(lon2)
        deg_dist = math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)
        return round(deg_dist * 111.0, 2)
    except (ValueError, TypeError):
        return 999.9

def match_nearest_ngo(restaurant_lat, restaurant_lon, ngos):
    """
    Matches a donating restaurant to the nearest NGO based on location.
    Returns the nearest NGO details and the list of NGOs sorted by proximity.
    """
    if not ngos:
        return None, []
        
    ngo_distances = []
    for ngo in ngos:
        dist = calculate_distance(restaurant_lat, restaurant_lon, ngo["latitude"], ngo["longitude"])
        ngo_distances.append({
            **ngo,
            "distance_km": dist
        })
        
    # Sort by distance ascending
    sorted_ngos = sorted(ngo_distances, key=lambda x: x["distance_km"])
    
    nearest_ngo = sorted_ngos[0] if sorted_ngos else None
    return nearest_ngo, sorted_ngos

def calculate_carbon_saved(quantity_kg):
    """
    Calculates carbon offset in kg CO2 equivalence.
    """
    return round(float(quantity_kg) * CARBON_FACTOR_PER_KG, 2)
