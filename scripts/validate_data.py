import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Directory Setup
# Define base directory relative to this script (scripts/validate_data.py)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
REPORTS_DIR = os.path.join(DATA_DIR, "reports")
if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR)

def validate_repair_records():
    print("--- VALIDATING repair_records.csv ---")
    df = pd.read_csv(f"{DATA_DIR}/repair_records.csv")
    
    # 1. Basic Stats
    print(f"Total Records: {len(df)}")
    print(f"Missing Values: {df.isnull().sum().sum()}")
    
    # 2. Class Balance (Top 10 Faults)
    print("\nTop 10 most frequent Fault Codes:")
    print(df['fault_code'].value_counts()[:10])
    
    # 3. STATISTICAL CORRELATION (Crucial for ML)
    # Checking if specific sensors actually move with certain faults
    # Example: vibration for Motor/Engine faults
    print("\n--- STATISTICAL PATTERN VERIFICATION ---")
    
    # Average Vibration for "Vibration" related vs others
    vib_avg_all = df['sensor_vibration'].mean()
    vib_avg_vib_faults = df[df['fault_code'].str.contains('VIB|P03|UE|BRG', na=False)]['sensor_vibration'].mean()
    print(f"Global Avg Vibration: {vib_avg_all:.2f}")
    print(f"Avg Vibration for Vibration-related faults: {vib_avg_vib_faults:.2f} (Difference: {vib_avg_vib_faults - vib_avg_all:.2f})")
    
    # Average Temp for "Thermal" related vs others
    temp_avg_all = df['sensor_temp'].mean()
    temp_avg_thermal_faults = df[df['fault_code'].str.contains('TEM|HE|E6|HOT|P0118', na=False)]['sensor_temp'].mean()
    print(f"\nGlobal Avg Temp: {temp_avg_all:.2f}")
    print(f"Avg Temp for Thermal-related faults: {temp_avg_thermal_faults:.2f} (Difference: {temp_avg_thermal_faults - temp_avg_all:.2f})")
    
    # 4. Target distribution (Total Cost)
    print(f"\nAvg Total Cost: ${df['total_cost'].mean():.2f}")
    print(f"Cost Variance: {df['total_cost'].std():.2f}")

    # Generate a small summary CSV for validation
    summary = df.groupby('device_type').agg({
        'sensor_temp': 'mean',
        'sensor_vibration': 'mean',
        'total_cost': 'mean'
    }).reset_index()
    summary.to_csv(f"{REPORTS_DIR}/data_validation_summary.csv", index=False)
    print(f"\n✅ Validation Summary saved to {REPORTS_DIR}/data_validation_summary.csv")

if __name__ == "__main__":
    if os.path.exists(f"{DATA_DIR}/repair_records.csv"):
        validate_repair_records()
    else:
        print("❌ Error: repair_records.csv not found!")
