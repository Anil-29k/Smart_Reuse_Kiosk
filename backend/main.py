from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from PIL import Image

from classifier import classify_image
from reward import calculate_points
from database import register_user, login_user, add_points, get_user, get_leaderboard

app = FastAPI(title="Waste Management API")

# ---------------- MODELS ----------------
class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class RewardRequest(BaseModel):
    user_id: str
    stage1_label: str
    weight_kg: float

# ---------------- USER ENDPOINTS ----------------
@app.post("/register")
def api_register(req: RegisterRequest):
    res = register_user(req.name, req.email, req.password)
    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])
    return res

@app.post("/login")
def api_login(req: LoginRequest):
    res = login_user(req.email, req.password)
    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])
    return res

@app.get("/user/{user_id}")
def api_get_user(user_id: str):
    res = get_user(user_id)
    if "error" in res:
        raise HTTPException(status_code=404, detail=res["error"])
    return res

@app.get("/leaderboard")
def api_leaderboard(top_n: int = 10):
    return {"leaderboard": get_leaderboard(top_n)}

# ---------------- IMAGE CLASSIFICATION ----------------
@app.post("/classify")
def api_classify(file: UploadFile = File(...)):
    try:
        image = Image.open(file.file).convert("RGB")
    except:
        raise HTTPException(status_code=400, detail="Invalid image file")
    
    stage1_label, stage2_label, confidence = classify_image(image)
    return {"stage1_class": stage1_label, "stage2_class": stage2_label, "confidence": confidence}

# ---------------- REWARD CALCULATION ----------------
@app.post("/calculate_reward")
def api_reward(req: RewardRequest):
    points = calculate_points(req.stage1_label, req.weight_kg)
    res = add_points(req.user_id, points)
    if "error" in res:
        raise HTTPException(status_code=404, detail=res["error"])
    return {"added_points": points, "total_points": res["total_points"]}