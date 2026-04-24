# Product Support & Service Intelligence Platform

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lmudu2/ProductSupportPlatform/blob/main/Colab_Demo_Launcher.ipynb)
A diagnostic decision engine and procurement orchestrator for industrial, automotive, and consumer hardware. It uses a combination of telemetry anomaly detection, computer vision audits, and LLM-driven strategy to automate "Repair vs. Replace" decisions.

## Quick Start

### 1. Environment Setup
Clone the repository and initialize a virtual environment:
```bash
python -m venv venv
source venv/bin/bin/activate  # Or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Secrets Configuration
Create a `.env` file in the root directory and add your Groq API key:
```text
GROQ_API_KEY=your_key_here
```

### 3. Launch Dashboard
```bash
streamlit run main.py
```

## Internal Architecture

The logic is decoupled into several core modules:

- **`main.py`**: Principal Streamlit orchestration and UI state management.
- **`modules/inference_engine.py`**: The analytical core. Processes telemetry through XGBoost and Isolation Forest models for fault diagnosis and anomaly detection.
- **`modules/parts_manager.py`**: Handles OEM catalog indexing and supplier performance metrics (on-time delivery, defect rates, and active discounts).
- **`modules/vision_inspector.py`**: Leverages Llama-3 Vision to ground diagnostics in physical reality by detecting sector-specific hardware damage (e.g., hydraulic leaks or thermal stress).
- **`modules/ui_styles.py`**: Custom CSS injections for the premium dashboard interface.

## Strategic Decision Engine: Repair vs. Replace

The platform performs high-stakes arbitration between servicing an asset and procuring a replacement. The decision logic is weighted based on the hardware sector:

- **Business (Industrial/Automotive)**: Prioritizes **Speed (ETA)**. Minimal downtime is valued higher than direct service savings.
- **Household (Appliance/Mobile)**: Prioritizes **Total Landing Cost**. Savings are prioritized over turnaround time.

Arbitration is mathematically enforced using a "Dominance Rule": an upgrade is only recommended if it is strictly more economical or significantly faster than the repair path, adjusted for the sector's specific ROI drivers.

## Tech Stack

- **ML**: XGBoost, Isolation Forest, Scikit-learn
- **Generative AI**: Llama-3 (70b-versatile for strategy, 8b-instant for mapping)
- **UI**: Streamlit (Premium CSS)
- **Data**: Pandas, Numpy, Joblib
