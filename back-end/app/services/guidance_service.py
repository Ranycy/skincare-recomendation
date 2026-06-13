SUPPORTED_LOCALES = {"id", "en"}
DEFAULT_LOCALE = "en"


LABELS = {
    "id": {
        "skin": {
            "normal": "normal",
            "dry": "kering",
            "oily": "berminyak",
            "combination": "kombinasi",
            "sensitive": "sensitif",
        },
        "concern": {
            "acne": "jerawat",
            "dullness": "kulit kusam",
            "aging": "tanda penuaan",
            "dark spots": "bekas jerawat atau noda gelap",
            "dehydration": "dehidrasi kulit",
        },
        "category": {
            "cleanser": "pembersih wajah",
            "moisturizer": "pelembap",
            "face mask": "masker wajah",
            "eye cream": "krim mata",
            "sunscreen": "tabir surya",
        },
    },
    "en": {
        "skin": {
            "normal": "normal",
            "dry": "dry",
            "oily": "oily",
            "combination": "combination",
            "sensitive": "sensitive",
        },
        "concern": {
            "acne": "acne",
            "dullness": "dullness",
            "aging": "aging signs",
            "dark spots": "dark spots",
            "dehydration": "dehydration",
        },
        "category": {
            "cleanser": "Cleanser",
            "moisturizer": "Moisturizer",
            "face mask": "Face mask",
            "eye cream": "Eye cream",
            "sunscreen": "Sunscreen",
        },
    },
}


def normalize_locale(locale: str | None, fallback: str | None = None) -> str:
    selected = (locale or "").strip().lower()
    if selected in SUPPORTED_LOCALES:
        return selected

    fallback_locale = (fallback or "").strip().lower()
    if fallback_locale in SUPPORTED_LOCALES:
        return fallback_locale

    return DEFAULT_LOCALE


def get_label(group: str, value: str | None, locale: str) -> str:
    current_locale = normalize_locale(locale)
    return LABELS[current_locale].get(group, {}).get(value or "", value or "")


def describe_weather_condition(weather_data: dict, locale: str = DEFAULT_LOCALE) -> str:
    locale = normalize_locale(locale)
    uv_index = weather_data.get("uv_index") or 0
    humidity = weather_data.get("humidity") or 0
    pm25 = weather_data.get("pm25") or 0

    if locale == "id":
        if uv_index >= 7:
            return "UV sedang tinggi"
        if humidity >= 70:
            return "kelembapan sedang tinggi"
        if humidity < 30:
            return "udara sedang kering"
        if pm25 >= 35:
            return "PM2.5 sedang meningkat"
        return "cuaca stabil"

    if uv_index >= 7:
        return "UV is high"
    if humidity >= 70:
        return "humidity is high"
    if humidity < 30:
        return "the air is dry"
    if pm25 >= 35:
        return "PM2.5 is elevated"
    return "the weather is stable"


