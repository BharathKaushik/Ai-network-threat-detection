from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson import ObjectId

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["threat_detection"]
collection = db["threats"]


# Convert MongoDB object to JSON
def serialize(threat):
    return {
        "id": str(threat["_id"]),
        "src_ip": threat.get("src_ip"),
        "dst_ip": threat.get("dst_ip"),
        "threat_type": threat.get("threat_type"),
        "packet_size": threat.get("packet_size"),
    }


# API route
@app.get("/threats")
def get_threats():

    threats = list(collection.find().sort("_id", -1).limit(50))

    return [serialize(t) for t in threats]