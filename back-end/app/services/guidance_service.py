SKIN_LABELS = {
    "normal": "normal",
    "dry": "kering",
    "oily": "berminyak",
    "combination": "kombinasi",
    "sensitive": "sensitif",
}

CONCERN_LABELS = {
    "acne": "jerawat",
    "dullness": "kulit kusam",
    "aging": "tanda penuaan",
    "dark spots": "bekas jerawat atau noda gelap",
    "dehydration": "dehidrasi kulit",
}

CATEGORY_LABELS = {
    "cleanser": "Cleanser",
    "moisturizer": "Moisturizer",
    "face mask": "Face mask",
    "eye cream": "Eye cream",
    "sunscreen": "Sunscreen",
}


def describe_weather_condition(weather_data: dict) -> str:
    uv_index = weather_data.get("uv_index") or 0
    humidity = weather_data.get("humidity") or 0
    pm25 = weather_data.get("pm25") or 0

    if uv_index >= 7:
        return "UV sedang tinggi"
    if humidity >= 70:
        return "kelembapan sedang tinggi"
    if humidity < 30:
        return "udara sedang kering"
    if pm25 >= 35:
        return "polusi PM2.5 sedang meningkat"
    return "cuaca sedang stabil"


def build_weather_insights(weather_data: dict, questionnaire: dict | None = None) -> list[dict]:
    uv_index = weather_data.get("uv_index") or 0
    humidity = weather_data.get("humidity") or 0
    pm25 = weather_data.get("pm25") or 0
    temperature = weather_data.get("temperature") or 0
    product_category = (questionnaire or {}).get("product_category")
    skin_type = (questionnaire or {}).get("skin_type")
    insights = []

    if uv_index >= 7:
        insights.append({
            "type": "uv",
            "level": "high",
            "message": f"UV index {uv_index:g} sedang tinggi. Prioritaskan sunscreen dan reapply saat banyak aktivitas luar ruangan.",
        })
    elif uv_index >= 3:
        insights.append({
            "type": "uv",
            "level": "moderate",
            "message": f"UV index {uv_index:g} tetap perlu perlindungan harian, terutama jika kamu keluar rumah.",
        })

    if humidity >= 70:
        insights.append({
            "type": "humidity",
            "level": "high",
            "message": f"Kelembapan {humidity}% cenderung membuat kulit terasa mudah gerah. Pilih tekstur ringan dan non-comedogenic.",
        })
    elif humidity < 30:
        insights.append({
            "type": "humidity",
            "level": "low",
            "message": f"Kelembapan {humidity}% cukup rendah. Tambahkan hidrasi dan dukungan skin barrier.",
        })
    else:
        insights.append({
            "type": "humidity",
            "level": "balanced",
            "message": f"Kelembapan {humidity}% relatif seimbang, jadi rutinitas dasar bisa tetap konsisten.",
        })

    if pm25 >= 35:
        insights.append({
            "type": "pollution",
            "level": "elevated",
            "message": f"PM2.5 berada di {pm25:g}. Bersihkan wajah dengan teliti pada malam hari untuk mengangkat buildup harian.",
        })
    else:
        insights.append({
            "type": "pollution",
            "level": "normal",
            "message": f"PM2.5 berada di {pm25:g}. Tetap jaga cleansing rutin tanpa perlu over-cleansing.",
        })

    if temperature >= 32:
        insights.append({
            "type": "temperature",
            "level": "hot",
            "message": f"Suhu {temperature:g}C cukup panas. Layer skincare sebaiknya tipis agar nyaman dipakai.",
        })
    elif temperature <= 24:
        insights.append({
            "type": "temperature",
            "level": "cool",
            "message": f"Suhu {temperature:g}C lebih sejuk. Fokus pada hidrasi agar kulit tidak mudah terasa kering.",
        })

    if skin_type == "oily" and humidity >= 70:
        insights.append({
            "type": "skin-weather",
            "level": "oily-humid",
            "message": "Kulit berminyak saat kelembapan tinggi biasanya lebih nyaman dengan gel, lotion ringan, atau formula oil-free.",
        })

    if product_category == "sunscreen":
        insights.append({
            "type": "category",
            "level": "sunscreen",
            "message": "Karena kategori yang dipilih sunscreen, perhatikan kenyamanan tekstur dan perlindungan UV.",
        })

    return insights


