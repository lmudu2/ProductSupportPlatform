import streamlit as st

def apply_premium_styles():
    """
    Injects high-end "Modern Enterprise" aesthetics.
    Focuses on depth, mesh gradients, and immersive single-page scroll dynamics.
    """
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@500;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap');

        @keyframes pulse-glow {
            0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
            100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
        }
        
        .pulse-glow {
            animation: pulse-glow 2s infinite;
        }

        /* Root Variables - Ultra-Premium Deep Indigo & Steel Palette */
        :root {
            --primary: #4F46E5;
            --primary-light: #6366F1;
            --primary-soft: rgba(79, 70, 229, 0.08);
            --secondary: #475569;
            --background: #FCFCFD;
            --surface: rgba(255, 255, 255, 0.9);
            --border: rgba(15, 23, 42, 0.06);
            --accent: #059669;
            --text-main: #0F172A;
            --text-muted: #64748B;
            --card-radius: 20px;
            --card-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 10px 15px -3px rgba(0, 0, 0, 0.03);
            --mesh-bg: 
                radial-gradient(at 0% 0%, rgba(79, 70, 229, 0.07) 0px, transparent 45%),
                radial-gradient(at 100% 0%, rgba(5, 150, 105, 0.04) 0px, transparent 40%),
                radial-gradient(at 50% 100%, rgba(99, 102, 241, 0.03) 0px, transparent 50%);
        }

        /* Global Foundation */
        .stApp, .main, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
            background-color: var(--background) !important;
            background-image: var(--mesh-bg) !important;
            font-family: 'Inter', sans-serif;
            color: var(--text-main) !important;
        }

        /* Typography */
        h1, h2, h3, h4, h5 {
            font-family: 'Outfit', sans-serif;
            letter-spacing: -0.025em;
            font-weight: 700;
            color: #1E293B;
        }

        /* Bento-Style Refined Cards */
        .metric-card {
            background: var(--surface);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid var(--border);
            padding: 1.5rem;
            border-radius: var(--card-radius);
            margin-bottom: 1.25rem;
            box-shadow: var(--card-shadow);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 220px;
        }

        .metric-card:hover {
            transform: translateY(-2px);
            border-color: rgba(79, 70, 229, 0.3);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05);
        }

        .intel-report ul {
            margin: 0.5rem 0;
            padding-left: 1.2rem;
        }
        .intel-report li {
            margin-bottom: 0.4rem;
            font-size: 0.8rem;
            line-height: 1.4;
        }

        /* Narrative Layer */
        .intel-report {
            background: #F8FAFC !important;
            border: 1px solid var(--border) !important;
            border-left: 4px solid var(--primary) !important;
            padding: 1.25rem;
            border-radius: 12px;
            font-size: 0.9rem;
            line-height: 1.6;
            color: #334155 !important;
            box-shadow: inset 0 2px 4px 0 rgba(0,0,0,0.02);
        }

        /* Command Buttons */
        div.stButton > button {
            background: linear-gradient(135deg, var(--primary), #4338CA);
            color: white !important;
            border-radius: 12px;
            border: none;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            font-family: 'Outfit', sans-serif;
            text-transform: none;
            letter-spacing: 0.01em;
            box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2);
            transition: all 0.2s ease;
            width: 100%;
        }

        div.stButton > button:hover {
            background: linear-gradient(135deg, #4338CA, #3730A3);
            transform: translateY(-1px);
            box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.3);
            color: white !important;
        }

        /* Strategic Zone Styling */
        .zone-header {
            font-size: 1.1rem;
            font-weight: 900;
            color: var(--secondary);
            text-transform: uppercase;
            letter-spacing: 0.15em;
            margin: 2rem 0 1rem 0;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .zone-header::after {
            content: "";
            flex-grow: 1;
            height: 1px;
            background: linear-gradient(90deg, var(--border), transparent);
        }

        /* Input Standard Overrides */
        .stTextInput input, .stSelectbox [data-baseweb="select"] {
            background-color: white !important;
            border-radius: 10px !important;
            border: 1px solid var(--border) !important;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: transparent !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 40px;
            white-space: pre-wrap;
            background-color: white !important;
            border-radius: 8px 8px 0 0 !important;
            gap: 0;
            padding: 10px 20px !important;
            border: 1px solid var(--border) !important;
        }

        .stTabs [aria-selected="true"] {
            background-color: var(--primary-soft) !important;
            border-bottom: 2px solid var(--primary) !important;
            color: var(--primary) !important;
        }

        /* Metrics */
        .metric-value {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--text-main);
            font-family: 'Outfit', sans-serif;
        }
        .metric-label {
            font-size: 0.7rem;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* Procurement Specifc Consolidated Card */
        .procurement-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-left: 6px solid var(--accent);
            border-radius: var(--card-radius);
            padding: 1.75rem;
            box-shadow: var(--card-shadow);
            margin-bottom: 2rem;
        }

        .performance-chip {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 700;
            color: #475569;
        }

        .strategy-note {
            background: #F8FAFC;
            border-top: 1px dashed #E2E8F0;
            padding: 1rem;
            margin-top: 1.5rem;
            border-radius: 0 0 12px 12px;
        }

        #MainMenu, footer, header {visibility: hidden;}

        </style>
    """, unsafe_allow_html=True)

def header_component():
    """
    Ultra-Premium Hero Header with animated gradient, badges, and live status.
    """
    st.markdown("""
        <style>
        @keyframes shimmer {
            0%   { background-position: -200% center; }
            100% { background-position:  200% center; }
        }
        @keyframes dot-pulse {
            0%, 100% { opacity: 1;   transform: scale(1);   }
            50%       { opacity: 0.4; transform: scale(0.75); }
        }
        .platform-header {
            background: linear-gradient(135deg,
                rgba(79,70,229,0.10) 0%,
                rgba(99,102,241,0.06) 40%,
                rgba(5,150,105,0.07) 100%);
            border: 1px solid rgba(79,70,229,0.14);
            border-radius: 20px;
            padding: 1.8rem 2rem 1.6rem 2rem;
            margin-bottom: 1.5rem;
            position: relative;
            overflow: hidden;
        }
        .platform-header::before {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(90deg,
                transparent 0%,
                rgba(255,255,255,0.20) 50%,
                transparent 100%);
            background-size: 200% 100%;
            animation: shimmer 4s linear infinite;
            border-radius: inherit;
            pointer-events: none;
        }
        .platform-title {
            font-family: 'Outfit', sans-serif;
            font-size: 2rem;
            font-weight: 900;
            letter-spacing: -0.03em;
            line-height: 1.15;
            background: linear-gradient(135deg, #4F46E5 0%, #6366F1 50%, #059669 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0 0 0.25rem 0;
        }
        .header-status-row {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 0.65rem;
            font-weight: 700;
            color: #059669;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }
        .live-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #10B981;
            display: inline-block;
            animation: dot-pulse 1.8s ease-in-out infinite;
            box-shadow: 0 0 6px rgba(16,185,129,0.6);
            flex-shrink: 0;
        }
        .header-badges {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 1rem;
        }
        .header-badge {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 5px 13px;
            border-radius: 30px;
            font-size: 0.67rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }
        .hb-indigo {
            background: rgba(79,70,229,0.09);
            color: #4F46E5;
            border: 1px solid rgba(79,70,229,0.20);
        }
        .hb-green {
            background: rgba(5,150,105,0.09);
            color: #059669;
            border: 1px solid rgba(5,150,105,0.20);
        }
        .hb-slate {
            background: rgba(71,85,105,0.07);
            color: #475569;
            border: 1px solid rgba(71,85,105,0.16);
        }
        </style>

        <div class="platform-header">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">
                <div>
                    <div class="platform-title">Product Support &amp; Service Intelligence</div>
                    <div class="header-status-row">
                        <span class="live-dot"></span>
                        Intelligence Engine &nbsp;&middot;&nbsp; Operational
                    </div>
                </div>
                <div style="text-align:right; display:flex; flex-direction:column; align-items:flex-end; gap:4px; padding-top:4px;">
                    <div style="font-size:0.58rem; font-weight:700; color:#94A3B8; text-transform:uppercase; letter-spacing:0.1em;">Platform</div>
                    <div style="font-size:1.1rem; font-weight:900; color:#1E293B; font-family:'Outfit',sans-serif; line-height:1;">v 4.4</div>
                </div>
            </div>
            <div class="header-badges">
                <span class="header-badge hb-indigo">&#9889; AI Diagnostics</span>
                <span class="header-badge hb-slate">&#128225; Predictive Maintenance</span>
                <span class="header-badge hb-green">&#128230; Smart Procurement</span>
                <span class="header-badge hb-indigo">&#128302; Vision Inspection</span>
                <span class="header-badge hb-slate">&#9878; Repair vs. Replace</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
