import { defineStore } from "pinia";
import { computed, reactive } from "vue";
import {products} from "../data/product";


export const useAnalysisStore = defineStore('profile', () => {
    const userProfile = reactive({
        skinType: '',
        concerns: [],
        products: [],
        activity: 'Indoor',
        avoidingIngredients: [],
        customAvoidingIngredients: '',
        isSet: false
    })

    const weatherData = reactive({
        location: "Yogyakarta, ID",
        temperature: 30,
        humidity: 78,
        uvIndex: 7,
        pm25: 45,
        condition: 'Hot & Humid'
    })

    const setProfile = (profile) => {
        userProfile.skinType = profile.skinType;
        userProfile.concerns = profile.concerns;
        userProfile.products = profile.products;
        userProfile.activity = profile.activity;
        userProfile.avoidingIngredients = profile.avoidingIngredients;
        userProfile.customAvoidingIngredients = profile.customAvoidingIngredients;
        userProfile.isSet = true;
    }

    const recommendations = computed(() => {
    if (!userProfile.isSet) return [];

    return products.filter(product => {
      const skinMatch = product.skin.includes('All') || 
                       product.skin.includes(userProfile.skinType) ||
                       userProfile.concerns.some(concern => product.skin.includes(concern));
      
      const weatherMatch = product.weather.includes('Any') || 
                          product.weather.includes(weatherData.condition) ||
                          (weatherData.uvIndex > 5 && product.weather.includes('High UV'));

      return skinMatch && weatherMatch;
    }).slice(0, 4);
  });

  const skinAlert = computed(() => {
    if (weatherData.uvIndex >= 7) {
      return "High UV today! Prioritize SPF protection and seek shade.";
    } else if (weatherData.humidity > 70) {
      return "High humidity detected. Use lightweight, non-comedogenic products.";
    } else if (weatherData.humidity < 30) {
      return "Dry air alert. Focus on barrier repair and deep hydration.";
    }
    return "Weather looks stable. Stick to your usual routine!";
  });


    return {
    userProfile,
    weatherData,
    setProfile,
    recommendations,
    skinAlert
  };
});