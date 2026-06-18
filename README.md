# SkinSense AI

**AI-Powered Skincare Recommendation System Based on Environmental Conditions**

SkinSense AI is a context-aware skincare recommendation system that combines user skin profiles and real-time environmental data to provide personalized skincare recommendations.

---

## 📖 Overview

Many users choose skincare products based on trends, popularity, or social media recommendations without considering environmental factors that significantly affect skin conditions.

SkinSense AI addresses this problem by integrating:

* Skin Type
* Skin Concerns
* Product Category
* Ingredients to Avoid
* Temperature
* Humidity
* UV Index
* Air Quality

The system utilizes a **Content-Based Filtering** approach combined with **Context-Aware Recommendation** techniques to generate personalized skincare recommendations.

---

## 🎯 Problem Statement

Current skincare recommendation platforms primarily focus on user preferences and product characteristics while often overlooking environmental factors.

This project aims to answer the following questions:

1. How can real-time environmental data be integrated efficiently into a recommendation system?
2. What approach is most effective for matching user profiles and weather conditions with suitable skincare products?

---

## ✨ Features

* User Authentication
* Personalized Skincare Recommendation
* Weather API Integration
* GPS-Based Location Detection
* Context-Aware Recommendation System
* Product Detail Page
* Favorite Products Feature
* Daily Skincare Routine Suggestion
* Responsive Web Design

---

## 🏗️ System Architecture

```text
User
 │
 ▼
Frontend (Vue.js)
 │
 ▼
Flask REST API
 │
 ▼
Recommendation Engine
 │
 ▼
Database

GPS Location
 │
 ▼
Weather API
 │
 ▼
Environmental Data

User Profile + Weather Data
 │
 ▼
Recommendation Engine
 │
 ▼
Recommended Products
```

---

## 🤖 Recommendation Method

### Content-Based Filtering

The recommendation engine matches products based on:

* Skin Type
* Skin Concerns
* Product Category
* Ingredients

### Context-Aware Recommendation

Recommendations are adjusted using environmental conditions such as:

* Temperature
* Humidity
* UV Index
* Air Quality

This allows the system to provide recommendations that adapt to changing environmental conditions.

---

## 🛠️ Technology Stack

### Frontend

* Vue.js

### Backend

* Python
* Flask

### Database

* SQLite 

### External Services

* WeatherAPI
* Browser Geolocation API

### Development Tools

* Google Colab
* GitHub

---

## 📊 Dataset

The skincare dataset contains information such as:

* Product Name
* Product Category/Type
* Ingredients
* Skin Type Compatibility
* Product Brand
* Rank
* Price

The project uses an international skincare dataset to support broader recommendation coverage.

---

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/your-username/skinsense-ai.git
cd skinsense-ai
```

### Backend Setup

```bash
cd backend

python -m venv venv
```

Activate virtual environment:

Windows:

```bash
venv\Scripts\activate
```

Linux/MacOS:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run backend server:

```bash
python run.py
```

---

### Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

---

## ⚙️ Environment Variables

Create a `.env` file:

```env
WEATHER_API_KEY=your_weather_api_key
DATABASE_URL=your_database_url
```

---

## 📱 Usage

1. Open the application.
2. Login or register.
3. Fill in the skincare profile form.
4. Allow GPS location access.
5. Submit the recommendation request.
6. View personalized skincare recommendations.
7. Save products to favorites.

---

## 📸 Screenshots

### Home Page

<img width="529" height="277" alt="Picture3" src="https://github.com/user-attachments/assets/cea8a788-4c62-44b8-9731-b5332995e065" />

### Input Form

<img width="504" height="391" alt="Picture2" src="https://github.com/user-attachments/assets/1bae9cf0-3575-48d7-a1dc-a3ee1ec7990e" />


### Recommendation Result

<img width="654" height="976" alt="Picture1" src="https://github.com/user-attachments/assets/598038ac-fe8b-4ad1-9856-c66b20bcb37c" />


### Product Detail

<img width="1901" height="912" alt="image" src="https://github.com/user-attachments/assets/bb4e3aa7-4e1d-4fd2-b40c-6ee090664266" />

---

## 📂 Project Structure

```text
SkinSense-AI/
│
├── front-end/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── back-end/
│   ├── run.py
│   ├── app/
│   └── requirements.txt
│
├── machine-learning/
│   ├── data/
│   ├── dataset/
│   ├── scratch/
│   ├── services/
│   └── requirements.txt
│
└── README.md
```

---

## 👥 Team

### PJK-GM066

* Yuusha Yuzka Ramzani
* Dewi Qurrotul Ainy
* Tia Kusuma Wardani
* Haidar Aditya Baran
* Andi Rizki Mahesa

---

## 📄 License

This project was developed for educational and research purposes as part of the Dicoding x Bangkit Capstone Project.
