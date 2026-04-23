import streamlit as st
import pandas as pd
import sys
import os
import plotly.express as px

# Internal Path Architecture
sys.path.append(os.path.join(os.getcwd(), 'modules'))

from ui_styles import apply_premium_styles, header_component
from inference_engine import InferenceEngine, NarrativeGenerator
from vision_inspector import VisionInspector
from parts_manager import PartsManager

# 1. Platform Initialization
st.set_page_config(
    page_title="Product Support & Service Intelligence Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_premium_styles()

@st.cache_resource(show_spinner="Syncing Global Intelligence Registry...")
def load_industrial_intelligence_v4():
    """
    Core Registry: Synchronizes ML Models, LLM Narrators, and Vision Audits.
    v4.4: Enforcing Strict Semantic Hardware Grouping.
    """
    # RESET CACHE: Ensure new logistics methods are registered
    return (InferenceEngine(), NarrativeGenerator(), 
            VisionInspector(), PartsManager())

@st.cache_data(show_spinner="Loading Historical Archive...", ttl=0)
def load_archive_data():
    """Nuclear Reset: Ensures archive is read fresh from disk."""
    return pd.read_csv("./data/repair_records.csv")

# Ensure we have fresh instances
engine, narrative_layer, vision_auditor, parts_pro = load_industrial_intelligence_v4()
archive = load_archive_data()

# SYNC: Force global reload if files were updated
if st.sidebar.button("🔄 Sync Global Realism Registry"):
    st.cache_resource.clear()
    st.cache_data.clear()
    st.rerun()

# 2. Shared Data Layer
if 'last_results' not in st.session_state: st.session_state.last_results = None
if 'archive_results' not in st.session_state: st.session_state.archive_results = None
if 'live_results' not in st.session_state: st.session_state.live_results = None
if 'vision_results' not in st.session_state: st.session_state.vision_results = None
if 'live_telemetry_cache' not in st.session_state: st.session_state.live_telemetry_cache = None

# 3. Main Dashboard Architecture
with st.sidebar:
    st.markdown("""
<div style="background: var(--primary-soft); border-radius: 16px; padding: 1.5rem; border: 1px solid var(--border);">
<div style="font-family: 'Outfit'; font-size: 0.9rem; font-weight: 700; color: var(--primary); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 1.2rem;">Intelligence Legend</div>
<div style="margin-bottom: 1.2rem;">
<div style="font-size: 0.65rem; font-weight: 800; color: var(--secondary); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">📡 01: Multi-Modal Ingest</div>
<div style="font-size: 0.8rem; color: var(--text-main); font-weight: 500; line-height: 1.4;">Real-time telemetry streams combined with computer vision hardware audits.</div>
</div>
<div style="margin-bottom: 1.2rem;">
<div style="font-size: 0.65rem; font-weight: 800; color: var(--secondary); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">🧠 02: ML Inference</div>
<div style="font-size: 0.8rem; color: var(--text-main); font-weight: 500; line-height: 1.4;">Isolation Forest anomaly detection & XGBoost cost prediction engines.</div>
</div>
<div style="margin-bottom: 1.2rem;">
<div style="font-size: 0.65rem; font-weight: 800; color: var(--secondary); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">📟 03: Live Monitoring</div>
<div style="font-size: 0.8rem; color: var(--text-main); font-weight: 500; line-height: 1.4;">AI-prioritized signal tracking adapted to specific device domains.</div>
</div>
<div style="margin-bottom: 1.5rem;">
<div style="font-size: 0.65rem; font-weight: 800; color: var(--secondary); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">📦 04: Logistics Sync</div>
<div style="font-size: 0.8rem; color: var(--text-main); font-weight: 500; line-height: 1.4;">OEM catalog cross-referencing & automated procurement workflows.</div>
</div>
<div style="margin-top: 2rem; padding-top: 1rem; border-top: 1px solid rgba(0,0,0,0.05);">
<div style="display: flex; align-items: center; gap: 10px;">
<div style="width: 8px; height: 8px; background: #10B981; border-radius: 50%; box-shadow: 0 0 10px #10B981;"></div>
<div style="font-size: 0.7rem; font-weight: 700; color: var(--accent); text-transform: uppercase;">Engine Operational</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

header_component()

def run_diagnostics(telemetry, uploaded_file):
    img_bytes = uploaded_file.getvalue() if uploaded_file else None
    results = []
    cost = 0.0
    visual_audit = None
    final_report = ""
    device_context = None

    d_context = "Industrial" 
    
    if not img_bytes:
        results = engine.diagnose(telemetry)
    
    if img_bytes:
        # 1. Sector Grounding: Vision AI identifies the hardware domain directly
        visual_audit = vision_auditor.audit_hardware(img_bytes, """
        1. CLASSIFY THE HARDWARE SECTOR: You MUST identify the object and start your response with exactly one of these tags:
           - [SECTOR: Industrial] (For heavy machinery, drills, factory gear)
           - [SECTOR: Mobile] (For smartphones, tablets, handheld consumer electronics)
           - [SECTOR: Appliance] (For ovens, washers, kitchen/home equipment)
           - [SECTOR: Automotive] (For engine bays, car parts, EV components)
           THIS TAG MUST BE THE FIRST LINE OF YOUR RESPONSE.
        
        2. Identify visible anomalies: Corrosion, fluid leaks, structural cracks, thermal discoloration.
        3. Assess component integrity: Surface wear patterns and connection stability.
        4. Tone: Professional, precise, minimalist.
        """)
        
        # Extraction with Hybrid Keyword Fallback
        import re
        s_match = re.search(r'\[SECTOR:\s*(.*?)\]', visual_audit)
        d_context = s_match.group(1).strip().title() if s_match else None
        
        if not d_context:
            v_lower = visual_audit.lower()[:200]
            if any(k in v_lower for k in ["smart", "phone", "mobile", "tablet", "screen"]): d_context = "Mobile"
            elif any(k in v_lower for k in ["oven", "washer", "kitchen", "appliance", "grill"]): d_context = "Appliance"
            elif any(k in v_lower for k in ["engine", "car", "auto", "vehicle", "suspension"]): d_context = "Automotive"
            else: d_context = "Industrial"
        
        st.markdown(f'<div style="font-size: 0.7rem; color: var(--secondary); font-weight: 700; margin-bottom: 1rem; text-transform: uppercase;">Autonomous Grounding: {d_context} Identified</div>', unsafe_allow_html=True)
        
        f_code = engine.map_vision_to_fault(visual_audit, d_context)
        
        if not f_code or f_code == "None":
            if d_context == "Mobile": f_code = "ERR_DISP_BRK"
            elif d_context == "Appliance": f_code = "ERR_APP_CORE"
            elif d_context == "Automotive": f_code = "P0455"
            else: f_code = "ERR_IND_HYD_L"
        
        match_row = engine.fault_labels[engine.fault_labels['fault_code'].str.strip() == f_code.strip()]
        if not match_row.empty:
            meta = match_row.iloc[0].to_dict()
            results = [{
                "fault_code": f_code, "confidence": 0.88,
                "system": meta.get('system_affected', 'General'),
                "description": meta.get('root_cause', 'Sector-Detect Hardware Anomaly'),
                "severity": meta.get('severity', 2),
                "device_type": d_context, "avg_parts_cost": meta.get('avg_parts_cost', 0)
            }]
        device_context = d_context

    if not results and (img_bytes or telemetry):
        d_type = device_context or "Industrial"
        f_code = "ERR_DISP_BRK" if d_type == "Mobile" else "ERR_IND_HYD_L" if d_type == "Industrial" else "ERR_APP_CORE" if d_type == "Appliance" else "P0455"
        
        match_row = engine.fault_labels[engine.fault_labels['fault_code'] == f_code]
        meta = match_row.iloc[0].to_dict() if not match_row.empty else {"system_affected": "General", "root_cause": f"Standard {d_type} System Audit", "severity": 2, "avg_parts_cost": 250.0}

        results = [{
            "fault_code": f_code, "confidence": 0.75,
            "system": meta.get('system_affected', 'General'), 
            "description": meta.get('root_cause', f"Standard {d_type} System Audit Required"),
            "severity": meta.get('severity', 2), "device_type": d_type, 
            "avg_parts_cost": meta.get('avg_parts_cost', 250.0)
        }]

    recommended_part = None
    if results:
        d_type = results[0].get('device_type', 'Industrial')
        catalog = parts_pro.catalog[parts_pro.catalog['device_type'] == d_type].copy()
        if not catalog.empty:
            sys_match = results[0]['system']
            f_desc = results[0]['description'].lower()
            target_price = results[0].get('avg_parts_cost', 0)
            
            system_parts = catalog[catalog['system'] == sys_match].copy()
            if system_parts.empty: system_parts = catalog.copy()
            
            system_parts['price_diff'] = (system_parts['price_oem'] - target_price).abs()
            recommended_part = system_parts.sort_values('price_diff').iloc[0].to_dict()
    
    if results:
        p_price = recommended_part['price_oem'] if recommended_part else 0.0
        d_type_for_cost = results[0].get('device_type', d_context)
        age_val = telemetry['age_years'] if telemetry else 5
        load_val = telemetry['telemetry_load_pct'] if telemetry else 50
        try:
            cost = engine.estimate_cost(
                results[0]['fault_code'], age_val, load_val,
                part_price=p_price, device_type=d_type_for_cost
            )
        except Exception as io_err:
            l_rate = {"Industrial": 180, "Mobile": 60, "Appliance": 110, "Automotive": 280}.get(d_type_for_cost, 60)
            cost = p_price + (8.0 * l_rate)
        
        cost = max(cost, p_price + 100)
    
    final_report = narrative_layer.generate_report(results, telemetry, visual_audit)
    
    return {
        "results": results, "cost": cost, "report": final_report, 
        "vision_insight": visual_audit, "recommended_part": recommended_part
    }

# --- MODULE C: GLOBAL FLEET INTELLIGENCE (Landing Mode) ---



@st.cache_data(show_spinner=False)
def get_priority_sensors(device_type, lr_results, avail_keys):
    # Pass a tuple to make it hashable for cache
    return narrative_layer.prioritize_sensors(device_type, lr_results, list(avail_keys))

def render_dashboard(lr, telemetry, uploaded_file, show_monitors=False, tab_id="archive"):
    """
    Unified Asset Dashboard.
    Now includes Strategic Portfolio Analysis (Product Level) and 
    Operational Logistics (Part Level).
    """

    # --- MODULE C: LIVE PHYSICS SIMULATOR & ASYNCHRONOUS MONITORING ---
    st.markdown('<div class="zone-header" style="margin-top: 1rem;">Predictive Intelligence</div>', unsafe_allow_html=True)

    if telemetry and show_monitors:
        
        # SYNC: Resolve severity for monitor sensitivity logic
        lr_data = lr or {}
        severity = lr_data['results'][0]['severity'] if lr_data.get('results') else 1
        
        anomalies = engine.detect_anomalies(telemetry, severity_context=severity)
        
        # AI-Driven Prioritization: LLM selects keys from available sensors
        avail_keys = list(anomalies.keys())
        
        priority_keys = get_priority_sensors(
            telemetry['device_type'], 
            lr_data.get('results', []), 
            avail_keys
        )
        
        # Normalize keys and filter
        top_sensors = {k.upper(): anomalies[k.upper()] for k in priority_keys if k.upper() in anomalies}
        # Fallback to first 4 if AI fails or returns empty
        if not top_sensors:
            top_sensors = dict(list(anomalies.items())[:4])
        
        sensor_name_map = {
            "TEMP": "Core Temperature",
            "VOLTAGE": "Voltage Supply",
            "LOAD_PCT": "System Load",
            "BATTERY": "Battery Life",
            "RPM": "Motor RPM",
            "PRESSURE": "Hydraulic Pressure",
            "CURRENT": "Amperage Draw",
            "VIBRATION": "Vibration Index",
            "FREQ": "Operating Frequency",
            "O2": "Oxygen Level",
            "COOLANT": "Coolant Pressure"
        }
        
        priority_labels = [sensor_name_map.get(k, k) for k in top_sensors.keys()]
        st.markdown(f'<div style="font-size: 0.65rem; color: var(--secondary); font-weight: 700; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 0.05em;">AI Monitor Priority: {", ".join(priority_labels)}</div>', unsafe_allow_html=True)
        
        mon_cols = st.columns(4)
        for i, (sensor, data) in enumerate(top_sensors.items()):
            display_name = sensor_name_map.get(sensor, sensor)
            status = data['status']
            score = data.get('score', 0.0)
            status_color = "#EF4444" if status == "CRITICAL" else "#F59E0B" if status == "WARNING" else "#10B981"
            
            # PROPORTIONAL STABILITY: Integrates individual signal score with global system severity
            base_stability = 100 + (score * 200)
            sev_reduction = (severity - 1) * 15 if severity else 0
            stability = max(0, min(100, base_stability - sev_reduction))
            
            mon_cols[i % 4].markdown(f"""
            <div class="metric-card" style="border-top: 4px solid {status_color};">
                <div class="metric-label">{display_name}</div>
                <div style="font-size: 1.8rem; font-weight: 800; margin: 0.5rem 0; color: {status_color};">{status}</div>
                <div style="font-size: 0.75rem; font-weight: 700; color: var(--secondary);">STABILITY: {stability:.1f}%</div>
                <div style="font-size: 0.65rem; font-weight: 600; color: #9CA3AF; margin-top: 4px; border-top: 1px dashed #E5E7EB; padding-top: 4px;">OPERATING BOUNDS: {data.get("thresholds", "[N/A]")}</div>
            </div>
            """, unsafe_allow_html=True)
    



    # --- MODULE B: PREDICTIVE INTELLIGENCE ---
    if lr:
        
        # 1. Health & Economic KPI Row (Standardized Miniature Tiles)
        k1, k2, k3 = st.columns(3)
        top_confidence = lr['results'][0]['confidence'] if lr['results'] else 0.85
        top_severity = lr['results'][0]['severity'] if lr['results'] else 2
        
        with k1:
            st.markdown(f"""
                <div class="metric-card" style="padding: 1rem; min-height: 140px;">
                    <div style="font-size: 0.6rem; font-weight: 800; color: var(--secondary); text-transform: uppercase;">Confidence Score</div>
                    <div style="font-size: 1.5rem; font-weight: 800; color: var(--primary); margin: 8px 0;">{top_confidence*100:.1f}%</div>
                    <div style="font-size: 0.65rem; color: var(--text-muted); font-weight: 600; line-height: 1.3;">Statistical certainty based on multi-modal telemetry patterns.</div>
                </div>
            """, unsafe_allow_html=True)
        with k2:
            severity_map = {
                1: ("NOMINAL", "#10B981", "PERFORMING WITHIN LIMITS"),
                2: ("ELEVATED", "#F59E0B", "MINOR ISSUES: MONITOR"),
                3: ("CRITICAL", "#EF4444", "URGENT: HIGH RISK"),
                4: ("CATASTROPHIC", "#7F1D1D", "STOP: FAILURE RISK")
            }
            sev_label, sev_color, sev_desc = severity_map.get(top_severity, ("UNKNOWN", "#64748B", "UNDETERMINED"))
            st.markdown(f"""
                <div class="metric-card" style="padding: 1rem; min-height: 140px;">
                    <div style="font-size: 0.6rem; font-weight: 800; color: var(--secondary); text-transform: uppercase;">System Status</div>
                    <div style="font-size: 1.3rem; font-weight: 800; color: {sev_color}; margin: 8px 0;">L{top_severity}: {sev_label}</div>
                    <div style="font-size: 0.65rem; color: var(--text-muted); font-weight: 800; letter-spacing: 0.05em;">{sev_desc}</div>
                </div>
            """, unsafe_allow_html=True)
        with k3:
            p_rec = lr.get('recommended_part')
            p_price = p_rec['price_oem'] if p_rec else 0.0
            labor_val = max(0, lr['cost'] - p_price)
            labor_rate_map = {"Industrial": 180, "Automotive": 280, "Mobile": 60, "Appliance": 110}
            d_type = lr['results'][0]['device_type'] if lr.get('results') else "Industrial"
            l_rate = labor_rate_map.get(d_type, 180)
            labor_hrs = labor_val / l_rate
            st.markdown(f"""
                <div class="metric-card" style="padding: 1rem; min-height: 140px;">
                    <div style="font-size: 0.6rem; font-weight: 800; color: var(--secondary); text-transform: uppercase;">Service Estimate</div>
                    <div style="font-size: 1.5rem; font-weight: 800; color: var(--text-main); margin: 8px 0;">${lr['cost']:,.0f}</div>
                    <div style="font-size: 0.6rem; color: var(--primary); font-weight: 800; text-transform: uppercase;">PART: ${p_price:,.0f} | LAB: ${labor_val:,.0f}</div>
                    <div style="font-size: 0.55rem; color: var(--text-muted); font-weight: 600; margin-top: 4px;">{labor_hrs:.1f} HRS @ ${l_rate}/HR BASE</div>
                </div>
            """, unsafe_allow_html=True)

        # 2. Predicted Faults (Compact Grid)
        st.markdown('<div class="zone-header" style="margin-top: 1rem;">Predicted Faults</div>', unsafe_allow_html=True)
        if lr['results']:
            f_cols = st.columns(3)
            for i, res in enumerate(lr['results']):
                with f_cols[i % 3]:
                    st.markdown(f"""
                    <div class="metric-card" style="padding: 1rem; min-height: 140px;">
                        <div style="font-size: 0.6rem; font-weight: 800; color: var(--secondary); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;">{res['system']}</div>
                        <div style="font-size: 1rem; font-weight: 800; color: var(--text-main); line-height: 1.2; min-height: 2.4em;">
                            {res['description']} 
                            <span style="font-family: monospace; font-size: 0.7rem; color: var(--primary); opacity: 0.8; margin-left: 5px;">[{res['fault_code']}]</span>
                        </div>
                        <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 8px;">
                            <span style="font-size: 0.6rem; font-weight: 800; color: var(--secondary);">{res['confidence']*100:.0f}% M-LY</span>
                            <div style="width: 60%; height: 4px; background: #E2E8F0; border-radius: 2px;">
                                <div style="height: 100%; width: {res['confidence']*100}%; background: var(--primary); border-radius: 2px;"></div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
        # 3. Narrative Extraction (Below Faults)
        st.markdown('<div class="zone-header" style="margin-top: 1rem;">Narrative Extraction</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="intel-report" style="margin-bottom: 1.5rem;">{lr["report"]}</div>', unsafe_allow_html=True)
        if uploaded_file:
            st.image(uploaded_file, use_container_width=False, width=400)
    


    # --- MODULE D: PORTFOLIO & PROCUREMENT LOGISTICS ---
    st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)
    st.markdown('<div class="zone-header">Logistics & Strategy</div>', unsafe_allow_html=True)
    
    if lr:
        # A. PORTFOLIO STRATEGY: ALTERNATIVE ASSETS
        st.markdown('<div class="zone-header" style="margin-top: 1rem;">Product Alternatives</div>', unsafe_allow_html=True)
        # Identify current product context
        current_model = telemetry.get('model_name', 'Unknown Asset') if telemetry else None
        current_type = telemetry.get('device_type', 'Industrial') if telemetry else None
        current_msrp = telemetry.get('product_msrp', 0.0) if telemetry else 0.0
        
        # Calculate Product Alternatives if context exists
        product_alts = {"primary": pd.DataFrame(), "secondary": pd.DataFrame()}
        if telemetry and current_model:
            product_alts = parts_pro.find_product_alternatives(archive, current_model, current_type, current_msrp)
        
        def render_alt_table(df, table_title, badge_label):
            """Renders a product alternatives table with full cost decomposition."""
            if df.empty:
                return
            
            rows_html = ""
            for _, p_row in df.iterrows():
                alt_msrp = p_row.get('product_msrp', 0)
                disc = p_row.get('discount_pct', 0)
                after_disc = p_row.get('after_discount_cost', alt_msrp)
                ship = p_row.get('shipping_cost', 0)
                install = p_row.get('installation_cost', 0)
                haul = p_row.get('hauling_cost', 0)
                eta = p_row.get('eta_days', 'N/A')
                supplier = p_row.get('product_supplier', 'N/A')
                labor = p_row.get('labor_cost', 0)
                
                rows_html += f"""
                <tr style="border-bottom: 1px solid var(--border);">
                    <td style="padding: 8px 10px; font-size: 0.78rem; color: var(--text-main); font-weight: 600;">{p_row['model_name']}</td>
                    <td style="padding: 8px 10px; font-size: 0.75rem; color: var(--secondary);">{supplier}</td>
                    <td style="padding: 8px 10px; font-size: 0.78rem; font-weight: 700; color: var(--text-muted); text-decoration: line-through;">${alt_msrp:,.0f}</td>
                    <td style="padding: 8px 10px; font-size: 0.7rem; color: #10B981; font-weight: 700;">{disc:.0f}%</td>
                    <td style="padding: 8px 10px; font-size: 0.82rem; font-weight: 800; color: var(--accent);">${after_disc:,.0f}</td>
                    <td style="padding: 8px 10px; font-size: 0.72rem; color: var(--text-muted);">${labor:,.0f}</td>
                    <td style="padding: 8px 10px; font-size: 0.72rem; color: var(--text-muted);">${install:,.0f}</td>
                    <td style="padding: 8px 10px; font-size: 0.72rem; color: var(--text-muted);">${haul:,.0f}</td>
                    <td style="padding: 8px 10px; font-size: 0.72rem; color: var(--text-muted);">${ship:,.0f}</td>
                    <td style="padding: 8px 10px; font-size: 0.72rem; font-weight: 700; color: var(--primary);">{eta}d</td>
                </tr>"""
            
            st.markdown(f"""
            <div style="margin-bottom: 0.8rem;">
                <div style="font-size: 0.7rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: var(--secondary); margin-bottom: 0.5rem; display: flex; align-items: center; gap: 8px;">
                    <span style="background: var(--primary-soft); color: var(--primary); padding: 2px 8px; border-radius: 4px; font-size: 0.6rem;">{badge_label}</span>
                    {table_title}
                </div>
                <table style="width: 100%; border-collapse: collapse; background: var(--card-bg); border-radius: 10px; overflow: hidden; border: 1px solid var(--border);">
                    <thead>
                        <tr style="background: var(--primary-soft); border-bottom: 2px solid var(--border);">
                            <th style="padding: 8px 10px; font-size: 0.6rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase;">Model</th>
                            <th style="padding: 8px 10px; font-size: 0.6rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase;">Supplier</th>
                            <th style="padding: 8px 10px; font-size: 0.6rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase;">MSRP</th>
                            <th style="padding: 8px 10px; font-size: 0.6rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase;">Discount</th>
                            <th style="padding: 8px 10px; font-size: 0.6rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase;">After Discount</th>
                            <th style="padding: 8px 10px; font-size: 0.6rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase;">Labor</th>
                            <th style="padding: 8px 10px; font-size: 0.6rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase;">Install</th>
                            <th style="padding: 8px 10px; font-size: 0.6rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase;">Hauling</th>
                            <th style="padding: 8px 10px; font-size: 0.6rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase;">Shipping</th>
                            <th style="padding: 8px 10px; font-size: 0.6rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase;">ETA</th>
                        </tr>
                    </thead>
                    <tbody>{rows_html}</tbody>
                </table>
            </div>
            """, unsafe_allow_html=True)
        
        # Render Primary (Apple to Apple)
        primary_df = product_alts.get("primary", pd.DataFrame()) if isinstance(product_alts, dict) else product_alts
        secondary_df = product_alts.get("secondary", pd.DataFrame()) if isinstance(product_alts, dict) else pd.DataFrame()
        primary_label = product_alts.get("primary_label", "Direct Replacements") if isinstance(product_alts, dict) else "Direct Replacements"
        secondary_label = product_alts.get("secondary_label", "Alternative Options") if isinstance(product_alts, dict) else "Alternative Options"
        
        if not primary_df.empty or not secondary_df.empty:
            render_alt_table(primary_df, primary_label, "DIRECT")
            render_alt_table(secondary_df, secondary_label, "ALTERNATIVE")
            
            # C. ASSET STRATEGY: REPAIR VS. REPLACE (Universal Decision Optimization)
            if not primary_df.empty or not secondary_df.empty:
                st.markdown('<div class="zone-header" style="margin-top: 1rem;">AI Strategy</div>', unsafe_allow_html=True)
                
                # 1. Replacement Candidate Pooling
                replace_pool = pd.concat([primary_df, secondary_df], ignore_index=True).drop_duplicates(subset=['model_name', 'product_supplier'])
                replace_pool['total_landing_cost'] = (
                    replace_pool['after_discount_cost'] + 
                    replace_pool['labor_cost'] + 
                    replace_pool['installation_cost'] + 
                    replace_pool['hauling_cost'] + 
                    replace_pool['shipping_cost']
                )
                
                # 2. Repair Path Mapping (The "Fix It" Candidate)
                primary_fault = lr['results'][0]
                repair_part_data = lr.get('recommended_part') or {}
                
                repair_candidate = {
                    "model_name": f"Repair: {primary_fault['description']}",
                    "total_landing_cost": lr['cost'],
                    "eta_days": repair_part_data.get('eta_days', 3), # Predictive Lead Time
                    "product_supplier": repair_part_data.get('supplier', 'OEM Hub'),
                    "shipping_cost": repair_part_data.get('shipping_cost', 0),
                    "labor_cost": max(0, lr['cost'] - repair_part_data.get('price_oem', 0)),
                    "installation_cost": 0,
                    "hauling_cost": 0,
                    "is_repair": True
                }
                
                # 3. Unified Strategic Pool
                best_replacements = replace_pool.sort_values('total_landing_cost').head(2).to_dict('records')
                unified_pool = [repair_candidate] + best_replacements
                
                # 4. Sector Weighting
                sector_map = {"Industrial": "Business", "Automotive": "Business", "Appliance": "Household", "Mobile": "Household"}
                active_sector = sector_map.get(current_type, "Business")
                
                with st.spinner(f"Arbitrating {active_sector} Strategy..."):
                    asset_strategy = narrative_layer.generate_product_strategy_rationale(
                        current_asset={"model_name": current_model, "device_type": current_type},
                        candidates=unified_pool,
                        sector=active_sector
                    )
                
                # 5. Parsing & UI Synchronization
                try:
                    parts = asset_strategy.split("|")
                    winner_id = parts[0].replace("WINNER:", "").strip()
                    verdict = parts[1].replace("VERDICT:", "").strip().upper()
                    rationale = parts[2].replace("RATIONALE:", "").strip()
                except:
                    winner_id = "REPAIR"
                    verdict = "REPAIR RECOMMENDED"
                    rationale = asset_strategy

                # 6. Winner Resolution & Economic Sanity Check (Removing Technical Debt)
                is_repair_won = "REPAIR" in winner_id.upper()
                
                if not is_repair_won:
                    win_match = replace_pool[replace_pool['model_name'] == winner_id]
                    potential_win_data = win_match.iloc[0].to_dict() if not win_match.empty else best_replacements[0]
                    
                    if repair_candidate['total_landing_cost'] < potential_win_data['total_landing_cost'] and \
                       repair_candidate['eta_days'] <= potential_win_data['eta_days']:
                        is_repair_won = True
                        verdict = "REPAIR RECOMMENDED"
                        rationale = "The repair path is mathematically prioritized as it offers both lower cost and faster turnaround."

                # Clean up display strings
                verdict = verdict.replace("(LOGIC OVERRIDE)", "").strip()
                rationale = rationale.replace("Economic Guardrail:", "").strip()

                if is_repair_won:
                    win_data = repair_candidate
                    badge_bg, badge_text = "#ECFDF5", "#059669"
                    winner_display = f"Maintain: {current_model}"
                    plan_desc = f"Service: {primary_fault['description']}"
                    savings_label = "REPAIR SAVINGS"
                else:
                    win_match = replace_pool[replace_pool['model_name'] == winner_id]
                    win_data = win_match.iloc[0].to_dict() if not win_match.empty else best_replacements[0]
                    badge_bg, badge_text = "#EEF2FF", "#6366F1"
                    winner_display = f"Upgrade: {win_data['model_name']}"
                    plan_desc = f"Strategic Procurement"
                    savings_label = "INVESTMENT DELTA"

                final_savings = abs(win_data['total_landing_cost'] - unified_pool[1 if win_data.get('is_repair') else 0]['total_landing_cost'])

                # 7. Decision Transparency Grid (Professional UI)
                best_replace = best_replacements[0]
                
                strategy_html = f'<div class="procurement-card" style="border-left-color: {badge_text}; padding: 1.5rem;">'
                strategy_html += f'<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.5rem;">'
                strategy_html += f'<div><div style="color: var(--text-muted); font-weight: 700; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.4rem;">Strategic Recommendation</div>'
                strategy_html += f'<div style="font-size: 1.6rem; font-weight: 900; color: var(--text-main); line-height: 1.1;">{winner_display}</div>'
                strategy_html += f'<div style="font-size: 0.75rem; color: var(--secondary); margin-top: 6px; font-weight: 700; text-transform: uppercase;">Outcome: {verdict}</div></div>'
                strategy_html += f'<div style="text-align: right;"><div style="font-size: 0.6rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase; margin-bottom: 4px;">{savings_label}</div><div style="font-size: 1.4rem; font-weight: 900; color: {badge_text};">${final_savings:,.2f}</div></div></div>'
                
                # Grid
                strategy_html += f'<div style="background: var(--primary-soft); border-radius: 12px; padding: 1rem; border: 1px solid var(--border); margin-bottom: 1.5rem;">'
                strategy_html += f'<div style="font-size: 0.65rem; font-weight: 800; color: var(--secondary); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.8rem;">Decision Comparison</div>'
                strategy_html += f'<table style="width: 100%; border-collapse: collapse;"><thead><tr style="border-bottom: 1px solid var(--border);">'
                strategy_html += f'<th style="padding: 6px 0; text-align: left; font-size: 0.6rem; color: var(--text-muted); width: 40%;">ANALYSIS METRIC</th>'
                
                # Column Header Highlighting
                repair_win_style = 'background: #ECFDF5; border-radius: 8px 8px 0 0;' if is_repair_won else ''
                strategy_html += f'<th style="padding: 10px 0; text-align: center; font-size: 0.65rem; color: var(--text-main); font-weight: 800; width: 30%; {repair_win_style}">REPAIR PATH</th>'
                
                replace_win_style = 'background: #EEF2FF; border-radius: 8px 8px 0 0;' if not is_repair_won else ''
                strategy_html += f'<th style="padding: 10px 0; text-align: center; font-size: 0.65rem; color: var(--text-main); font-weight: 800; width: 30%; {replace_win_style}">REPLACE PATH</th>'
                strategy_html += f'</tr></thead><tbody>'
                
                # Rows
                r_tlc, b_tlc = repair_candidate['total_landing_cost'], best_replace['total_landing_cost']
                r_eta, b_eta = repair_candidate['eta_days'], best_replace['eta_days']
                
                strategy_html += f'<tr style="border-bottom: 1px solid rgba(0,0,0,0.05);">'
                strategy_html += f'<td style="padding: 12px 0; font-size: 0.75rem; font-weight: 700; color: var(--text-main);">Total Landing Cost</td>'
                strategy_html += f'<td style="padding: 12px 0; text-align: center; font-size: 0.85rem; font-weight: 800; color: {"#10B981" if r_tlc < b_tlc else "#EF4444"}; {repair_win_style}">${r_tlc:,.2f}</td>'
                strategy_html += f'<td style="padding: 12px 0; text-align: center; font-size: 0.85rem; font-weight: 800; color: {"#10B981" if b_tlc < r_tlc else "#EF4444"}; {replace_win_style}">${b_tlc:,.2f}</td></tr>'
                
                strategy_html += f'<tr style="border-bottom: 1px solid rgba(0,0,0,0.05);">'
                strategy_html += f'<td style="padding: 12px 0; font-size: 0.75rem; font-weight: 700; color: var(--text-main);">Turnaround Time (ETA)</td>'
                strategy_html += f'<td style="padding: 12px 0; text-align: center; font-size: 0.85rem; font-weight: 800; color: {"#10B981" if r_eta <= b_eta else "#F59E0B"}; {repair_win_style}">{r_eta} Days</td>'
                strategy_html += f'<td style="padding: 12px 0; text-align: center; font-size: 0.85rem; font-weight: 800; color: {"#10B981" if b_eta < r_eta else "#F59E0B"}; {replace_win_style}">{b_eta} Days</td></tr>'
                
                strategy_html += f'<tr><td style="padding: 12px 0; font-size: 0.75rem; font-weight: 600; color: var(--secondary);">Strategic Action</td>'
                strategy_html += f'<td style="padding: 12px 0; text-align: center; font-size: 0.65rem; font-weight: 700; color: var(--text-muted); {repair_win_style}">{repair_candidate["model_name"]}</td>'
                strategy_html += f'<td style="padding: 12px 0; text-align: center; font-size: 0.65rem; font-weight: 700; color: var(--text-muted); {replace_win_style}">Upgrade: {best_replace["model_name"]}</td></tr>'
                strategy_html += f'</tbody></table></div>'
                
                # Rationale
                strategy_html += f'<div style="border-left: 4px solid {badge_text}; background: #F9FAFB; padding: 1rem; border-radius: 0 8px 8px 0;">'
                strategy_html += f'<div style="font-size: 0.65rem; font-weight: 800; color: var(--secondary); text-transform: uppercase; margin-bottom: 0.5rem;">Analytical Rationale</div>'
                strategy_html += f'<div style="font-size: 0.88rem; color: var(--text-main); line-height: 1.5; font-weight: 500;">{rationale}</div></div></div>'
                
                st.markdown(strategy_html, unsafe_allow_html=True)
        else:
            st.info("No alternative portfolio assets found for this category.")


        # B. PART ALTERNATIVES
        st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
        
        part_row = lr.get('recommended_part')
        query = part_row['part_number'] if part_row is not None else ""
        
        if query:
            lookup_results = parts_pro.find_compatible_alternatives(query)
            if lookup_results:
                st.markdown('<div class="zone-header" style="margin-top: 1rem;">Part Alternatives</div>', unsafe_allow_html=True)
                alt_df = lookup_results['alternatives']
                
                # We want to create a unified list of options for the user to choose from
                # Start with the naturally recommended part from the diagnostic step
                all_options = []
                if part_row is not None:
                    p_orig = part_row.copy()
                    all_options.append(p_orig)
                
                for _, row in alt_df.iterrows():
                    all_options.append(row.to_dict())

                if all_options:
                    # --- LEVEL 1: Sort in-stock options to the top ---
                    # Guarantees the selectbox always defaults to a procurable part.
                    all_options.sort(key=lambda p: (0 if p.get('in_stock', False) else 1, p.get('price_oem', 0)))

                    # --- LEVEL 2: Detect all-OOS state ---
                    any_in_stock = any(p.get('in_stock', False) for p in all_options)

                    if not any_in_stock:
                        # ESCALATION BANNER: All parts are backordered — repair path is blocked
                        best_replace_name = "the best available replacement" 
                        if not primary_df.empty:
                            best_replace_name = f"**{primary_df.iloc[0]['model_name']}**"
                        elif not secondary_df.empty:
                            best_replace_name = f"**{secondary_df.iloc[0]['model_name']}**"

                        st.markdown(f"""
                        <div style="background: #FEF2F2; border: 1.5px solid #EF4444; border-left: 5px solid #DC2626;
                                    border-radius: 10px; padding: 1.2rem 1.5rem; margin-bottom: 1rem;">
                            <div style="display: flex; align-items: flex-start; gap: 12px;">
                                <div style="font-size: 1.4rem; margin-top: 2px;">🚨</div>
                                <div>
                                    <div style="font-size: 0.7rem; font-weight: 900; color: #DC2626; text-transform: uppercase;
                                                letter-spacing: 0.08em; margin-bottom: 6px;">
                                        Supply Chain Alert — Repair Path Blocked
                                    </div>
                                    <div style="font-size: 0.88rem; color: #374151; font-weight: 500; line-height: 1.55;">
                                        All compatible parts are currently <strong>out of stock</strong> across every supplier in the registry.
                                        The repair path cannot be executed at this time.
                                    </div>
                                    <div style="margin-top: 10px; padding: 10px 14px; background: white; border-radius: 8px;
                                                border: 1px solid #FECACA; font-size: 0.82rem; color: #7F1D1D; font-weight: 600;">
                                        ⬆ Escalation: Review the <strong>AI Strategy</strong> section above. The
                                        <strong>Replace Path</strong> is now the recommended action.
                                        Recommended next action: Procure {best_replace_name} as the replacement unit.
                                    </div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    # Build selectbox labels (in-stock first order is already applied)
                    labels = []
                    for p in all_options:
                        stock_tag = "✅ IN STOCK" if p.get('in_stock', False) else "❌ OUT OF STOCK"
                        labels.append(f"{p.get('brand','NA')} - {p.get('supplier','NA')} (${p.get('price_oem',0):.2f}) — {stock_tag}")

                    s_id = telemetry.get('service_id', 'live') if telemetry else 'vision_only'
                    selection_label = st.selectbox(
                        "Select Procurement Source",
                        labels,
                        key=f"supplier_select_{s_id}",
                        label_visibility="collapsed"
                    )

                    selected_idx = labels.index(selection_label)
                    part_row = all_options[selected_idx]

                    # --- LEVEL 3: CAUTION badge when user selects an OOS part ---
                    if not part_row.get('in_stock', False):
                        # Build a list of in-stock alternatives to show directly in the warning
                        instock_options = [p for p in all_options if p.get('in_stock', False)]
                        
                        if instock_options:
                            alt_chips_html = ""
                            for p in instock_options:
                                alt_chips_html += f"""
                                <div style="display: flex; align-items: center; gap: 8px; padding: 6px 10px;
                                            background: white; border: 1px solid #FCD34D; border-radius: 6px;">
                                    <div style="width: 7px; height: 7px; border-radius: 50%; background: #10B981; flex-shrink: 0;"></div>
                                    <div>
                                        <span style="font-size: 0.75rem; font-weight: 700; color: #374151;">
                                            {p.get('brand','N/A')} — {p.get('supplier','N/A')}
                                        </span>
                                        <span style="font-size: 0.7rem; color: #6B7280; margin-left: 6px;">
                                            {p.get('condition','N/A')} · ${p.get('price_oem', 0):.2f}
                                        </span>
                                    </div>
                                </div>"""
                            
                            st.markdown(f"""
                            <div style="background: #FFFBEB; border: 1px solid #F59E0B; border-left: 4px solid #D97706;
                                        border-radius: 8px; padding: 1rem 1.2rem; margin-bottom: 0.8rem;">
                                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.7rem;">
                                    <span style="font-size: 1rem;">⚠️</span>
                                    <span style="font-size: 0.7rem; font-weight: 900; color: #D97706;
                                                 text-transform: uppercase; letter-spacing: 0.06em;">Backorder Selected</span>
                                    <span style="font-size: 0.8rem; color: #78350F; font-weight: 500;">
                                        — This part is not currently available. Switch to one of these in-stock options:
                                    </span>
                                </div>
                                <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                                    {alt_chips_html}
                                </div>
                                <div style="font-size: 0.72rem; color: #92400E; margin-top: 8px; font-weight: 500;">
                                    Use the dropdown above to switch your selection.
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            # No in-stock options at all — already handled by the Level 2 escalation banner
                            st.markdown("""
                            <div style="background: #FFFBEB; border: 1px solid #F59E0B; border-left: 4px solid #D97706;
                                        border-radius: 8px; padding: 0.8rem 1.2rem; margin-bottom: 0.8rem;
                                        display: flex; align-items: center; gap: 10px;">
                                <span style="font-size: 1rem;">⚠️</span>
                                <span style="font-size: 0.7rem; font-weight: 900; color: #D97706; text-transform: uppercase;
                                             letter-spacing: 0.06em;">Backorder Selected</span>
                                <span style="font-size: 0.82rem; color: #78350F; font-weight: 500; margin-left: 8px;">
                                    No in-stock alternatives exist. See the Supply Chain Alert above.
                                </span>
                            </div>
                            """, unsafe_allow_html=True)

                    # Comparison table
                    rows_html = ""
                    for p in all_options:
                        stock_color = "#10B981" if p['in_stock'] else "#EF4444"
                        stock_bg = "#ECFDF5" if p['in_stock'] else "#FEF2F2"
                        stock_label = "IN STOCK" if p['in_stock'] else "OUT OF STOCK"
                        cond = p.get('condition', 'N/A')
                        cond_color = '#10B981' if cond == 'New' else '#6366F1' if 'Never Used' in cond else '#F59E0B' if 'Pre-Owned' in cond else '#8B5CF6' if 'Refurbished' in cond else '#94A3B8'
                        cond_bg = '#ECFDF5' if cond == 'New' else '#EEF2FF' if 'Never Used' in cond else '#FFFBEB' if 'Pre-Owned' in cond else '#F5F3FF' if 'Refurbished' in cond else '#F1F5F9'
                        # Dim out-of-stock rows visually
                        row_opacity = "1.0" if p['in_stock'] else "0.55"

                        rows_html += f"""
                        <tr style="border-bottom: 1px solid #F1F5F9; opacity: {row_opacity};">
                            <td style="padding: 10px 12px; font-size: 0.8rem; color: #374151; font-weight: 600;">{p.get('part_number','')}</td>
                            <td style="padding: 10px 12px;">
                                <span style="font-size: 0.7rem; font-weight: 800; color: {cond_color}; background: {cond_bg}; padding: 3px 8px; border-radius: 20px; text-transform: uppercase;">{cond}</span>
                            </td>
                            <td style="padding: 10px 12px; font-size: 0.8rem; color: #374151;">{p.get('supplier', 'Local Dealer')}</td>
                            <td style="padding: 10px 12px; font-size: 0.8rem; color: #374151;">{p.get('brand','')}</td>
                            <td style="padding: 10px 12px; font-size: 0.85rem; font-weight: 700; color: var(--primary);">${p.get('price_oem', 0):.2f}</td>
                            <td style="padding: 10px 12px;">
                                <span style="font-size: 0.7rem; font-weight: 800; color: {stock_color}; background: {stock_bg}; padding: 4px 10px; border-radius: 20px;">{stock_label}</span>
                            </td>
                        </tr>"""

                    st.markdown(f"""
                    <table style="width: 100%; border-collapse: collapse; background: white; border-radius: 10px;
                                  overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,0.06); margin-bottom: 1rem;">
                        <thead>
                            <tr style="background: #F8FAFC; border-bottom: 2px solid #E2E8F0;">
                                <th style="padding: 10px 12px; font-size: 0.7rem; font-weight: 800; color: #6B7280; text-transform: uppercase;">Part No.</th>
                                <th style="padding: 10px 12px; font-size: 0.7rem; font-weight: 800; color: #6B7280; text-transform: uppercase;">Condition</th>
                                <th style="padding: 10px 12px; font-size: 0.7rem; font-weight: 800; color: #6B7280; text-transform: uppercase;">Supplier</th>
                                <th style="padding: 10px 12px; font-size: 0.7rem; font-weight: 800; color: #6B7280; text-transform: uppercase;">Brand</th>
                                <th style="padding: 10px 12px; font-size: 0.7rem; font-weight: 800; color: #6B7280; text-transform: uppercase;">Price</th>
                                <th style="padding: 10px 12px; font-size: 0.7rem; font-weight: 800; color: #6B7280; text-transform: uppercase;">Stock</th>
                            </tr>
                        </thead>
                        <tbody>{rows_html}</tbody>
                    </table>
                    """, unsafe_allow_html=True)
                else:
                    st.info("No direct manufacturer alternatives found.")

        # C. PROCUREMENT STRATEGY: REPLACEMENT COMPONENTS
        if part_row is not None:
            st.markdown('<div class="zone-header" style="margin-top: 1rem;">AI Purchasing Intelligence</div>', unsafe_allow_html=True)
            supplier = part_row.get('supplier', 'Local Dealer')
            intel = parts_pro.get_supplier_dossier(supplier)
            if not intel:
                intel = {
                    "supplier_name": supplier, "rating": "N/A", "speed_class": "Standard", "active_discount": "None",
                    "on_time_pct": 0, "defect_rate_pct": 0
                }
                
            # Extract and compute actual discount from vendor terms
            discount_text = intel.get('active_discount', 'None')
            discount_pct = 0.0
            import re
            m = re.search(r'(\d+)%', discount_text)
            if m:
                discount_pct = int(m.group(1)) / 100.0
                
            oem_cost = float(part_row['price_oem'])
            final_cost = oem_cost * (1.0 - discount_pct)
            
            # Helper for stock indicators
            stock_color = '#10B981' if part_row['in_stock'] else '#EF4444'
            stock_bg = '#ECFDF5' if part_row['in_stock'] else '#FEF2F2'
            stock_text = 'IN STOCK' if part_row['in_stock'] else 'OUT OF STOCK'

            # Build the Consolidated "Purchasing Details" Card
            html_block_top = f"""
<div class="procurement-card">
<div style="display: grid; grid-template-columns: 1.2fr 1fr 0.8fr; gap: 2rem; align-items: start;">
<div>
<div style="color: var(--text-muted); font-weight: 700; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.5rem;">Part to Order</div>
<div style="font-size: 1.4rem; font-weight: 900; color: var(--text-main); line-height: 1.2;">{part_row['description']}</div>
<div style="font-size: 0.8rem; color: var(--secondary); margin-top: 6px; font-weight: 600;">
BRAND: <span style="color: var(--primary);">{part_row['brand']}</span> &nbsp;|&nbsp; SKU: {part_row['part_number']}
</div>
<div style="margin-top: 8px;">
<span style="font-size: 0.7rem; font-weight: 800; color: {'#10B981' if part_row.get('condition','') == 'New' else '#F59E0B'}; background: {'#ECFDF5' if part_row.get('condition','') == 'New' else '#FFFBEB'}; padding: 3px 8px; border-radius: 4px;">{part_row.get('condition', 'Standard')}</span>
</div>
</div>
<div style="border-left: 1px solid var(--border); padding-left: 2rem;">
<div style="color: var(--text-muted); font-weight: 700; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.5rem;">Supplier Reliability</div>
<div style="font-size: 1.1rem; font-weight: 800; color: var(--text-main);">{supplier}</div>
<div style="margin-top: 10px; display: flex; flex-direction: column; gap: 8px;">
<div class="performance-chip">
🚚 {intel.get('speed_class','Standard')} Delivery
</div>
<div style="display: flex; gap: 8px;">
<div class="performance-chip" style="color: var(--accent); background: #ECFDF5;">
⏱️ {intel.get('on_time_pct', 0)}% Delivered On-Time
</div>
<div class="performance-chip" style="color: #EF4444; background: #FEF2F2;">
🛡️ {intel.get('defect_rate_pct', 0)}% Quality Issues
</div>
</div>
</div>
</div>
<div style="text-align: right;">
<div style="color: var(--text-muted); font-size: 0.65rem; font-weight: 700; text-transform: uppercase; margin-bottom: 0.5rem;">Final Price</div>
{f'<div style="font-size: 0.8rem; color: #94A3B8; text-decoration: line-through; margin-bottom: -2px;">Original: ${oem_cost:,.2f}</div>' if discount_pct > 0 else ""}
<div style="color: var(--accent); font-size: 2rem; font-weight: 900; line-height: 1;">${final_cost:,.2f}</div>
<div style="font-size: 0.65rem; color: #10B981; font-weight: 800; margin-top: 6px; background: #ECFDF5; padding: 2px 8px; border-radius: 4px; display: inline-block;">
{f"🏷️ {discount_text}" if discount_pct > 0 else "✓ BEST MARKET PRICE"}
</div>
<div style="margin-top: 12px;">
<div style="font-size: 0.7rem; font-weight: 800; color: {stock_color}; background: {stock_bg}; padding: 4px 10px; border-radius: 6px; display: inline-block; border: 1px solid {stock_color}22;">
{stock_text}
</div>
</div>
</div>
</div>
"""

            # 3. LIVE AI REASONING CORE
            # We call the LLM live to synthesize the strategy based on numbers, ignoring CSV text
            with st.spinner("Analyzing Vendor Performance Strategy..."):
                raw_response = narrative_layer.generate_purchasing_rationale(
                    part_data={
                        "description": part_row['description'],
                        "brand": part_row['brand'],
                        "price_oem": part_row['price_oem'],
                        "in_stock": part_row['in_stock']
                    },
                    supplier_data=intel
                )

            # Robust Parsing for Structured AI Output
            try:
                if "|" in raw_response:
                    v_part, r_part = raw_response.split("|", 1)
                    verdict = v_part.replace("VERDICT:", "").strip().upper()
                    rationale = r_part.replace("RATIONALE:", "").strip()
                else:
                    verdict = "RECOMMENDED"
                    rationale = raw_response
                
                # FINAL SANITIZER: Aggressively strip any stray verdicts or bold tags (LLM stubbornness)
                import re
                # 1. Remove ANY bold tags (even in the middle)
                rationale = re.sub(r'\*\*.*?\*\*', '', rationale)
                # 2. Case-insensitively remove the verdict keywords if they are standing alone
                verdict_keywords = ["RECOMMENDED", "HIGHLY RECOMMENDED", "CAUTION", "AVOID", "ACCEPTABLE", "APPROVED"]
                pattern = r'\b(' + '|'.join(verdict_keywords) + r')\b'
                rationale = re.sub(pattern, '', rationale, flags=re.IGNORECASE)
                # 3. Clean up extra spaces or punctuation left behind
                rationale = re.sub(r'\s+', ' ', rationale).strip()
                rationale = rationale.strip(' .:') + "." # Ensure a clean single period at the end
                
            except:
                verdict = "RECOMMENDED"
                rationale = raw_response

            # Decision Badge Logic
            badge_bg = "#ECFDF5" # Default Green
            badge_text = "#10B981"
            if any(x in verdict for x in ["CAUTION", "WARNING", "PENDING"]):
                badge_bg = "#FFFBEB" # Amber
                badge_text = "#D97706"
            elif any(x in verdict for x in ["AVOID", "HIGH RISK"]):
                badge_bg = "#FEF2F2" # Red
                badge_text = "#DC2626"

            html_footer = f"""
<div class="strategy-note" style="border-top: 1px dashed var(--border); margin-top: 1.5rem; padding-top: 1rem;">
<div style="display: flex; flex-direction: column; gap: 12px;">
<div style="display: flex; justify-content: space-between; align-items: center;">
<div style="font-size: 0.7rem; font-weight: 800; color: var(--secondary); text-transform: uppercase; letter-spacing: 0.05em;">AI Recommendation</div>
<div style="background: {badge_bg}; color: {badge_text}; font-size: 0.65rem; font-weight: 900; padding: 4px 12px; border-radius: 6px; border: 1px solid {badge_text}33;">
{verdict}
</div>
</div>
<div style="display: flex; gap: 12px; align-items: flex-start;">
<div style="font-size: 1.2rem;"></div>
<div style="font-size: 0.85rem; color: var(--text-main); line-height: 1.5; font-weight: 500;">
{rationale}
</div>
</div>
</div>
</div>
</div>
"""
            st.markdown(html_block_top + html_footer, unsafe_allow_html=True)




    

# --- MODULE A: PRODUCT INTELLIGENCE HUB ---
st.markdown('<div class="zone-header" style="margin-top: 0;">Product Intelligence </div>', unsafe_allow_html=True)

# Tabs grouping Live Diagnostics and Visual Audit within the Intelligence workflow
archive_tab, live_tab, vision_tab = st.tabs(["Product Analytics", "Interactive Intelligence", "Vision Inspection"])

with archive_tab:
    sample_options = ["--- Select a Product ---"] + (archive['service_id'].astype(str) + " - " + 
                      archive['model_name']).tolist()
    selected_sample = st.selectbox("Select Product", options=sample_options, key="archive_select")
    if selected_sample != "--- Select a Product ---":
        sample_id = selected_sample.split(" - ")[0]
        match_df = archive[archive['service_id'] == sample_id]
        if not match_df.empty:
            base_data = match_df.iloc[0]
        else:
            base_data = None
            st.warning("Selected record not found in database.")
        
        if base_data is not None:
            device_type = base_data.get('device_type', '')
            is_mobile = device_type == "Mobile"
            
            with st.container(border=True):
                st.markdown('<div class="zone-header" style="font-size: 0.85rem; margin-top: 0;">Current Statistics of the Product</div>', unsafe_allow_html=True)
                
                # Product Condition Badge
                prod_cond = base_data.get('product_condition', 'N/A')
                cond_color_map = {
                    "New": ("#10B981", "#ECFDF5"),
                    "Certified Pre-Owned": ("#F59E0B", "#FFFBEB"),
                    "Refurbished": ("#8B5CF6", "#F5F3FF"),
                    "Never Used (Old Stock)": ("#6366F1", "#EEF2FF"),
                    "Used": ("#94A3B8", "#F1F5F9"),
                }
                c_fg, c_bg = cond_color_map.get(prod_cond, ("#94A3B8", "#F1F5F9"))
                st.markdown(f"""
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px; padding-bottom:10px; border-bottom:1px dashed #E2E8F0;">
                    <span style="font-size:0.7rem; font-weight:800; color:#6B7280; text-transform:uppercase; letter-spacing:0.08em;">Product Condition</span>
                    <span style="font-size:0.85rem; font-weight:800; color:{c_fg}; background:{c_bg}; padding:4px 14px; border-radius:20px; letter-spacing:0.04em;">{prod_cond}</span>
                </div>
                """, unsafe_allow_html=True)
                
                bc1, bc2, bc3, bc4 = st.columns(4)
                bc1.metric("Temperature", f"{base_data['telemetry_temp']} °C")
                bc2.metric("Voltage", f"{base_data['telemetry_voltage']} V")
                bc3.metric("Load", f"{base_data['telemetry_load_pct']} %")
                bc4.metric("Battery", f"{base_data.get('telemetry_battery', 0)} %")
                
                if not is_mobile:
                    bc5, bc6, bc7, bc8 = st.columns(4)
                    bc5.metric("RPM", f"{base_data['telemetry_rpm']}")
                    bc6.metric("Pressure", f"{base_data['telemetry_pressure']} PSI")
                    bc7.metric("Current", f"{base_data['telemetry_current']} A")
                    bc8.metric("Vibration", f"{base_data.get('telemetry_vibration', 0)}")
            
            # Default telemetry is exactly the baseline
            telemetry = {
                "service_id": base_data['service_id'],
                "device_type": base_data['device_type'], "telemetry_temp": float(base_data['telemetry_temp']),
                "telemetry_rpm": float(base_data.get('telemetry_rpm', 0.0)), "telemetry_voltage": float(base_data['telemetry_voltage']),
                "telemetry_vibration": float(base_data.get('telemetry_vibration', 0.0)), "telemetry_load_pct": float(base_data['telemetry_load_pct']),
                "telemetry_pressure": float(base_data.get('telemetry_pressure', 0.0)), "telemetry_current": float(base_data.get('telemetry_current', 0.0)),
                "telemetry_freq": base_data['telemetry_freq'], "telemetry_o2": base_data['telemetry_o2'],
                "telemetry_battery": float(base_data.get('telemetry_battery', 0.0)),
                "telemetry_coolant": base_data['telemetry_coolant'], "age_years": base_data['age_years']
            }
            
            # Pass product metadata for Portfolio Analysis
            telemetry.update({
                "model_name": base_data['model_name'],
                "product_msrp": float(base_data['product_msrp'])
            })
            
            st.markdown(f'<div class="zone-header" style="margin-top: 1.5rem;">Product Category: {base_data["device_type"]} ({base_data["service_id"]})</div>', unsafe_allow_html=True)
            if st.button("EXECUTE ANALYTICS", type="primary", use_container_width=True):
                with st.spinner("Processing..."):
                    try:
                        st.session_state.archive_results = run_diagnostics(telemetry, None)
                    except Exception as e:
                        st.error(f"Diagnostic Engine Error: {e}")

    else:
        # Separate CSS for stability
        st.markdown("""<style>
@keyframes floatGenius {
0% { transform: translateY(0px) rotate(0deg); }
50% { transform: translateY(-12px) rotate(5deg); }
100% { transform: translateY(0px) rotate(0deg); }
}
@keyframes fadeIn {
0% { opacity: 0; transform: translateY(20px) scale(0.98); }
100% { opacity: 1; transform: translateY(0px) scale(1); }
}
</style>""", unsafe_allow_html=True)

        landing_html = """<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 70vh; text-align: center; animation: fadeIn 1.2s cubic-bezier(0.4, 0, 0.2, 1) forwards;">
<div style="margin-bottom: 2.5rem;">
<div style="font-size: 4rem; color: var(--primary); margin-bottom: 1.5rem; filter: drop-shadow(0 10px 15px rgba(79,70,229,0.3)); animation: floatGenius 4s ease-in-out infinite;">⚙️</div>
<h2 style="font-family: 'Outfit'; font-size: 3rem; font-weight: 800; color: var(--text-main); letter-spacing: -0.02em; margin-bottom: 0.8rem; background: linear-gradient(135deg, var(--text-main), var(--secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Service Intelligence Suite</h2>
<p style="font-family: 'Inter'; color: var(--text-muted); font-weight: 500; font-size: 1.15rem; max-width: 700px; line-height: 1.6; margin: 0 auto;">Select an Product from the registry to deploy an integrated stack of AI-driven maintenance and logistics intelligence.</p>
</div>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem; width: 100%; max-width: 1200px; margin-top: 1rem;">
<div class="metric-card" style="min-height: 200px; text-align: left; background: linear-gradient(135deg, white, rgba(79, 70, 229, 0.02));">
<div style="font-size: 1.5rem; margin-bottom: 1rem;">🔍</div>
<div style="font-size: 0.7rem; font-weight: 800; color: var(--primary); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem;">Use Case: Reliability Audit</div>
<div style="font-size: 1.1rem; font-weight: 700; color: var(--text-main); margin-bottom: 0.5rem;">Autonomous Asset Audits</div>
<div style="font-size: 0.85rem; color: var(--text-muted); line-height: 1.5;">Deploy Vision AI to detect structural fatigue, corrosion, and fluid leaks across diverse hardware sectors including Industrial & Automotive.</div>
</div>
<div class="metric-card" style="min-height: 200px; text-align: left; background: linear-gradient(135deg, white, rgba(5, 150, 105, 0.02));">
<div style="font-size: 1.5rem; margin-bottom: 1rem;">🧠</div>
<div style="font-size: 0.7rem; font-weight: 800; color: var(--accent); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem;">Use Case: Predictive Maintenance</div>
<div style="font-size: 1.1rem; font-weight: 700; color: var(--text-main); margin-bottom: 0.5rem;">Real-time Telemetry Analysis</div>
<div style="font-size: 0.85rem; color: var(--text-muted); line-height: 1.5;">Monitor critical sensor streams with advanced anomaly detection to predict sub-system failures before they escalate into catastrophic downtime.</div>
</div>
<div class="metric-card" style="min-height: 200px; text-align: left; background: linear-gradient(135deg, white, rgba(245, 158, 11, 0.02));">
<div style="font-size: 1.5rem; margin-bottom: 1rem;">⚖️</div>
<div style="font-size: 0.7rem; font-weight: 800; color: #F59E0B; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem;">Use Case: Economic Strategy</div>
<div style="font-size: 1.1rem; font-weight: 700; color: var(--text-main); margin-bottom: 0.5rem;">Repair vs. Replace Modeling</div>
<div style="font-size: 0.85rem; color: var(--text-muted); line-height: 1.5;">Synthesize data-driven financial strategies by comparing service costs, asset age, and market MSRP to optimize total cost of ownership.</div>
</div>
<div class="metric-card" style="min-height: 200px; text-align: left; background: linear-gradient(135deg, white, rgba(79, 70, 229, 0.02));">
<div style="font-size: 1.5rem; margin-bottom: 1rem;">📦</div>
<div style="font-size: 0.7rem; font-weight: 800; color: var(--primary); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem;">Use Case: Logistics Sync</div>
<div style="font-size: 1.1rem; font-weight: 700; color: var(--text-main); margin-bottom: 0.5rem;">Autonomous Procurement</div>
<div style="font-size: 0.85rem; color: var(--text-muted); line-height: 1.5;">Map diagnostic failures directly to global OEM catalogs, identifying part alternatives and scoring supplier risk in real-time.</div>
</div>
</div>
</div>"""
        st.markdown(landing_html, unsafe_allow_html=True)
                    
    # Render Dashboard within the Archive Tab
    if st.session_state.archive_results and (selected_sample != "--- Select a Product ---" and base_data is not None):
        st.markdown("<br>", unsafe_allow_html=True)
        render_dashboard(st.session_state.archive_results, telemetry, None, tab_id="archive_tab")


if 'live_results' not in st.session_state: st.session_state.live_results = None
if 'live_telemetry_cache' not in st.session_state: st.session_state.live_telemetry_cache = None

with live_tab:
    st.info("**Try a Scenario:** Adjust the sliders below to see how different sensor readings affect the system's health and repair costs.")
    
    # We require the user to pick an anchor machine or at least a device type
    sim_options = ["--- Choose a Product ---"] + (archive['model_name'] + " (" + archive['device_type'] + ")").unique().tolist()
    selected_sim = st.selectbox("Pick a product to test:", options=sim_options, key="sim_base_select")
    
    if selected_sim != "--- Choose a Product ---":
        _model = selected_sim.split(" (")[0]
        match_df = archive[archive['model_name'] == _model]
        if not match_df.empty:
            base_sim_data = match_df.iloc[0]
        else:
            base_sim_data = None
            st.warning("Base model data not found in archive.")
        
        if base_sim_data is not None:
            telemetry = {
                "service_id": "sim_override",
                "device_type": base_sim_data['device_type'], "telemetry_temp": float(base_sim_data['telemetry_temp']),
                "telemetry_rpm": float(base_sim_data.get('telemetry_rpm', 0.0)), "telemetry_voltage": float(base_sim_data['telemetry_voltage']),
                "telemetry_vibration": float(base_sim_data.get('telemetry_vibration', 0.0)), "telemetry_load_pct": float(base_sim_data['telemetry_load_pct']),
                "telemetry_pressure": float(base_sim_data.get('telemetry_pressure', 0.0)), "telemetry_current": float(base_sim_data.get('telemetry_current', 0.0)),
                "telemetry_freq": base_sim_data['telemetry_freq'], "telemetry_o2": base_sim_data['telemetry_o2'],
                "telemetry_battery": float(base_sim_data.get('telemetry_battery', 0.0)),
                "telemetry_coolant": base_sim_data['telemetry_coolant'], "age_years": base_sim_data['age_years']
            }
            # Pass product metadata for Portfolio Analysis within Simulation
            telemetry.update({
                "model_name": base_sim_data['model_name'],
                "product_msrp": float(base_sim_data['product_msrp'])
            })
            
            # Move Interactive Diagnostic Controls here (Module C part 1)
            # Physical Operating Bounds per Device Category
            device_type = telemetry.get('device_type', 'Industrial')
            
            # SECTOR GOLD STANDARD: Strict Engineering Masks
            # Ensures ONLY realistic sensors are visible for each sector, overriding dirty data.
            SECTOR_GOLD_STANDARD = {
                "Appliance": ["temp", "voltage", "load_pct"],
                "Mobile": ["temp", "battery", "voltage", "load_pct"],
                "Automotive": ["temp", "rpm", "pressure", "voltage", "load_pct", "vibration"],
                "Industrial": ["temp", "rpm", "vibration", "current", "voltage", "load_pct"]
            }
            allowed_sensors = SECTOR_GOLD_STANDARD.get(device_type, [])
            
            range_dict = {
                "Mobile": {"temp": (0.0, 120.0), "volt": (0.0, 24.0), "load": (0.0, 100.0), "batt": (0.0, 100.0), "rpm": (0.0, 0.0), "pressure": (0.0, 0.0), "current": (0.0, 10.0), "vibration": (0.0, 5.0)},
                "Appliance": {"temp": (0.0, 250.0), "volt": (110.0, 240.0), "load": (0.0, 100.0), "batt": (0.0, 0.0), "rpm": (0.0, 2000.0), "pressure": (0.0, 150.0), "current": (0.0, 30.0), "vibration": (0.0, 10.0)},
                "Automotive": {"temp": (-40.0, 200.0), "volt": (10.0, 480.0), "load": (0.0, 100.0), "batt": (0.0, 100.0), "rpm": (0.0, 8000.0), "pressure": (0.0, 300.0), "current": (0.0, 300.0), "vibration": (0.0, 20.0)},
                "Industrial": {"temp": (-40.0, 450.0), "volt": (0.0, 1000.0), "load": (0.0, 150.0), "batt": (0.0, 100.0), "rpm": (0.0, 15000.0), "pressure": (0.0, 2000.0), "current": (0.0, 500.0), "vibration": (0.0, 50.0)}
            }
            bounds = range_dict.get(device_type, range_dict["Industrial"])
            
            with st.container(border=True):
                st.markdown('<div class="zone-header" style="margin-top: 0;">Interactive Diagnostic Controls</div>', unsafe_allow_html=True)
                simulator_cols = st.columns(2)
                
                def smart_slider(col_obj, label, key_name, min_v, max_v, default):
                    # 1. HIDE if category-wide bounds are inactive
                    if max_v == min_v:
                        return float(default)
                    
                    # 2. HIDE if sensor is NOT part of the Professional Gold Standard for this sector
                    if key_name not in allowed_sensors:
                        return float(default)
                        
                    # We need a unique key per machine so sliders reset when selecting a new archive
                    service_id = telemetry.get('service_id', 'live')
                    s_key = f"sim_{service_id}_{key_name}"
                    
                    safe_default = max(float(min_v), min(float(max_v), float(default)))
                    
                    # Bind value into session state correctly to avoid snap-back logic
                    if s_key not in st.session_state:
                        st.session_state[s_key] = safe_default
                        
                    return col_obj.slider(label, float(min_v), float(max_v), key=s_key)
        
                base_telemetry = telemetry.copy()
                sim_temp = smart_slider(simulator_cols[0], "Temp (°C)", "temp", bounds["temp"][0], bounds["temp"][1], base_telemetry.get('telemetry_temp', 0))
                sim_volt = smart_slider(simulator_cols[1], "Voltage (V)", "voltage", bounds["volt"][0], bounds["volt"][1], base_telemetry.get('telemetry_voltage', 0))
                sim_load = smart_slider(simulator_cols[0], "Load (%)", "load_pct", bounds["load"][0], bounds["load"][1], base_telemetry.get('telemetry_load_pct', 0))
                sim_batt = smart_slider(simulator_cols[1], "Battery (%)", "battery", bounds["batt"][0], bounds["batt"][1], base_telemetry.get('telemetry_battery', 0))
                
                sim_rpm = smart_slider(simulator_cols[0], "RPM", "rpm", bounds["rpm"][0], bounds["rpm"][1], base_telemetry.get('telemetry_rpm', 0.0))
                sim_pressure = smart_slider(simulator_cols[1], "Pressure (PSI)", "pressure", bounds["pressure"][0], bounds["pressure"][1], base_telemetry.get('telemetry_pressure', 0.0))
                sim_current = smart_slider(simulator_cols[0], "Current (A)", "current", bounds["current"][0], bounds["current"][1], base_telemetry.get('telemetry_current', 0.0))
                sim_vibration = smart_slider(simulator_cols[1], "Vibration", "vibration", bounds["vibration"][0], bounds["vibration"][1], base_telemetry.get('telemetry_vibration', 0.0))
            
            # Mutate telemetry for downstream monitors
            telemetry.update({
                "telemetry_temp": float(sim_temp), "telemetry_voltage": float(sim_volt), 
                "telemetry_load_pct": float(sim_load), "telemetry_battery": float(sim_batt),
                "telemetry_rpm": float(sim_rpm), "telemetry_pressure": float(sim_pressure), 
                "telemetry_current": float(sim_current), "telemetry_vibration": float(sim_vibration)
            })
        
        
            if st.button("EXECUTE ANALYSIS", type="primary", use_container_width=True):
                with st.spinner("Calculating Physics AI Override..."):
                    try:
                        st.session_state.live_results = run_diagnostics(telemetry, None)
                        st.session_state.live_telemetry_cache = telemetry.copy()
                    except Exception as e:
                        st.error(f"Live Simulation Error: {e}")
                    
    if st.session_state.live_results and st.session_state.live_telemetry_cache:
        st.markdown("<br>", unsafe_allow_html=True)
        render_dashboard(st.session_state.live_results, st.session_state.live_telemetry_cache, None, show_monitors=True, tab_id="live_tab")


with vision_tab:
    uploaded_file = st.file_uploader("Upload Hardware Imagery for Audit", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        st.info("Vision Intelligence Mode Active")
        st.markdown(f"#### Vision Only Analysis")
        if st.button("EXECUTE VISION AUDIT", type="primary", use_container_width=True):
            with st.spinner("Processing Imagery..."):
                try:
                    st.session_state.vision_results = run_diagnostics(None, uploaded_file)
                except Exception as e:
                    st.error(f"Vision Engine Error: {e}")
                    
    # Render Dashboard within the Vision Tab
    if st.session_state.vision_results:
        st.markdown("<br>", unsafe_allow_html=True)
        render_dashboard(st.session_state.vision_results, None, uploaded_file, tab_id="vision_tab")
