import time
import board
import adafruit_dht
import requests
from RPLCD.i2c import CharLCD
from datetime import datetime
import psycopg2

# Initialize the DHT11 sensor and LCD
dhtDevice = adafruit_dht.DHT11(board.D20)  # GPIO20 for DHT11
lcd = CharLCD('PCF8574', 0x27)  # I2C LCD address

# PostgreSQL connection
conn = psycopg2.connect(
    dbname="temperature_data",
    user="postgres",
    password="admin",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Weather API (Open-Meteo) for outdoor temperature and weather conditions
latitude = 45.5017
longitude = -73.5673
weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"

# RGB LED pastel colors for temperature thresholds
def set_rgb_color(r, g, b):
    print(f"Setting RGB to ({r}, {g}, {b})")  # Simulate RGB change

def get_rgb_color(outdoor_temp):
    if 5 <= outdoor_temp < 10:
        return (255, 182, 193)  # Pastel pink
    elif 0 <= outdoor_temp < 5:
        return (224, 255, 255)  # Light cyan
    elif -5 <= outdoor_temp < 0:
        return (255, 228, 225)  # Misty rose
    elif -10 <= outdoor_temp < -5:
        return (240, 255, 240)  # Honeydew
    elif -15 <= outdoor_temp < -10:
        return (250, 240, 230)  # Linen
    else:  # Below -15
        return (255, 240, 245)  # Lavender blush

def get_outdoor_weather():
    """Fetch outdoor temperature and weather using the Open-Meteo API."""
    try:
        response = requests.get(weather_url)
        weather_data = response.json()
        temperature = weather_data['current_weather']['temperature']
        is_snowing = weather_data['current_weather']['weathercode'] == 71  # Code for snow
        return temperature, is_snowing
    except Exception as e:
        print(f"Failed to retrieve outdoor weather data: {e}")
        return None, False

def is_daytime():
    """Determine if it's daytime based on the hour (8 AM to 8 PM is considered daytime)."""
    current_hour = datetime.now().hour
    return 8 <= current_hour < 20
def read_sensor_with_retry(max_retries=3):
    """Retry mechanism for reading sensor data."""
    for _ in range(max_retries):
        try:
            temperature = dhtDevice.temperature
            humidity = dhtDevice.humidity
            if temperature is not None and humidity is not None:
                return temperature, humidity
        except RuntimeError as e:
            print(f"Sensor read failed: {e}. Retrying...")
            time.sleep(2)  # Wait before retrying
    return None, None  # Return None if all retries fail

def main():
    try:
        while True:
            # Read indoor temperature and humidity
            indoor_temp, humidity = read_sensor_with_retry()
            if indoor_temp is None or humidity is None:
                lcd.clear()
                lcd.write_string("Sensor Error")
                print("Failed to retrieve data from the sensor")
                continue

            # Fetch outdoor weather data
            outdoor_temp, is_snowing = get_outdoor_weather()
            if outdoor_temp is None:
                print("Failed to retrieve outdoor temperature")
                continue

            # Display data on LCD
            lcd.clear()
            lcd.write_string(f"Indoor:{indoor_temp}°C")
            lcd.crlf()
            lcd.write_string(f"Outdoor:{outdoor_temp}°C")
            print(f"Indoor Temperature: {indoor_temp}°C")
            print(f"Humidity: {humidity}%")
            print(f"Outdoor Temperature: {outdoor_temp}°C")
            print(f"Is it snowing? {'Yes' if is_snowing else 'No'}")

            # Set RGB LED color based on outdoor temperature
            r, g, b = get_rgb_color(outdoor_temp)
            set_rgb_color(r, g, b)

            # Display alerts on LCD
            if humidity > 60:
                lcd.clear()
                lcd.write_string("High Humidity!")
                lcd.crlf()
                lcd.write_string("Open Door")
                print("High Humidity! Open Door")

            if is_snowing:
                lcd.clear()
                lcd.write_string("It's Snowing!")
                print("It's Snowing!")

            # Save data to PostgreSQL
            try:
                query = """
                    INSERT INTO temperature_data (timestamp, indoor_temperature, outdoor_temperature, is_snowing, humidity)
                    VALUES (%s, %s, %s, %s, %s);
                """
                timestamp = datetime.now()
                cursor.execute(query, (timestamp, indoor_temp, outdoor_temp, is_snowing, humidity))
                conn.commit()
                print("Data saved to PostgreSQL successfully.")
            except Exception as e:
                print(f"Error saving to database: {e}")

            time.sleep(10)  # Wait before the next reading

    except KeyboardInterrupt:
        print("Exiting program...")
    finally:
        dhtDevice.exit()
        conn.close()

if __name__ == "__main__":
    main()
