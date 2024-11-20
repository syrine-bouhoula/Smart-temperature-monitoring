import time
import board
import adafruit_dht
import requests
from RPLCD.i2c import CharLCD
from datetime import datetime

# Initialize the DHT11 sensor and LCD
dhtDevice = adafruit_dht.DHT11(board.D20)  # GPIO20 for DHT11
lcd = CharLCD('PCF8574', 0x27)  # I2C LCD address

# Temperature Thresholds
DAY_LOW_TEMP = 20
DAY_HIGH_TEMP = 22
NIGHT_LOW_TEMP = 19
NIGHT_HIGH_TEMP = 21
DAY_WINDOW_OPEN_TEMP = 15  # Condition to open windows

# Weather API (Open-Meteo) for outdoor temperature (latitude and longitude of Montreal)
latitude = 45.5017
longitude = -73.5673
weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"

def get_outdoor_temperature():
    """Fetch outdoor temperature using the Open-Meteo API."""
    try:
        response = requests.get(weather_url)
        weather_data = response.json()
        return weather_data['current_weather']['temperature']
    except Exception as e:
        print(f"Failed to retrieve outdoor weather data: {e}")
        return None

def is_daytime():
    """Determine if it's daytime based on the hour (8 AM to 8 PM is considered daytime)."""
    current_hour = datetime.now().hour
    return 8 <= current_hour < 20

# Main function to run once
def main():
    # Read indoor temperature from the DHT11 sensor
    temperature = dhtDevice.temperature
    outdoor_temperature = get_outdoor_temperature()

    if temperature is not None:
        # Clear LCD display for new message
        lcd.clear()
        lcd.write_string(f"Indoor:{temperature}°C")
        lcd.crlf()  # Move the cursor to the beginning of the next line
        lcd.write_string(f"Outdoor:{outdoor_temperature}°C")
        print(f"Indoor Temperature: {temperature}°C")

        if outdoor_temperature is not None:
            print(f"Outdoor Temperature: {outdoor_temperature}°C")

        # Determine if it's daytime or nighttime
        if is_daytime():
            # Daytime temperature alerts
            if temperature < DAY_LOW_TEMP:
                lcd.write_string("Turn ON heater")
                print("It's too cold for the daytime! Turn ON the heater.")
            elif temperature > DAY_HIGH_TEMP:
                lcd.write_string("Turn OFF heater")
                print("It's too hot for the daytime! Turn OFF the heater.")
            if outdoor_temperature is not None and outdoor_temperature > DAY_WINDOW_OPEN_TEMP:
                lcd.write_string("Open windows")
                print("It's above 15°C. Turn OFF the heater and open the windows.")
        else:
            # Nighttime temperature alerts
            if temperature < NIGHT_LOW_TEMP:
                lcd.write_string("Turn ON heater")
                print("It's too cold for the nighttime! Turn ON the heater.")
            elif temperature > NIGHT_HIGH_TEMP:
                lcd.write_string("Turn OFF heater")
                print("It's too hot for the nighttime! Turn OFF the heater.")
    else:
        lcd.clear()
        lcd.write_string("Sensor Error")
        print("Failed to retrieve data from the sensor")

if __name__ == "__main__":
    try:
        main()
    finally:
        dhtDevice.exit()