def build_explanation_factors(product: dict, questionnaire: dict, weather_data: dict) -> dict:
    skin_type = questionnaire.get("skin_type")
    concerns = questionnaire.get("skin_concerns") or []
    avoided = [item.lower() for item in questionnaire.get("avoided_ingredients") or []]
    ingredients = product.get("active_ingredients") or []
    ingredient_text = " ".join(ingredients).lower()
    avoided_hits = [item for item in avoided if item and item in ingredient_text]
    skin_label = SKIN_LABELS.get(skin_type, skin_type or "profil kulitmu")
    concern_labels = [CONCERN_LABELS.get(concern, concern) for concern in concerns]
    ingredient_highlights = ingredients[:3]
    weather_reason = describe_weather_condition(weather_data)

    summary_points = []
    if skin_type in (product.get("skin_types") or []):
        summary_points.append(f"Cocok untuk kulit {skin_label}")
    if concern_labels:
        summary_points.append(f"Relevan untuk {', '.join(concern_labels[:2])}")
    if ingredient_highlights:
        summary_points.append(f"Ingredient utama: {', '.join(ingredient_highlights[:2])}")
    summary_points.append(f"Disesuaikan dengan {weather_reason}")

    return {
        "skin_type_match": skin_type in (product.get("skin_types") or []),
        "matched_concerns": concern_labels,
        "weather_reason": weather_reason,
        "ingredient_highlights": ingredient_highlights,
        "summary_points": summary_points[:4],
        "avoidance_note": (
            f"Perlu dicek karena mengandung kandungan yang kamu hindari: {', '.join(avoided_hits)}"
            if avoided_hits
            else "Tidak terdeteksi kandungan yang kamu pilih untuk dihindari"
        ),
    }


def build_dynamic_why_recommended(product: dict, questionnaire: dict, weather_data: dict) -> str:
    factors = build_explanation_factors(product, questionnaire, weather_data)
    brand = product.get("brand") or "Produk ini"
    name = product.get("product_name") or "produk ini"
    score = round((product.get("score") or 0) * 100)
    category = product.get("category") or questionnaire.get("product_category") or "produk"
    category_label = CATEGORY_LABELS.get(category, category)
    ingredients = factors["ingredient_highlights"]
    concerns = factors["matched_concerns"]

    sentences = [
        f"{brand} {name} menjadi kandidat {category_label} dengan match score {score}%.",
    ]

    if factors["skin_type_match"]:
        skin_label = SKIN_LABELS.get(questionnaire.get("skin_type"), questionnaire.get("skin_type"))
        sentences.append(f"Formula ini terdata cocok untuk kulit {skin_label}, sesuai profil yang kamu pilih.")

    if concerns:
        sentences.append(f"Rekomendasi ini juga relevan dengan fokus {', '.join(concerns[:2])}.")

    if ingredients:
        sentences.append(f"Ingredient utama yang menonjol: {', '.join(ingredients[:3])}.")

    sentences.append(f"Pemilihannya ikut mempertimbangkan kondisi cuaca saat ini: {factors['weather_reason']}.")
    sentences.append(factors["avoidance_note"] + ".")

    return " ".join(sentences)


def build_routine_summary(questionnaire: dict, weather_data: dict, recommendations: list[dict]) -> dict:
    avoided = questionnaire.get("avoided_ingredients") or []
    top_ingredients = []
    for product in recommendations[:3]:
        for ingredient in product.get("active_ingredients") or []:
            if ingredient not in top_ingredients:
                top_ingredients.append(ingredient)
            if len(top_ingredients) >= 4:
                break
        if len(top_ingredients) >= 4:
            break

    uv_index = weather_data.get("uv_index") or 0
    humidity = weather_data.get("humidity") or 0
    pm25 = weather_data.get("pm25") or 0

    product_category = questionnaire.get("product_category")
    skin_type = questionnaire.get("skin_type")

    morning_focus = "Hidrasi ringan dan proteksi harian"
    midday_focus = "Jaga kenyamanan kulit dan hindari layer berlebihan"
    evening_focus = "Cleansing lembut dan dukungan skin barrier"
    weekly_focus = "Evaluasi reaksi kulit sebelum menambah produk baru"

    if uv_index >= 7:
        morning_focus = "Proteksi sunscreen dan reapply saat banyak di luar ruangan"
        midday_focus = "Reapply sunscreen dan cari shade ketika UV terasa tinggi"
    elif humidity >= 70:
        morning_focus = "Hidrasi ringan dengan tekstur non-comedogenic"
    elif humidity < 30:
        morning_focus = "Layer hidrasi dan dukungan barrier"

    if pm25 >= 35:
        evening_focus = "Cleansing lebih teliti lalu hidrasi yang menenangkan"

    if skin_type == "oily":
        weekly_focus = "Pantau area T-zone dan pilih tekstur yang tidak terasa berat"
    elif skin_type == "dry":
        weekly_focus = "Perhatikan tanda ketarik dan tambahkan hidrasi bila perlu"
    elif skin_type == "sensitive":
        weekly_focus = "Patch test produk baru dan jaga routine tetap sederhana"

    if product_category == "face mask":
        weekly_focus = "Gunakan masker secukupnya dan perhatikan respon kulit setelah pemakaian"

    return {
        "morning_focus": morning_focus,
        "midday_focus": midday_focus,
        "evening_focus": evening_focus,
        "weekly_focus": weekly_focus,
        "ingredient_focus": top_ingredients,
        "avoid_reminder": avoided,
        "steps": [
            {"time": "Morning", "message": morning_focus},
            {"time": "Midday", "message": midday_focus},
            {"time": "Evening", "message": evening_focus},
            {"time": "Weekly", "message": weekly_focus},
        ],
    }
