# Weather App Python

A simple Python application that fetches and displays the current weather for a given city using the OpenWeatherMap API.

## Features

- Fetches current weather data for any city.
- Displays temperature and weather description.
- Uses the OpenWeatherMap API.

## Requirements

- Python 3.x
- `requests` library

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/muhammadumermemon/weather-app-python.git
    ```
2. Navigate to the project directory:
    ```bash
    cd weather-app-python
    ```
3. Install the required libraries:
    ```bash
    pip install requests
    ```

## Usage

1. Get your API key from OpenWeatherMap.
2. Replace `'YOUR_API_KEY'` in the `weather_app.py` file with your actual API key.
3. Run the script:
    ```bash
    python weather_app.py
    ```
4. Enter the name of the city when prompted to get the current weather information.

## Example

```bash
Enter city name: London
City: London
Temperature: 15°C
Weather: clear sky
