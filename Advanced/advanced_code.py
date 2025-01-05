import requests
import json
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from threading import Thread
import hashlib
import hmac
import os
from cryptography.fernet import Fernet
import base64

Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

Create a rotating file handler
handler = RotatingFileHandler('weather_app.log', maxBytes=1000000, backupCount=1)
handler.setLevel(logging.DEBUG)

Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

Add the handler to the logger
logger.addHandler(handler)

class WeatherApp:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url
        self.params = {
            'appid': self.api_key,
            'units': 'metric'
        }
        self.cipher_suite = Fernet.generate_key()

    def get_weather(self, city):
        try:
            self.params['q'] = city
            response = requests.get(self.base_url, params=self.params)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.HTTPError as errh:
            logger.error(f"HTTP Error: {errh}")
            return None
        except requests.exceptions.ConnectionError as errc:
            logger.error(f"Error Connecting: {errc}")
            return None
        except requests.exceptions.Timeout as errt:
            logger.error(f"Timeout Error: {errt}")
            return None
        except requests.exceptions.RequestException as err:
            logger.error(f"Something went wrong: {err}")
            return None

    def encrypt_data(self, data):
        cipher_suite = Fernet(self.cipher_suite)
        cipher_text = cipher_suite.encrypt(data.encode())
        return cipher_text

    def decrypt_data(self, cipher_text):
        cipher_suite = Fernet(self.cipher_suite)
        plain_text = cipher_suite.decrypt(cipher_text)
        return plain_text.decode()

    def calculate_signature(self, data):
        signature = hmac.new(self.cipher_suite, data.encode(), hashlib.sha256).hexdigest()
        return signature

def main():
    api_key = 'YOUR_API_KEY'
    base_url = '(link unavailable)'
    app = WeatherApp(api_key, base_url)

    city = input("Enter city name: ")
    data = app.get_weather(city)

    if data:
        main_data = data['main']
        weather_data = data['weather'][0]

        encrypted_temp = app.encrypt_data(str(main_data['temp']))
        encrypted_weather = app.encrypt_data(weather_data['description'])

        signature = app.calculate_signature(str(data))

        logger.debug(f"City: {city}")
        logger.debug(f"Temperature: {main_data['temp']}°C")
        logger.debug(f"Weather: {weather_data['description']}")
        logger.debug(f"Encrypted Temperature: {encrypted_temp}")
        logger.debug(f"Encrypted Weather: {encrypted_weather}")
        logger.debug(f"Signature: {signature}")

        print(f"City: {city}")
        print(f"Temperature: {main_data['temp']}°C")
        print(f"Weather: {weather_data['description']}")
        print(f"Encrypted Temperature: {encrypted_temp}")
        print(f"Encrypted Weather: {encrypted_weather}")
        print(f"Signature: {signature}")

if __name__ == "__main__":
    main()
