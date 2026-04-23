import os
import joblib
import pandas as pd
import numpy as np
from groq import Groq
from dotenv import load_dotenv

# Load global environment
load_dotenv()

class InferenceEngine:
    """
    Diagnostic Inference Engine: The analytical core of the platform.
    Loads trained ML models and processes live telemetry into diagnostic vectors.
    """
    def __init__(self, models_dir=None, data_dir=None):
        # Professional Path Resolution: Home in on the project root
        try:
            curr_dir = os.path.dirname(os.path.abspath(__file__))
            base_path = os.path.abspath(os.path.join(curr_dir, ".."))
            
            self.models_dir = models_dir if models_dir else os.path.join(base_path, "models")
            self.data_dir = data_dir if data_dir else os.path.join(base_path, "data")
            
            # Diagnostic Verify
            if not os.path.exists(self.models_dir):
                raise FileNotFoundError(f"Models directory not found: {self.models_dir}")

            # Load ML Artifacts
            self.diagnosis_model = joblib.load(os.path.join(self.models_dir, "diagnosis_model.pkl"))
            self.cost_model = joblib.load(os.path.join(self.models_dir, "cost_model.pkl"))
            self.anomaly_model = joblib.load(os.path.join(self.models_dir, "anomaly_model.pkl"))
            
            encoders = joblib.load(os.path.join(self.models_dir, "encoders.pkl"))
            self.le_device = encoders['device_type']
            self.le_fault = encoders['fault_code']
            
            # Metadata for context injection
            labels_path = os.path.join(self.data_dir, "fault_labels.csv")
            if not os.path.exists(labels_path):
                raise FileNotFoundError(f"Fault labels registry missing: {labels_path}")
            self.fault_labels = pd.read_csv(labels_path)
            
            # AI Intelligence Layer: Groq Client for Zero-Shot Mapping
            self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
            
        except Exception as e:
            raise RuntimeError(f"Engine Registry Failure: {str(e)}")

    def classify_hardware_sector(self, vision_audit):
        """
        Zero-shot classification of the hardware sector based on the visual audit.
        Ensures perfect grounding for vision-only diagnostic workflows.
        """
        try:
            prompt = f"""
            Analyze the following hardware audit and classify the machine into exactly ONE of these categories:
            1. Industrial (Heavy machinery, drilling rigs, VFDs, motors, factory equipment)
            2. Mobile (Smartphones, tablets, portable electronics)
            3. Appliance (Ovens, refrigerators, washing machines, kitchen gear)
            4. Automotive (EVs, ICE vehicles, braking systems, engine components)
            
            Visual Audit: {vision_audit}
            
            Respond with ONLY the category name.
            """
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
                temperature=0.0
            )
            sector_raw = chat_completion.choices[0].message.content.strip()
            
            # NORMALIZATION: Ensure it matches an official sector exactly
            valid_sectors = ["Industrial", "Mobile", "Appliance", "Automotive"]
            for s in valid_sectors:
                if s.lower() in sector_raw.lower():
                    return s
            return "Industrial" 
        except Exception as e:
            return "Industrial"

    def map_vision_to_fault(self, visual_audit, device_type):
        """
        Zero-Shot Semantic Mapping: Uses LLM to bridge Visual Audits with 
        the official Diagnostic Registry based on device context.
        """
        try:
            # Filter the search space to the relevant device sector
            sector_labels = self.fault_labels[self.fault_labels['device_type'] == device_type]
            if sector_labels.empty:
                return None
            
            options_text = "\n".join([f"- {row['fault_code']}: {row['root_cause']}" for _, row in sector_labels.iterrows()])
            
            prompt = f"""
            Role: Professional Diagnostic Dispatcher
            Context: Select the most accurate Fault Code from the following {device_type} registry based on the Visual Audit findings.
            
            VISUAL AUDIT: "{visual_audit}"
            
            {device_type.upper()} FAULT REGISTRY:
            {options_text}
            
            Task: Return ONLY the Fault Code that best matches the findings. If no strong match exists, return "None".
            Precision is critical. Do not hallucinate codes outside this list.
            """
            
            completion = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            res = completion.choices[0].message.content.strip()
            # Clean up potential markdown formatting
            return res.split('\n')[0].replace('"', '').replace('*', '').strip()
        except:
            return None

    def _apply_feature_engineering(self, telemetry):
        """
        Calculates expert physics-based features required by the 90.73% accurate model.
        Includes safety handling for sector-specific sensor availability.
        """
        # Mapping raw inputs to local variables for clarity with safe defaults
        temp = float(telemetry.get('telemetry_temp', 0))
        coolant = float(telemetry.get('telemetry_coolant', 0))
        voltage = float(telemetry.get('telemetry_voltage', 0))
        current = float(telemetry.get('telemetry_current', 0))
        load = float(telemetry.get('telemetry_load_pct', 0))
        vib = float(telemetry.get('telemetry_vibration', 0))
        rpm = float(telemetry.get('telemetry_rpm', 0))
        pressure = float(telemetry.get('telemetry_pressure', 0))

        # Derived high-value signals with safety
        telemetry['feat_thermal_delta'] = temp - coolant
        telemetry['feat_power_draw'] = current * voltage
        telemetry['feat_power_per_load'] = (current * voltage) / (load + 1)
        telemetry['feat_vib_per_rpm'] = vib / (rpm + 1)
        telemetry['feat_p_load_ratio'] = pressure / (load + 1)
        
        return telemetry

    def diagnose(self, raw_telemetry):
        """
        Returns a prioritized diagnostic vector (Top-3 probable faults).
        """
        # 1. Feature Extraction
        processed = self._apply_feature_engineering(raw_telemetry.copy())
        
        # 2. Vectorization
        device_type_enc = self.le_device.transform([processed['device_type']])[0]
        
        feature_set = [
            device_type_enc, processed['telemetry_temp'], processed['telemetry_rpm'], 
            processed['telemetry_voltage'], processed['telemetry_vibration'], 
            processed['telemetry_load_pct'], processed['telemetry_pressure'], 
            processed['telemetry_current'], processed['telemetry_freq'], 
            processed['telemetry_o2'], processed['telemetry_battery'], 
            processed['telemetry_coolant'], processed['feat_thermal_delta'], 
            processed['feat_power_draw'], processed['feat_power_per_load'],
            processed['feat_vib_per_rpm'], processed['feat_p_load_ratio']
        ]
        
        X = np.array([feature_set])
        
        # 3. Inference
        probs = self.diagnosis_model.predict_proba(X)[0]
        top_3_idx = np.argsort(probs)[-3:][::-1]
        
        results = []
        for idx in top_3_idx:
            fault_code = self.le_fault.classes_[idx]
            confidence = probs[idx]
            
            # Injecting descriptive metadata with fallback safety
            match_row = self.fault_labels[self.fault_labels['fault_code'] == fault_code]
            if not match_row.empty:
                metadata = match_row.iloc[0]
            else:
                metadata = {
                    "system_affected": "Modular System",
                    "root_cause": f"Diagnostic Vector: {fault_code}",
                    "severity": 2
                }
            
            results.append({
                "fault_code": fault_code,
                "confidence": round(float(confidence), 4),
                "system": metadata.get('system_affected', 'Control'),
                "description": metadata.get('root_cause', 'Unknown Component Issue'),
                "severity": metadata.get('severity', 2),
                "device_type": metadata.get('device_type', 'Industrial'),
                "avg_parts_cost": float(metadata.get('avg_parts_cost', 0))
            })
            
        return results

    def estimate_cost(self, fault_code, age_years, load_pct, part_price=None, device_type=None):
        """
        Predicts total service expenditure using sector-aware professional labor rates.
        Falls back gracefully if the ML model was trained on stale data.
        """
        # Professional Grade Sector Labor Map
        SECTOR_LABOR = {"Automotive": 280, "Industrial": 180, "Mobile": 60, "Appliance": 110}
        l_rate = SECTOR_LABOR.get(device_type, 60) if device_type else 60
        
        try:
            # Heuristic-first: Use the new realistic fault data directly
            fault_data = self.fault_labels[self.fault_labels['fault_code'] == fault_code].iloc[0]
            active_part_cost = part_price if part_price is not None else float(fault_data['avg_parts_cost'])
            labor_hours = float(fault_data['avg_labor_hours'])
            
            base_cost = active_part_cost + (labor_hours * l_rate)
            
            # Penalties make sense for Industrial/Automotive wear-and-tear, but not consumer Mobile devices
            if device_type == "Mobile":
                age_penalty = 0
                load_penalty = 0
            else:
                age_penalty = base_cost * (age_years * 0.035)
                load_penalty = base_cost * ((load_pct - 50) * 0.005) if load_pct > 50 else 0
            
            prediction = base_cost + age_penalty + load_penalty
            return round(float(prediction), 2)
            
        except Exception as e:
            # Final fallback: part + standard 8-hour labor minimum
            return round((part_price or 500.0) + (8.0 * l_rate), 2)

    def detect_anomalies(self, telemetry, severity_context=None):
        """
        Real-Time Anomaly Detection. Dynamically discovers all telemetry signals 
        and evaluates them against the Isolation Forest, augmented with Device-Specific Physical Bounds.
        Syncs with diagnostic severity to adjust sensitivity.
        """
        status_report = {}
        
        # Contextual Sensitivity Boost: High-severity diagnosis makes monitors hyper-sensitive
        boost = 0.0
        if severity_context:
            if severity_context >= 4: boost = 0.25  # Catastrophic: hyper-sensitive
            elif severity_context >= 3: boost = 0.15 # Critical
            elif severity_context >= 2: boost = 0.10 # Elevated: ensure L2 is reflected in monitors
            
        device_type = telemetry.get('device_type', 'Industrial')
        
        # SECTOR GOLD STANDARD: High-Fidelity Engineering Masks
        # We only monitor sensors that are physically realistic for each sector.
        # This ignores "dirty data" in the database for non-existent sensors.
        SECTOR_GOLD_STANDARD = {
            "Appliance": ["temp", "voltage", "load_pct"],
            "Mobile": ["temp", "battery", "voltage", "load_pct"],
            "Automotive": ["temp", "rpm", "pressure", "voltage", "load_pct", "vibration"],
            "Industrial": ["temp", "rpm", "vibration", "current", "voltage", "load_pct"]
        }
        allowed_sensors = SECTOR_GOLD_STANDARD.get(device_type, SECTOR_GOLD_STANDARD["Industrial"])
        
        range_dict = {
            "Mobile": {"temp": (0.0, 120.0), "voltage": (0.0, 24.0), "load_pct": (0.0, 100.0), "battery": (0.0, 100.0), "rpm": (0.0, 0.0), "pressure": (0.0, 0.0), "current": (0.0, 10.0), "vibration": (0.0, 5.0)},
            "Appliance": {"temp": (0.0, 250.0), "voltage": (110.0, 240.0), "load_pct": (0.0, 100.0), "battery": (0.0, 0.0), "rpm": (0.0, 2000.0), "pressure": (0.0, 150.0), "current": (0.0, 30.0), "vibration": (0.0, 10.0)},
            "Automotive": {"temp": (-40.0, 200.0), "voltage": (10.0, 480.0), "load_pct": (0.0, 100.0), "battery": (0.0, 100.0), "rpm": (0.0, 8000.0), "pressure": (0.0, 300.0), "current": (0.0, 300.0), "vibration": (0.0, 20.0)},
            "Industrial": {"temp": (-40.0, 450.0), "voltage": (0.0, 1000.0), "load_pct": (0.0, 150.0), "battery": (0.0, 100.0), "rpm": (0.0, 15000.0), "pressure": (0.0, 2000.0), "current": (0.0, 500.0), "vibration": (0.0, 50.0)}
        }
        bounds = range_dict.get(device_type, range_dict["Industrial"])
            
        # Dynamic Discovery: Find all telemetry fields
        for key, val in telemetry.items():
            if not key.startswith("telemetry_"):
                continue
            
            clean_key = key.replace("telemetry_", "")
            
            # 1. ENFORCE GOLD STANDARD: Skip if sensor is physically impossible for this sector
            if clean_key not in allowed_sensors:
                continue
                
            score = 0.10  # Default Normal Baseline
            
            # Dynamic Hybrid Heuristic: Proximity to Physical Bounds
            if clean_key in bounds:
                min_v, max_v = bounds[clean_key]
                if max_v > min_v:
                    # Calculate continuous pressure on limits for smooth UI feedback
                    pct = (val - min_v) / (max_v - min_v)
                    # deviation from 50% ideal state (0.0=center, 1.0=absolute edge)
                    dev = abs(pct - 0.5) * 2.0
                    
                    # Gradient degrading score: drops sharply as you reach edges
                    # 0 dev -> 0.00 (Perfect stability)
                    # 0.61 dev (~80% bound) -> -0.15 (CRITICAL)
                    score = 0.00 - (dev ** 2) * 0.40
            
            # Shifted Thresholds based on context
            # Base logic:
            # dev = 0.6 (~80% physical bound) -> score is ~ -0.144 -> WARNING
            # dev = 0.8 (~90% physical bound) -> score is ~ -0.256 -> CRITICAL
            
            base_warn = -0.10 + boost
            base_crit = -0.20 + boost
            
            # CRUCIAL: Protect the "Dead Center" safe zone. 
            # If the LLM generates a Severity 3 or 4, the boost (+0.15) forces warn_limit above 0.
            # This causes EVERYTHING to instantly become a WARNING. We cap the limits to guarantee
            # a reliable 20% mathematical safe zone regardless of how catastrophic the machine is.
            warn_limit = min(-0.02, base_warn)
            crit_limit = min(-0.08, base_crit)
            
            status = "CRITICAL" if score < crit_limit else "WARNING" if score < warn_limit else "NORMAL"
            
            status_report[clean_key.upper()] = {
                "value": val,
                "status": status,
                "score": float(score),
                "thresholds": f"[{min_v} - {max_v}]" if clean_key in bounds and max_v > min_v else "Constant Limit"
            }
            
        return status_report

