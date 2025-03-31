import json
from pymongo import MongoClient

# Load the JSON data from the file
with open('JSON_Files/Infected_crop.json', 'r') as file:
    data = json.load(file)

client = MongoClient("mongodb://localhost:27017/")  # Update with your MongoDB URI if needed
db = client["Crop_Disease_Prediction"]  # Database name
collection = db["Infected_Crop"]  # Collection name

# Insert data into MongoDB
collection.insert_many(data["infected_crops"])

print("Data inserted successfully!")