def build_weather_insights(
    weather_data: dict,
    questionnaire: dict | None = None,
    locale: str = DEFAULT_LOCALE,
) -> list[dict]:
    locale = normalize_locale(locale)
    uv_index = weather_data.get("uv_index") or 0
    humidity = weather_data.get("humidity") or 0
    pm25 = weather_data.get("pm25") or 0
    temperature = weather_data.get("temperature") or 0
    product_category = (questionnaire or {}).get("product_category")
    skin_type = (questionnaire or {}).get("skin_type")
    insights = []

    if locale == "id":
        if uv_index >= 7:
            insights.append({
                "type": "uv",
                "level": "high",
                "message": f"Indeks UV {uv_index:g} sedang tinggi. Prioritaskan tabir surya dan gunakan ulang saat banyak aktivitas luar ruangan.",
            })
        elif uv_index >= 3:
            insights.append({
                "type": "uv",
                "level": "moderate",
                "message": f"Indeks UV {uv_index:g} tetap perlu perlindungan harian, terutama jika kamu keluar rumah.",
            })

        if humidity >= 70:
            insights.append({
                "type": "humidity",
                "level": "high",
                "message": f"Kelembapan {humidity}% dapat membuat kulit terasa mudah gerah. Pilih tekstur ringan dan non-komedogenik.",
            })
        elif humidity < 30:
            insights.append({
                "type": "humidity",
                "level": "low",
                "message": f"Kelembapan {humidity}% cukup rendah. Tambahkan hidrasi dan dukungan lapisan pelindung kulit.",
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
                "message": f"PM2.5 berada di {pm25:g}. Bersihkan wajah dengan teliti pada malam hari untuk mengangkat penumpukan kotoran harian.",
            })
        else:
            insights.append({
                "type": "pollution",
                "level": "normal",
                "message": f"PM2.5 berada di {pm25:g}. Pertahankan pembersihan rutin tanpa membersihkan wajah secara berlebihan.",
            })

        if temperature >= 32:
            insights.append({
                "type": "temperature",
                "level": "hot",
                "message": f"Suhu {temperature:g}C cukup panas. Lapisan perawatan kulit sebaiknya tipis agar tetap nyaman.",
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
                "message": "Kulit berminyak saat kelembapan tinggi biasanya lebih nyaman dengan gel, losion ringan, atau formula bebas minyak.",
            })

        if product_category == "sunscreen":
            insights.append({
                "type": "category",
                "level": "sunscreen",
                "message": "Karena kategori yang dipilih adalah tabir surya, perhatikan kenyamanan tekstur dan perlindungan UV.",
            })

        return insights

    if uv_index >= 7:
        insights.append({
            "type": "uv",
            "level": "high",
            "message": f"UV index {uv_index:g} is high. Prioritize sunscreen and reapply during outdoor activity.",
        })
    elif uv_index >= 3:
        insights.append({
            "type": "uv",
            "level": "moderate",
            "message": f"UV index {uv_index:g} still needs daily protection, especially when you go outside.",
        })

    if humidity >= 70:
        insights.append({
            "type": "humidity",
            "level": "high",
            "message": f"Humidity is {humidity}%. Choose lightweight, non-comedogenic textures to stay comfortable.",
        })
    elif humidity < 30:
        insights.append({
            "type": "humidity",
            "level": "low",
            "message": f"Humidity is {humidity}%. Add hydration and support your skin barrier.",
        })
    else:
        insights.append({
            "type": "humidity",
            "level": "balanced",
            "message": f"Humidity is {humidity}%, so your basic routine can stay consistent.",
        })

    if pm25 >= 35:
        insights.append({
            "type": "pollution",
            "level": "elevated",
            "message": f"PM2.5 is {pm25:g}. Cleanse thoroughly at night to remove daily buildup.",
        })
    else:
        insights.append({
            "type": "pollution",
            "level": "normal",
            "message": f"PM2.5 is {pm25:g}. Keep cleansing consistent without over-cleansing.",
        })

    if temperature >= 32:
        insights.append({
            "type": "temperature",
            "level": "hot",
            "message": f"Temperature is {temperature:g}C. Keep skincare layers light for comfort.",
        })
    elif temperature <= 24:
        insights.append({
            "type": "temperature",
            "level": "cool",
            "message": f"Temperature is {temperature:g}C. Focus on hydration so skin does not feel dry.",
        })

    if skin_type == "oily" and humidity >= 70:
        insights.append({
            "type": "skin-weather",
            "level": "oily-humid",
            "message": "Oily skin in high humidity usually feels better with gel, light lotion, or oil-free formulas.",
        })

    if product_category == "sunscreen":
        insights.append({
            "type": "category",
            "level": "sunscreen",
            "message": "Since you selected sunscreen, prioritize texture comfort and UV protection.",
        })

    return insights


def build_explanation_factors(
    product: dict,
    questionnaire: dict,
    weather_data: dict,
    locale: str = DEFAULT_LOCALE,
) -> dict:
    locale = normalize_locale(locale)
    skin_type = questionnaire.get("skin_type")
    concerns = questionnaire.get("skin_concerns") or []
    avoided = [item.lower() for item in questionnaire.get("avoided_ingredients") or []]
    ingredients = product.get("active_ingredients") or []
    ingredient_text = " ".join(ingredients).lower()
    avoided_hits = [item for item in avoided if item and item in ingredient_text]
    skin_label = get_label("skin", skin_type, locale) or ("profil kulitmu" if locale == "id" else "your skin profile")
    concern_labels = [get_label("concern", concern, locale) for concern in concerns]
    ingredient_highlights = ingredients[:3]
    weather_reason = describe_weather_condition(weather_data, locale)

    if locale == "id":
        summary_points = []
        if skin_type in (product.get("skin_types") or []):
            summary_points.append(f"Cocok untuk kulit {skin_label}")
        if concern_labels:
            summary_points.append(f"Relevan untuk {', '.join(concern_labels[:2])}")
        if ingredient_highlights:
            summary_points.append(f"Kandungan utama: {', '.join(ingredient_highlights[:2])}")
        summary_points.append(f"Disesuaikan dengan {weather_reason}")
        avoidance_note = (
            f"Perlu dicek karena mengandung kandungan yang kamu hindari: {', '.join(avoided_hits)}"
            if avoided_hits
            else "Tidak terdeteksi kandungan yang kamu pilih untuk dihindari"
        )
    else:
        summary_points = []
        if skin_type in (product.get("skin_types") or []):
            summary_points.append(f"Suitable for {skin_label} skin")
        if concern_labels:
            summary_points.append(f"Relevant for {', '.join(concern_labels[:2])}")
        if ingredient_highlights:
            summary_points.append(f"Key ingredients: {', '.join(ingredient_highlights[:2])}")
        summary_points.append(f"Adjusted for current weather: {weather_reason}")
        avoidance_note = (
            f"Check carefully because it contains ingredients you avoid: {', '.join(avoided_hits)}"
            if avoided_hits
            else "No selected avoided ingredients were detected"
        )

    return {
        "skin_type_match": skin_type in (product.get("skin_types") or []),
        "matched_concerns": concern_labels,
        "weather_reason": weather_reason,
        "ingredient_highlights": ingredient_highlights,
        "summary_points": summary_points[:4],
        "avoidance_note": avoidance_note,
    }


