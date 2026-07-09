import pandas as pd
import json
import os


# 프로젝트 루트 찾기
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# csv 위치
csv_path = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "used_cars_featured.csv"
)


# json 저장 위치
json_path = os.path.join(
    BASE_DIR,
    "data",
    "vehicle_info.json"
)



print("CSV PATH :", csv_path)



df = pd.read_csv(csv_path)



# 필요한 컬럼 확인
columns = [

    "make_name",
    "model_name",

    "fuel_type",
    "transmission",

    "body_type",

    "engine_displacement",
    "engine_cylinders",
    "engine_type",

    "wheel_system",

    "city_fuel_economy",
    "highway_fuel_economy"

]


df = df[columns]



vehicle_info = {}



for _, row in df.iterrows():

    brand = row["make_name"]

    model = row["model_name"]


    if brand not in vehicle_info:

        vehicle_info[brand] = {}



    if model not in vehicle_info[brand]:


        vehicle_info[brand][model] = {


            "make_name": brand,

            "model_name": model,


            "fuel_type":
                row["fuel_type"],


            "transmission":
                row["transmission"],


            "body_type":
                row["body_type"],



            "engine_displacement":
                row["engine_displacement"],


            "engine_cylinders":
                row["engine_cylinders"],


            "engine_type":
                row["engine_type"],


            "wheel_system":
                row["wheel_system"],



            "city_fuel_economy":
                row["city_fuel_economy"],


            "highway_fuel_economy":
                row["highway_fuel_economy"]

        }




with open(
    json_path,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        vehicle_info,
        f,
        ensure_ascii=False,
        indent=4
    )



print("vehicle_info.json 생성 완료")
print("차량 브랜드 개수 :", len(vehicle_info))