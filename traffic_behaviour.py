still_in_progrss



Stefan Versan
​
Stefan Versan (External)
​
import sqlite3

import random

from datetime import datetime

import matplotlib.pyplot as plt

import matplotlib.image as mpimg

from colorama import Fore

import csv

 

# Define the speed limits for different types of roads

SPEED_LIMITS = {

    "town": 50,

    "normal_road": 90,

    "urban_street": 100,

    "highway": 130,

    "schools": 10

}

 

# Connect to SQLite database

conn = sqlite3.connect('car_speed_tracking.db')

cursor = conn.cursor()

 

# Create tables

cursor.execute('''

CREATE TABLE IF NOT EXISTS drivers (

    id INTEGER PRIMARY KEY,

    age INTEGER

)

''')

 

cursor.execute('''

CREATE TABLE IF NOT EXISTS cars (

    id INTEGER PRIMARY KEY,

    driver_id INTEGER,

    make TEXT,

    model TEXT,

    license_plate TEXT,

    town TEXT,

    FOREIGN KEY (driver_id) REFERENCES drivers(id)

)

''')

 

cursor.execute('''

CREATE TABLE IF NOT EXISTS speed_records (

    id INTEGER PRIMARY KEY,

    driver_id INTEGER,

    car_id INTEGER,

    speed REAL,

    speed_limit REAL,

    road_type TEXT,

    timestamp TEXT,

    FOREIGN KEY (car_id) REFERENCES cars(id),

    FOREIGN KEY (driver_id) REFERENCES drivers(id)

)

''')

 

cursor.execute('''

CREATE TABLE IF NOT EXISTS notifications (

    id INTEGER PRIMARY KEY,

    car_id INTEGER,

    speed REAL,

    timestamp TEXT,

    FOREIGN KEY(car_id) REFERENCES cars(id)

)

''')

 

cursor.execute('''

CREATE TABLE IF NOT EXISTS car_behaviours (

    id INTEGER PRIMARY KEY,

    car_id INTEGER,

    over_speed_limit BOOLEAN,

    timestamp TEXT,

    FOREIGN KEY (car_id) REFERENCES cars(id)

)

''')

 

# Commit the changes to the database

conn.commit()

 

# Function to add a car

def add_car(license_plate, town, driver_id, make="Unknown", model="Unknown"):

    cursor.execute('''

    INSERT INTO cars (license_plate, town, driver_id, make, model)

    VALUES (?, ?, ?, ?, ?)

    ''', (license_plate, town, driver_id, make, model))

    conn.commit()

 

# Function to simulate getting the current speed of a car

def get_current_speed():

    return random.uniform(0, 150)  # Simulate a speed between 0 and 150 km/h

 

# Function to get the speed limit based on the road type

def get_speed_limit(road_type):

    return SPEED_LIMITS[road_type]

 

# Function to log speed record

def log_speed_record(car_id, driver_id, speed, speed_limit, road_type):

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''

        INSERT INTO speed_records (car_id, driver_id, speed, speed_limit, road_type, timestamp)

        VALUES (?, ?, ?, ?, ?, ?)

    ''', (car_id, driver_id, speed, speed_limit, road_type, timestamp))

    conn.commit()

 

# Function to log notification

def log_notification(car_id, speed):

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''

        INSERT INTO notifications (car_id, speed, timestamp)

        VALUES (?, ?, ?)

    ''', (car_id, speed, timestamp))

    conn.commit()

 

# Function to log car behavior