def build_dynamic_why_recommended(
    product: dict,
    questionnaire: dict,
    weather_data: dict,
    locale: str = DEFAULT_LOCALE,
) -> str:
    locale = normalize_locale(locale)
    factors = build_explanation_factors(product, questionnaire, weather_data, locale)
    brand = product.get("brand") or ("Produk ini" if locale == "id" else "This product")
    name = product.get("product_name") or ("produk ini" if locale == "id" else "this product")
    score = round((product.get("score") or 0) * 100)
    category = product.get("category") or questionnaire.get("product_category") or "produk"
    category_label = get_label("category", category, locale) or category
    ingredients = factors["ingredient_highlights"]
    concerns = factors["matched_concerns"]

    if locale == "id":
        sentences = [
            f"{brand} {name} menjadi kandidat {category_label} dengan skor kecocokan {score}%.",
        ]

        if factors["skin_type_match"]:
            skin_label = get_label("skin", questionnaire.get("skin_type"), locale)
            sentences.append(f"Formula ini terdata cocok untuk kulit {skin_label}, sesuai profil yang kamu pilih.")

        if concerns:
            sentences.append(f"Rekomendasi ini juga relevan dengan fokus {', '.join(concerns[:2])}.")

        if ingredients:
            sentences.append(f"Kandungan utama yang menonjol: {', '.join(ingredients[:3])}.")

        sentences.append(f"Pemilihannya ikut mempertimbangkan kondisi cuaca saat ini: {factors['weather_reason']}.")
        sentences.append(factors["avoidance_note"] + ".")
        return " ".join(sentences)

    sentences = [
        f"{brand} {name} is a strong {category_label} candidate with a match score of {score}%.",
    ]

    if factors["skin_type_match"]:
        skin_label = get_label("skin", questionnaire.get("skin_type"), locale)
        sentences.append(f"Its formula is listed as suitable for {skin_label} skin, matching your selected profile.")

    if concerns:
        sentences.append(f"This recommendation is also relevant for {', '.join(concerns[:2])}.")

    if ingredients:
        sentences.append(f"Key ingredients include {', '.join(ingredients[:3])}.")

    sentences.append(f"The selection also considers current weather: {factors['weather_reason']}.")
    sentences.append(factors["avoidance_note"] + ".")
    return " ".join(sentences)


def build_routine_summary(
    questionnaire: dict,
    weather_data: dict,
    recommendations: list[dict],
    locale: str = DEFAULT_LOCALE,
) -> dict:
    locale = normalize_locale(locale)
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

    if locale == "id":
        morning_focus = "Hidrasi ringan dan perlindungan harian"
        midday_focus = "Jaga kenyamanan kulit dan hindari lapisan berlebihan"
        evening_focus = "Pembersihan lembut dan dukungan lapisan pelindung kulit"
        weekly_focus = "Evaluasi reaksi kulit sebelum menambah produk baru"

        if uv_index >= 7:
            morning_focus = "Perlindungan tabir surya dan pemakaian ulang saat banyak aktivitas luar ruangan"
            midday_focus = "Gunakan ulang tabir surya dan cari tempat teduh ketika UV terasa tinggi"
        elif humidity >= 70:
            morning_focus = "Hidrasi ringan dengan tekstur non-komedogenik"
        elif humidity < 30:
            morning_focus = "Lapisan hidrasi dan dukungan pelindung kulit"

        if pm25 >= 35:
            evening_focus = "Pembersihan lebih teliti lalu hidrasi yang menenangkan"

        if skin_type == "oily":
            weekly_focus = "Pantau area T dan pilih tekstur yang tidak terasa berat"
        elif skin_type == "dry":
            weekly_focus = "Perhatikan tanda ketarik dan tambahkan hidrasi bila perlu"
        elif skin_type == "sensitive":
            weekly_focus = "Uji tempel produk baru dan jaga rutinitas tetap sederhana"

        if product_category == "face mask":
            weekly_focus = "Gunakan masker secukupnya dan perhatikan respon kulit setelah pemakaian"
    else:
        morning_focus = "Light hydration and daily protection"
        midday_focus = "Keep skin comfortable and avoid heavy layering"
        evening_focus = "Gentle cleansing and skin barrier support"
        weekly_focus = "Review skin response before adding new products"

        if uv_index >= 7:
            morning_focus = "Sunscreen protection and reapplication during outdoor activity"
            midday_focus = "Reapply sunscreen and seek shade when UV feels high"
        elif humidity >= 70:
            morning_focus = "Light hydration with non-comedogenic textures"
        elif humidity < 30:
            morning_focus = "Hydration layers and skin barrier support"

        if pm25 >= 35:
            evening_focus = "More thorough cleansing followed by calming hydration"

        if skin_type == "oily":
            weekly_focus = "Monitor the T-zone and choose textures that do not feel heavy"
        elif skin_type == "dry":
            weekly_focus = "Watch for tightness and add hydration when needed"
        elif skin_type == "sensitive":
            weekly_focus = "Patch test new products and keep the routine simple"

        if product_category == "face mask":
            weekly_focus = "Use masks moderately and observe skin response after use"

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
