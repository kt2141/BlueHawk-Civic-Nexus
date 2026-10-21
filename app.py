import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="BlueHawk Civic Nexus", layout="wide")

# Header
st.title("🦅 BlueHawk Civic Nexus: Autonomous Rover & AI-GIS Governance Grid")
st.markdown("**Hybrid Edge-AI Street Surveillance, Citizen Complaint Portal & GIS Decision Support System**")

# Initialize live database in session state
if "incidents" not in st.session_state:
    st.session_state.incidents = pd.DataFrame([
        {"Time": "10:15 AM", "Source": "HAWK-Bot-01 (Auto)", "Category": "Emergency Threat (Police)", "Issue": "Suspicious Perimeter Breach / Unattended Object", "lat": 26.5123, "lon": 80.2329, "Severity": "CRITICAL", "Route_To": "Police Control Room (PCR)", "Status": "Active Tracking"},
        {"Time": "10:30 AM", "Source": "Citizen Mobile App", "Category": "Civic Hazard (Municipal)", "Issue": "Uncollected Waste Pile & Blocked Drain", "lat": 26.5145, "lon": 80.2351, "Severity": "HIGH", "Route_To": "Ward Sanitation & Youth Circle", "Status": "Assigned"},
        {"Time": "11:05 AM", "Source": "HAWK-Bot-02 (Auto)", "Category": "Civic Hazard (Municipal)", "Issue": "Waterlogging & Streetlight Fault", "lat": 26.5101, "lon": 80.2310, "Severity": "MEDIUM", "Route_To": "Municipal Ward Engineer", "Status": "Pending"}
    ])

# Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🤖 1. Autonomous H.A.W.K. Bot Feed",
    "📱 2. Citizen Mobile/Web Complaint",
    "🗺️ 3. Live GIS Heatmap & Police/Ward Dashboard",
    "🤝 4. Youth Dialogue & Action Log"
])

# TAB 1: AUTONOMOUS ROVER SIMULATOR & AI CLASSIFIER
with tab1:
    st.subheader("Autonomous H.A.W.K. Rover — Edge AI & Sensor Telemetry")
    col1, col2 = st.columns(2)
    with col1:
        st.info("**Live Hardware State Machine (Arduino + CV Node)**")
        dist = st.slider("Ultrasonic Sensor Target Distance (cm)", 0, 200, 45)
        ir_left = st.checkbox("Left IR Sensor Triggered")
        ir_right = st.checkbox("Right IR Sensor Triggered")
        
        if dist == 0 or dist > 120:
            state = "STATE_STOP (Scanning Perimeter)"
        elif ir_right and not ir_left:
            state = "STATE_TURN_RIGHT (Tracking Target Right)"
        elif ir_left and not ir_right:
            state = "STATE_TURN_LEFT (Tracking Target Left)"
        else:
            state = "STATE_FORWARD (Following / Patrolling)"
        st.success(f"**Current Rover Motor State:** `{state}`")

    with col2:
        st.warning("**Simulated Rover Camera / AI Vision Detection**")
        detected_Input = st.selectbox("Simulate Rover Camera / Sensor Detection:", [
            "Emergency: Suspicious Intrusion / Distress Gesture in Vulnerable Zone",
            "Emergency: Fire / Thermal UV Anomaly Detected",
            "Civic: Overflowing Garbage Pile on Street Corner",
            "Civic: Clogged Drainage & Severe Waterlogging"
        ])
        if st.button("🚨 Trigger Autonomous Bot Detection & Auto-Route"):
            is_emergency = "Emergency" in detected_Input
            new_row = {
                "Time": datetime.now().strftime("%I:%M %p"),
                "Source": "HAWK-Bot-01 (Auto CV)",
                "Category": "Emergency Threat (Police)" if is_emergency else "Civic Hazard (Municipal)",
                "Issue": detected_Input,
                "lat": 26.5123 + np.random.uniform(-0.004, 0.004),
                "lon": 80.2329 + np.random.uniform(-0.004, 0.004),
                "Severity": "CRITICAL" if is_emergency else "HIGH",
                "Route_To": "Police Control Room (PCR)" if is_emergency else "Ward Sanitation & Youth Circle",
                "Status": "Alert Dispatched"
            }
            st.session_state.incidents = pd.concat([pd.DataFrame([new_row]), st.session_state.incidents], ignore_index=True)
            st.toast("Detection classified by AI and routed automatically!")

# TAB 2: CITIZEN MOBILE / WEB REPORTING PORTAL
with tab2:
    st.subheader("📱 Citizen Omni-Channel Reporting Portal (Mobile / Web)")
    with st.form("citizen_form"):
        complaint_text = st.text_input("Describe the Street Issue or Emergency:", placeholder="e.g., Garbage dump near Ward 4 park or broken streetlight...")
        uploaded_img = st.file_uploader("Upload Photo from Mobile (Optional)", type=["jpg", "png", "jpeg"])
        submit_btn = st.form_submit_button("Submit to AI Classifier")
        
        if submit_btn and complaint_text:
            emergency_keywords = ["attack", "fire", "thief", "weapon", "emergency", "danger", "police", "intruder", "accident"]
            is_emerg = any(k in complaint_text.lower() for k in emergency_keywords)
            new_row = {
                "Time": datetime.now().strftime("%I:%M %p"),
                "Source": "Citizen Mobile Web",
                "Category": "Emergency Threat (Police)" if is_emerg else "Civic Hazard (Municipal)",
                "Issue": complaint_text,
                "lat": 26.5123 + np.random.uniform(-0.004, 0.004),
                "lon": 80.2329 + np.random.uniform(-0.004, 0.004),
                "Severity": "CRITICAL" if is_emerg else "MEDIUM",
                "Route_To": "Police Control Room (PCR)" if is_emerg else "Municipal Ward Dashboard",
                "Status": "Logged & Mapped"
            }
            st.session_state.incidents = pd.concat([pd.DataFrame([new_row]), st.session_state.incidents], ignore_index=True)
            st.success(f"AI Classified as **{'EMERGENCY (Sent to Police)' if is_emerg else 'CIVIC ISSUE (Sent to Municipality)'}**!")

# TAB 3: LIVE GIS HEATMAP & COMMAND DASHBOARD
with tab3:
    st.subheader("🗺️ Real-Time Ward GIS Hotspot Map & Automated Triage Register")
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Active Detections", len(st.session_state.incidents))
    m2.metric("Police PCR Emergency Alerts", len(st.session_state.incidents[st.session_state.incidents["Category"].str.contains("Emergency")]))
    m3.metric("Municipal & Youth Civic Tasks", len(st.session_state.incidents[st.session_state.incidents["Category"].str.contains("Civic")]))
    
    st.map(st.session_state.incidents[["lat", "lon"]])
    st.dataframe(st.session_state.incidents, use_container_width=True)

# TAB 4: YOUTH ACTION LOG & DIALOGUE CIRCLES
with tab4:
    st.subheader("🤝 Youth-Led Peace & Dialogue Circles — Ward Action Log")
    st.write("Bridging *Technology Precision* with *Community Empathy* (Dwividhta Framework):")
    st.table(pd.DataFrame([
        {"Ward": "Ward 12 (Kanpur)", "Activity": "Youth Environmental Audit & Rover Escort", "Volunteers": 14, "Impact": "Cleared 3 waste hotspots; 35% faster municipal pickup"},
        {"Ward": "Ward 05 (Kanpur)", "Activity": "Peace & Dialogue Circle on Drainage & Sanitation", "Volunteers": 22, "Impact": "Resolved resident-municipal deadlock on clogged drain"}
    ]))
