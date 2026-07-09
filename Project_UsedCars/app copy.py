from flask import Flask, render_template, jsonify, request

import os
import json

import pandas as pd

from catboost import CatBoostRegressor

import shap



app = Flask(__name__)





# ======================================
# PATH
# ======================================


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)





# ======================================
# JSON LOAD
# ======================================


brand_model_file = os.path.join(

    BASE_DIR,

    "data",

    "brand_model.json"

)


vehicle_file = os.path.join(

    BASE_DIR,

    "data",

    "vehicle_info.json"

)





with open(

    brand_model_file,

    encoding="utf-8"

) as f:

    brand_model = json.load(f)





with open(

    vehicle_file,

    encoding="utf-8"

) as f:

    vehicle_info = json.load(f)





print("JSON LOAD COMPLETE")







# ======================================
# CATBOOST LOAD
# ======================================


model_file = os.path.join(

    BASE_DIR,

    "models",

    "catboost_final.cbm"

)





cat_model = CatBoostRegressor()



cat_model.load_model(

    model_file

)





print("CATBOOST MODEL LOAD COMPLETE")







# ======================================
# SHAP LOAD
# ======================================


explainer = shap.TreeExplainer(

    cat_model

)





print("SHAP LOAD COMPLETE")









# ======================================
# FEATURE NAME
# ======================================


feature_name_map = {


    "make_name":

        "제조사",


    "model_name":

        "차량 모델",


    "year":

        "제조 연도",


    "vehicle_age":

        "차량 연식",


    "mileage":

        "주행거리",


    "mileage_per_year":

        "연평균 주행거리",


    "body_type":

        "차체 타입",


    "fuel_type":

        "연료 타입",


    "transmission":

        "변속기",


    "engine_displacement":

        "엔진 배기량",


    "engine_cylinders":

        "엔진 실린더",


    "engine_type":

        "엔진 타입",


    "wheel_system":

        "구동 방식",


    "city_fuel_economy":

        "도심 연비",


    "highway_fuel_economy":

        "고속도로 연비",


    "has_accidents":

        "사고 여부",


    "frame_damaged":

        "프레임 손상",


    "is_large_engine":

        "대배기량 엔진"

}









# ======================================
# HOME
# ======================================


@app.route("/")

def home():


    brands = sorted(

        brand_model.keys()

    )


    return render_template(

        "index.html",

        brands=brands

    )









# ======================================
# MODEL API
# ======================================


@app.route("/models/<brand>")

def get_models(brand):


    return jsonify(

        brand_model.get(

            brand,

            []

        )

    )









# ======================================
# VEHICLE API
# ======================================


@app.route("/vehicle/<brand>/<model>")

def get_vehicle(

    brand,

    model

):


    info = vehicle_info.get(

        brand,

        {}

    ).get(

        model,

        {}

    )


    return jsonify(info)


# ======================================
# RESULT PAGE
# ======================================


@app.route("/result")

def result():


    shap_string = request.args.get(

        "shap",

        "[]"

    )


    try:

        shap_data = json.loads(

            shap_string

        )


    except Exception as e:


        print(

            "SHAP LOAD ERROR",

            e

        )


        shap_data = []





    return render_template(

        "result.html",


        price=request.args.get(

            "price",

            ""

        ),


        brand=request.args.get(

            "brand",

            ""

        ),


        model=request.args.get(

            "model",

            ""

        ),


        year=request.args.get(

            "year",

            ""

        ),


        mileage=request.args.get(

            "mileage",

            ""

        ),


        fuel=request.args.get(

            "fuel",

            ""

        ),


        transmission=request.args.get(

            "transmission",

            ""

        ),


        engine=request.args.get(

            "engine",

            ""

        ),


        wheel=request.args.get(

            "wheel",

            ""

        ),


        shap=shap_data,
        
       
        confidence=request.args.get(
            "confidence",
            "85"
        )

    )









# ======================================
# PREDICT
# ======================================


@app.route(

    "/predict",

    methods=["POST"]

)

