import sqlite3
import math


class CityCoordinatesDatabase:
    def __init__(self, db_name='city_coordinates.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS city_coordinates (
                city_name TEXT PRIMARY KEY,
                latitude REAL,
                longitude REAL
            )
        ''')
        self.conn.commit()

    def get_coordinates(self, city_name):
        self.cursor.execute(f'SELECT * FROM city_coordinates WHERE city_name = "{city_name}"')
        result = self.cursor.fetchone()
        if result:
            return result[1], result[2]
        else:
            print(f"Coordinates for {city_name} not found.")
            latitude = float(input(f'Enter the latitude for "{city_name}": '))
            longitude = float(input(f'Enter the longitude for "{city_name}": '))
            self.cursor.execute(f'INSERT INTO city_coordinates VALUES ("{city_name}", "{latitude}", "{longitude}")')
            self.conn.commit()
            return latitude, longitude


class CityDistanceCalculator:
    def __init__(self, db_name='city_coordinates.db'):
        self.db = CityCoordinatesDatabase(db_name)

    def calculate_distance(self, city1, city2):
        coordinates1 = self.db.get_coordinates(city1)
        coordinates2 = self.db.get_coordinates(city2)

        if coordinates1 and coordinates2:
            lat1, lon1 = coordinates1
            lat2, lon2 = coordinates2

            earth_radius = 6371.0

            lat1 = math.radians(lat1)
            lon1 = math.radians(lon1)
            lat2 = math.radians(lat2)
            lon2 = math.radians(lon2)

            # Haversine formula
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            distance = earth_radius * c

            return distance
        else:
            return None


def main():
    calculator = CityDistanceCalculator()
    city1 = input("Enter the first city name: ").strip()
    city2 = input("Enter the second city name: ").strip()
    distance = calculator.calculate_distance(city1, city2)
    if distance:
        print(f"The straight-line distance between {city1} and {city2} is {distance:.2f} kilometers.")
    else:
        print("Unable to calculate the distance.")


if __name__ == "__main__":
    main()
