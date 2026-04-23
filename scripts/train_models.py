import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_absolute_error
import xgboost as xgb
import joblib
import os

# Configuration paths and directory initialization
# Define base directory relative to this script (scripts/train_models.py)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")

if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)

def apply_feature_engineering(df):
    """
    Transforms raw telemetry into high-value physical signals.
    """
    # 1. Thermal Delta: Captures overheating differentials
    df['feat_thermal_delta'] = df['telemetry_temp'] - df['telemetry_coolant']
    
    # 2. Power Load Quotient: Captures electrical efficiency loss
    df['feat_power_draw'] = df['telemetry_current'] * df['telemetry_voltage']
    df['feat_power_per_load'] = df['feat_power_draw'] / (df['telemetry_load_pct'] + 1)
    
    # 3. Mechanical Harmonic Distortion: Vibration normalized by RPM
    df['feat_vib_per_rpm'] = df['telemetry_vibration'] / (df['telemetry_rpm'] + 1)
    
    # 4. Load/Pressure Correlation: Identifies leaks and blockages
    df['feat_p_load_ratio'] = df['telemetry_pressure'] / (df['telemetry_load_pct'] + 1)
    
    return df

def train_diagnosis_model(df):
    """
    Trains the multi-class gradient-boosted classifier for fault diagnosis.
    """
    print("Training Diagnostic Classifier (Boosted Engine)...")
    
    # Categorical Encoding
    le_device = LabelEncoder()
    df['device_type_enc'] = le_device.fit_transform(df['device_type'])
    
    le_fault = LabelEncoder()
    df['fault_code_enc'] = le_fault.fit_transform(df['fault_code'])
    
    # Feature Derivation
    df = apply_feature_engineering(df)
    
    # Define primary telemetry and derived features
    primary_telemetry = [
        'device_type_enc', 'telemetry_temp', 'telemetry_rpm', 'telemetry_voltage', 
        'telemetry_vibration', 'telemetry_load_pct', 'telemetry_pressure', 
        'telemetry_current', 'telemetry_freq', 'telemetry_o2', 
        'telemetry_battery', 'telemetry_coolant'
    ]
    derived_features = [
        'feat_thermal_delta', 'feat_power_draw', 'feat_power_per_load',
        'feat_vib_per_rpm', 'feat_p_load_ratio'
    ]
    
    feature_set = primary_telemetry + derived_features
    X = df[feature_set]
    y = df['fault_code_enc']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # XGBoost: Balanced for speed AND accuracy with 54 canonical fault classes
    diagnosis_clf = xgb.XGBClassifier(
        n_estimators=200,
        learning_rate=0.08,
        max_depth=7,
        subsample=0.8,
        colsample_bytree=0.8,
        objective='multi:softprob',
        num_class=len(le_fault.classes_),
        tree_method='hist',
        n_jobs=-1,
        random_state=42
    )
    
    diagnosis_clf.fit(X_train, y_train)
    
    # Evaluation metrics
    acc = accuracy_score(y_test, diagnosis_clf.predict(X_test))
    print(f"Diagnosis Engine Accuracy: {acc:.2%}")
    
    # Artifact Persistence
    joblib.dump(diagnosis_clf, f"{MODELS_DIR}/diagnosis_model.pkl")
    return le_device, le_fault

def train_cost_regressor(df, le_fault):
    """
    Trains the regressor for service cost estimations.
    """
    print("Training Service cost regressor...")
    df['fault_code_enc'] = le_fault.transform(df['fault_code'])
    
    X = df[['fault_code_enc', 'age_years', 'telemetry_load_pct']]
    y = df['total_service_cost']
    
    cost_reg = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1)
    cost_reg.fit(X, y)
    
    mae = mean_absolute_error(y, cost_reg.predict(X))
    print(f"Cost Mean Absolute Error: ${mae:.2f}")
    
    joblib.dump(cost_reg, f"{MODELS_DIR}/cost_model.pkl")

def train_anomaly_detector():
    """
    Trains the Isolation Forest for real-time telemetry anomaly detection.
    """
    print("Anomaly Detection (Isolation Forest) calibrated.")
    df_raw = pd.read_csv(f"{DATA_DIR}/sensor_readings.csv")
    
    anom_det = IsolationForest(contamination=0.05, random_state=42).fit(df_raw[['value']])
    print("[Instrumentation] Anomaly detection parameters calibrated.")
    
    joblib.dump(anom_det, f"{MODELS_DIR}/anomaly_model.pkl")

if __name__ == "__main__":
    archive_path = f"{DATA_DIR}/repair_records.csv"
    if not os.path.exists(archive_path):
        print(f"[Critical] Archive not found at {archive_path}")
    else:
        df_full = pd.read_csv(archive_path)
        
        # Comprehensive Training Pipeline
        le_dev, le_flt = train_diagnosis_model(df_full)
        train_cost_regressor(df_full, le_flt)
        train_anomaly_detector()
        
        # Encoder Persistence
        joblib.dump({'device_type': le_dev, 'fault_code': le_flt}, f"{MODELS_DIR}/encoders.pkl")
        print("All systems calibrated. Deployment artifacts archived in ./models/")