def predict():


    data = request.json





    # ===============================
    # USER INPUT
    # ===============================


    brand = data["make_name"]


    model_name = data["model_name"]





    vehicle = vehicle_info[brand][model_name]





    year = int(

        data["year"]

    )


    mileage = int(

        data["mileage"]

    )





    current_year = 2026





    vehicle_age = (

        current_year - year

    )





    if vehicle_age <= 0:


        vehicle_age = 1





    mileage_per_year = (

        mileage /

        vehicle_age

    )





    is_large_engine = (

        vehicle["engine_displacement"]

        >=

        3000

    )









    # ===============================
    # MODEL DATA
    # ===============================


    input_data = {


        "make_name":

            vehicle["make_name"],


        "model_name":

            vehicle["model_name"],


        "year":

            year,


        "vehicle_age":

            vehicle_age,


        "mileage":

            mileage,


        "mileage_per_year":

            mileage_per_year,


        "body_type":

            vehicle["body_type"],


        "fuel_type":

            vehicle["fuel_type"],


        "transmission":

            vehicle["transmission"],


        "engine_displacement":

            vehicle["engine_displacement"],


        "engine_cylinders":

            vehicle["engine_cylinders"],


        "engine_type":

            vehicle["engine_type"],


        "wheel_system":

            vehicle["wheel_system"],


        "has_accidents":

            data["has_accidents"],


        "frame_damaged":

            data["frame_damaged"],


        "city_fuel_economy":

            vehicle["city_fuel_economy"],


        "highway_fuel_economy":

            vehicle["highway_fuel_economy"],


        "is_large_engine":

            is_large_engine


    }









    feature_order = [


        "make_name",

        "model_name",

        "year",

        "vehicle_age",

        "mileage",

        "mileage_per_year",

        "body_type",

        "fuel_type",

        "transmission",

        "engine_displacement",

        "engine_cylinders",

        "engine_type",

        "wheel_system",

        "has_accidents",

        "frame_damaged",

        "city_fuel_economy",

        "highway_fuel_economy",

        "is_large_engine"


    ]









    df = pd.DataFrame(

        [input_data],

        columns=feature_order

    )









    # ===============================
    # PRICE PREDICT
    # ===============================


    prediction = cat_model.predict(

        df

    )





    price = float(

        prediction[0]

    )









    # ===============================
    # SHAP
    # ===============================


    shap_values = explainer.shap_values(

        df

    )





    shap_result = []









    for feature, value in zip(

        feature_order,

        shap_values[0]

    ):


        shap_result.append(


            {


                "feature":

                    feature_name_map.get(

                        feature,

                        feature

                    ),


                "impact":

                    round(

                        float(value),

                        2

                    )

            }


        )





    shap_result = sorted(

        shap_result,

        key=lambda x:

            abs(

                x["impact"]

            ),

        reverse=True

    )[:5]


    # ======================================
    # SHAP 방향 추가
    # ======================================


    for item in shap_result:


        if item["impact"] >= 0:


            item["direction"] = "가격 상승 요인"

            item["icon"] = "📈"



        else:


            item["direction"] = "가격 하락 요인"

            item["icon"] = "📉"









    # ======================================
    # AI CONFIDENCE
    # ======================================


    confidence = 85





    if mileage < 50000:


        confidence += 5





    if vehicle_age <= 5:


        confidence += 5





    if confidence > 98:


        confidence = 98










    # ======================================
    # RETURN
    # ======================================


    return jsonify(

        {

            "price":

                round(
                    price,
                    2
                ),


            "brand":

                brand,


            "model":

                model_name,


            "year":

                year,


            "mileage":

                mileage,


            "fuel":

                vehicle["fuel_type"],


            "transmission":

                vehicle["transmission"],


            "engine":

                vehicle["engine_displacement"],


            "wheel":

                vehicle["wheel_system"],


            "shap":

                shap_result,


            "confidence":

                confidence

        }

    )





# ======================================
# RUN
# ======================================


if __name__ == "__main__":


    app.run(

        debug=True

    )



