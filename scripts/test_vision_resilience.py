import sys
import os
import io

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))

try:
    from vision_inspector import VisionInspector
    from PIL import Image
    import numpy as np
except ImportError as e:
    print(f"FAILED: Import Error: {str(e)}")
    sys.exit(1)

def verify_bridge():
    print("\n--- GROQ VISION RESILIENCE AUDIT ---")
    
    # 1. Initialize Inspector
    try:
        inspector = VisionInspector()
        print(f"[STATUS] Resilient Bridge Initialized with {len(inspector.model_candidates)} candidates.")
    except Exception as e:
        print(f"FAILED: Initialization Error: {str(e)}")
        return

    # 2. Fabricate Test Frame (Synthetic Sensor)
    print("[ACTION] Fabricating synthetic test frame...")
    img = Image.fromarray(np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8))
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    image_bytes = img_byte_arr.getvalue()

    # 3. Execution (Failover Test)
    print("[ACTION] Executing Multimodal Handshake...")
    result = inspector.audit_hardware(image_bytes, "Synthetic Test Chip")
    
    if "Offline" in result:
        print(f"FAILED: {result}")
    else:
        print(f"SUCCESS: Vision Bridge Active.")
        print(f"--- Response Fragment ---\n{result[:150]}...")
    
    print("\n--- AUDIT COMPLETE ---")

if __name__ == "__main__":
    verify_bridge()
