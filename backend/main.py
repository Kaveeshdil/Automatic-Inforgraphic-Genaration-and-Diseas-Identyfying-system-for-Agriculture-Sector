from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from pydantic import BaseModel
from typing import List
from PIL import Image, ImageDraw, ImageFont
import io
from fastapi.responses import StreamingResponse

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
    
    categories = list(set(d["category"] for d in DISEASES.values()))
    return {"categories": categories}

@app.get("/symptoms/{category}")
def get_symptoms_by_category(category: str):
   
    symptoms = []
    for d in DISEASES.values():
        if d["category"] == category:
            symptoms.extend(d["symptoms"])
    return {"symptoms": list(set(symptoms))}

class DiagnosisRequest(BaseModel):
    selected_symptoms: List[str]

@app.post("/diagnose")
def diagnose(request: DiagnosisRequest):
    user_input = request.selected_symptoms
    
    if not user_input:
        return {"error": "කරුණාකර රෝග ලක්ෂණ කිහිපයක් තෝරන්න."}

    best_match = None
    highest_score = 0

    
    for disease_id, details in DISEASES.items():
        
        common_symptoms = set(user_input) & set(details["symptoms"])
        score = len(common_symptoms)

       
        if score > highest_score:
            highest_score = score
            best_match = details

    if best_match:
        return {
            "identified": True,
            "disease": best_match["name"],
            "remedies": best_match["remedies"],
            "severity": best_match["severity"]
        }
    else:
        return {"identified": False, "message": "ගැලපෙන රෝගයක් හමු නොවීය."}
    
    from PIL import Image, ImageDraw, ImageFont
import io
from fastapi.responses import StreamingResponse

def create_infographic(disease_name, remedies, severity):
  
    img = Image.new('RGB', (800, 550), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
  
    font_path = "IskoolaPota.ttf" 
    title_font = ImageFont.truetype(font_path, 45)
    text_font = ImageFont.truetype(font_path, 25)
    
  
    draw.rectangle([0, 0, 800, 80], fill=(34, 139, 34))
    draw.text((20, 15), "කෘෂි රෝග විනිශ්චය වාර්තාව", fill=(255, 255, 255), font=title_font)
    
    draw.text((30, 110), f"හඳුනාගත් රෝගය: {disease_name}", fill=(0, 0, 0), font=title_font)
    
   
    draw.text((30, 190), "බරපතලකම:", fill=(0, 0, 0), font=text_font)
    draw.rectangle([200, 200, 700, 220], outline=(200, 200, 200), width=2) 
    bar_width = 200 + (severity * 5) 
    draw.rectangle([200, 200, bar_width, 220], fill=(220, 20, 60)) 
    draw.text((710, 190), f"{severity}%", fill=(220, 20, 60), font=text_font)

 
    draw.text((30, 260), "නිර්දේශිත පිළියම්:", fill=(34, 139, 34), font=text_font)
    
    
    wrapped_remedies = ""
    for i in range(0, len(remedies), 50): 
        wrapped_remedies += remedies[i:i+50] + "\n"
    
    draw.text((30, 300), wrapped_remedies, fill=(50, 50, 50), font=text_font)

    
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr


@app.post("/diagnose")
def diagnose(request: DiagnosisRequest):
    user_input = request.selected_symptoms
    best_match = None
    highest_score = 0

    for key, data in DISEASES.items():
        score = len(set(user_input) & set(data["symptoms"]))
        if score > highest_score:
            highest_score = score
            best_match = data

    if best_match:
        
        img_buffer = create_infographic(best_match["name"], best_match["remedies"], best_match["severity"])
        return StreamingResponse(img_buffer, media_type="image/png")
    
    return {"error": "ගැලපෙන රෝගයක් හමු නොවීය."}