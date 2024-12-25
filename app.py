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
        .sidebar {
            transform: translateX(100%);
            transition: transform 0.3s ease-in-out;
        }
        .sidebar.open {
            transform: translateX(0);
        }
        .blur-bg {
            backdrop-filter: blur(5px);
        }
    </style>
</head>
<body class="bg-gradient-to-br from-blue-50 to-purple-50 min-h-screen flex items-center justify-center p-4 text-gray-800">
    <main class="relative bg-white rounded-3xl p-8 shadow-lg w-full max-w-lg overflow-hidden">
        <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-blue-400 to-purple-400"></div>
        <h1 class="text-4xl font-bold mb-6 text-center text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-purple-500">Weather Now</h1>
        
        <!-- Hamburger Menu Icon -->
        <button id="menu-btn" class="absolute top-4 right-4 text-gray-600 hover:text-gray-800">
            <span class="iconify" data-icon="heroicons-outline:menu" data-width="24"></span>
        </button>
        
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

    <!-- Sidebar -->
    <div id="sidebar" class="sidebar fixed top-0 right-0 h-full w-4/5 md:w-2/3 lg:w-1/2 bg-white shadow-lg z-50 p-6 flex flex-col">
        <button id="close-sidebar" class="self-end text-gray-600 hover:text-gray-800 mb-6">
            <span class="iconify" data-icon="heroicons-outline:x" data-width="24"></span>
        </button>
        <div class="flex flex-col space-y-4">
            <button id="get-api-btn" class="bg-blue-500 text-white font-semibold py-2 px-4 rounded hover:bg-blue-600 transition duration-300">GET API</button>
            <a href="http://t.me/vzr7x" target="_blank" class="bg-green-500 text-white font-semibold py-2 px-4 rounded hover:bg-green-600 transition duration-300 text-center">CONTACT</a>
        </div>
    </div>

    <!-- Popup 1 -->
    <div id="popup1" class="fixed inset-0 flex items-center justify-center z-50 hidden">
        <div class="absolute inset-0 bg-black opacity-50 blur-bg"></div>
        <div class="bg-white rounded-lg p-8 max-w-md w-full relative z-10">
            <button id="close-popup1" class="absolute top-2 right-2 text-gray-600 hover:text-gray-800">
                <span class="iconify" data-icon="heroicons-outline:x" data-width="24"></span>
            </button>
            <h2 class="text-2xl font-bold mb-4">Generate API</h2>
            <p class="mb-6">Click the button below to generate your API URL.</p>
            <button id="generate-api-btn" class="bg-red-500 text-white font-semibold py-2 px-4 rounded hover:bg-red-600 transition duration-300">GENERATE API</button>
        </div>
    </div>

    <!-- Popup 2 -->
    <div id="popup2" class="fixed inset-0 flex items-center justify-center z-50 hidden">
        <div class="absolute inset-0 bg-black opacity-50 blur-bg"></div>
        <div class="bg-white rounded-lg p-8 max-w-md w-full relative z-10">
            <button id="close-popup2" class="absolute top-2 right-2 text-gray-600 hover:text-gray-800">
                <span class="iconify" data-icon="heroicons-outline:x" data-width="24"></span>
            </button>
            <h2 class="text-2xl font-bold mb-4">Your API URL</h2>
            <input type="text" id="api-url" value="" readonly class="w-full p-2 border rounded mb-4 bg-gray-100">
            <button id="copy-api-btn" class="bg-blue-500 text-white font-semibold py-2 px-4 rounded hover:bg-blue-600 transition duration-300">COPY API URL</button>
            <p id="copy-message" class="mt-2 text-green-500 hidden">Copied!</p>
        </div>
    </div>

    <script>
        // Existing weather fetching code
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

        // New JavaScript for sidebar and popups
        const sidebar = document.getElementById('sidebar');
        const menuBtn = document.getElementById('menu-btn');
        const closeSidebarBtn = document.getElementById('close-sidebar');
        const getApiBtn = document.getElementById('get-api-btn');
        const popup1 = document.getElementById('popup1');
        const popup2 = document.getElementById('popup2');
        const closePopup1Btn = document.getElementById('close-popup1');
        const closePopup2Btn = document.getElementById('close-popup2');
        const generateApiBtn = document.getElementById('generate-api-btn');
        const copyApiBtn = document.getElementById('copy-api-btn');
        const copyMessage = document.getElementById('copy-message');

        menuBtn.addEventListener('click', () => {
            sidebar.classList.add('open');
        });

        closeSidebarBtn.addEventListener('click', () => {
            sidebar.classList.remove('open');
        });

        getApiBtn.addEventListener('click', () => {
            sidebar.classList.remove('open');
            popup1.classList.remove('hidden');
        });

        closePopup1Btn.addEventListener('click', () => {
            popup1.classList.add('hidden');
        });

        closePopup2Btn.addEventListener('click', () => {
            popup2.classList.add('hidden');
        });

        generateApiBtn.addEventListener('click', () => {
            popup1.classList.add('hidden');
            popup2.classList.remove('hidden');
        });

        copyApiBtn.addEventListener('click', () => {
            const apiUrl = document.getElementById('api-url');
            apiUrl.select();
            document.execCommand('copy');
            copyMessage.classList.remove('hidden');
            setTimeout(() => {
                copyMessage.classList.add('hidden');
            }, 2000);
        });

        // Set the API URL with the current domain
        function setApiUrl() {
            const currentDomain = window.location.origin;
            const apiUrl = `${currentDomain}/today-weather`;
            document.getElementById('api-url').value = apiUrl;
        }

        // Call setApiUrl when the second popup is shown
        document.getElementById('generate-api-btn').addEventListener('click', () => {
            popup1.classList.add('hidden');
            popup2.classList.remove('hidden');
            setApiUrl();
        });
    </script>
</body>
</html>
    """
    return render_template_string(html_code)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=True)
