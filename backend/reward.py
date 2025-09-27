# Reward points based on waste type and weight (kg)
WASTE_POINTS = {
    "E-waste": 10,
    "Not Recyclable": 2,
    "Organic": 1,
    "Recyclable": 5
}

def calculate_points(stage1_label: str, weight_kg: float) -> float:
    base_points = WASTE_POINTS.get(stage1_label, 0)
    return base_points * weight_kg