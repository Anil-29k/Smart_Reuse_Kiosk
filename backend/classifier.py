import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

DEVICE = torch.device("cpu")

# -------- MODELS PATH --------
STAGE1_MODEL_PATH = r"..\models\stage1_model_cpu.pth"
STAGE2_MODEL_PATH = r"..\models\stage2_model_cpu.pth"

# -------- CLASS NAMES --------
STAGE1_CLASSES = ["E-waste", "Not Recyclable", "Organic", "Recyclable"]
STAGE2_CLASSES = ["Plastic", "Metal", "Paper", "Glass", "Clothes", "Shoes"]

# -------- TRANSFORM --------
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# -------- LOAD MODEL FUNCTION --------
def load_model(num_classes, path):
    model = models.mobilenet_v3_small(weights=models.MobileNet_V3_Small_Weights.DEFAULT)
    model.classifier[3] = nn.Linear(model.classifier[3].in_features, num_classes)
    model.load_state_dict(torch.load(path, map_location=DEVICE))
    model.eval()
    return model.to(DEVICE)

# Load models
stage1_model = load_model(len(STAGE1_CLASSES), STAGE1_MODEL_PATH)
stage2_model = load_model(len(STAGE2_CLASSES), STAGE2_MODEL_PATH)

# -------- PREDICTION FUNCTION --------
def classify_image(image: Image.Image):
    img_tensor = transform(image).unsqueeze(0).to(DEVICE)

    # Stage1
    with torch.no_grad():
        outputs1 = stage1_model(img_tensor)
        probs1 = torch.softmax(outputs1, dim=1)
        conf1, pred1 = torch.max(probs1, 1)
        stage1_label = STAGE1_CLASSES[pred1.item()]

    # Stage2 (optional)
    stage2_label = None
    if stage1_label in ["Recyclable", "Not Recyclable"]:
        with torch.no_grad():
            outputs2 = stage2_model(img_tensor)
            probs2 = torch.softmax(outputs2, dim=1)
            _, pred2 = torch.max(probs2, 1)
            stage2_label = STAGE2_CLASSES[pred2.item()]

    return stage1_label, stage2_label, conf1.item()