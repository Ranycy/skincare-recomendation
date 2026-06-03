import os
import re
import csv
import json

CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dataset", "cosmetics.csv")
JSON_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "products.json")

KEY_ACTIVES = [
    "niacinamide", "vitamin c", "vitamin e", "green tea", "centella asiatica", 
    "ceramide", "salicylic acid", "hyaluronic acid", "glycolic acid", "lactic acid", 
    "retinol", "tea tree", "aloe vera", "collagen", "squalane", "panthenol"
]

def clean_name(name):
    """Cleans product names by resolving typical encoding errors."""
    name = name.replace("\u00e9", "e").replace("\u00e8", "e")
    name = name.replace("dcollet", "decollete")
    return name.strip()

def parse_ingredients(ingredients_text):
    """Parses ingredients to identify first 4 and any extra known active ingredients."""
    if not isinstance(ingredients_text, str) or not ingredients_text.strip():
        return ["Water", "Glycerin"]
    
    parts = [p.strip() for p in ingredients_text.split(",") if p.strip()]
    
    base_actives = [p.lower() for p in parts[:4]]
    
    found_actives = []
    text_lower = ingredients_text.lower()
    for active in KEY_ACTIVES:
        if active in text_lower:
            found_actives.append(active)
            
    combined = []
    for item in base_actives + found_actives:
        item_lower = item.lower()
        if item_lower == "vitamin c":
            item_cleaned = "Vitamin C"
        elif item_lower == "vitamin e":
            item_cleaned = "Vitamin E"
        elif item_lower == "green tea":
            item_cleaned = "Green Tea"
        elif item_lower == "centella asiatica":
            item_cleaned = "Centella Asiatica"
        elif item_lower == "salicylic acid":
            item_cleaned = "Salicylic Acid"
        elif item_lower == "hyaluronic acid":
            item_cleaned = "Hyaluronic Acid"
        elif item_lower == "glycolic acid":
            item_cleaned = "Glycolic Acid"
        elif item_lower == "lactic acid":
            item_cleaned = "Lactic Acid"
        elif item_lower == "tea tree":
            item_cleaned = "Tea Tree"
        elif item_lower == "aloe vera":
            item_cleaned = "Aloe Vera"
        else:
            item_cleaned = item.title() if len(item) > 3 else item.upper()
            
        if item_cleaned not in combined:
            combined.append(item_cleaned)
            
    return combined[:6]

def parse_spf(name):
    """Attempts to find SPF value in the product name."""
    spf_match = re.search(r"spf\s*(\d+)", name.lower())
    if spf_match:
        return int(spf_match.group(1))
    return None

def convert_csv_to_json():
    print(f"Reading dataset from {CSV_PATH}...")
    if not os.path.exists(CSV_PATH):
        print(f"Error: {CSV_PATH} does not exist!")
        return
        
    products = []
    
    with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            label = row.get("Label", "").strip()
            brand = row.get("Brand", "").strip()
            name = clean_name(row.get("Name", "").strip())
            ingredients = row.get("Ingredients", "").strip()
            
            name_lower = name.lower()
            label_lower = label.lower()
            
            
            
            
            category = "moisturizer"
            if label_lower == "cleanser":
                if "wash" in name_lower or "foam" in name_lower:
                    category = "face_wash"
                else:
                    category = "cleanser"
            elif label_lower == "treatment":
                if "essence" in name_lower:
                    category = "essence"
                elif "toner" in name_lower or "lotion" in name_lower:
                    category = "toner"
                else:
                    category = "serum"
            elif label_lower == "moisturizer":
                if "toner" in name_lower or "lotion" in name_lower:
                    category = "toner"
                else:
                    category = "moisturizer"
            elif label_lower == "sun protect":
                category = "sunscreen"
            elif label_lower == "eye cream":
                category = "moisturizer"
            elif label_lower == "face mask":
                category = "moisturizer"
            
            
            
            skin_types = []
            if row.get("Normal") == "1": skin_types.append("normal")
            if row.get("Dry") == "1": skin_types.append("dry")
            if row.get("Oily") == "1": skin_types.append("oily")
            if row.get("Combination") == "1": skin_types.append("combination")
            if row.get("Sensitive") == "1": skin_types.append("sensitive")
            
            if not skin_types:
                skin_types = ["normal", "dry", "oily", "combination"]
                

            active_ingredients = parse_ingredients(ingredients)
            
            spf = parse_spf(name)
            if spf is None and category == "sunscreen":
                spf = 50  # Fallback for generic sun protect products
                
            is_non_comedogenic = True
            if "cream" in name_lower or "oil" in name_lower or "butter" in name_lower:
                is_non_comedogenic = False
                
            ideal_weather = {
                "temp_min": 15.0,
                "temp_max": 38.0,
                "humidity_min": 40.0,
                "humidity_max": 95.0,
                "uv_max": 10.0
            }
            avoid_weather = []
            
            if category == "sunscreen":
                ideal_weather = {
                    "temp_min": 18.0,
                    "temp_max": 45.0,
                    "humidity_min": 30.0,
                    "humidity_max": 100.0,
                    "uv_max": 15.0
                }
            elif category == "moisturizer":
                if "gel" in name_lower or "water" in name_lower or "light" in name_lower:
                    ideal_weather["temp_min"] = 20.0
                    ideal_weather["temp_max"] = 40.0
                    ideal_weather["humidity_max"] = 100.0
                elif "cream" in name_lower or "rich" in name_lower or "heavy" in name_lower:
                    ideal_weather["temp_max"] = 26.0
                    ideal_weather["humidity_max"] = 75.0
                    avoid_weather = ["high humidity", "extremely hot temperature"]
                    is_non_comedogenic = False
                    
            products.append({
                "product_name": name,
                "brand": brand,
                "category": category,
                "skin_types": skin_types,
                "ideal_weather": ideal_weather,
                "avoid_weather": avoid_weather,
                "active_ingredients": active_ingredients,
                "is_non_comedogenic": is_non_comedogenic,
                "spf": spf
            })
            
    print(f"Loaded {len(products)} products from CSV.")
    
    os.makedirs(os.path.dirname(JSON_PATH), exist_ok=True)
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    print(f"Successfully saved products to {JSON_PATH}!")

if __name__ == "__main__":
    convert_csv_to_json()
