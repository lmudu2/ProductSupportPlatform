import sys
import os
from pprint import pprint

# Ensure the modules directory is in path relative to this script
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.append(os.path.join(project_root, 'modules'))

from inference_engine import InferenceEngine, NarrativeGenerator

def verify_inference_bridge():
    """
    Simulates a live telemetry stream and verifies the 
    90.73% ML Engine and the Groq Narrative Layer.
    """
    print("--- INFERENCE BRIDGE VERIFICATION ---")
    
    # 1. Initialize Core Components
    try:
        engine = InferenceEngine()
        narrative = NarrativeGenerator()
    except Exception as e:
        print(f"FAILED: Initialization Error: {e}")
        return

    # 2. Mock Telemetry Payload (SR_000003 - Automotive Fault)
    telemetry_payload = {
        "device_type": "Automotive",
        "telemetry_temp": 108.4,
        "telemetry_rpm": 4185.0,
        "telemetry_voltage": 12.88,
        "telemetry_vibration": 4.0629,
        "telemetry_load_pct": 92.5,
        "telemetry_pressure": 158.26,
        "telemetry_current": 52.57,
        "telemetry_freq": 49.98,
        "telemetry_o2": 1.499,
        "telemetry_battery": 82.1,
        "telemetry_coolant": 63.45,
        "age_years": 12
    }

    print("\n[ACTION] Executing Diagnostic Vector Analysis...")
    
    # 3. ML Diagnostic
    results = engine.diagnose(telemetry_payload)
    
    print("\n--- ML Result: Top 3 Candidates ---")
    for res in results:
        print(f"[{res['fault_code']}] {res['description']}")
        print(f"   Confidence: {res['confidence']:.2%} | System: {res['system']} | Severity: {res['severity']}")

    # 4. Cost Estimation
    top_fault = results[0]['fault_code']
    cost_est = engine.estimate_cost(top_fault, telemetry_payload['age_years'], telemetry_payload['telemetry_load_pct'])
    print(f"\n[ECON] Projected Service Expenditure: ${cost_est}")

    # 5. Narrative Insight (Groq)
    print("\n[ACTION] Synthesizing Narrative Report (Groq/Llama-3)...")
    report = narrative.generate_report(results, telemetry_payload)
    
    print("\n--- Narrative Field Service Report ---")
    print(report)
    print("\n--- VERIFICATION COMPLETE ---")

if __name__ == "__main__":
    verify_inference_bridge()
