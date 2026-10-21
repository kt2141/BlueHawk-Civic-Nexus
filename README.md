# BlueHawk Civic Nexus

BlueHawk Civic Nexus is an integrated hybrid civic-tech and public safety platform that combines:

- **H.A.W.K.**: autonomous edge-AI ground rovers for street telemetry, hazard sensing, and vision alerts.
- **BlueBridge**: a centralized GIS-enabled municipal and emergency response grid for triage, routing, and ward-level operations.

## 1) Architecture & System Overview

### Dual-Pipeline Ingestion

BlueHawk Civic Nexus ingests two real-time channels:

1. **Autonomous rover telemetry + vision feeds (H.A.W.K.)**
   - Ultrasonic, IR, UV, and edge-camera metadata from rovers.
   - Edge CV detections (YOLO/OpenCV) with confidence and geotags.
2. **Omni-channel citizen complaints (mobile/web/voice-to-text)**
   - Citizen issue reports with location, free text, and optional media.

### AI/CV + NLP Triage and Routing Engine

Incoming events are normalized into a shared incident envelope and triaged by:

- **Computer Vision classifier** for on-road security anomalies and municipal hazards (waste/drainage/environment).
- **NLP complaint router** for keyword + sentiment-assisted complaint categorization.

Routing policy:

- **Emergency Security Threats** -> direct escalation to **Police Control Room (PCR)** queue.
- **Municipal / Environmental Hazards** -> persistence in **PostgreSQL/PostGIS** with severity scoring for ward dashboards.

### GIS Operations Layer

- PostGIS-backed geospatial storage and ward indexing.
- Ward Sustainability Heatmap with green-to-red severity overlays.
- Resolution loop tracking for governance accountability and service closure analytics.

### Reference Modules in This Repository

- `/hardware_rover_HAWK` - Embedded rover firmware + wiring map.
- `/ai_cv_classifier` - CV stream detection and complaint NLP routing scripts.
- `/backend_gis_dashboard` - Streamlit command dashboard and PostGIS schema.
- `/sample_data` - Standardized test vectors for triage validation.

## 2) Innovator Background

Developed by **Aravind K T** — Electrical Engineering undergraduate at the **Indian Institute of Technology (IIT) Kanpur**, **Devbhoomi Rashtriya Ratna Awardee**, **UN Social Forum Delegate (Geneva)**, **NTU Singapore i-SEA Fellow**, and former **Secretary of the Public Policy & Opinion Cell (IIT Kanpur)**.

Portfolio: https://sites.google.com/view/aravind-k-t-iitk/

## 3) Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run backend_gis_dashboard/app.py
```

## 4) Open-Source Notice

This repository provides a production-ready open-source project structure with modular code artifacts that can be extended for municipal deployments, field pilot integration, and emergency command center interoperability.
