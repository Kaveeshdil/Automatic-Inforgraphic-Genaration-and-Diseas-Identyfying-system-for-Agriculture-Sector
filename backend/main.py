from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# React (CORS) five permission to add
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# read json data
def load_data():
    with open("diseases.json", "r", encoding="utf-8") as file:
        return json.load(file)

DISEASES = load_data()

@app.get("/categories")
def get_categories():
    # සියලුම රෝග වලින් category ටික විතරක් අරගෙන double වෙන්නේ නැති වෙන්න (set) සකස් කිරීම
    categories = list(set(d["category"] for d in DISEASES.values()))
    return {"categories": categories}

@app.get("/symptoms/{category}")
def get_symptoms_by_category(category: str):
    # තෝරාගත් category එකට අදාළ රෝග ලක්ෂණ පමණක් ලබා දීම
    symptoms = []
    for d in DISEASES.values():
        if d["category"] == category:
            symptoms.extend(d["symptoms"])
    return {"symptoms": list(set(symptoms))}