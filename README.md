# 🦅 BlueHawk Civic Nexus
**An Autonomous Edge-AI Street Patrol Rover (H.A.W.K.) & GIS Urban Governance Grid (BlueBridge) for Proactive Emergency Threat Alerting and Sustainable Municipal Action**

*Submitted to **Hack for Social Cause (HSC) — Viksit Bharat Young Leaders Dialogue (VBYLD) 2027** | Ministry of Youth Affairs & Sports (MoYAS), Govt. of India & IIT Bombay*
> **Author:** [Aravind K. T. (Aravind Koolagurki Thimmarayappa) — Official Digital Portfolio & Command Center](https://kt2141.github.io/)

🔗 **Innovator Digital Portfolio & Live Project Hub:** [https://sites.google.com/view/aravind-k-t-iitk/](https://sites.google.com/view/aravind-k-t-iitk/)

---

## 📌 1. Problem Context & The Hybrid Vision
Indian cities and high-footfall vulnerable zones face a dual visibility crisis:
1. **Municipal & Environmental Blind Spots:** Uncollected waste piles, clogged drainage, waterlogging, and broken civic infrastructure remain unaddressed due to scattered complaint channels, unoptimized sanitation worker routes, and invisible ward-level governance gaps.
2. **Street-Level Public Safety & Emergency Gaps:** Vulnerable tourist corridors, campuses, and crowded urban wards lack low-cost, autonomous mobile surveillance capable of detecting perimeter breaches, distress gestures, or fire/thermal anomalies in real time.

**BlueHawk Civic Nexus** fuses two self-developed innovations into one closed-loop hardware-software ecosystem:
* **H.A.W.K. (Human-Tracking Autonomous Rover):** A 4-wheel Arduino + Edge-CV mobile sentinel utilizing Ultrasonic, IR, UV, and Computer Vision bounding-box detection to autonomously patrol streets and track anomalies safely.
* **BlueBridge Civic Nexus (AI + PostGIS Governance Grid):** An omni-channel AI/NLP & Computer Vision classifier that ingests both **automated H.A.W.K. rover detections** and **citizen mobile/web complaints**, routing **Emergency Threats** directly to the Police Control Room (PCR) and **Civic Hazards** onto a real-time PostgreSQL/PostGIS Ward Sustainability Heatmap backed by **Youth-Led Peace & Dialogue Circles**.

---

## ⚙️ 2. System Architecture & Dual Routing Flow
```text
[Input Channel 1: Autonomous H.A.W.K. Patrol Rover]     [Input Channel 2: Citizen Mobile Web/App Portal]
 (Arduino Uno + Ultrasonic/IR/UV + Edge CV Camera)       (Geo-tagged Photo, Voice, or Text Grievance)
                        │                                                       │
                        └───────────────────►  +  ◄─────────────────────────────┘
                                               │
                             [BlueHawk AI/ML & CV Triage Engine]
                             (OpenCV/YOLO Vision + Python NLP)
                                               │
                 ┌─────────────────────────────┴─────────────────────────────┐
                 ▼                                                           ▼
   🚨 PATH A: EMERGENCY THREATS                                ♻️ PATH B: MUNICIPAL & CIVIC HAZARDS
   • Triggers: Intrusion, Distress, Fire/UV Anomaly            • Triggers: Waste Piles, Blocked Drains, Waterlogging
   • Rover Action: Non-aggressive target tracking              • GIS Action: PostgreSQL/PostGIS Green-to-Red Heatmap
   • Alert: Live Bounding-Box & GPS to Police (PCR)            • Resolution: Optimized Sanitation Routes + Youth Action Log
