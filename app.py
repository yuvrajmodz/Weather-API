from flask import Flask, jsonify, render_template_string
from bs4 import BeautifulSoup
import requests
import json
import os

app = Flask(__name__)

# Copyright © 2024 𝐌𝐀𝐓𝐑𝐈𝐗

# Developed By @YuvrajMODZ

# Scraping Purpose

@app.route('/today-weather', methods=['GET'])
def get_weather():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    }
    
    # Fetching location and weather data
    location_response = requests.get("https://www.google.com/search?q=my+location", headers=headers)
    location_soup = BeautifulSoup(location_response.text, "html.parser")
    
    location_data_tag = location_soup.select_one(".vk_sh.vk_bk .aiAXrc")
    location_data = location_data_tag.text.strip() if location_data_tag else "Unknown Location"
    
    region_data_tag = location_soup.select_one(".vk_sh.vk_bk .fMYBhe")
    region_data = region_data_tag.text.strip() if region_data_tag else ""
    weather_for = f"{location_data}, {region_data}".strip()
    
    weather_response = requests.get("https://www.google.com/search?q=weather", headers=headers)
    weather_soup = BeautifulSoup(weather_response.text, "html.parser")
    
    day_time_tag = weather_soup.select_one("#wob_dts")
    day_time = day_time_tag.text.strip() if day_time_tag else "N/A"
    
    temperature_tag = weather_soup.select_one("#wob_tm")
    temperature = temperature_tag.text.strip() + " degree" if temperature_tag else "N/A"
    
    precipitation_tag = weather_soup.select_one("#wob_pp")
    precipitation = precipitation_tag.text.strip() if precipitation_tag else "N/A"
    
    humidity_tag = weather_soup.select_one("#wob_hm")
    humidity = humidity_tag.text.strip() if humidity_tag else "N/A"
    
    wind_tag = weather_soup.select_one("#wob_ws")
    wind = wind_tag.text.strip() if wind_tag else "N/A"
    
    weather_data = {
        "weather-for": weather_for,
        "day-time": day_time,
        "temperature": temperature,
        "other-details": {
            "precipitation": precipitation,
            "humidity": humidity,
            "wind": wind
        }
    }
    
    formatted_response = json.dumps(weather_data, indent=4)
    return app.response_class(formatted_response, mimetype='application/json')

@app.route('/')
def home():
    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Modern Light Weather App</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://code.iconify.design/2/2.1.0/iconify.min.js"></script>
        <style>
            @keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-10px); }}
            @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.7; }}
            .float { animation: float 6s ease-in-out infinite; }
            .pulse { animation: pulse 2s ease-in-out infinite; }
            .spinner {
                border: 4px solid rgba(255, 255, 255, 0.3);
                border-top: 4px solid #3498db;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body class="bg-gradient-to-br from-blue-50 to-purple-50 min-h-screen flex items-center justify-center p-4 text-gray-800">
        <main class="relative bg-white rounded-3xl p-8 shadow-lg w-full max-w-lg overflow-hidden">
            <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-blue-400 to-purple-400"></div>
            <h1 class="text-4xl font-bold mb-6 text-center text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-purple-500">Weather Now</h1>
            
            <!-- Loading Spinner -->
            <div id="loading-spinner" class="flex justify-center mt-10">
                <div class="spinner"></div>
            </div>
            
            <div id="weather-info" class="space-y-6 hidden">
                <div class="flex justify-center">
                    <div class="text-8xl float" id="weather-icon">🌤️</div>
                </div>
                <div class="text-center">
                    <h2 class="text-2xl font-semibold" id="location"></h2>
                    <p class="text-lg text-gray-600" id="day-time"></p>
                    <p class="text-5xl font-bold mt-2" id="temperature"></p>
                </div>
                <div class="grid grid-cols-3 gap-4 text-center">
                    <div class="bg-gray-50 rounded-2xl p-3 shadow-sm">
                        <p class="text-sm text-gray-500">Precipitation</p>
                        <p class="text-xl font-semibold mt-1" id="precipitation"></p>
                    </div>
                    <div class="bg-gray-50 rounded-2xl p-3 shadow-sm">
                        <p class="text-sm text-gray-500">Humidity</p>
                        <p class="text-xl font-semibold mt-1" id="humidity"></p>
                    </div>
                    <div class="bg-gray-50 rounded-2xl p-3 shadow-sm">
                        <p class="text-sm text-gray-500">Wind</p>
                        <p class="text-xl font-semibold mt-1" id="wind"></p>
                    </div>
                </div>
            </div>
            
            <div class="mt-6 text-center">
                <button id="refresh-btn" class="bg-gradient-to-r from-blue-400 to-purple-400 text-white font-semibold py-2 px-6 rounded-full hover:from-blue-500 hover:to-purple-500 transition duration-300 ease-in-out transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-400">
                    Refresh Weather
                </button>
            </div>
            <div class="mt-4 text-center text-xs text-gray-400">
                Last updated: <span id="last-updated"></span>
            </div>
        </main>

        <script>
            async function fetchWeatherData() {
                try {
                    document.getElementById('loading-spinner').style.display = 'flex';
                    document.getElementById('weather-info').style.display = 'none';
                    
                    const response = await fetch('/today-weather');
                    const data = await response.json();
                    updateWeather(data);
                    
                } catch (error) {
                    console.error('Error fetching weather data:', error);
                } finally {
                    document.getElementById('loading-spinner').style.display = 'none';
                    document.getElementById('weather-info').style.display = 'block';
                }
            }

            function updateWeather(data) {
                document.getElementById('location').textContent = data["weather-for"];
                document.getElementById('day-time').textContent = data["day-time"];
                document.getElementById('temperature').textContent = data["temperature"];
                document.getElementById('precipitation').textContent = data["other-details"]["precipitation"];
                document.getElementById('humidity').textContent = data["other-details"]["humidity"];
                document.getElementById('wind').textContent = data["other-details"]["wind"];
                document.getElementById('last-updated').textContent = new Date().toLocaleTimeString();
            }

            document.getElementById('refresh-btn').addEventListener('click', fetchWeatherData);

            fetchWeatherData();  // Initial fetch
        </script>
    </body>
    </html>
    """
    return render_template_string(html_code)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=True)