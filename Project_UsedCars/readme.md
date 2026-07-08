AI Used Car Price Prediction System

기능

가격 예측
가격에 영향을 준 요소 분석(SHAP)
비슷한 차량 추천
Flask 웹 서비스


used-car-ai/
│
├── data/
│   ├── raw/          # 원본 CSV
│   ├── processed/    # 전처리된 CSV
│
├── notebooks/        # EDA 분석(Jupyter)
│
├── src/
│   ├── preprocessing.py
│   ├── train.py
│   ├── predict.py
│   ├── explain.py
│
├── models/
│   ├── model.pkl
│   ├── encoder.pkl
│
├── web/
│   ├── app.py
│   ├── templates/
│   ├── static/
│
├── requirements.txt
└── README.md


## Experiment History

| Experiment | MAE | RMSE | R² |
|------------|-----:|------:|------:|
| Baseline | 3725 | 14040 | 0.6105 |
| Outlier Removal + EarlyStopping | 2924 | 4181 | 0.9214 |