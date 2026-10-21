from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st

from ai_cv_classifier.nlp_complaint_router import route_complaint

st.set_page_config(page_title="BlueHawk Civic Nexus", layout="wide")
st.title("BlueHawk Civic Nexus Command Platform")

st.caption(
    "Unified dashboard for H.A.W.K. rover telemetry, citizen complaints, GIS hazard monitoring, and peace action logs."
)

# (a) Rover Telemetry & Vision Simulator
st.header("(a) H.A.W.K. Rover Telemetry & Vision Simulator")
col1, col2, col3 = st.columns(3)
with col1:
    speed = st.slider("Speed (m/s)", 0.0, 5.0, 1.8, 0.1)
with col2:
    distance = st.slider("Obstacle Distance (cm)", 0, 300, 120)
with col3:
    uv = st.slider("UV Anomaly Index", 0, 1000, 420)

st.json(
    {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "speed_mps": speed,
        "obstacle_distance_cm": distance,
        "uv_index": uv,
        "vision_detection": "security_anomaly" if distance < 30 else "normal",
    }
)

# (b) Citizen Omni-Channel Complaint Portal
st.header("(b) Citizen Omni-Channel Mobile Complaint Portal")
complaint = st.text_area(
    "Enter complaint text / transcribed voice",
    "",
    placeholder="Example: Large garbage dump causing severe smell near Ward 8 park",
)
if st.button("Route Complaint"):
    if complaint.strip():
        decision = route_complaint(complaint)
        st.success(f"Category: {decision.category} | Priority: {decision.priority}")
        st.info(decision.reason)
    else:
        st.warning("Please enter a complaint before routing.")

# (c) GIS Ward Sustainability Heatmap & Emergency Register
st.header("(c) Live GIS Ward Sustainability Heatmap & Emergency Triage Register")
np.random.seed(42)
ward_df = pd.DataFrame(
    {
        "ward_id": [f"W-{i:02d}" for i in range(1, 13)],
        "lat": 26.45 + np.random.rand(12) * 0.12,
        "lon": 80.18 + np.random.rand(12) * 0.12,
        "severity": np.random.randint(1, 10, 12),
    }
)

st.map(ward_df.rename(columns={"lat": "latitude", "lon": "longitude"}))
st.dataframe(ward_df.sort_values("severity", ascending=False), use_container_width=True)

emergency_df = pd.DataFrame(
    [
        {"incident_id": "E-1001", "type": "Security Threat", "status": "Escalated to PCR"},
        {"incident_id": "E-1002", "type": "Public Disturbance", "status": "PCR Dispatching"},
    ]
)
st.subheader("Emergency Triage Register")
st.table(emergency_df)

# (d) Youth-Led Peace & Dialogue Circles Action Log
st.header("(d) Youth-Led Peace & Dialogue Circles Action Log")
action_note = st.text_input("Add action item")
if "action_log" not in st.session_state:
    st.session_state.action_log = []

if st.button("Add Action") and action_note.strip():
    st.session_state.action_log.append(
        {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "note": action_note.strip(),
        }
    )

if st.session_state.action_log:
    st.dataframe(pd.DataFrame(st.session_state.action_log), use_container_width=True)
else:
    st.caption("No dialogue-circle action items yet.")
