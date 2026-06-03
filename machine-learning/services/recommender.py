import os
import json
import logging
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

PRODUCTS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "products.json")

CONCERN_INGREDIENTS = {
    "acne": ["salicylic acid", "benzoyl peroxide", "tea tree", "centella", "niacinamide", "bha", "sulfur", "zinc"],
    "dullness": ["vitamin c", "niacinamide", "glycolic acid", "aha", "licorice", "alpha arbutin", "lactic acid", "brightening"],
    "aging": ["retinol", "peptide", "adenosine", "collagen", "coenzyme q10", "ginseng", "bakuchiol", "hyaluronic acid"],
    "dark spots": ["vitamin c", "niacinamide", "alpha arbutin", "kojic acid", "tranexamic acid", "licorice", "glycolic acid"],
    "dehydration": ["hyaluronic acid", "glycerin", "ceramide", "squalane", "panthenol", "aloe vera", "sodium hyaluronate"]
}

class SkincareRecommender:
    def __init__(self):
        self.products = []
        self.load_products()
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.product_vectors = None
        self.initialize_ml_model()

    def load_products(self):
        """Loads product dataset from products.json file."""
        try:
            with open(PRODUCTS_PATH, 'r', encoding='utf-8') as f:
                self.products = json.load(f)
            logger.info(f"Successfully loaded {len(self.products)} products.")
        except Exception as e:
            logger.error(f"Error loading products.json: {str(e)}")
            self.products = []

    def initialize_ml_model(self):
        """Initializes TF-IDF representations of the skincare products."""
        if not self.products:
            return

        product_docs = []
        for p in self.products:
            skin_types_str = " ".join(p.get("skin_types", []))
            ingredients_str = " ".join([i.lower().replace(" ", "_") for i in p.get("active_ingredients", [])])
            non_comedogenic_str = "non_comedogenic" if p.get("is_non_comedogenic") else ""
            spf_str = f"spf{p.get('spf')}" if p.get("spf") else ""
            
            doc = f"{p.get('brand').lower()} {p.get('category')} {skin_types_str} {ingredients_str} {non_comedogenic_str} {spf_str}"
            product_docs.append(doc)

        try:
            self.product_vectors = self.vectorizer.fit_transform(product_docs)
            logger.info("Successfully trained scikit-learn Content-Based Recommendation model.")
        except Exception as e:
            logger.error(f"Error initializing scikit-learn model: {str(e)}")

    def get_product_type(self, product):
        """Classify a product into moisturizer, cleanser, face mask, eye cream, or sunscreen."""
        name = product.get("product_name", "").lower()
        cat = product.get("category", "").lower()
        
        if "mask" in name or "masque" in name:
            return "face mask"
        
        if "eye" in name or "undereye" in name:
            if "remover" not in name and "solvent" not in name and "wipe" not in name and "towelette" not in name:
                return "eye cream"
                
        if cat == "sunscreen":
            return "sunscreen"
            
        if cat in ("cleanser", "face_wash"):
            return "cleanser"
            
        if cat == "moisturizer":
            return "moisturizer"
            
        return None

    def get_recommendations(self, weather_data, skin_type, selected_products=None, concerns=None, activity="indoor", avoid_ingredients=None):
        """
        Recommends top 5-8 skincare products using a weighted scikit-learn content-based
        similarity score and heuristic weather, skin type, concerns, and allergy rules.
        """
        if not self.products:
            return []

        if selected_products is None:
            selected_products = []
        if concerns is None:
            concerns = []
        if avoid_ingredients is None:
            avoid_ingredients = []

        temp = weather_data.get("temperature", 28.0)
        humidity = weather_data.get("humidity", 70)
        uv = weather_data.get("uv_index", 4.0)
        pm25 = weather_data.get("pm25", 25.0)

        target_types = {p.lower() for p in selected_products}
        if not target_types:

            target_types = {"moisturizer", "cleanser", "face mask", "eye cream", "sunscreen"}

        query_terms = [skin_type]
        for category in target_types:
            query_terms.append(category)
        for concern in concerns:
            query_terms.append(concern)

        if uv > 6:
            query_terms.extend(["sunscreen", "spf50", "antioxidant", "high_uv"])
        if humidity > 80:
            query_terms.extend(["lightweight", "non_comedogenic", "gel", "gel_based"])
        if temp > 33:
            query_terms.extend(["water_based", "gel", "lightweight"])
        if pm25 > 55:
            query_terms.extend(["niacinamide", "vitamin_c", "antioxidant", "pollution_protection"])
        if temp < 25:
            query_terms.extend(["rich", "cream", "deep_moisture"])

        query_str = " ".join(query_terms)
        
        ml_scores = np.zeros(len(self.products))
        if self.product_vectors is not None:
            try:
                query_vector = self.vectorizer.transform([query_str])
                ml_scores = cosine_similarity(query_vector, self.product_vectors).flatten()
            except Exception as e:
                logger.error(f"Error calculating ML similarity: {str(e)}")

        scored_products = []
        for idx, product in enumerate(self.products):
      
            prod_type = self.get_product_type(product)
            if not prod_type or prod_type not in target_types:
                continue

           
            if avoid_ingredients:
                active_ings = [i.lower() for i in product.get("active_ingredients", [])]
                prod_name_lower = product.get("product_name", "").lower()
                
                is_allergic = False
                for avoid_ing in avoid_ingredients:
                    avoid_ing_clean = avoid_ing.strip().lower()
                    if not avoid_ing_clean:
                        continue
                    if any(avoid_ing_clean in ing for ing in active_ings) or avoid_ing_clean in prod_name_lower:
                        is_allergic = True
                        break
                if is_allergic:
                    continue

           
            skin_match = 1.0 if skin_type.lower() in [s.lower() for s in product.get("skin_types", [])] else 0.0
            
            weather_suitability = 1.0
            ideal = product.get("ideal_weather", {})

            temp_match = 1.0
            if "temp_min" in ideal and "temp_max" in ideal:
                if not (ideal["temp_min"] <= temp <= ideal["temp_max"]):
                    temp_match = 0.5

            humidity_match = 1.0
            if "humidity_min" in ideal and "humidity_max" in ideal:
                if not (ideal["humidity_min"] <= humidity <= ideal["humidity_max"]):
                    humidity_match = 0.5

            uv_match = 1.0
            if "uv_max" in ideal:
                if uv > ideal["uv_max"]:
                    uv_match = 0.5

            weather_suitability = (temp_match * 0.33) + (humidity_match * 0.33) + (uv_match * 0.34)

            if temp > 33 and product.get("category") == "moisturizer":
                if "gel" not in product.get("product_name", "").lower():
                    weather_suitability -= 0.3

            if humidity > 80:
                if "gel" in product.get("product_name", "").lower() or product.get("category") == "cleanser":
                    weather_suitability += 0.1
                elif "cream" in product.get("product_name", "").lower():
                    weather_suitability -= 0.3

            if prod_type == "sunscreen":
                spf = product.get("spf", 0) or 0
                if activity == "outdoor":
                    if spf >= 50:
                        weather_suitability += 0.25
                    elif spf < 30:
                        weather_suitability -= 0.4
                elif activity == "indoor":
                    if spf == 30:
                        weather_suitability += 0.15

            weather_suitability = max(0.0, min(1.0, weather_suitability))

            concern_match = 0.0
            matched_concerns = []
            if concerns:
                active_ings = [i.lower() for i in product.get("active_ingredients", [])]
                prod_name_lower = product.get("product_name", "").lower()
                
                matched_count = 0
                for concern in concerns:
                    concern_clean = concern.strip().lower()
                    if concern_clean in CONCERN_INGREDIENTS:
                        keywords = CONCERN_INGREDIENTS[concern_clean]
                        if any(any(kw in ing for kw in keywords) for ing in active_ings) or any(kw in prod_name_lower for kw in keywords):
                            matched_count += 1
                            matched_concerns.append(concern)
                
                if len(concerns) > 0:
                    concern_match = matched_count / len(concerns)
            else:
                concern_match = 1.0 # If no concerns specified, neutral match

            pm_protection = 1.0
            if pm25 > 55:
                antioxidant_keywords = ["niacinamide", "vitamin c", "vitamin e", "green tea", "centella asiatica", "sabiwhite", "pomegranate"]
                has_antioxidants = any(any(kw in ing.lower() for kw in antioxidant_keywords) for ing in product.get("active_ingredients", []))
                pm_protection = 1.0 if has_antioxidants else 0.3
            else:
                pm_protection = 1.0

            heuristic_score = (
                (skin_match * 0.30) +
                (weather_suitability * 0.30) +
                (concern_match * 0.30) +
                (pm_protection * 0.10)
            )

            ml_score = ml_scores[idx] if len(ml_scores) > idx else 0.0
            final_score = (heuristic_score * 0.8) + (ml_score * 0.2)
            final_score = round(max(0.0, min(1.0, final_score)), 2)

            why_reasons = []
            if skin_match > 0:
                why_reasons.append(f"sangat cocok untuk tipe kulit {skin_type.lower()}")
            
            if matched_concerns:
                why_reasons.append(f"membantu mengatasi masalah {', '.join(matched_concerns)}")

            if prod_type == "sunscreen":
                spf = product.get("spf", 30) or 30
                if activity == "outdoor":
                    why_reasons.append(f"melindungi dengan SPF {spf} tinggi yang ideal untuk aktivitas luar ruangan (outdoor)")
                else:
                    why_reasons.append(f"dilengkapi SPF {spf} yang nyaman untuk aktivitas dalam ruangan (indoor)")
            elif humidity > 80 and "gel" in product.get("product_name", "").lower():
                why_reasons.append("memiliki formula gel ringan yang nyaman di cuaca lembap")
            elif temp > 33 and "water" in product.get("product_name", "").lower():
                why_reasons.append("menghidrasi secara water-based tanpa membuat kulit gerah di cuaca panas")
            elif temp < 25 and prod_type == "moisturizer" and "ceramide" in [i.lower() for i in product.get("active_ingredients", [])]:
                why_reasons.append("menjaga kelembapan kulit secara optimal di udara dingin dengan kandungan Ceramide")
            elif weather_suitability > 0.8:
                why_reasons.append("sangat ideal untuk kondisi cuaca saat ini")

            if pm25 > 55 and pm_protection == 1.0:
                active_match = [i for i in product.get("active_ingredients", []) if any(kw in i.lower() for kw in ["niacinamide", "vitamin c", "vitamin e", "green tea", "centella"])]
                if active_match:
                    why_reasons.append(f"mengandung {active_match[0]} untuk memproteksi barrier kulit dari polusi PM2.5 ({pm25:.1f})")
            
            if len(why_reasons) < 2 and product.get("active_ingredients"):
                ingredients_list = ", ".join(product.get("active_ingredients")[:2])
                why_reasons.append(f"kaya akan {ingredients_list} yang menutrisi kulit secara mendalam")

            why_recommended = "Cocok karena " + ", serta ".join(why_reasons) + "."
            
            scored_products.append({
                "product_name": product["product_name"],
                "brand": product["brand"],
                "category": prod_type, # Use classified type for frontend consistency
                "skin_types": product["skin_types"],
                "active_ingredients": product["active_ingredients"],
                "why_recommended": why_recommended,
                "score": float(final_score)
            })

        scored_products.sort(key=lambda x: x["score"], reverse=True)
        limit = max(5, min(8, len(scored_products)))
        return scored_products[:limit]