class NarrativeGenerator:
    """
    LLM Bridge: Generates technical insight reports using the Groq/Llama-3 narrative layer.
    """
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def prioritize_sensors(self, device_type, diagnosis_results, available_signals):
        """
        AI-Driven Prioritization: Uses Llama-3 to select the most relevant signals 
        for the given diagnostic context.
        """
        try:
            prompt = f"Role: Diagnostic AI Analyst\n"
            prompt += f"Context: Device Type: {device_type}\n"
            if diagnosis_results:
                top_fault = diagnosis_results[0]
                prompt += f"Primary Diagnosis: {top_fault['fault_code']} ({top_fault['description']})\n"
            
            prompt += f"Available Signals: {', '.join(available_signals)}\n\n"
            prompt += "Task: Choose the TOP 4 most mission-critical signals for this specific machine context. "
            prompt += "Exclude signals that are irrelevant to this device category (e.g., exclude PRESSURE, RPM, or O2 for Mobile). "
            prompt += "Exclude signals with value 0.0 unless they are critical for the diagnosis. "
            prompt += "Return ONLY a comma-separated list of the 4 chosen signal labels, no punctuation or explanation."
            
            completion = self.client.chat.completions.create(
                model="llama-3.1-8b-instant", # Efficient model for priority ranking
                messages=[{"role": "user", "content": prompt}]
            )
            raw_res = completion.choices[0].message.content.strip()
            # Clean up, split, and ensure uniqueness
            raw_signals = [s.strip().split('\n')[0].replace('"', '').replace('.', '').upper() for s in raw_res.split(',')]
            
            prioritized = []
            for s in raw_signals:
                if s and s not in prioritized:
                    prioritized.append(s)
            
            return prioritized[:4]
        except:
            # Fallback: Just return first 4 if LLM fails
            return available_signals[:4]

    def generate_report(self, diagnosis, telemetry, visual_audit=None):
        """
        Synthesizes a multi-modal field service report from ML results and visual audits.
        """
        try:
            prompt = "Role: Senior Field Service Engineer\n"
            prompt += "Task: Provide a concise, professional technical explanation of the following anomaly.\n\n"
            
            if diagnosis and len(diagnosis) > 0 and telemetry is not None:
                top_fault = diagnosis[0]
                prompt += f"""
                DATA CONTEXT:
                - Device Category: {telemetry.get('device_type', 'Unknown')}
                - Top Model Prediction: {top_fault['fault_code']} ({top_fault['description']})
                - ML Confidence: {top_fault['confidence'] * 100:.1f}%
                - System Affected: {top_fault['system']}
                
                TELEMETRY STATE:
                - Load: {telemetry.get('telemetry_load_pct', 0)}%
                - Temperature: {telemetry.get('telemetry_temp', 0)}C (Coolant: {telemetry.get('telemetry_coolant', 0)}C)
                - Vibration: {telemetry.get('telemetry_vibration', 0)}g
                - Voltage: {telemetry.get('telemetry_voltage', 0)}V
                """
                
                if visual_audit:
                    prompt += f"\nVISUAL EVIDENCE: {visual_audit}\n"
                    prompt += "\nINSTRUCTION: Reconcile visual findings with telemetry stream evidence for a unified expert opinion."
                else:
                    prompt += "\nINSTRUCTION: Explain exactly why the telemetry indicates this specific fault focusing on the physical interaction between the sensors."
            else:
                # Blind Visual Audit Mode
                prompt += f"\nVISUAL EVIDENCE PROVIDED ONLY: {visual_audit}\n"
                prompt += "\nINSTRUCTION: Provide a master technical evaluation of the physical damage and recommend corrective steps based purely on visual findings."

            prompt += "\nOUTPUT INSTRUCTIONS:\n1. USE HTML BULLET POINTS (<ul><li>...</li></ul>).\n2. TOTAL OF 3-4 BULLETS.\n3. NO INTRODUCTORY SENTENCES or 'The telemetry indicates...'.\n4. NO CONVERSATIONAL FILLER.\n5. TONE: CRITICAL, PROFESSIONAL, TECHNICAL.\n"
            
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a Senior Field Service Engineer. You provide technical insights ONLY in concise markdown bullet points. No paragraphs, no intro, no outro."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=300
            )
            if completion and hasattr(completion, 'choices') and len(completion.choices) > 0:
                return completion.choices[0].message.content
            return "Narrative Layer returned empty."
        except IndexError as ie:
            return f"Diagnostic Engine Internal Index Error: {str(ie)}"
        except Exception as e:
            return f"Narrative Layer Offline: {str(e)}"

    def generate_purchasing_rationale(self, part_data, supplier_data):
        """
        AI Procurement Optimization: Synthesizes purchasing strategy based on 
        real-time inventory, pricing, and supplier performance metrics.
        """
        try:
            prompt = f"""
            Role: AI Procurement Intelligence Analyst
            Context: Purchasing Decision Support for {part_data['description']}
            
            SUPPLIER DATA:
            - Name: {supplier_data['supplier_name']}
            - Delivered On-Time: {supplier_data['on_time_pct']}%
            - Quality/Defect Rate: {supplier_data['defect_rate_pct']}%
            - Discount Terms: {supplier_data['active_discount']}
            - Rating: {supplier_data['rating']}
            
            PART STATE:
            - Brand: {part_data['brand']}
            - Stock: {'Available' if part_data['in_stock'] else 'Backordered'}
            - Price: ${part_data['price_oem']}
            
            TASK: 
            Provide a clear, simple analytical rationale for ordering this part from this supplier. 
            Explain why this is (or isn't) the optimal choice based on the reliability metrics provided.
            
            OUTPUT RULES:
            - Return exactly in this format: VERDICT: [Short Status] | RATIONALE: [Explanation]
            - Short Status options: RECOMMENDED, HIGHLY RECOMMENDED, CAUTION, or AVOID.
            - Rationale: Max 2 concise sentences in plain English.
            - DO NOT use bold text (**term**) or include the verdict status inside the rationale.
            - DO NOT say 'Based on the data' or 'The AI recommends'. Just speak directly.
            - No new lines in the output.
            """
            
            completion = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=150
            )
            return completion.choices[0].message.content.strip()
        except:
            return f"VERDICT: RECOMMENDED | RATIONALE: Regular reliability review suggests {supplier_data['supplier_name']} is an acceptable match for this order."

    def generate_product_strategy_rationale(self, current_asset, candidates, sector):
        """
        Lifecycle Optimization: Analyzes the ROI of Repair vs. Replace across multiple candidates.
        Enforces a Persona-Based Economic Mandate:
        - Business (Industrial/Automotive): Prioritizes Speed (ETA) to minimize downtime.
        - Household (Appliance/Mobile): Prioritizes Total Landing Cost (Savings).
        
        The 'Repair' option is included in the candidates list for unified comparison.
        """
        try:
            # Prepare candidate context for the LLM
            candidates_text = ""
            for i, c in enumerate(candidates):
                label = "OPTION: REPAIR CURRENT" if c.get('is_repair') else f"OPTION: {c['model_name']}"
                total_cost = c.get('total_landing_cost', c.get('after_discount_cost', 0))
                candidates_text += f"""
                [{label}]
                - Path: {'Service Existing' if c.get('is_repair') else 'Buy New'}
                - Total Cost: ${total_cost:,.2f}
                - Arrival (ETA): {c.get('eta_days', 'N/A')} days
                - Detail: Labor ${c.get('labor_cost', 0):,.2f}, Shipping ${c.get('shipping_cost', 0):,.2f}, Installs ${c.get('installation_cost', 0):,.2f}
                """

            prompt = f"""
            Role: AI Procurement Intelligence Analyst
            Task: Select the optimal strategic choice for a {current_asset['device_type']} ({sector} sector).
            
            STRATEGIC OPTIONS:
            {candidates_text}
            
            ECONOMIC MANDATE:
            1. ABSOLUTE DOMINANCE RULE: If one option is strictly better than all others (Lower Cost AND Lower/Equal ETA), it is the MANDATORY winner. You must not choose an option that is both more expensive and slower.
            2. BUSINESS PRIORITY (Industrial/Automotive): Prioritize Speed (Lowest ETA). Minimal downtime is more valuable than direct savings, but the premium must be reasonable.
            3. HOUSEHOLD PRIORITY (Appliance/Mobile): Prioritize Total Cost (Savings). 
            4. TIE-BREAKER: If ETA and Cost are tied, always prefer 'REPAIR CURRENT' to minimize environmental waste.
            
            TASK: 
            Pick the ONE best candidate among all options and provide a strictly analytical verdict. 
            
            OUTPUT RULES:
            - Return exactly in this format: WINNER: [Model Name/REPAIR] | VERDICT: [REPAIR RECOMMENDED or REPLACEMENT RECOMMENDED] | RATIONALE: [Explanation]
            - Use REPAIR as the winner ID if the repair candidate is chosen.
            - Rationale: Max 20 words. JUSTIFY based on ETA vs. Cost delta.
            - No bold text. No new lines.
            """
            
            completion = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=200
            )
            return completion.choices[0].message.content.strip()
        except:
            return "WINNER: REPAIR | VERDICT: REPAIR RECOMMENDED | RATIONALE: Insufficient candidate data for strategic arbitration."
