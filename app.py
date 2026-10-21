"""
BlueHawk Civic Nexus | National Innovation Dashboard
H.A.W.K. Autonomous Edge-AI Street Rover  +  BlueBridge GIS Urban Governance Grid

Run:   pip install streamlit pandas numpy pillow
       streamlit run app.py

All data is simulated for demonstration. Streamlit's bundled pydeck is used for maps.
"""

import io
import math
import random
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ----------------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------------
PORTFOLIO_URL = "https://sites.google.com/view/aravind-k-t-iitk/"
GITHUB_URL = "https://github.com/"          # TODO: replace with your repository URL
DOCS_URL = "https://sites.google.com/view/aravind-k-t-iitk/"  # TODO: replace with live docs URL

DECK_FILE = "BlueHawk_-main_ppt.docx"
COMPENDIUM_FILE = "BlueHawk_Civic_Nexus_Design_Compendium.docx"

st.set_page_config(
    page_title="BlueHawk Civic Nexus | National Innovation Dashboard",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# STYLING
# ----------------------------------------------------------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
:root{
  --bg:#070b14; --panel:#0e1626; --panel2:#131f35; --line:#22314d;
  --txt:#e8eefc; --mut:#8fa3c7; --blue:#3b82f6; --cyan:#22d3ee;
  --green:#22c55e; --amber:#f59e0b; --red:#ef4444; --violet:#8b5cf6;
}
html, body, [class*="css"], .stApp {font-family:'Inter',sans-serif;}
.stApp{
  background:
    radial-gradient(1200px 600px at 10% -10%, rgba(59,130,246,.18), transparent 60%),
    radial-gradient(900px 500px at 100% 0%, rgba(34,211,238,.12), transparent 55%),
    var(--bg);
  color:var(--txt);
}
.block-container{padding-top:1.2rem; max-width:1500px;}
header[data-testid="stHeader"]{background:transparent;}
section[data-testid="stSidebar"]{background:#0a1120; border-right:1px solid var(--line);}

.hero{
  position:relative; overflow:hidden; border:1px solid var(--line); border-radius:22px;
  padding:30px 34px; margin-bottom:14px;
  background:linear-gradient(135deg, rgba(20,34,64,.95), rgba(9,15,30,.95));
  box-shadow:0 20px 60px rgba(0,0,0,.45);
}
.hero:before{content:""; position:absolute; inset:-40% -10% auto auto; width:520px; height:520px;
  background:radial-gradient(circle, rgba(59,130,246,.35), transparent 65%); filter:blur(10px);}
.hero h1{margin:0; font-size:2.35rem; font-weight:800; letter-spacing:-.02em;
  background:linear-gradient(90deg,#fff,#9cc4ff 55%,#22d3ee); -webkit-background-clip:text; background-clip:text; color:transparent;}
.hero p.sub{margin:6px 0 16px; color:var(--mut); font-size:1.05rem; max-width:980px;}
.badge{display:inline-block; padding:5px 12px; margin:3px 6px 3px 0; border-radius:999px; font-size:.76rem; font-weight:600;
  border:1px solid var(--line); background:rgba(255,255,255,.04); color:var(--txt);}
.badge.b{border-color:rgba(59,130,246,.6); color:#9cc4ff;}
.badge.g{border-color:rgba(34,197,94,.6); color:#86efac;}
.badge.a{border-color:rgba(245,158,11,.6); color:#fcd34d;}
.badge.r{border-color:rgba(239,68,68,.6); color:#fca5a5;}
.badge.v{border-color:rgba(139,92,246,.6); color:#c4b5fd;}
.credit{margin-top:8px; padding:12px 16px; border-radius:14px; background:rgba(59,130,246,.10);
  border:1px solid rgba(59,130,246,.35); font-size:.92rem; line-height:1.55;}
.links a{display:inline-block; margin:10px 10px 0 0; padding:8px 16px; border-radius:10px; text-decoration:none!important;
  font-weight:600; font-size:.85rem; color:#fff!important; background:linear-gradient(90deg,#2563eb,#0ea5e9);
  box-shadow:0 6px 18px rgba(37,99,235,.35); transition:transform .15s;}
.links a:hover{transform:translateY(-2px);}

.card{background:linear-gradient(180deg,var(--panel2),var(--panel)); border:1px solid var(--line);
  border-radius:16px; padding:16px 18px; margin-bottom:10px;}
.kpi{background:linear-gradient(180deg,var(--panel2),var(--panel)); border:1px solid var(--line);
  border-radius:16px; padding:14px 16px; position:relative; overflow:hidden;}
.kpi:after{content:""; position:absolute; left:0; top:0; bottom:0; width:4px; background:var(--accent,#3b82f6);}
.kpi .l{font-size:.72rem; text-transform:uppercase; letter-spacing:.09em; color:var(--mut); font-weight:600;}
.kpi .v{font-size:1.9rem; font-weight:800; line-height:1.15; margin-top:2px;}
.kpi .s{font-size:.78rem; color:var(--mut);}
.sec{font-size:1.15rem; font-weight:700; margin:6px 0 8px; display:flex; align-items:center; gap:8px;}
.sec small{color:var(--mut); font-weight:500; font-size:.8rem;}
.term{font-family:'JetBrains Mono',monospace; font-size:.78rem; background:#050912; color:#7dfcb0;
  border:1px solid #1a2a44; border-radius:12px; padding:12px 14px; height:290px; overflow-y:auto; line-height:1.55;}
.term .w{color:#fcd34d;} .term .e{color:#fca5a5;} .term .i{color:#93c5fd;}
.pill{display:inline-block; padding:3px 10px; border-radius:999px; font-size:.74rem; font-weight:700;}
.pill.ok{background:rgba(34,197,94,.16); color:#86efac;}
.pill.warn{background:rgba(245,158,11,.16); color:#fcd34d;}
.pill.bad{background:rgba(239,68,68,.16); color:#fca5a5;}
.pill.info{background:rgba(59,130,246,.16); color:#93c5fd;}
.cred{border:1px solid var(--line); border-radius:16px; padding:18px; height:100%;
  background:linear-gradient(160deg,rgba(59,130,246,.10),rgba(14,22,38,.9));}
.cred .ic{font-size:2rem;} .cred h4{margin:6px 0 4px; font-size:1.02rem;} .cred p{margin:0; color:var(--mut); font-size:.86rem;}
.duality{border-radius:16px; padding:18px; border:1px solid var(--line); height:100%;}
.duality.t{background:linear-gradient(160deg,rgba(34,211,238,.12),rgba(14,22,38,.9));}
.duality.c{background:linear-gradient(160deg,rgba(245,158,11,.12),rgba(14,22,38,.9));}
.stTabs [data-baseweb="tab-list"]{gap:6px; border-bottom:1px solid var(--line);}
.stTabs [data-baseweb="tab"]{background:var(--panel); border:1px solid var(--line); border-radius:12px 12px 0 0; padding:10px 16px; font-weight:600;}
.stTabs [aria-selected="true"]{background:linear-gradient(180deg,#1d3a73,#12234a)!important; color:#fff!important;}
.stButton>button, .stDownloadButton>button{border-radius:10px; font-weight:600; border:1px solid var(--line);}
.stButton>button[kind="primary"]{background:linear-gradient(90deg,#2563eb,#0ea5e9); border:none;}
.footer{text-align:center; color:var(--mut); font-size:.78rem; padding:18px 0 6px;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# DOMAIN DATA
# ----------------------------------------------------------------------------
WARDS = {
    "Ward 04 - Kalyanpur": (26.5083, 80.2420),
    "Ward 11 - Kakadeo": (26.4700, 80.3020),
    "Ward 17 - Swaroop Nagar": (26.4780, 80.3180),
    "Ward 21 - Govind Nagar": (26.4420, 80.3120),
    "Ward 26 - Arya Nagar": (26.4660, 80.3330),
    "Ward 30 - Civil Lines": (26.4730, 80.3470),
}
DEPOT = ("BlueBridge Sanitation Depot", 26.4600, 80.3200)

CATEGORIES = ["Garbage", "Drainage", "Safety Threat"]
CAT_WEIGHT = {"Garbage": 1.0, "Drainage": 1.5, "Safety Threat": 2.5}
CAT_ICON = {"Garbage": "🗑️", "Drainage": "🌊", "Safety Threat": "🚨"}
CHANNELS = ["Web Form", "Mobile App", "Helpline Text", "Rover Auto-Report"]

KEYWORDS = {
    "Safety Threat": ["fire", "knife", "weapon", "theft", "chori", "robbery", "fight", "intruder", "harass", "threat",
                      "assault", "suspicious", "dark", "unsafe", "aag", "chhedkhani", "hathiyar", "danger", "gun",
                      "लड़ाई", "आग", "चोरी", "खतरा", "हथियार", "संदिग्ध", "अंधेरा"],
    "Drainage": ["drain", "sewer", "overflow", "waterlog", "clog", "blocked", "flood", "manhole", "nali", "naala",
                 "paani", "जल", "नाली", "नाला", "सीवर", "जलभराव", "बंद", "बहाव", "गंदा पानी"],
    "Garbage": ["garbage", "waste", "trash", "litter", "dump", "kooda", "kachra", "dustbin", "smell", "plastic",
                "कचरा", "कूड़ा", "गंदगी", "डस्टबिन", "बदबू", "प्लास्टिक"],
}

SEED_DESCS = {
    "Garbage": ["Overflowing dustbin near market gate", "Kachra dump on roadside for 3 days", "Plastic litter near bus stop",
                "कूड़ा सड़क किनारे जमा है"],
    "Drainage": ["Drain blocked, water logging on lane", "Sewer overflow near school", "नाली बंद है, गंदा पानी सड़क पर",
                 "Manhole cover missing near park"],
    "Safety Threat": ["Suspicious group loitering near dark lane", "Street light dead, unsafe for women at night",
                      "Reported theft near ATM", "रात में अंधेरा, संदिग्ध लोग घूम रहे हैं"],
}

# ----------------------------------------------------------------------------
# HELPERS
# ----------------------------------------------------------------------------
def haversine_km(a_lat, a_lon, b_lat, b_lon):
    r = 6371.0
    p1, p2 = math.radians(a_lat), math.radians(b_lat)
    dphi = p2 - p1
    dl = math.radians(b_lon - a_lon)
    h = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))


def nearest_ward(lat, lon):
    return min(WARDS, key=lambda w: haversine_km(lat, lon, WARDS[w][0], WARDS[w][1]))


def classify(text, picked_category=None):
    """Lightweight bilingual (Hindi/English) keyword NLP triage with confidence scoring."""
    t = (text or "").lower()
    scores = {c: 0.0 for c in CATEGORIES}
    for cat, words in KEYWORDS.items():
        for w in words:
            if w in t:
                scores[cat] += 1.0 + 0.2 * min(len(w), 8) / 8
    if picked_category in scores:
        scores[picked_category] += 0.8
    total = sum(scores.values())
    if total == 0:
        cat = picked_category or "Garbage"
        return cat, 0.52, scores
    cat = max(scores, key=scores.get)
    conf = min(0.99, 0.55 + 0.4 * (scores[cat] / total) * min(1.0, total / 3.0) + 0.05)
    return cat, round(conf, 2), scores


def route_path(category):
    return "A - Police PCR Emergency" if category == "Safety Threat" else "B - Municipal Sanitation"


def priority_for(category, conf):
    if category == "Safety Threat":
        return "CRITICAL"
    if category == "Drainage" and conf > 0.8:
        return "HIGH"
    return "MEDIUM" if conf > 0.65 else "LOW"


def new_id():
    st.session_state.cid += 1
    return f"BH-{st.session_state.cid:04d}"


def make_complaint(channel, ward, category, desc, lat, lon, conf=None, created=None, status="Open", res_hrs=None):
    cat, c, _ = classify(desc, category)
    if category:
        cat = category if conf is not None or c < 0.6 else cat
    conf_final = conf if conf is not None else c
    return {
        "ID": new_id(), "Channel": channel, "Ward": ward, "Category": cat, "Description": desc,
        "Lat": lat, "Lon": lon, "Path": route_path(cat), "Confidence": conf_final,
        "Priority": priority_for(cat, conf_final), "Status": status,
        "Created": created or datetime.now(), "ResolvedHrs": res_hrs,
    }


def seed_complaints():
    rng = random.Random(2027)
    rows = []
    ward_bias = {"Ward 04 - Kalyanpur": 0.9, "Ward 11 - Kakadeo": 0.5, "Ward 17 - Swaroop Nagar": 0.7,
                 "Ward 21 - Govind Nagar": 0.25, "Ward 26 - Arya Nagar": 0.45, "Ward 30 - Civil Lines": 0.15}
    for ward, (la, lo) in WARDS.items():
        n = int(3 + ward_bias[ward] * 6)
        for _ in range(n):
            cat = rng.choices(CATEGORIES, weights=[5, 3, 1.5 + ward_bias[ward]])[0]
            desc = rng.choice(SEED_DESCS[cat])
            age = rng.uniform(1, 90) * (0.5 + ward_bias[ward])
            status = rng.choices(["Open", "Dispatched", "Resolved"], weights=[5, 2, 3])[0]
            res = round(rng.uniform(4, 40), 1) if status == "Resolved" else None
            rows.append(make_complaint(
                rng.choice(CHANNELS), ward, cat, desc,
                la + rng.uniform(-0.006, 0.006), lo + rng.uniform(-0.006, 0.006),
                conf=round(rng.uniform(0.66, 0.97), 2),
                created=datetime.now() - timedelta(hours=age), status=status, res_hrs=res))
    return rows


def init_state():
    ss = st.session_state
    if "init" in ss:
        return
    ss.init = True
    ss.cid = 1000
    ss.complaints = pd.DataFrame(seed_complaints())
    ss.rover = {"mode": "IDLE", "battery": 96.0, "lat": DEPOT[1], "lon": DEPOT[2], "tick": 0, "wp": 0,
                "detections": 0, "estop": False}
    ss.log = [("i", f"[{datetime.now():%H:%M:%S}] BOOT  H.A.W.K. firmware v2.7 | Arduino Uno R3 | UART 115200")]
    ss.route = None
    ss.actions = pd.DataFrame([
        {"Date": "2026-08-14", "Ward": "Ward 04 - Kalyanpur", "Grievance": "Chronic garbage dumping near market",
         "Intervention": "Cleanup drive", "Volunteers": 38, "Hours": 114, "Ward Councillor": True, "Youth Lead": True,
         "Municipal Officer": True, "Resident Welfare Assoc.": True},
        {"Date": "2026-08-29", "Ward": "Ward 17 - Swaroop Nagar", "Grievance": "Dark lanes, women safety concerns",
         "Intervention": "Lighting audit walk", "Volunteers": 22, "Hours": 66, "Ward Councillor": True, "Youth Lead": True,
         "Municipal Officer": True, "Resident Welfare Assoc.": False},
        {"Date": "2026-09-12", "Ward": "Ward 11 - Kakadeo", "Grievance": "Drain blockage before monsoon end",
         "Intervention": "Awareness session", "Volunteers": 31, "Hours": 62, "Ward Councillor": True, "Youth Lead": True,
         "Municipal Officer": False, "Resident Welfare Assoc.": True},
        {"Date": "2026-10-03", "Ward": "Ward 26 - Arya Nagar", "Grievance": "Open dumping vs. segregation gaps",
         "Intervention": "Cleanup drive", "Volunteers": 45, "Hours": 135, "Ward Councillor": True, "Youth Lead": True,
         "Municipal Officer": True, "Resident Welfare Assoc.": True},
    ])
    ss.circles = 14
    ss.verified = 41


init_state()
ss = st.session_state


def kpi(label, value, sub="", accent="#3b82f6"):
    return (f'<div class="kpi" style="--accent:{accent}"><div class="l">{label}</div>'
            f'<div class="v">{value}</div><div class="s">{sub}</div></div>')


def style_df(df, col_map):
    """Apply colour styling to a dataframe; works across pandas versions."""
    sty = df.style
    fn = getattr(sty, "map", None) or sty.applymap
    for col, mapper in col_map.items():
        if col in df.columns:
            sty = fn(mapper, subset=[col])
            fn = getattr(sty, "map", None) or sty.applymap
    return sty


def status_color(v):
    return {"Open": "background-color:#7f1d1d;color:#fecaca;font-weight:700",
            "Dispatched": "background-color:#78350f;color:#fde68a;font-weight:700",
            "Resolved": "background-color:#14532d;color:#bbf7d0;font-weight:700"}.get(v, "")


def path_color(v):
    if str(v).startswith("A"):
        return "background-color:#4c1d95;color:#ddd6fe;font-weight:700"
    return "background-color:#0c4a6e;color:#bae6fd;font-weight:700"


def prio_color(v):
    return {"CRITICAL": "color:#fca5a5;font-weight:800", "HIGH": "color:#fdba74;font-weight:700",
            "MEDIUM": "color:#fde68a", "LOW": "color:#86efac"}.get(v, "")


def sev_rgb(score):
    """Green -> amber -> red for a 0-100 severity score."""
    s = max(0.0, min(100.0, score)) / 100.0
    if s < 0.5:
        k = s / 0.5
        return [int(34 + (245 - 34) * k), int(197 + (158 - 197) * k), int(94 + (11 - 94) * k), 190]
    k = (s - 0.5) / 0.5
    return [int(245 + (239 - 245) * k), int(158 + (68 - 158) * k), int(11 + (68 - 11) * k), 200]


def ward_scores(df):
    out = []
    now = datetime.now()
    for ward, (la, lo) in WARDS.items():
        w = df[df.Ward == ward]
        op = w[w.Status != "Resolved"]
        raw = 0.0
        for _, r in op.iterrows():
            age_h = max(0.0, (now - r.Created).total_seconds() / 3600)
            raw += CAT_WEIGHT[r.Category] * (1 + min(age_h, 96) / 48)
        res = w[w.Status == "Resolved"].ResolvedHrs.dropna()
        out.append({
            "Ward": ward, "Lat": la, "Lon": lo, "Open": len(op),
            "Garbage": int((op.Category == "Garbage").sum()), "Drainage": int((op.Category == "Drainage").sum()),
            "Safety": int((op.Category == "Safety Threat").sum()),
            "AvgAgeHrs": round(float(np.mean([(now - c).total_seconds() / 3600 for c in op.Created])) if len(op) else 0, 1),
            "AvgResHrs": round(float(res.mean()), 1) if len(res) else 0.0,
            "Emergency": int(((op.Path.str.startswith("A")) & (op.Status == "Open")).sum()),
            "Severity": round(min(100.0, raw * 3.2), 1),
        })
    return pd.DataFrame(out)


def log(kind, msg):
    ss.log.append((kind, f"[{datetime.now():%H:%M:%S}] {msg}"))
    ss.log = ss.log[-60:]


# ----------------------------------------------------------------------------
# ROVER SIMULATION
# ----------------------------------------------------------------------------
PATROL_WAYPOINTS = [(WARDS[w][0] + 0.002, WARDS[w][1] - 0.002) for w in WARDS]


def rover_tick(dist_cm, ir_l, ir_r, uv, servo):
    r = ss.rover
    r["tick"] += 1
    if r["estop"]:
        log("e", "TX> MOTORS=0 | E-STOP LATCHED | awaiting manual reset")
        return
    if r["battery"] < 15 and r["mode"] != "RETURN_TO_BASE":
        r["mode"] = "RETURN_TO_BASE"
        log("w", f"PWR  low battery {r['battery']:.0f}% -> auto RTB")
    log("i", f"RX< HC-SR04={dist_cm}cm IR=[{int(ir_l)},{int(ir_r)}] UV={uv:.1f} SERVO={servo}deg")
    if r["mode"] == "PATROL":
        if dist_cm < 20:
            log("w", "NAV  obstacle <20cm -> OBSTACLE_AVOID: reverse 0.5s, servo scan L/R, re-route")
        elif ir_l and not ir_r:
            log("i", "NAV  line drift right -> M1 +12%, M2 -8%")
        elif ir_r and not ir_l:
            log("i", "NAV  line drift left -> M1 -8%, M2 +12%")
        else:
            log("i", "NAV  line locked | PWM L=180 R=180")
        if uv >= 8:
            log("w", f"SENS UV index {uv:.1f} high -> logging exposure alert")
        tgt = PATROL_WAYPOINTS[r["wp"] % len(PATROL_WAYPOINTS)]
        r["lat"] += (tgt[0] - r["lat"]) * 0.35
        r["lon"] += (tgt[1] - r["lon"]) * 0.35
        if haversine_km(r["lat"], r["lon"], tgt[0], tgt[1]) < 0.12:
            r["wp"] += 1
            log("i", f"GPS  waypoint {r['wp']} reached")
        r["battery"] = max(0.0, r["battery"] - 1.4)
    elif r["mode"] == "RETURN_TO_BASE":
        r["lat"] += (DEPOT[1] - r["lat"]) * 0.45
        r["lon"] += (DEPOT[2] - r["lon"]) * 0.45
        log("i", "NAV  RTB heading to depot")
        if haversine_km(r["lat"], r["lon"], DEPOT[1], DEPOT[2]) < 0.1:
            r["mode"] = "IDLE"
            log("i", "NAV  docked | charging")
        r["battery"] = max(0.0, r["battery"] - 0.6)
    else:
        r["battery"] = min(100.0, r["battery"] + 2.0)
        log("i", "IDLE  motors=0 | charging/standby")


def rover_state_label():
    r = ss.rover
    if r["estop"]:
        return "E_STOP", "bad"
    return r["mode"], {"PATROL": "ok", "IDLE": "info", "RETURN_TO_BASE": "warn"}.get(r["mode"], "info")


# ----------------------------------------------------------------------------
# VISION SIMULATOR
# ----------------------------------------------------------------------------
DETECT_CLASSES = {
    "Litter / Garbage pile": ("Garbage", (245, 158, 11), "litter"),
    "Drainage obstruction": ("Drainage", (34, 211, 238), "drain_block"),
    "Night-time security intrusion": ("Safety Threat", (239, 68, 68), "intruder"),
    "Thermal / fire anomaly": ("Safety Threat", (255, 90, 30), "fire"),
}


def build_frame(cls_name, conf, bx, by, bw, bh, night, thermal, seed):
    W, H = 760, 430
    rng = np.random.default_rng(seed)
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):  # sky -> ground gradient
        t = y / H
        d.line([(0, y), (W, y)], fill=(int(120 - 70 * t), int(160 - 80 * t), int(210 - 110 * t)))
    d.polygon([(0, 250), (W, 250), (W, H), (0, H)], fill=(58, 60, 66))           # road
    d.polygon([(0, 205), (W, 205), (W, 250), (0, 250)], fill=(92, 96, 90))        # footpath
    for i in range(7):                                                              # buildings
        x0 = i * 115 - 10
        h = 80 + (i * 37) % 70
        d.rectangle([x0, 205 - h, x0 + 100, 205], fill=(70 + i * 8, 74 + i * 5, 90))
        for wy in range(205 - h + 12, 195, 22):
            for wx in range(x0 + 10, x0 + 90, 26):
                d.rectangle([wx, wy, wx + 12, wy + 10], fill=(250, 220, 120) if (wx + wy) % 3 else (60, 70, 90))
    for x in range(20, W, 120):                                                     # lane marks
        d.rectangle([x, 340, x + 60, 348], fill=(220, 220, 210))
    gx, gy = int(bx * W), int(by * H)
    gw, gh = int(bw * W), int(bh * H)
    kind = DETECT_CLASSES[cls_name][2]
    if kind == "litter":
        for _ in range(26):
            px, py = gx + rng.integers(0, max(gw, 2)), gy + rng.integers(0, max(gh, 2))
            d.ellipse([px, py, px + 14, py + 10], fill=tuple(int(v) for v in rng.integers(90, 230, 3)))
    elif kind == "drain_block":
        d.rectangle([gx, gy + gh // 2, gx + gw, gy + gh], fill=(30, 36, 28))
        for k in range(0, gw, 14):
            d.line([(gx + k, gy + gh // 2), (gx + k, gy + gh)], fill=(90, 90, 80), width=2)
        d.ellipse([gx, gy + gh // 3, gx + gw, gy + gh - 4], outline=(70, 140, 160), width=3)
    elif kind == "intruder":
        cx = gx + gw // 2
        d.ellipse([cx - gw // 7, gy, cx + gw // 7, gy + gh // 5], fill=(20, 20, 24))
        d.rectangle([cx - gw // 5, gy + gh // 5, cx + gw // 5, gy + int(gh * 0.65)], fill=(18, 18, 22))
        d.rectangle([cx - gw // 5, gy + int(gh * 0.65), cx + gw // 5, gy + gh], fill=(26, 26, 34))
    elif kind == "fire":
        for _ in range(60):
            px = gx + int(rng.integers(0, max(gw, 2)))
            py = gy + gh - int(abs(rng.normal(0, gh * 0.33)))
            r = int(rng.integers(4, 14))
            d.ellipse([px - r, py - r, px + r, py + r], fill=(255, int(rng.integers(80, 220)), 20))
    arr = np.asarray(img).astype(np.float32)
    if night:
        arr *= np.array([0.22, 0.28, 0.45])
        arr += rng.normal(0, 6, arr.shape)
    if thermal:
        lum = arr.mean(axis=2) / 255.0
        if kind == "fire":
            lum[gy:gy + gh, gx:gx + gw] = np.clip(lum[gy:gy + gh, gx:gx + gw] + 0.6, 0, 1)
        arr = np.stack([np.clip(lum * 2.2, 0, 1) * 255, np.clip((lum - 0.3) * 2.0, 0, 1) * 255,
                        np.clip(1.0 - lum * 2.0, 0, 1) * 255 * 0.8], axis=2)
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    if night or thermal:
        img = img.filter(ImageFilter.GaussianBlur(0.6))
    d = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    color = DETECT_CLASSES[cls_name][1]
    d.rectangle([gx, gy, gx + gw, gy + gh], outline=color, width=3)
    for cx, cy in [(gx, gy), (gx + gw, gy), (gx, gy + gh), (gx + gw, gy + gh)]:
        d.rectangle([cx - 4, cy - 4, cx + 4, cy + 4], fill=color)
    label = f" {cls_name.split('/')[0].strip()}  {conf:.0%} "
    d.rectangle([gx, max(0, gy - 18), gx + 8 * len(label), max(18, gy)], fill=color)
    d.text((gx + 2, max(0, gy - 15)), label, fill=(0, 0, 0), font=font)
    d.rectangle([0, 0, W, 22], fill=(0, 0, 0))
    mode = "THERMAL-IR" if thermal else ("NIGHT-VISION" if night else "RGB DAY")
    d.text((8, 6), f"H.A.W.K. CAM-01 | {mode} | YOLO-sim v8n | {datetime.now():%H:%M:%S} | REC", fill=(125, 252, 176), font=font)
    d.rectangle([0, H - 20, W, H], fill=(0, 0, 0))
    d.text((8, H - 15), "EDGE INFERENCE: 28.4 ms/frame | 35 FPS | OpenCV 4.x | CPU-only", fill=(147, 197, 253), font=font)
    return img


# ----------------------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🦅 BlueHawk Control")
    st.caption("National Innovation Dashboard | Demo Environment")
    now_df = ss.complaints
    st.metric("Total complaints logged", len(now_df))
    st.metric("Open emergencies (Path A)", int(((now_df.Path.str.startswith("A")) & (now_df.Status == "Open")).sum()))
    st.metric("Rover battery", f"{ss.rover['battery']:.0f}%")
    st.divider()
    st.markdown("**Event**  \nMinistry of Youth Affairs & Sports  \nIIT Bombay VBYLD 2027")
    st.markdown("**Stack**  \nArduino Uno R3 · OpenCV/YOLO · NLP Triage · PostgreSQL/PostGIS · Streamlit")
    st.divider()
    if st.button("♻️ Reset demo data", use_container_width=True):
        for k in list(ss.keys()):
            del ss[k]
        st.rerun()

# ----------------------------------------------------------------------------
# HERO
# ----------------------------------------------------------------------------
st.markdown(f"""
<div class="hero">
  <span class="badge g">● LIVE DEMO</span><span class="badge b">Edge-AI</span><span class="badge v">GIS · PostGIS</span>
  <span class="badge a">Hackathon: MYAS × IIT Bombay VBYLD 2027</span>
  <h1>🦅 BlueHawk Civic Nexus | National Innovation Dashboard</h1>
  <p class="sub">Autonomous Edge-AI Street Surveillance, Multi-Modal Citizen Complaint Portal &amp; GIS Decision Support Grid</p>
  <div class="credit">
    <b>Developed by Aravind K. T.</b> | B.Tech Electrical Engineering, IIT Kanpur (AISHE Code: U-0517)<br>
    <span class="badge a">Devbhoomi National Awardee</span><span class="badge b">UN Geneva Delegate</span>
    <span class="badge g">NTU Singapore Fellow</span>
  </div>
  <div class="links">
    <a href="{PORTFOLIO_URL}" target="_blank">🌐 Portfolio</a>
    <a href="{GITHUB_URL}" target="_blank">💻 GitHub Repository</a>
    <a href="{DOCS_URL}" target="_blank">📄 Live Docs</a>
  </div>
</div>
""", unsafe_allow_html=True)

df_all = ss.complaints
open_df = df_all[df_all.Status != "Resolved"]
c1, c2, c3, c4, c5 = st.columns(5)
c1.markdown(kpi("Open hazards", len(open_df), "across 6 wards", "#ef4444"), unsafe_allow_html=True)
c2.markdown(kpi("Path A emergencies", int((open_df.Path.str.startswith("A")).sum()), "Police PCR alerts", "#8b5cf6"), unsafe_allow_html=True)
c3.markdown(kpi("Path B sanitation", int((open_df.Path.str.startswith("B")).sum()), "Municipal routes", "#0ea5e9"), unsafe_allow_html=True)
c4.markdown(kpi("Avg AI confidence", f"{df_all.Confidence.mean():.0%}", "NLP + vision triage", "#22c55e"), unsafe_allow_html=True)
c5.markdown(kpi("Rover detections", ss.rover["detections"], "this session", "#f59e0b"), unsafe_allow_html=True)
st.write("")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🤖 H.A.W.K. Rover Command", "📱 Citizen Reporting Portal", "🗺️ GIS Ward Heatmap & Triage",
    "🤝 Peace & Dialogue Circles", "🏆 Innovator Dossier"])

# ============================================================================
# TAB 1 - ROVER
# ============================================================================
with tab1:
    left, right = st.columns([1.15, 1])
    with left:
        st.markdown('<div class="sec">📡 Edge-Vision Bounding-Box Simulator <small>YOLO/OpenCV classification preview</small></div>',
                    unsafe_allow_html=True)
        a, b = st.columns(2)
        cls_name = a.selectbox("Detection class", list(DETECT_CLASSES.keys()))
        conf = b.slider("Model confidence", 0.40, 0.99, 0.87, 0.01)
        s1, s2, s3, s4 = st.columns(4)
        bx = s1.slider("Box X", 0.05, 0.80, 0.42, 0.01)
        by = s2.slider("Box Y", 0.30, 0.80, 0.58, 0.01)
        bw = s3.slider("Width", 0.08, 0.35, 0.18, 0.01)
        bh = s4.slider("Height", 0.08, 0.35, 0.20, 0.01)
        m1, m2 = st.columns(2)
        night = m1.toggle("🌙 Night-vision mode", value=cls_name.startswith("Night"))
        thermal = m2.toggle("🔥 Thermal-IR overlay", value=cls_name.startswith("Thermal"))
        try:
            frame = build_frame(cls_name, conf, bx, by, bw, bh, night, thermal, seed=7)
            st.image(frame, use_container_width=True)
        except Exception as exc:  # robust fallback so the demo never crashes
            st.error(f"Frame renderer error: {exc}")
        cat_pick = DETECT_CLASSES[cls_name][0]
        st.markdown(
            f'<span class="pill info">Class → {cat_pick}</span> '
            f'<span class="pill {"bad" if cat_pick == "Safety Threat" else "ok"}">Route → {route_path(cat_pick)}</span> '
            f'<span class="pill warn">Conf {conf:.0%}</span>', unsafe_allow_html=True)
        if st.button("📤 Send detection as Rover Auto-Report", type="primary", use_container_width=True):
            la, lo = ss.rover["lat"], ss.rover["lon"]
            ward = nearest_ward(la, lo)
            row = make_complaint("Rover Auto-Report", ward, cat_pick,
                                 f"[H.A.W.K. CAM-01] {cls_name} detected, conf {conf:.0%}", la, lo, conf=round(conf, 2))
            ss.complaints = pd.concat([ss.complaints, pd.DataFrame([row])], ignore_index=True)
            ss.rover["detections"] += 1
            log("w" if cat_pick == "Safety Threat" else "i",
                f"TX> REPORT {row['ID']} {cls_name} -> {row['Path']} | ward {ward}")
            st.success(f"Report {row['ID']} routed to {row['Path']} - see GIS tab.")
            st.rerun()

    with right:
        st.markdown('<div class="sec">🧠 Hardware State Machine <small>Arduino Uno R3 + Adafruit Motor Shield</small></div>',
                    unsafe_allow_html=True)
        label, cls = rover_state_label()
        r = ss.rover
        st.markdown(
            f'<div class="card"><span class="pill {cls}" style="font-size:.95rem">STATE: {label}</span> '
            f'&nbsp;<span class="pill info">Tick {r["tick"]}</span> '
            f'<span class="pill {"ok" if r["battery"] > 30 else "bad"}">Battery {r["battery"]:.0f}%</span><br>'
            f'<span style="color:var(--mut);font-size:.82rem">GPS {r["lat"]:.5f}, {r["lon"]:.5f}</span></div>',
            unsafe_allow_html=True)
        k1, k2 = st.columns(2)
        dist = k1.slider("HC-SR04 distance (cm)", 2, 200, 85)
        servo = k2.slider("Servo scan angle (°)", 0, 180, 90)
        k3, k4, k5 = st.columns(3)
        ir_l = k3.toggle("IR left on line", True)
        ir_r = k4.toggle("IR right on line", True)
        uv = k5.slider("UV index", 0.0, 12.0, 3.2, 0.1)

        b1, b2, b3 = st.columns(3)
        if b1.button("🛑 EMERGENCY STOP", use_container_width=True):
            r["estop"] = True
            r["mode"] = "IDLE"
            log("e", "CMD  EMERGENCY STOP -> relay open, motors=0, brake engaged")
            st.rerun()
        if b2.button("▶️ Autonomous Patrol", use_container_width=True):
            r["estop"] = False
            r["mode"] = "PATROL"
            log("i", "CMD  AUTONOMOUS PATROL engaged | geofence = 6 wards")
            st.rerun()
        if b3.button("🏠 Return to Base", use_container_width=True):
            r["estop"] = False
            r["mode"] = "RETURN_TO_BASE"
            log("w", "CMD  RETURN TO BASE")
            st.rerun()
        t1, t2 = st.columns(2)
        if t1.button("⏱️ Advance 1 tick", use_container_width=True):
            rover_tick(dist, ir_l, ir_r, uv, servo)
            st.rerun()
        if t2.button("⏩ Advance 5 ticks", use_container_width=True):
            for _ in range(5):
                rover_tick(dist, ir_l, ir_r, uv, servo)
            st.rerun()
        if r["estop"] and st.button("🔓 Reset E-STOP latch", use_container_width=True):
            r["estop"] = False
            log("i", "CMD  E-STOP latch cleared by operator")
            st.rerun()

        st.markdown('<div class="sec">📟 Live UART Telemetry</div>', unsafe_allow_html=True)
        html = "<br>".join(f'<span class="{k}">{m}</span>' for k, m in ss.log[-25:][::-1])
        st.markdown(f'<div class="term">{html}</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec">🧩 Sensor Suite Status</div>', unsafe_allow_html=True)
    sc = st.columns(5)
    sc[0].markdown(kpi("Ultrasonic", f"{dist} cm", "OBSTACLE" if dist < 20 else "CLEAR", "#ef4444" if dist < 20 else "#22c55e"), unsafe_allow_html=True)
    sc[1].markdown(kpi("IR line", f"{int(ir_l)}|{int(ir_r)}", "LOCKED" if ir_l and ir_r else "DRIFT", "#22c55e" if ir_l and ir_r else "#f59e0b"), unsafe_allow_html=True)
    sc[2].markdown(kpi("UV sensor", f"{uv:.1f}", "HIGH" if uv >= 8 else "NORMAL", "#f59e0b" if uv >= 8 else "#22c55e"), unsafe_allow_html=True)
    sc[3].markdown(kpi("Servo", f"{servo}°", "scanning", "#8b5cf6"), unsafe_allow_html=True)
    sc[4].markdown(kpi("Motor shield", "ARMED" if not r["estop"] else "LOCKED", "Adafruit v2", "#0ea5e9" if not r["estop"] else "#ef4444"), unsafe_allow_html=True)

# ============================================================================
# TAB 2 - CITIZEN PORTAL
# ============================================================================
with tab2:
    st.markdown('<div class="sec">📱 Omni-Channel Citizen Reporting <small>Web · Mobile · Helpline · Rover</small></div>',
                unsafe_allow_html=True)
    fcol, pcol = st.columns([1.2, 1])
    with fcol:
        channel = st.radio("Input channel", CHANNELS, horizontal=True)
        ward_pick = st.selectbox("Ward", list(WARDS.keys()))
        cat_in = st.selectbox("Hazard category", CATEGORIES, format_func=lambda c: f"{CAT_ICON[c]} {c}")
        lang = st.radio("Description language", ["English", "हिन्दी"], horizontal=True)
        placeholder = ("e.g. Drain is blocked and dirty water is overflowing near the school"
                       if lang == "English" else "उदाहरण: स्कूल के पास नाली बंद है और गंदा पानी बह रहा है")
        desc = st.text_area("Describe the issue", placeholder=placeholder, height=110, key="desc_in")
        up = st.file_uploader("Upload sample image (optional)", type=["png", "jpg", "jpeg"])
        if up is not None:
            try:
                st.image(Image.open(io.BytesIO(up.getvalue())), caption="Evidence attached", width=240)
            except Exception:
                st.warning("Could not preview this image, it will still be attached.")
        base_la, base_lo = WARDS[ward_pick]
        g1, g2 = st.columns(2)
        lat_in = g1.number_input("Latitude", value=float(round(base_la, 5)), format="%.5f", step=0.0005)
        lon_in = g2.number_input("Longitude", value=float(round(base_lo, 5)), format="%.5f", step=0.0005)
        st.map(pd.DataFrame({"lat": [lat_in], "lon": [lon_in]}), size=40)

    with pcol:
        st.markdown('<div class="sec">🧠 Instant AI / NLP Triage Preview</div>', unsafe_allow_html=True)
        pred_cat, pred_conf, sc_map = classify(desc, cat_in)
        path = route_path(pred_cat)
        prio = priority_for(pred_cat, pred_conf)
        tone = "bad" if pred_cat == "Safety Threat" else "ok"
        st.markdown(f"""
        <div class="card">
          <div style="color:var(--mut);font-size:.75rem;text-transform:uppercase;letter-spacing:.08em">Predicted class</div>
          <div style="font-size:1.7rem;font-weight:800">{CAT_ICON[pred_cat]} {pred_cat}</div>
          <div style="margin:8px 0"><span class="pill {tone}">Priority {prio}</span>
          <span class="pill info">Path {path}</span></div>
          <div style="color:var(--mut);font-size:.8rem">Auto-assigned to: <b style="color:#fff">
          {"Police Control Room (PCR) + Ward Councillor" if pred_cat == "Safety Threat" else "Municipal Sanitation Division, nearest vehicle"}</b></div>
        </div>""", unsafe_allow_html=True)
        st.progress(float(pred_conf), text=f"Model confidence: {pred_conf:.0%}")
        if pred_conf < 0.65:
            st.warning("Low confidence → flagged for human-in-the-loop verification.")
        tot = sum(sc_map.values()) or 1.0
        prob_df = pd.DataFrame({"Class": list(sc_map.keys()), "Score": [v / tot for v in sc_map.values()]}).set_index("Class")
        st.bar_chart(prob_df, height=180)
        if st.button("✅ Submit complaint", type="primary", use_container_width=True):
            if not desc.strip():
                st.error("Please describe the issue before submitting (Hindi or English).")
            else:
                final_ward = nearest_ward(lat_in, lon_in)
                row = make_complaint(channel, final_ward, pred_cat, desc.strip(), float(lat_in), float(lon_in),
                                     conf=pred_conf)
                ss.complaints = pd.concat([ss.complaints, pd.DataFrame([row])], ignore_index=True)
                log("w" if pred_cat == "Safety Threat" else "i", f"CITIZEN {row['ID']} via {channel} -> {row['Path']}")
                st.success(f"Complaint **{row['ID']}** filed in {final_ward} and routed to **{row['Path']}**. "
                           "Open the GIS tab to see it on the heatmap.")
                st.balloons()
    st.markdown('<div class="sec">🧾 Latest submissions</div>', unsafe_allow_html=True)
    recent = ss.complaints.sort_values("Created", ascending=False).head(6)[["ID", "Channel", "Ward", "Category", "Confidence", "Path", "Status"]]
    st.dataframe(style_df(recent, {"Status": status_color, "Path": path_color}), use_container_width=True, hide_index=True)

# ============================================================================
# TAB 3 - GIS
# ============================================================================
with tab3:
    st.markdown('<div class="sec">🗺️ Live GIS Ward Sustainability Heatmap <small>PostGIS-style spatial aggregation</small></div>',
                unsafe_allow_html=True)
    ws = ward_scores(ss.complaints)
    ws["color"] = ws.Severity.apply(sev_rgb)
    ws["radius"] = 350 + ws.Severity * 6
    ws["Label"] = ws.Ward + " | Severity " + ws.Severity.astype(str)

    mcol, scol = st.columns([1.6, 1])
    with mcol:
        pts = ss.complaints[ss.complaints.Status != "Resolved"].copy()
        pts["color"] = pts.Category.map({"Garbage": [245, 158, 11, 210], "Drainage": [34, 211, 238, 210], "Safety Threat": [239, 68, 68, 230]})
        layers = [
            pdk.Layer("ScatterplotLayer", ws, get_position="[Lon, Lat]", get_fill_color="color", get_radius="radius",
                      pickable=True, opacity=0.35, stroked=True, get_line_color=[255, 255, 255, 120], line_width_min_pixels=1),
            pdk.Layer("HeatmapLayer", pts, get_position="[Lon, Lat]", aggregation="SUM", radius_pixels=70, opacity=0.55),
            pdk.Layer("ScatterplotLayer", pts, get_position="[Lon, Lat]", get_fill_color="color", get_radius=55, pickable=True),
        ]
        if ss.route:
            layers.append(pdk.Layer("PathLayer", [{"path": ss.route["coords"]}], get_path="path", get_color=[59, 130, 246],
                                    width_min_pixels=4))
            layers.append(pdk.Layer("ScatterplotLayer", pd.DataFrame({"Lon": [DEPOT[2]], "Lat": [DEPOT[1]]}),
                                    get_position="[Lon, Lat]", get_fill_color=[255, 255, 255, 255], get_radius=120))
        view = pdk.ViewState(latitude=26.472, longitude=80.318, zoom=11.3, pitch=35)
        try:
            st.pydeck_chart(pdk.Deck(layers=layers, initial_view_state=view,
                                     tooltip={"text": "{Label}{ID} {Category}\n{Description}"}), height=520)
        except Exception as exc:
            st.error(f"Map render error: {exc}")
            st.map(pts.rename(columns={"Lat": "lat", "Lon": "lon"})[["lat", "lon"]])
        st.markdown('<span class="pill ok">Low severity</span> <span class="pill warn">Moderate</span> '
                    '<span class="pill bad">Critical</span> &nbsp; Dots: 🟠 Garbage · 🔵 Drainage · 🔴 Safety', unsafe_allow_html=True)
    with scol:
        st.markdown('<div class="sec">🏙️ Ward Scorecard</div>', unsafe_allow_html=True)
        sel = st.selectbox("Select ward", ws.Ward.tolist())
        w = ws[ws.Ward == sel].iloc[0]
        sev = w.Severity
        tone = "#22c55e" if sev < 35 else ("#f59e0b" if sev < 65 else "#ef4444")
        st.markdown(kpi("Sustainability severity", f"{sev:.0f}/100", "higher = worse", tone), unsafe_allow_html=True)
        st.write("")
        a, b = st.columns(2)
        a.markdown(kpi("Open hazards", int(w.Open), f"🗑️{int(w.Garbage)} 🌊{int(w.Drainage)} 🚨{int(w.Safety)}", "#3b82f6"), unsafe_allow_html=True)
        b.markdown(kpi("Avg age", f"{w.AvgAgeHrs:.0f} h", "open items", "#f59e0b"), unsafe_allow_html=True)
        a.markdown(kpi("Avg resolution", f"{w.AvgResHrs:.0f} h", "closed items", "#22c55e"), unsafe_allow_html=True)
        b.markdown(kpi("Active alerts", int(w.Emergency), "Path A open", "#8b5cf6"), unsafe_allow_html=True)
        if w.Emergency > 0:
            st.error(f"🚨 {int(w.Emergency)} active emergency alert(s) in {sel}: PCR notified.")
        st.bar_chart(ws.set_index("Ward")[["Garbage", "Drainage", "Safety"]], height=210)

    st.markdown('<div class="sec">📋 Automated Triage Register <small>Path A: Police PCR · Path B: Municipal Sanitation</small></div>',
                unsafe_allow_html=True)
    f1, f2, f3 = st.columns(3)
    f_path = f1.selectbox("Path", ["All", "Path A - Police PCR", "Path B - Municipal Sanitation"])
    f_stat = f2.selectbox("Status", ["All", "Open", "Dispatched", "Resolved"])
    f_ward = f3.selectbox("Ward filter", ["All"] + list(WARDS.keys()))
    reg = ss.complaints.copy()
    if f_path.startswith("Path A"):
        reg = reg[reg.Path.str.startswith("A")]
    elif f_path.startswith("Path B"):
        reg = reg[reg.Path.str.startswith("B")]
    if f_stat != "All":
        reg = reg[reg.Status == f_stat]
    if f_ward != "All":
        reg = reg[reg.Ward == f_ward]
    reg = reg.sort_values("Created", ascending=False)
    show = reg[["ID", "Created", "Channel", "Ward", "Category", "Description", "Confidence", "Priority", "Path", "Status"]].copy()
    show["Created"] = show.Created.dt.strftime("%d %b %H:%M")
    st.dataframe(style_df(show, {"Status": status_color, "Path": path_color, "Priority": prio_color}),
                 use_container_width=True, hide_index=True, height=320)

    u1, u2, u3 = st.columns([1.3, 1, 1])
    with u1:
        ids = ss.complaints.ID.tolist()[::-1]
        pick_id = st.selectbox("Update complaint", ids)
        new_status = st.radio("New status", ["Open", "Dispatched", "Resolved"], horizontal=True)
        if st.button("Apply status update", use_container_width=True):
            idx = ss.complaints.index[ss.complaints.ID == pick_id][0]
            ss.complaints.at[idx, "Status"] = new_status
            if new_status == "Resolved":
                age = (datetime.now() - ss.complaints.at[idx, "Created"]).total_seconds() / 3600
                ss.complaints.at[idx, "ResolvedHrs"] = round(max(age, 0.5), 1)
            st.rerun()
    with u2:
        st.write("")
        if st.button("🚛 Generate Optimized Sanitation Route", type="primary", use_container_width=True):
            todo = ss.complaints[(ss.complaints.Path.str.startswith("B")) & (ss.complaints.Status == "Open")]
            if todo.empty:
                st.info("No open Path B items. Nothing to route.")
            else:
                remaining = todo.to_dict("records")
                cur = (DEPOT[1], DEPOT[2])
                order, total = [], 0.0
                while remaining:  # nearest-neighbour heuristic, weighted by priority
                    nxt = min(remaining, key=lambda r: haversine_km(cur[0], cur[1], r["Lat"], r["Lon"]) /
                              (1.5 if r["Priority"] == "HIGH" else 1.0))
                    total += haversine_km(cur[0], cur[1], nxt["Lat"], nxt["Lon"])
                    cur = (nxt["Lat"], nxt["Lon"])
                    order.append(nxt)
                    remaining.remove(nxt)
                total += haversine_km(cur[0], cur[1], DEPOT[1], DEPOT[2])
                coords = [[DEPOT[2], DEPOT[1]]] + [[o["Lon"], o["Lat"]] for o in order] + [[DEPOT[2], DEPOT[1]]]
                ss.route = {"coords": coords, "stops": order, "km": total}
                st.rerun()
    with u3:
        st.write("")
        wards_txt = "\n".join(f"{r.Ward}: severity {r.Severity}, open {r.Open}, emergencies {r.Emergency}, avg resolution {r.AvgResHrs}h"
                              for r in ws.itertuples())
        report = (f"BLUEHAWK CIVIC NEXUS - OFFICIAL WARD REPORT\nGenerated: {datetime.now():%d %b %Y %H:%M}\n"
                  f"Prepared for: Municipal Commissioner / PCR Control\n{'-' * 60}\n{wards_txt}\n{'-' * 60}\n"
                  f"Total complaints: {len(ss.complaints)} | Open: {int((ss.complaints.Status != 'Resolved').sum())}\n"
                  "Note: demonstration data.\n\nFULL REGISTER (CSV) FOLLOWS\n\n")
        report += ss.complaints.drop(columns=["ResolvedHrs"]).to_csv(index=False)
        st.download_button("📄 Export Official Ward Report", report.encode("utf-8"),
                           file_name=f"BlueHawk_Ward_Report_{datetime.now():%Y%m%d_%H%M}.txt", mime="text/plain",
                           use_container_width=True)
    if ss.route:
        st.success(f"Optimized route: {len(ss.route['stops'])} stops · {ss.route['km']:.1f} km · "
                   f"est. {ss.route['km'] / 18 * 60 + len(ss.route['stops']) * 6:.0f} min incl. service time")
        rd = pd.DataFrame([{"Stop": i + 1, "ID": s["ID"], "Ward": s["Ward"], "Category": s["Category"], "Priority": s["Priority"]}
                           for i, s in enumerate(ss.route["stops"])])
        st.dataframe(rd, use_container_width=True, hide_index=True)

# ============================================================================
# TAB 4 - PEACE CIRCLES
# ============================================================================
with tab4:
    st.markdown('<div class="sec">🤝 Youth-Led Peace &amp; Dialogue Circles <small>Dwividhta (Design Duality) framework</small></div>',
                unsafe_allow_html=True)
    d1, d2 = st.columns(2)
    d1.markdown("""<div class="duality t"><h4>⚙️ Technology Precision</h4>
    <p style="color:var(--mut);margin:0">Edge-AI detection, PostGIS spatial triage, severity scoring and optimised routing give every
    grievance a verifiable, time-stamped, geo-tagged record.</p></div>""", unsafe_allow_html=True)
    d2.markdown("""<div class="duality c"><h4>💛 Community Empathy</h4>
    <p style="color:var(--mut);margin:0">Youth-led dialogue circles listen first, verify on the ground, and co-design interventions with
    residents, councillors and officers before any action is signed off.</p></div>""", unsafe_allow_html=True)
    st.write("")
    ac = ss.actions
    signed = int((ac[["Ward Councillor", "Youth Lead", "Municipal Officer", "Resident Welfare Assoc."]].all(axis=1)).sum())
    m = st.columns(4)
    m[0].markdown(kpi("Dialogue circles held", ss.circles, "youth-facilitated", "#22d3ee"), unsafe_allow_html=True)
    m[1].markdown(kpi("Issues verified on ground", ss.verified, "field-validated", "#22c55e"), unsafe_allow_html=True)
    m[2].markdown(kpi("Volunteer hours", int(ac.Hours.sum()), f"{int(ac.Volunteers.sum())} volunteers", "#f59e0b"), unsafe_allow_html=True)
    m[3].markdown(kpi("Actions fully signed off", f"{signed}/{len(ac)}", "4-party consensus", "#8b5cf6"), unsafe_allow_html=True)
    st.write("")
    st.markdown('<div class="sec">📒 Community Action Log</div>', unsafe_allow_html=True)
    edited = st.data_editor(
        ac, use_container_width=True, hide_index=True, num_rows="fixed", key="actions_editor",
        column_config={
            "Ward Councillor": st.column_config.CheckboxColumn("Councillor ✔"),
            "Youth Lead": st.column_config.CheckboxColumn("Youth Lead ✔"),
            "Municipal Officer": st.column_config.CheckboxColumn("Officer ✔"),
            "Resident Welfare Assoc.": st.column_config.CheckboxColumn("RWA ✔"),
        })
    ss.actions = edited
    with st.expander("➕ Log a new community intervention"):
        with st.form("new_action", clear_on_submit=True):
            n1, n2 = st.columns(2)
            nw = n1.selectbox("Ward", list(WARDS.keys()))
            ni = n2.selectbox("Intervention", ["Cleanup drive", "Lighting audit walk", "Awareness session", "Drain desilting watch"])
            ng = st.text_input("Ward grievance addressed")
            n3, n4 = st.columns(2)
            nv = n3.number_input("Volunteers", 1, 500, 20)
            nh = n4.number_input("Hours logged", 1, 2000, 40)
            if st.form_submit_button("Add to action log"):
                if not ng.strip():
                    st.error("Please describe the grievance.")
                else:
                    ss.actions = pd.concat([ss.actions, pd.DataFrame([{
                        "Date": datetime.now().strftime("%Y-%m-%d"), "Ward": nw, "Grievance": ng.strip(),
                        "Intervention": ni, "Volunteers": int(nv), "Hours": int(nh), "Ward Councillor": False,
                        "Youth Lead": True, "Municipal Officer": False, "Resident Welfare Assoc.": False}])], ignore_index=True)
                    ss.circles += 1
                    ss.verified += 2
                    st.rerun()

# ============================================================================
# TAB 5 - DOSSIER
# ============================================================================
with tab5:
    st.markdown('<div class="sec">🏆 Innovator Dossier &amp; Institutional Verification</div>', unsafe_allow_html=True)
    creds = [
        ("🏅", "Devbhoomi Rashtriya Ratna Puraskar 2025", "National award recognising outstanding contribution and youth leadership."),
        ("🌍", "UN Social Forum, Geneva", "Delegate badge: represented youth perspectives at the international forum."),
        ("🇸🇬", "NTU Singapore i-SEA Fellowship", "International fellowship on sustainability and innovation."),
        ("🇮🇳", "My Bharat Budget Quest 2026", "National Finalist."),
        ("🏛️", "Public Policy & Opinion Cell, IIT Kanpur", "Former Secretary, leading policy research and campus-civic engagement."),
        ("🎓", "IIT Kanpur · B.Tech EE", "AISHE Code: U-0517. Electrical Engineering, institutional affiliation."),
    ]
    for i in range(0, len(creds), 3):
        cols = st.columns(3)
        for col, (ic, t, p) in zip(cols, creds[i:i + 3]):
            col.markdown(f'<div class="cred"><div class="ic">{ic}</div><h4>{t}</h4><p>{p}</p></div>', unsafe_allow_html=True)
        st.write("")
    st.markdown('<div class="sec">📥 Official Documents</div>', unsafe_allow_html=True)

    def find_file(name):
        for base in (Path(__file__).parent, Path.cwd(), Path(__file__).parent / "assets"):
            p = base / name
            if p.exists():
                return p
        return None

    dcols = st.columns(2)
    for col, (title, fname) in zip(dcols, [("HSC-27 · 7-Slide Presentation Deck", DECK_FILE),
                                           ("Design Compendium", COMPENDIUM_FILE)]):
        with col:
            fp = find_file(fname)
            st.markdown(f'<div class="card"><b>{title}</b><br><span style="color:var(--mut);font-size:.82rem">{fname}</span></div>',
                        unsafe_allow_html=True)
            if fp:
                st.download_button(f"⬇️ Download {title}", fp.read_bytes(), file_name=fname,
                                   mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                   use_container_width=True)
            else:
                st.info(f"Place `{fname}` next to app.py (or in an `assets/` folder) to enable download.")

st.markdown('<div class="footer">🦅 BlueHawk Civic Nexus · Built by Aravind K. T., IIT Kanpur · '
            'All data shown is simulated for demonstration · MYAS × IIT Bombay VBYLD 2027</div>', unsafe_allow_html=True)
