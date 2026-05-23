from pymongo import MongoClient

# Connect MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Database
mydb = client["threat_detection"]

# Collection
threat_collection = mydb["threats"]


def save_threat(data):

    threat_collection.insert_one(data)

    print("Threat saved to database")