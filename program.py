import csv
import random
import datetime

# Define crops and their growing conditions
crops_conditions = {
    "Rice": {
        "temperature": (20, 25, 35, 40),  # (lower_min, ideal_min, ideal_max, higher_max)
        "humidity": (60, 70, 90, 100),
        "soil_moisture": (50, 60, 80, 90),
        "light_intensity": (8000, 10000, 20000, 22000)
    },
    "Jute": {
        "temperature": (20, 24, 38, 42),
        "humidity": (50, 60, 80, 90),
        "soil_moisture": (30, 40, 60, 70),
        "light_intensity": (25000, 30000, 50000, 55000)
    },
    "Wheat": {
        "temperature": (10, 12, 25, 28),
        "humidity": (40, 50, 60, 70),
        "soil_moisture": (10, 20, 40, 50),
        "light_intensity": (12000, 15000, 25000, 28000)
    },
    "Potato": {
        "temperature": (15, 18, 22, 25),
        "humidity": (70, 80, 90, 95),
        "soil_moisture": (60, 70, 85, 90),
        "light_intensity": (6000, 8000, 15000, 17000)
    },
    "Sugarcane": {
        "temperature": (20, 25, 35, 40),
        "humidity": (50, 60, 80, 90),
        "soil_moisture": (30, 40, 70, 80),
        "light_intensity": (18000, 20000, 30000, 35000)
    }
}

# Function to generate environmental data (Lower, Ideal, Higher)
def generate_condition(condition_range):
    rand_value = random.random()
    if rand_value < 0.33:
        # Lower condition
        return random.uniform(condition_range[0], condition_range[1])
    elif rand_value < 0.66:
        # Ideal condition
        return random.uniform(condition_range[1], condition_range[2])
    else:
        # Higher condition
        return random.uniform(condition_range[2], condition_range[3])

# Function to label the condition as "Low", "Ideal", or "High"
def get_lih_label(value, condition_range):
    if value < condition_range[1]:
        return "Low"
    elif condition_range[1] <= value <= condition_range[2]:
        return "Ideal"
    else:
        return "High"

# Function to generate advice based on the LIH labels
def generate_advice(temp_lih, humidity_lih, soil_moisture_lih, light_intensity_lih):
    advice = []
    if temp_lih == "High":
        advice.append("Implement shade nets or use reflective mulch to reduce soil and air temperatures.")
    if humidity_lih == "Low":
        advice.append("Consider installing a misting system or using organic mulch to raise humidity levels.")
    if soil_moisture_lih == "Low":
        advice.append("Increase irrigation frequency or use soil moisture-retention techniques.")
    if light_intensity_lih == "Low":
        advice.append("Adjust light exposure if possible or use supplementary lighting.")
    
    # Ensure that there is at least one piece of advice
    if not advice:
        advice.append("Conditions are within the ideal range.")
    
    return " ".join(advice)

# Function to generate random dates and times within the last year
def generate_random_datetime():
    start_date = datetime.datetime.now() - datetime.timedelta(days=365)  # One year ago
    random_date = start_date + datetime.timedelta(days=random.randint(0, 365))
    random_time = datetime.timedelta(seconds=random.randint(0, 86400))  # Random time of day
    random_datetime = random_date + random_time
    return random_datetime.strftime("%Y-%m-%d"), random_datetime.strftime("%H:%M:%S")

# Function to introduce a 3% error in the data
def introduce_error(value):
    error_range = random.uniform(-0.05, 0.05)  # ±5% error
    return value * (1 + error_range)

# Generate the CSV file
with open('V3_crop_environment_data_with_lih_and_advice_with_error.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([
        "Date", "Time", "Crop Name", "Temperature", "Humidity", "Soil Moisture", "Light Intensity",
        "Temperature_LIH", "Humidity_LIH", "Soil_Moisture_LIH", "Light_Intensity_LIH", "Advice"
    ])

    for _ in range(1000):
        crop_name = random.choice(list(crops_conditions.keys()))
        conditions = crops_conditions[crop_name]

        # Generate random conditions for the crop
        temperature = generate_condition(conditions["temperature"])
        humidity = generate_condition(conditions["humidity"])
        soil_moisture = generate_condition(conditions["soil_moisture"])
        light_intensity = generate_condition(conditions["light_intensity"])

        # Introduce error in 3% of the data
        if random.random() < 0.03:  # 3% chance to introduce error
            temperature = introduce_error(temperature)
            humidity = introduce_error(humidity)
            soil_moisture = introduce_error(soil_moisture)
            light_intensity = introduce_error(light_intensity)

        # Get LIH labels for each condition
        temperature_lih = get_lih_label(temperature, conditions["temperature"])
        humidity_lih = get_lih_label(humidity, conditions["humidity"])
        soil_moisture_lih = get_lih_label(soil_moisture, conditions["soil_moisture"])
        light_intensity_lih = get_lih_label(light_intensity, conditions["light_intensity"])

        # Generate advice based on LIH labels
        advice = generate_advice(temperature_lih, humidity_lih, soil_moisture_lih, light_intensity_lih)

        # Get random date and time
        date, time = generate_random_datetime()

        # Write the row to the CSV file
        writer.writerow([
            date, time, crop_name,
            round(temperature, 2), round(humidity, 2), round(soil_moisture, 2), round(light_intensity, 2),
            temperature_lih, humidity_lih, soil_moisture_lih, light_intensity_lih,
            advice
        ])

print("CSV file generated successfully with LIH values, advice, and 3% error.")
