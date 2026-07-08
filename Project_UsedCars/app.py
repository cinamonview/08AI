from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

json_path = os.path.join(BASE_DIR, "data", "brand_model.json")

print("BASE_DIR =", BASE_DIR)
print("JSON PATH =", json_path)
print("EXISTS =", os.path.exists(json_path))

# 브랜드 모델 정보 
with open(json_path, encoding="utf-8") as f:
    brand_model = json.load(f)

vehicle_path = os.path.join(BASE_DIR, "data", "vehicle_info.json")

with open(vehicle_path, encoding="utf-8") as f:
    vehicle_info = json.load(f)

@app.route("/")
def home():
    brands = sorted(brand_model.keys())
    return render_template(
        "index.html",
        brands=brands
    )

@app.route("/models/<brand>")
def get_models(brand):
    return jsonify(brand_model.get(brand, []))

# ⭐ 이것도 새로 추가
@app.route("/vehicle/<brand>/<model>")
def get_vehicle_info(brand, model):
    info = vehicle_info.get(brand, {}).get(model, {})
    return jsonify(info)


if __name__ == "__main__":
    app.run(debug=True)