def log_car_behavior(car_id, over_speed_limit):

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''

        INSERT INTO car_behaviours (car_id, over_speed_limit, timestamp)

        VALUES (?, ?, ?)

    ''', (car_id, over_speed_limit, timestamp))

    conn.commit()

 

# Function to send notification if speed limit is exceeded

def send_notification(car_id, speed, speed_limit):

    print(f"Notification: Car ID {car_id} exceeded the speed limit! Speed: {speed:.2f} km/h, Limit: {speed_limit} km/h")

    log_notification(car_id, speed)

 

# Add some sample drivers

cursor.execute("INSERT INTO drivers (age) VALUES (25)")  # Driver 1

cursor.execute("INSERT INTO drivers (age) VALUES (40)")  # Driver 2

cursor.execute("INSERT INTO drivers (age) VALUES (65)")  # Driver 3

cursor.execute("INSERT INTO drivers (age) VALUES (18)")  # Driver 4

conn.commit()

 

# Add cars for these drivers

add_car("ABC123", "MARS", 1)  # Car for Driver 1

add_car("XYZ789", "MARS", 2)  # Car for Driver 2

add_car("CDZ799", "MARS", 3)  # Car for Driver 3

add_car("XAZ689", "MARS", 4)  # Car for Driver 4

 

# Function to simulate tracking speeds for the cars

def track_speeds():

    cursor.execute('SELECT id FROM cars WHERE town = "MARS"')

    cars = cursor.fetchall()

 

    for car in cars:

        car_id = car[0]

        driver_id = car[0]  # assuming driver_id is the same as car_id for this example

        speed = get_current_speed()

        road_type = random.choice(["town", "normal_road", "urban_street", "highway", "schools"])

        speed_limit = get_speed_limit(road_type)

 

        print(f"Car ID: {car_id}, Speed: {speed:.2f} km/h, Speed Limit: {speed_limit} km/h ({road_type})")

 

        log_speed_record(car_id, driver_id, speed, speed_limit, road_type)

 

        if speed > speed_limit:

            send_notification(car_id, speed, speed_limit)

            log_car_behavior(car_id, True)

        else:

            log_car_behavior(car_id, False)

 

# Call track_speeds to populate speed data in the database

track_speeds()

 

# Function to generate and display a pie chart of car behaviors

def display_dashboard():

    cursor.execute('''SELECT over_speed_limit, COUNT(*)

                   FROM car_behaviours

                   GROUP BY over_speed_limit''')

    results = cursor.fetchall()

   

    cursor.execute('''

        SELECT car_id, COUNT(*)

        FROM speed_records

        GROUP BY car_id

        HAVING COUNT(*) = (SELECT COUNT(*) FROM speed_records WHERE car_id = car_id AND speed <= speed_limit)

        ''')

   

    skilled_drivers_result = cursor.fetchall()

    skilled_drivers_count = len(skilled_drivers_result)

    overspeed_count = results[1][1] if len(results) > 1 else 0

    within_speed_limit_count = results[0][1] if len(results) > 0 else 0

   

    labels = ['Skilled Drivers (Speed Limit Adhering)', 'Over Speed Limit Cars', 'Within Speed Limit)']

    sizes = [skilled_drivers_count, overspeed_count,within_speed_limit_count]

    colors = ['green','orange','blue']

    explode = (0.1,0,0)

    if len(results) == 0:

        print(Fore.LIGHTRED_EX + "No data available for car behaviors!")

        return

 

    '''labels = ['Within Speed Limit', 'Over Speed Limit']

    sizes = [result[1] for result in results]

    colors = ['red', 'yellow']

    explode = (0, 0.1)  # explode the second slice (Over Speed Limit)'''

    total_drivers = sum(sizes)

    respecting_percentage = (sizes[0] / total_drivers) * 100

 

    # Create the figure and subplots grid

    fig, axs = plt.subplots(1, 3, figsize=(15, 6))  # Create a 1x3 grid for pie chart, image, and speed chart

 

    fig.patch.set_facecolor('beige')

 

    # Pie chart

    axs[0].pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',

               shadow=True, startangle=140)

    axs[0].set_title("Car Behavior")

 

    # Load the vehicle icon (replace with your icon path)

    try:

        vehicle_icon = mpimg.imread('car.png')  # Make sure the image is in the same directory or provide full path

        axs[1].imshow(vehicle_icon, aspect='auto', alpha=0.6)

        axs[1].axis('off')  # Hide the axes for the image

        axs[1].set_title("Vehicle Pictogram")

    except FileNotFoundError:

        axs[1].text(0.5, 0.5, 'Car Image Not Found', horizontalalignment='center', verticalalignment='center')

 

    # Line chart for speed (replace with actual speed data if needed)

    cursor.execute('SELECT timestamp, speed FROM speed_records ORDER BY timestamp DESC LIMIT 10')

    speed_data = cursor.fetchall()

    timestamps = [entry[0] for entry in speed_data]

    speeds = [entry[1] for entry in speed_data]

    axs[2].plot(timestamps, speeds, marker='o', color='b', linestyle='-', markersize=5)

    axs[2].set_title("Car Speed Over Time")

    axs[2].set_xlabel("Time")

    axs[2].set_ylabel("Speed (km/h)")

    axs[2].tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better readability

 

    fig.tight_layout()

    plt.draw()

    plt.show()

 

# Function to generate and display statistics

def generate_statistics():

    cursor.execute('''SELECT COUNT(*) FROM speed_records WHERE driver_id IN (SELECT id FROM drivers WHERE age BETWEEN 18 AND 35)''')

    young_drivers = cursor.fetchone()[0]

    cursor.execute('''SELECT COUNT(*) FROM speed_records WHERE driver_id IN (SELECT id FROM drivers WHERE age BETWEEN 35 AND 65)''')

    experienced_drivers = cursor.fetchone()[0]

 

    sizes = [young_drivers, experienced_drivers]

    if sum(sizes) == 0:

        print(Fore.LIGHTGREEN_EX, "No speed data available. Cannot generate statistics!")

        return

 

    labels = ['Young Drivers (18-35)', 'Experienced Drivers (35-65)']

    colors = ['blue', 'green']

    explode = (0, 0.1)

 

    plt.figure(figsize=(6, 6))

    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)

    plt.title("Driver Rule Adherence Statistics")

    plt.draw()

    plt.show()

 

# Generate statistics and display the dashboard

generate_statistics()

display_dashboard()

 

# Close the database connection

conn.close()

 

 

