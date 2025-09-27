# Waste Management & Recycling App

A smart waste management system with AI-based waste classification, reward points system, and user management. Users can deposit waste, scan QR codes, earn rewards, and track their points. The system also supports a machine interface to detect waste, open bins, and display leaderboards.

---

## Features

### Backend
- User registration and account management
- Waste image classification (Stage 1 & Stage 2)
- Reward points calculation based on waste type & weight
- REST API using FastAPI
- MongoDB integration

### Frontend
**User App (Desktop/Phone)**
- Registration & login
- QR code scanning to claim points
- Dashboard to view points
- Leaderboard
- Redeem points for coupons  

**Machine Interface**
- Waste detection via camera
- Weight measurement
- Automatic bin opening
- Display leaderboard and points via QR

### AI Models
- Stage 1: Classifies waste as `E-waste`, `Not Recyclable`, `Organic`, `Recyclable`  
- Stage 2: Classifies subcategories such as `Plastic`, `Metal`, `Paper`, `Glass`, `Clothes`, `Shoes`

---
## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/Anil-29k/Smart_Reuse_Kiosk
cd Smart_Reuse_Kiosk
```
### Data set Link
```
https://drive.google.com/drive/folders/1-3oMnpJ--VhC0JSGuPBjM6JFihbTUUbF?usp=sharing

Downlode and name the folder as given below 
```

## Folder Structure
```
project/ 
│ ├─ backend/               # FastAPI backend scripts 
│  ├─ main.py             # API endpoints 
│  ├─ classifier.py       # Stage1 & Stage2 inference code 
│  ├─ reward.py           # Reward calculation logic 
│  ├─ database.py         # MongoDB interface 
│ ├─ frontend_user/         # User frontend (Tkinter) 
│  ├─ main.py 
│  ├─ qr_scanner.py 
│  ├─ dashboard.py 
|  ├─ api.py
│ ├─ models/                # Pre-trained model files (.pth) 
│  ├─ stage1_model_cpu.pth   
|  ├─ stage2_model_cpu.pth   
| ├─ data/                  # Preprocessed data for training (optional, small size) 
│  ├─Processed_Stage1   
│  ├─Processed_Stage2    
│ ├─ train_stage1.py  # Training & preprocessing scripts 
│ ├─ train_stage2.py 
| ├─ README.md
| ├─ requirements.txt
```
### 2. Create and activate a virtual environment
```
python3.12 -m venv .venv
source .venv/Scripts/activate   # Windows
```
### 3. Install dependencies
```
pip install -r requirements.txt

```
### 4. Train AI Models (Optional pre-trained models are already available)
```
    python sg1_trainning.py 
```
```
    python sg2_trainning.py
```


### 5. Setup MongoDB
```
Install MongoDB locally or use a cloud instance.
Update backend/database.py with your MongoDB URI if not default.
```

### 6. Backend
```
cd backend
uvicorn main:app --reload
```
### 7. user frontend
```
cd frontend_user
python main.py

```

