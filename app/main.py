from fastapi import FastAPI
import time
import os

app = FastAPI(title="ML Prediction Service")

@app.get("/predict")
def predict(text: str):
    time.sleep(1)
    # Читаем версию из переменной окружения. Если её нет, берём "v1.0-local"
    version = os.getenv("APP_VERSION", "v4.0-rolling-update")
    return {
        "input_text": text,
        "prediction": "positive",
        "confidence": 0.95,
        "model_version": version
    }

@app.get("/health")
def health_check():
    # Читаем окружение и проверяем, передал ли K8s пароль
    env = os.getenv("APP_ENV", "unknown")
    pwd_status = "set" if os.getenv("DB_PASSWORD") else "missing"
    
    return {
        "status": "healthy", 
        "env": env, 
        "db_password_status": pwd_status
    }
