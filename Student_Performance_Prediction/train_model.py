from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "dataset" / "student_performance.csv"
MODEL_PATH = BASE_DIR / "model" / "student_model.joblib"
FEATURES = ["study_hours", "attendance", "previous_marks", "assignment_score", "sleep_hours"]
TARGET = "final_marks"

def train():
    df = pd.read_csv(DATA_PATH)
    X = df[FEATURES]
    y = df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model = RandomForestRegressor(
        n_estimators=180, max_depth=12, min_samples_leaf=2, random_state=42
    )
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5
    r2 = r2_score(y_test, predictions)
    MODEL_PATH.parent.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print("Model trained and saved successfully.")
    print(f"Test MAE : {mae:.2f}")
    print(f"Test RMSE: {rmse:.2f}")
    print(f"Test R2  : {r2:.3f}")
    return model

if __name__ == "__main__":
    train()
