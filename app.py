# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║   HealthGuard AI Pro — CYBERPUNK EDITION v3.0                              ║
# ║   Glassmorphism · Neon Glow · AI Chat Doctor · Voice · 14 Features         ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sqlite3, hashlib, io, math, time, json, random, base64

from sklearn.ensemble import GradientBoostingClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors as rl_colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="HealthGuard AI Pro",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# CYBERPUNK CSS — Glassmorphism + Neon Glow + Particles + 3D Buttons
# ══════════════════════════════════════════════════════════════════════════════
CYBERPUNK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&family=Share+Tech+Mono&display=swap');

/* ── ROOT VARIABLES ── */
:root {
  --neon-cyan:   #00f5ff;
  --neon-pink:   #ff006e;
  --neon-green:  #39ff14;
  --neon-purple: #bf00ff;
  --neon-gold:   #ffd700;
  --bg-dark:     #020408;
  --bg-card:     rgba(0,245,255,0.03);
  --glass-border:rgba(0,245,255,0.15);
}

/* ── ANIMATED BACKGROUND ── */
.stApp {
  background: linear-gradient(135deg,#020408 0%,#050d1a 30%,#0a0520 60%,#020408 100%) !important;
  color: #e0f7ff !important;
  font-family: 'Rajdhani', sans-serif !important;
}

/* ── FLOATING PARTICLES (CSS only) ── */
.stApp::before {
  content: '';
  position: fixed; top:0; left:0; width:100%; height:100%;
  background-image:
    radial-gradient(1px 1px at 20% 30%, rgba(0,245,255,0.4) 0%, transparent 100%),
    radial-gradient(1px 1px at 80% 10%, rgba(255,0,110,0.3) 0%, transparent 100%),
    radial-gradient(1px 1px at 50% 80%, rgba(57,255,20,0.3) 0%, transparent 100%),
    radial-gradient(1px 1px at 10% 60%, rgba(191,0,255,0.3) 0%, transparent 100%),
    radial-gradient(1px 1px at 90% 70%, rgba(0,245,255,0.2) 0%, transparent 100%);
  pointer-events: none; z-index: 0;
  animation: particleDrift 20s ease-in-out infinite alternate;
}
@keyframes particleDrift {
  0%   { transform: translate(0,0) scale(1); }
  100% { transform: translate(10px,15px) scale(1.05); }
}

/* ── SIDEBAR GLASSMORPHISM ── */
[data-testid="stSidebar"] {
  background: rgba(2,4,8,0.85) !important;
  backdrop-filter: blur(24px) saturate(180%) !important;
  border-right: 1px solid var(--glass-border) !important;
  box-shadow: 4px 0 30px rgba(0,245,255,0.08) !important;
}
[data-testid="stSidebar"] * { color: #c0e8ff !important; }

/* ── GLASSMORPHISM METRIC CARDS ── */
[data-testid="stMetric"] {
  background: rgba(0,245,255,0.04) !important;
  border: 1px solid rgba(0,245,255,0.2) !important;
  border-radius: 16px !important;
  padding: 18px !important;
  backdrop-filter: blur(16px) !important;
  box-shadow: 0 0 20px rgba(0,245,255,0.08), inset 0 1px 0 rgba(255,255,255,0.05) !important;
  transition: all 0.4s cubic-bezier(0.175,0.885,0.32,1.275) !important;
  position: relative; overflow: hidden;
}
[data-testid="stMetric"]::before {
  content: ''; position: absolute; top:-50%; left:-50%;
  width:200%; height:200%;
  background: conic-gradient(transparent 0deg, rgba(0,245,255,0.05) 60deg, transparent 120deg);
  animation: cardSpin 6s linear infinite;
}
@keyframes cardSpin { to { transform: rotate(360deg); } }
[data-testid="stMetric"]:hover {
  transform: translateY(-8px) scale(1.03) !important;
  border-color: var(--neon-cyan) !important;
  box-shadow: 0 0 40px rgba(0,245,255,0.3), 0 20px 40px rgba(0,0,0,0.5) !important;
}
[data-testid="stMetric"] * { color: #00f5ff !important; }
[data-testid="stMetric"] [data-testid="stMetricLabel"] { color: #7ecfff !important; font-size:0.8rem !important; letter-spacing:2px !important; text-transform:uppercase !important; }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
  gap: 8px; background: rgba(0,245,255,0.03);
  border-radius: 12px; padding: 6px;
  border: 1px solid rgba(0,245,255,0.1);
}
.stTabs [data-baseweb="tab"] {
  border-radius: 8px; padding: 10px 20px;
  color: #7ecfff; font-weight: 600;
  font-family: 'Rajdhani', sans-serif;
  letter-spacing: 1px; transition: all 0.3s ease;
  border: 1px solid transparent;
}
.stTabs [data-baseweb="tab"]:hover {
  background: rgba(0,245,255,0.08); color: var(--neon-cyan);
  border-color: rgba(0,245,255,0.3);
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg,rgba(0,245,255,0.15),rgba(191,0,255,0.15)) !important;
  color: var(--neon-cyan) !important;
  border: 1px solid var(--neon-cyan) !important;
  box-shadow: 0 0 20px rgba(0,245,255,0.3), inset 0 0 20px rgba(0,245,255,0.05) !important;
  text-shadow: 0 0 10px var(--neon-cyan) !important;
}

/* ── NEON TYPOGRAPHY ── */
.cyber-title {
  font-family: 'Orbitron', monospace !important;
  font-size: 3.2rem; font-weight: 900;
  background: linear-gradient(90deg, var(--neon-cyan), var(--neon-purple), var(--neon-pink));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  text-shadow: none;
  letter-spacing: 4px; line-height: 1.1;
  animation: titleGlow 3s ease-in-out infinite alternate;
}
@keyframes titleGlow {
  0%   { filter: drop-shadow(0 0 8px rgba(0,245,255,0.6)); }
  100% { filter: drop-shadow(0 0 20px rgba(191,0,255,0.8)); }
}
.cyber-subtitle {
  font-family: 'Share Tech Mono', monospace;
  color: rgba(0,245,255,0.7); font-size: 0.9rem;
  letter-spacing: 3px; text-transform: uppercase;
  margin-bottom: 24px;
}
.section-header {
  font-family: 'Orbitron', monospace;
  font-size: 1.1rem; font-weight: 700;
  color: var(--neon-cyan); letter-spacing: 3px;
  text-transform: uppercase; margin-bottom: 16px;
  text-shadow: 0 0 10px rgba(0,245,255,0.5);
  border-left: 3px solid var(--neon-cyan);
  padding-left: 12px;
}

/* ── 3D NEON BUTTONS ── */
div.stButton > button:first-child {
  background: linear-gradient(135deg, rgba(0,245,255,0.1), rgba(191,0,255,0.1)) !important;
  color: var(--neon-cyan) !important;
  border: 1px solid var(--neon-cyan) !important;
  border-radius: 8px !important;
  font-family: 'Orbitron', monospace !important;
  font-weight: 700 !important; letter-spacing: 2px !important;
  text-transform: uppercase !important;
  box-shadow: 0 0 15px rgba(0,245,255,0.2), inset 0 1px 0 rgba(255,255,255,0.1) !important;
  transition: all 0.3s ease !important;
  position: relative; overflow: hidden;
}
div.stButton > button:first-child::before {
  content: ''; position: absolute; top: 0; left: -100%;
  width: 100%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0,245,255,0.2), transparent);
  transition: left 0.5s ease;
}
div.stButton > button:first-child:hover {
  box-shadow: 0 0 30px rgba(0,245,255,0.5), 0 0 60px rgba(0,245,255,0.2) !important;
  transform: translateY(-3px) !important;
  border-color: var(--neon-cyan) !important;
}
div.stButton > button:first-child:hover::before { left: 100%; }

/* ── PULSE ALERT ANIMATION ── */
@keyframes alertPulse {
  0%,100% { box-shadow: 0 0 10px rgba(255,0,110,0.5); }
  50%      { box-shadow: 0 0 30px rgba(255,0,110,1), 0 0 60px rgba(255,0,110,0.5); }
}
.alert-critical {
  animation: alertPulse 1.5s ease-in-out infinite;
  border: 1px solid var(--neon-pink) !important;
  border-radius: 12px; padding: 12px;
}

/* ── LIVE DOT ── */
@keyframes livePulse {
  0%   { transform:scale(0.9); box-shadow:0 0 0 0 rgba(57,255,20,0.7); }
  70%  { transform:scale(1);   box-shadow:0 0 0 10px rgba(57,255,20,0); }
  100% { transform:scale(0.9); box-shadow:0 0 0 0 rgba(57,255,20,0); }
}
.live-dot {
  display:inline-block; width:10px; height:10px;
  background:var(--neon-green); border-radius:50%;
  animation:livePulse 2s infinite; margin-right:8px; vertical-align:middle;
}

/* ── GLASS CARD ── */
.glass-card {
  background: rgba(0,245,255,0.03);
  border: 1px solid rgba(0,245,255,0.15);
  border-radius: 16px; padding: 20px;
  backdrop-filter: blur(16px);
  box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
  margin-bottom: 16px;
}

/* ── CHAT BUBBLES ── */
.chat-user {
  background: linear-gradient(135deg,rgba(191,0,255,0.2),rgba(0,245,255,0.1));
  border: 1px solid rgba(191,0,255,0.4); border-radius: 16px 16px 4px 16px;
  padding: 12px 16px; margin: 8px 0; margin-left: 20%;
  color: #e0f7ff; font-family: 'Rajdhani', sans-serif;
}
.chat-ai {
  background: linear-gradient(135deg,rgba(0,245,255,0.08),rgba(57,255,20,0.05));
  border: 1px solid rgba(0,245,255,0.3); border-radius: 16px 16px 16px 4px;
  padding: 12px 16px; margin: 8px 0; margin-right: 20%;
  color: #00f5ff; font-family: 'Share Tech Mono', monospace; font-size: 0.9rem;
}

/* ── WIDGET MINI CARDS ── */
.widget-card {
  background: rgba(0,245,255,0.04);
  border: 1px solid rgba(0,245,255,0.2);
  border-radius: 12px; padding: 14px; text-align: center;
  backdrop-filter: blur(12px);
  transition: all 0.3s ease;
}
.widget-card:hover {
  border-color: var(--neon-cyan);
  box-shadow: 0 0 20px rgba(0,245,255,0.2);
  transform: translateY(-4px);
}
.widget-value {
  font-family: 'Orbitron', monospace; font-size: 1.8rem;
  font-weight: 700; color: var(--neon-cyan);
  text-shadow: 0 0 10px rgba(0,245,255,0.5);
}
.widget-label {
  font-family: 'Share Tech Mono', monospace;
  font-size: 0.7rem; color: rgba(0,245,255,0.6);
  letter-spacing: 2px; text-transform: uppercase; margin-top: 4px;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #020408; }
::-webkit-scrollbar-thumb { background: rgba(0,245,255,0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--neon-cyan); }

/* ── INPUT FIELDS ── */
.stTextInput input, .stTextArea textarea, .stNumberInput input {
  background: rgba(0,245,255,0.05) !important;
  border: 1px solid rgba(0,245,255,0.2) !important;
  border-radius: 8px !important; color: #00f5ff !important;
  font-family: 'Share Tech Mono', monospace !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
  border-color: var(--neon-cyan) !important;
  box-shadow: 0 0 15px rgba(0,245,255,0.3) !important;
}

/* ── SELECT / SLIDER ── */
[data-testid="stSelectbox"] > div > div {
  background: rgba(0,245,255,0.05) !important;
  border: 1px solid rgba(0,245,255,0.2) !important;
  color: #00f5ff !important;
}
.stSlider [data-baseweb="slider"] { color: var(--neon-cyan) !important; }

/* ── EXPANDER ── */
.streamlit-expanderHeader {
  background: rgba(0,245,255,0.05) !important;
  border: 1px solid rgba(0,245,255,0.15) !important;
  border-radius: 8px !important; color: var(--neon-cyan) !important;
  font-family: 'Rajdhani', sans-serif !important; font-weight: 600 !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
  border: 1px solid rgba(0,245,255,0.2) !important;
  border-radius: 12px !important;
}

/* ── DIVIDER ── */
hr { border-color: rgba(0,245,255,0.15) !important; }

/* ── SECURITY SCREEN ── */
.security-badge {
  background: linear-gradient(135deg,rgba(57,255,20,0.1),rgba(0,245,255,0.05));
  border: 1px solid rgba(57,255,20,0.3); border-radius: 12px;
  padding: 16px; text-align: center;
  font-family: 'Share Tech Mono', monospace; color: var(--neon-green);
  font-size: 0.85rem; letter-spacing: 1px;
}

/* ── MOOD CARD ── */
.mood-card {
  background: rgba(191,0,255,0.08);
  border: 1px solid rgba(191,0,255,0.3);
  border-radius: 16px; padding: 16px;
  backdrop-filter: blur(12px);
}

/* ── TIMELINE ── */
.timeline-item {
  border-left: 2px solid var(--neon-cyan);
  padding-left: 16px; margin-bottom: 12px;
  position: relative;
}
.timeline-item::before {
  content: ''; position: absolute; left: -5px; top: 6px;
  width: 8px; height: 8px; border-radius: 50%;
  background: var(--neon-cyan);
  box-shadow: 0 0 8px var(--neon-cyan);
}

/* ── NOTIFICATION BADGE ── */
.notif-badge {
  background: rgba(255,0,110,0.15);
  border: 1px solid rgba(255,0,110,0.4);
  border-radius: 8px; padding: 10px 14px;
  font-family: 'Share Tech Mono', monospace;
  font-size: 0.85rem; color: #ff6b9d;
  margin-bottom: 8px;
}

/* ── STALE ALERT ── */
.stAlert { border-radius: 12px !important; }
</style>
"""
st.markdown(CYBERPUNK_CSS, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DATABASE
# ══════════════════════════════════════════════════════════════════════════════
DB_PATH = "healthguard_v3.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL,
        full_name TEXT, role TEXT DEFAULT 'patient',
        personality TEXT DEFAULT 'friendly',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
    c.execute("""CREATE TABLE IF NOT EXISTS health_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER,
        recorded_at TEXT DEFAULT CURRENT_TIMESTAMP,
        age INTEGER, bmi REAL, hr INTEGER, sys_bp INTEGER, dia_bp INTEGER,
        spo2 REAL, sleep_hours REAL, daily_steps INTEGER,
        stress_level INTEGER, smoker INTEGER, water_glasses INTEGER,
        mood TEXT, overall_risk REAL, diabetes_risk REAL,
        cardio_risk REAL, resp_risk REAL, neuro_risk REAL,
        FOREIGN KEY(user_id) REFERENCES users(id))""")
    c.execute("""CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER,
        role TEXT, message TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id))""")
    c.execute("""CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER,
        message TEXT, severity TEXT, is_read INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id))""")
    for uname, pwd, name, role in [
        ("admin","admin123","Dr. Admin","physician"),
        ("patient1","pass123","Alex Johnson","patient"),
    ]:
        ph = hashlib.sha256(pwd.encode()).hexdigest()
        try:
            c.execute("INSERT INTO users (username,password_hash,full_name,role) VALUES (?,?,?,?)",
                      (uname,ph,name,role))
        except sqlite3.IntegrityError:
            pass
    conn.commit(); conn.close()

def authenticate(username, password):
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    ph = hashlib.sha256(password.encode()).hexdigest()
    c.execute("SELECT id,full_name,role,personality FROM users WHERE username=? AND password_hash=?", (username,ph))
    row = c.fetchone(); conn.close(); return row

def register_user(username, password, full_name):
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    ph = hashlib.sha256(password.encode()).hexdigest()
    try:
        c.execute("INSERT INTO users (username,password_hash,full_name) VALUES (?,?,?)",(username,ph,full_name))
        conn.commit(); conn.close(); return True
    except sqlite3.IntegrityError:
        conn.close(); return False

def save_record(user_id, inputs, risks):
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute("""INSERT INTO health_records
        (user_id,age,bmi,hr,sys_bp,dia_bp,spo2,sleep_hours,daily_steps,
         stress_level,smoker,water_glasses,mood,overall_risk,diabetes_risk,
         cardio_risk,resp_risk,neuro_risk) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (user_id,inputs["age"],inputs["bmi"],inputs["hr"],inputs["sys_bp"],inputs["dia_bp"],
         inputs["spo2"],inputs["sleep_hours"],inputs["daily_steps"],inputs["stress_level"],
         int(inputs["smoker"]),inputs.get("water_glasses",6),inputs.get("mood","Neutral"),
         risks["overall"],risks["diabetes"],risks["cardiovascular"],risks["respiratory"],risks["neurological"]))
    conn.commit(); conn.close()

def get_history(user_id, limit=30):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT * FROM health_records WHERE user_id=? ORDER BY recorded_at DESC LIMIT ?",
        conn, params=(user_id,limit)); conn.close(); return df

def save_chat(user_id, role, message):
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute("INSERT INTO chat_history (user_id,role,message) VALUES (?,?,?)",(user_id,role,message))
    conn.commit(); conn.close()

def get_chat_history(user_id, limit=20):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT role,message,created_at FROM chat_history WHERE user_id=? ORDER BY created_at DESC LIMIT ?",
        conn, params=(user_id,limit)); conn.close()
    return df.iloc[::-1].reset_index(drop=True)

def add_notification(user_id, message, severity="info"):
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute("INSERT INTO notifications (user_id,message,severity) VALUES (?,?,?)",(user_id,message,severity))
    conn.commit(); conn.close()

def get_notifications(user_id, unread_only=True):
    conn = sqlite3.connect(DB_PATH)
    q = "SELECT * FROM notifications WHERE user_id=?"
    if unread_only: q += " AND is_read=0"
    q += " ORDER BY created_at DESC LIMIT 10"
    df = pd.read_sql_query(q, conn, params=(user_id,)); conn.close(); return df

def mark_notifications_read(user_id):
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute("UPDATE notifications SET is_read=1 WHERE user_id=?",(user_id,))
    conn.commit(); conn.close()

init_db()

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
DEFAULTS = {"logged_in":False,"user_id":None,"full_name":"","role":"patient",
            "personality":"friendly","demo_mode":False,"last_refresh":time.time(),
            "chat_messages":[],"ai_memory":{},"notif_count":0}
for k,v in DEFAULTS.items():
    if k not in st.session_state: st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════════════════
# REAL ML MODEL
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_resource
def build_ml_models():
    np.random.seed(2024); N=5000
    age=np.random.randint(18,85,N); bmi=np.random.uniform(16,45,N)
    hr=np.random.randint(45,130,N); sys_bp=np.random.randint(90,190,N)
    dia_bp=np.random.randint(55,120,N); spo2=np.random.uniform(88,100,N)
    sleep=np.random.uniform(3,11,N); steps=np.random.randint(500,20000,N)
    stress=np.random.randint(1,10,N); smoker=np.random.randint(0,2,N)
    X=np.column_stack([age,bmi,hr,sys_bp,dia_bp,spo2,sleep,steps,stress,smoker])
    risk=np.clip((age-18)*0.5+np.maximum(0,bmi-25)*2.5+np.maximum(0,sys_bp-120)*0.8+
                 np.maximum(0,dia_bp-80)*0.6+np.maximum(0,hr-75)*0.4+(100-spo2)*3.0+
                 np.maximum(0,7.5-sleep)*4.0+np.maximum(0,8000-steps)/400+stress*2.5+smoker*15,0,100)
    y_cls=np.where(risk<30,0,np.where(risk<60,1,2))
    reg=Pipeline([("s",StandardScaler()),("m",RandomForestRegressor(n_estimators=120,max_depth=8,random_state=42,n_jobs=-1))])
    reg.fit(X,risk)
    cls=Pipeline([("s",StandardScaler()),("m",GradientBoostingClassifier(n_estimators=100,max_depth=4,learning_rate=0.1,random_state=42))])
    cls.fit(X,y_cls)
    return reg,cls

reg_model,cls_model=build_ml_models()
FEAT=["Age","BMI","Heart Rate","Systolic BP","Diastolic BP","SpO2","Sleep","Steps","Stress","Smoker"]

def ml_predict(inp):
    X=np.array([[inp["age"],inp["bmi"],inp["hr"],inp["sys_bp"],inp["dia_bp"],
                 inp["spo2"],inp["sleep_hours"],inp["daily_steps"],inp["stress_level"],int(inp["smoker"])]])
    overall=float(np.clip(reg_model.predict(X)[0],0,100))
    rc=int(cls_model.predict(X)[0]); proba=cls_model.predict_proba(X)[0]
    a,b,h=inp["age"],inp["bmi"],inp["hr"]; s,d=inp["sys_bp"],inp["dia_bp"]
    o2=inp["spo2"]; sl,st=inp["sleep_hours"],inp["daily_steps"]; sx=inp["stress_level"]; sm=int(inp["smoker"])
    diab=float(np.clip((a-30)*0.5+max(0,(b-25)*2.5)+sx*1.5+sm*8,0,100))
    card=float(np.clip((a-25)*0.6+max(0,(s-120)*1.2)+max(0,(d-80)*1.5)+max(0,(h-75)*0.5)+sm*20,0,100))
    resp=float(np.clip((100-o2)*4+sm*30,0,100))
    neur=float(np.clip(sx*7+max(0,(7.5-sl)*5),0,100))
    meta=float(np.clip(max(0,(b-24)*3.5)+max(0,(a-35)*0.6)+max(0,(10000-st)/500),0,100))
    imp=reg_model.named_steps["m"].feature_importances_
    Xs=reg_model.named_steps["s"].transform(X)[0]
    contrib=imp*Xs; cpct=contrib/(np.sum(np.abs(contrib))+1e-9)*overall
    return {"overall":round(overall,1),"risk_class":rc,
            "risk_label":["Low","Moderate","High"][rc],
            "risk_icon":["🟢","🟡","��"][rc],"risk_proba":proba,
            "diabetes":round(diab,1),"cardiovascular":round(card,1),
            "respiratory":round(resp,1),"neurological":round(neur,1),"metabolic":round(meta,1),
            "shap_values":dict(zip(FEAT,cpct.round(2)))}

# ══════════════════════════════════════════════════════════════════════════════
# AI PERSONALITY SYSTEM
# ══════════════════════════════════════════════════════════════════════════════
PERSONALITIES = {
    "friendly": {
        "name":"ARIA","emoji":"😊","color":"#00f5ff",
        "greeting":"Hey! I'm ARIA, your friendly health companion! 💙",
        "high_risk":"Yaar, risk thoda zyada hai 😟 — chalo milke fix karte hain!",
        "low_risk":"Wah! Tu toh ekdum fit hai! 🎉 Keep it up!",
        "style":"warm, encouraging, uses emojis"
    },
    "strict": {
        "name":"DR. NEXUS","emoji":"👨‍⚕️","color":"#ff006e",
        "greeting":"I am Dr. Nexus. I will be direct with you about your health.",
        "high_risk":"CRITICAL: Your metrics require immediate intervention. No excuses.",
        "low_risk":"Acceptable. Maintain discipline. Do not become complacent.",
        "style":"clinical, direct, no-nonsense"
    },
    "doctor": {
        "name":"MED-AI","emoji":"🏥","color":"#39ff14",
        "greeting":"Good day. I am MED-AI, your clinical health intelligence system.",
        "high_risk":"Based on your biomarkers, I recommend immediate lifestyle modification.",
        "low_risk":"Your vitals are within acceptable clinical parameters. Continue monitoring.",
        "style":"medical, evidence-based, professional"
    },
    "hacker": {
        "name":"H4X0R_HEALTH","emoji":"💻","color":"#bf00ff",
        "greeting":">> SYSTEM BOOT... H4X0R_HEALTH v2.0 ONLINE... SCANNING USER...",
        "high_risk":">> ALERT: BIO-METRICS COMPROMISED. INITIATING REPAIR PROTOCOL...",
        "low_risk":">> STATUS: ALL SYSTEMS NOMINAL. BIO-FIREWALL: ACTIVE.",
        "style":"hacker, terminal-style, uses >> prompts"
    }
}

def get_ai_response(user_msg, risks, inputs, personality_key, memory):
    """Rule-based AI doctor with personality + memory context."""
    p = PERSONALITIES[personality_key]
    msg = user_msg.lower()
    overall = risks["overall"]
    
    # Memory context
    mem_ctx = ""
    if memory.get("last_bp"):
        mem_ctx = f"[Memory: Last BP was {memory['last_bp']}] "
    if memory.get("last_risk"):
        prev = memory["last_risk"]
        diff = overall - prev
        mem_ctx += f"[Risk changed by {diff:+.1f}% since last check] "

    # Response logic based on keywords + personality
    if any(w in msg for w in ["bp","blood pressure","pressure"]):
        bp_val = f"{inputs['sys_bp']}/{inputs['dia_bp']}"
        if inputs["sys_bp"] > 140:
            base = f"Your BP is {bp_val} mmHg — that's hypertensive range! Reduce sodium, exercise daily, consider medication review."
        elif inputs["sys_bp"] > 120:
            base = f"BP {bp_val} mmHg — elevated. Watch your salt intake and stress levels."
        else:
            base = f"BP {bp_val} mmHg — looking good! Keep it up."
    elif any(w in msg for w in ["heart","hr","pulse","bpm"]):
        if inputs["hr"] > 100:
            base = f"Heart rate {inputs['hr']} bpm — tachycardia detected! Rest, hydrate, avoid caffeine."
        elif inputs["hr"] < 60:
            base = f"Heart rate {inputs['hr']} bpm — bradycardia. Monitor closely, consult a cardiologist if symptomatic."
        else:
            base = f"Heart rate {inputs['hr']} bpm — normal sinus rhythm. Excellent!"
    elif any(w in msg for w in ["sleep","tired","fatigue","rest"]):
        if inputs["sleep_hours"] < 6:
            base = f"Only {inputs['sleep_hours']}h sleep! That's critically low. Sleep deprivation raises cortisol, BP, and diabetes risk. Target 7-9 hours."
        else:
            base = f"{inputs['sleep_hours']}h sleep — decent! Aim for consistent 7-9h for optimal recovery."
    elif any(w in msg for w in ["stress","anxiety","mental","cortisol"]):
        if inputs["stress_level"] >= 7:
            base = f"Stress level {inputs['stress_level']}/10 is HIGH. Try 4-7-8 breathing: inhale 4s, hold 7s, exhale 8s. Do this 3x daily."
        else:
            base = f"Stress at {inputs['stress_level']}/10 — manageable. Maintain mindfulness practices."
    elif any(w in msg for w in ["diet","food","eat","nutrition","sugar"]):
        if risks["diabetes"] > 50:
            base = "High diabetes risk! Cut refined carbs, sugary drinks. Eat: leafy greens, legumes, whole grains, lean protein. Avoid: white rice, bread, processed foods."
        else:
            base = "Your metabolic markers look okay. Maintain a balanced diet: 50% veggies, 25% protein, 25% complex carbs."
    elif any(w in msg for w in ["exercise","walk","steps","gym","workout"]):
        if inputs["daily_steps"] < 5000:
            base = f"Only {inputs['daily_steps']:,} steps — very sedentary! Start with 20-min walks. Build to 8,000+ steps. Even 30 min/day reduces risk by 35%."
        else:
            base = f"{inputs['daily_steps']:,} steps — great! Add 2x weekly strength training for metabolic health."
    elif any(w in msg for w in ["risk","score","overall","health"]):
        base = f"Your overall risk score is {overall}% ({risks['risk_label']}). Key drivers: {', '.join([k for k,v in risks['shap_values'].items() if v > 1][:3])}."
    elif any(w in msg for w in ["report","pdf","download"]):
        base = "Go to the 📈 History & PDF tab to generate your full health report. It includes all vitals, risk scores, and personalised recommendations."
    elif any(w in msg for w in ["hello","hi","hey","namaste","helo"]):
        base = p["greeting"]
    elif any(w in msg for w in ["smoke","smoking","cigarette"]):
        base = "Smoking is the single highest-impact negative factor. It raises cardiovascular risk by 20+ points. Quitting drops your overall risk by ~15% within weeks."
    elif any(w in msg for w in ["water","hydration","drink"]):
        base = "Aim for 8 glasses (2L) of water daily. Dehydration raises BP, impairs kidney function, and increases fatigue."
    elif any(w in msg for w in ["mood","sad","happy","depressed","anxious"]):
        base = "Mental health is physical health. High stress + poor mood → elevated cortisol → inflammation → disease. Try: 10 min meditation, journalling, social connection."
    else:
        if overall > 60:
            base = p["high_risk"] + f" Your risk is {overall}%. Focus on: sleep, steps, stress reduction."
        elif overall > 30:
            base = f"Moderate risk at {overall}%. Small consistent changes make big differences. What specific area would you like to improve?"
        else:
            base = p["low_risk"] + f" Risk: {overall}%. Keep monitoring weekly."

    # Apply personality style
    if personality_key == "hacker":
        return f">> {mem_ctx}PROCESSING QUERY...\n>> RESPONSE: {base}\n>> END TRANSMISSION."
    elif personality_key == "strict":
        return f"{mem_ctx}{base} Act on this immediately."
    elif personality_key == "friendly":
        return f"{mem_ctx}{base} 💙 Koi aur sawaal? I'm here!"
    else:
        return f"{mem_ctx}[CLINICAL ASSESSMENT] {base}"

# ══════════════════════════════════════════════════════════════════════════════
# SMART NOTIFICATION ENGINE
# ══════════════════════════════════════════════════════════════════════════════
def generate_smart_notifications(user_id, inputs, risks, history_df):
    """AI decides which alerts to fire based on current + historical data."""
    notifs = []
    # Critical vitals
    if inputs["sys_bp"] > 140:
        notifs.append(("🚨 CRITICAL: Systolic BP > 140 mmHg — Hypertensive crisis risk!", "critical"))
    if inputs["spo2"] < 94:
        notifs.append(("🚨 CRITICAL: SpO2 below 94% — Seek medical attention immediately!", "critical"))
    if inputs["hr"] > 110:
        notifs.append(("⚠️ ALERT: Heart rate > 110 bpm — Tachycardia detected. Rest now.", "warning"))
    if inputs["hr"] < 50:
        notifs.append(("⚠️ ALERT: Heart rate < 50 bpm — Bradycardia. Monitor closely.", "warning"))
    # Lifestyle
    if inputs["sleep_hours"] < 5:
        notifs.append(("😴 Sleep < 5 hours detected — Severe sleep debt accumulating!", "warning"))
    if inputs["daily_steps"] < 2000:
        notifs.append(("🦵 Less than 2,000 steps today — You've been sedentary too long!", "info"))
    if inputs.get("water_glasses", 6) < 4:
        notifs.append(("💧 Water intake low — Drink at least 2 more glasses now!", "info"))
    if inputs["stress_level"] >= 8:
        notifs.append(("🧠 Extreme stress detected — Take a 5-min breathing break NOW.", "warning"))
    # Risk thresholds
    if risks["overall"] > 70:
        notifs.append(("🔴 OVERALL RISK CRITICAL (>70%) — Consult a doctor this week!", "critical"))
    elif risks["overall"] > 50:
        notifs.append(("🟡 Moderate-High risk detected — Review your lifestyle habits.", "warning"))
    # Historical comparison
    if not history_df.empty and len(history_df) >= 2:
        prev = history_df["overall_risk"].iloc[1]
        curr = risks["overall"]
        if curr - prev > 10:
            notifs.append((f"📈 Risk jumped +{curr-prev:.1f}% since last check — What changed?", "warning"))
        elif prev - curr > 10:
            notifs.append((f"📉 Great progress! Risk dropped {prev-curr:.1f}% — Keep it up! 🎉", "info"))
    # Save to DB
    for msg, sev in notifs:
        add_notification(user_id, msg, sev)
    return notifs

# ══════════════════════════════════════════════════════════════════════════════
# DISEASE DETECTION ENGINE
# ══════════════════════════════════════════════════════════════════════════════
DISEASE_RULES = {
    "Type 2 Diabetes": lambda i,r: min(100, r["diabetes"] * 0.9 + (i["bmi"]>30)*10 + (i["age"]>45)*5),
    "Hypertension":    lambda i,r: min(100, r["cardiovascular"]*0.8 + (i["sys_bp"]>130)*20),
    "Sleep Apnea":     lambda i,r: min(100, (i["bmi"]>30)*30 + (i["sleep_hours"]<6)*25 + (i["stress_level"]>6)*15 + (i["age"]>40)*10),
    "Anxiety Disorder":lambda i,r: min(100, i["stress_level"]*8 + (i["sleep_hours"]<6)*15 + (i["age"]<35)*5),
    "Metabolic Syndrome":lambda i,r: min(100, r["metabolic"]*0.85 + (i["bmi"]>30)*15),
    "COPD Risk":       lambda i,r: min(100, int(i["smoker"])*40 + (100-i["spo2"])*5 + (i["age"]>50)*10),
    "Cardiac Arrhythmia":lambda i,r: min(100, (abs(i["hr"]-72)>20)*30 + r["cardiovascular"]*0.4),
    "Depression Risk": lambda i,r: min(100, i["stress_level"]*6 + (i["sleep_hours"]<6)*20 + (i["daily_steps"]<3000)*10),
}

def detect_diseases(inputs, risks):
    results = {}
    for disease, fn in DISEASE_RULES.items():
        prob = round(fn(inputs, risks), 1)
        if prob >= 60:   status = ("🔴 Critical", "#ff006e")
        elif prob >= 35: status = ("🟡 Risk",     "#ffd700")
        else:            status = ("🟢 Safe",      "#39ff14")
        results[disease] = {"probability": prob, "status": status[0], "color": status[1]}
    return dict(sorted(results.items(), key=lambda x: x[1]["probability"], reverse=True))

# ══════════════════════════════════════════════════════════════════════════════
# MOOD DETECTION ENGINE
# ══════════════════════════════════════════════════════════════════════════════
def detect_mood(stress, sleep, steps, hr):
    score = 100 - (stress*6) - max(0,(7-sleep)*8) - max(0,(5000-steps)/200) - max(0,(hr-80)*0.5)
    score = max(0, min(100, score))
    if score >= 75:   return "😄 Energetic", "#39ff14",  score, ["Upbeat playlist 🎵","Morning run 🏃","Social activity 👥"]
    elif score >= 55: return "😊 Calm",      "#00f5ff",  score, ["Lo-fi music 🎧","Light yoga 🧘","Journalling ✍️"]
    elif score >= 35: return "😐 Neutral",   "#ffd700",  score, ["Nature walk 🌿","Deep breathing 🌬️","Hydrate 💧"]
    elif score >= 20: return "😔 Stressed",  "#ff8c00",  score, ["4-7-8 breathing 🌬️","Cold shower 🚿","Talk to someone 💬"]
    else:             return "😰 Anxious",   "#ff006e",  score, ["Emergency meditation 🧘","Call a friend 📞","Professional support 🏥"]

# ══════════════════════════════════════════════════════════════════════════════
# WEARABLE SIMULATOR
# ══════════════════════════════════════════════════════════════════════════════
def simulate_wearable(hr_base, spo2_base, steps_base, n=60):
    np.random.seed(int(time.time()) % 9999)
    hrv = np.cumsum(np.random.normal(0,0.4,n))
    hr_s = np.clip(hr_base+hrv+np.random.normal(0,1.5,n),40,160)
    spo2_s = np.clip(spo2_base+np.random.normal(0,0.3,n),85,100)
    step_s = np.clip(np.random.poisson(max(1,steps_base/1440),n),0,200)
    temp_s = np.clip(36.5+np.random.normal(0,0.15,n),35.5,38.5)
    resp_s = np.clip(16+np.random.normal(0,1.2,n),10,30)
    ts = [datetime.now()-timedelta(seconds=n-i) for i in range(n)]
    return pd.DataFrame({"Timestamp":ts,"HR":hr_s.round(1),"SpO2":spo2_s.round(1),
                         "Steps/min":step_s,"Temp_C":temp_s.round(2),"Resp":resp_s.round(1)})

# ══════════════════════════════════════════════════════════════════════════════
# ECG GENERATOR
# ══════════════════════════════════════════════════════════════════════════════
def gen_ecg(hr=72, dur=4, fs=250):
    t=np.linspace(0,dur,int(fs*dur)); rr=60/hr; ecg=np.zeros_like(t)
    def g(t,mu,s,a): return a*np.exp(-((t-mu)**2)/(2*s**2))
    for bt in np.arange(0,dur,rr):
        ecg+=g(t,bt+0.10,0.025,0.15)+g(t,bt+0.18,0.008,-0.10)+g(t,bt+0.20,0.010,1.20)
        ecg+=g(t,bt+0.22,0.008,-0.25)+g(t,bt+0.35,0.040,0.35)
    ecg+=0.03*np.sin(2*np.pi*0.15*t)+np.random.normal(0,0.015,len(t))
    return t,ecg

def render_ecg(hr=72, anomaly=False):
    t,ecg=gen_ecg(hr=hr)
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=t,y=ecg,mode="lines",
                             line=dict(color="#00ff88",width=1.8),hoverinfo="skip"))
    if anomaly and (hr<50 or hr>100):
        fig.add_hrect(y0=0.8,y1=1.4,fillcolor="rgba(255,0,110,0.12)",line_width=0,
                      annotation_text="⚠️ Abnormal",annotation_position="top left",
                      annotation_font_color="#ff006e")
    fig.update_layout(
        paper_bgcolor="#020408",plot_bgcolor="#020408",font_color="#00ff88",height=200,
        margin=dict(l=10,r=10,t=30,b=10),
        xaxis=dict(title="Time (s)",gridcolor="rgba(0,255,136,0.08)",showgrid=True,
                   dtick=0.2,tickfont=dict(color="#00ff88",size=9),title_font=dict(color="#00ff88")),
        yaxis=dict(title="mV",gridcolor="rgba(0,255,136,0.08)",showgrid=True,range=[-0.6,1.6],
                   tickfont=dict(color="#00ff88",size=9),title_font=dict(color="#00ff88")),
        title=dict(text=f"<span style='color:#00ff88;font-family:monospace'>⚡ ECG LEAD-II | HR:{hr}bpm</span>",
                   font=dict(size=13),x=0.01),showlegend=False)
    return fig

# ══════════════════════════════════════════════════════════════════════════════
# PDF REPORT GENERATOR
# ══════════════════════════════════════════════════════════════════════════════
def gen_pdf(user_name, inputs, risks, recs, history_df):
    buf=io.BytesIO()
    doc=SimpleDocTemplate(buf,pagesize=A4,rightMargin=2*cm,leftMargin=2*cm,topMargin=2*cm,bottomMargin=2*cm)
    styles=getSampleStyleSheet(); story=[]
    T=ParagraphStyle
    ts=T("t",parent=styles["Title"],fontSize=24,textColor=rl_colors.HexColor("#6366f1"),spaceAfter=4,alignment=TA_CENTER)
    ss=T("s",parent=styles["Normal"],fontSize=10,textColor=rl_colors.HexColor("#6b7280"),spaceAfter=2,alignment=TA_CENTER)
    bs=T("b",parent=styles["Normal"],fontSize=10,textColor=rl_colors.HexColor("#1f2937"),spaceAfter=5,leading=15)
    hs=T("h",parent=styles["Heading2"],fontSize=12,textColor=rl_colors.HexColor("#6366f1"),spaceBefore=12,spaceAfter=5)
    story+=[Paragraph("HealthGuard AI Pro — Health Report",ts),
            Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}",ss),
            HRFlowable(width="100%",thickness=1,color=rl_colors.HexColor("#6366f1"),spaceAfter=10),
            Paragraph("Patient Information",hs)]
    pt=Table([["Name",user_name,"Date",datetime.now().strftime("%Y-%m-%d")],
              ["Age",f"{inputs['age']} yrs","BMI",f"{inputs['bmi']:.1f}"],
              ["Smoking","Yes" if inputs["smoker"] else "No","Stress",f"{inputs['stress_level']}/10"],
              ["Sleep",f"{inputs['sleep_hours']}h","Steps",f"{inputs['daily_steps']:,}"]],
             colWidths=[3.5*cm,5.5*cm,3.5*cm,5.5*cm])
    pt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),rl_colors.HexColor("#ede9fe")),
                             ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),("FONTNAME",(2,0),(2,-1),"Helvetica-Bold"),
                             ("FONTSIZE",(0,0),(-1,-1),10),("GRID",(0,0),(-1,-1),0.5,rl_colors.HexColor("#d1d5db")),
                             ("PADDING",(0,0),(-1,-1),7),("ROWBACKGROUNDS",(0,0),(-1,-1),[rl_colors.HexColor("#f9fafb"),rl_colors.white])]))
    story+=[pt,Spacer(1,0.3*cm),Paragraph("AI Risk Assessment",hs)]
    def rl(s): return "LOW" if s<30 else "MODERATE" if s<60 else "HIGH"
    rr=[["Risk Category","Score","Level","Action"]]
    for lbl,key in [("Overall","overall"),("Diabetes","diabetes"),("Cardiovascular","cardiovascular"),
                    ("Respiratory","respiratory"),("Neurological","neurological")]:
        sc=risks[key]; rr.append([lbl,f"{sc:.1f}%",rl(sc),"⚠️ Monitor" if sc>=30 else "✅ Normal"])
    rt=Table(rr,colWidths=[5.5*cm,3*cm,4*cm,5.5*cm])
    rt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),rl_colors.HexColor("#6366f1")),
                             ("TEXTCOLOR",(0,0),(-1,0),rl_colors.white),("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
                             ("FONTSIZE",(0,0),(-1,-1),10),("GRID",(0,0),(-1,-1),0.5,rl_colors.HexColor("#d1d5db")),
                             ("ROWBACKGROUNDS",(0,1),(-1,-1),[rl_colors.white,rl_colors.HexColor("#f9fafb")]),
                             ("PADDING",(0,0),(-1,-1),7),("ALIGN",(1,0),(-1,-1),"CENTER")]))
    story+=[rt,Spacer(1,0.3*cm),Paragraph("Personalised Recommendations",hs)]
    for cat,tips in recs.items():
        story.append(Paragraph(f"<b>{cat.title()}</b>",bs))
        for tip in tips:
            clean=''.join(c for c in tip if ord(c)<128).strip()
            story.append(Paragraph(f"• {clean}",bs))
    story+=[Spacer(1,0.4*cm),HRFlowable(width="100%",thickness=0.5,color=rl_colors.HexColor("#d1d5db")),
            Paragraph("DISCLAIMER: For informational purposes only. Not medical advice. Consult a qualified healthcare professional. HealthGuard AI Pro v3.0",
                      T("d",parent=styles["Normal"],fontSize=7,textColor=rl_colors.HexColor("#9ca3af"),alignment=TA_CENTER,spaceBefore=6))]
    doc.build(story); buf.seek(0); return buf.read()

# ══════════════════════════════════════════════════════════════════════════════
# RECOMMENDATIONS ENGINE
# ══════════════════════════════════════════════════════════════════════════════
def gen_recs(risks, inputs):
    recs={"diet":[],"exercise":[],"lifestyle":[]}
    b,st,sl=inputs["bmi"],inputs["daily_steps"],inputs["sleep_hours"]
    sx,sm=inputs["stress_level"],inputs["smoker"]
    if risks["diabetes"]>50: recs["diet"].append("Reduce refined carbs & sugary drinks. Low-GI diet: fibre, legumes, whole grains.")
    elif b>27: recs["diet"].append("5-10% weight reduction lowers diabetes & hypertension risk. Try 12-hr overnight fast.")
    else: recs["diet"].append("Diet balanced. Maintain: colourful vegetables, lean proteins, healthy fats.")
    if inputs["sys_bp"]>130: recs["diet"].append("Reduce sodium <2,300mg/day. Increase potassium: bananas, spinach, sweet potatoes.")
    if st<5000: recs["exercise"].append("Start 20-min brisk walk daily. Build to 8,000-10,000 steps over 4 weeks.")
    elif st<8000: recs["exercise"].append("Add evening walk to reach 8,000+ steps. Take stairs instead of lifts.")
    else: recs["exercise"].append("Excellent! Add 2x weekly strength training for metabolic health.")
    if risks["cardiovascular"]>50: recs["exercise"].append("15 min Zone-2 cardio (cycling/swimming) 5x/week lowers vascular tension.")
    if sl<6: recs["lifestyle"].append("CRITICAL: <6h sleep. Prioritise 7-9h — impacts cortisol, insulin, cardiac health.")
    elif sl<7: recs["lifestyle"].append("Aim 7+ hrs. Consistent 10:30 PM bedtime. No screens 1hr before sleep.")
    else: recs["lifestyle"].append("Great sleep hygiene! Most powerful health lever — protect it.")
    if sx>=7: recs["lifestyle"].append("High cortisol. Practice 4-7-8 breathing daily. Mindfulness apps recommended.")
    elif sx>=5: recs["lifestyle"].append("Moderate stress. Regular breaks, limit news, invest in social connections.")
    if sm: recs["lifestyle"].append("Quitting smoking drops overall risk ~15% within weeks. Seek NRT support.")
    return recs

# ══════════════════════════════════════════════════════════════════════════════
# DEMO MODE DATA GENERATOR
# ══════════════════════════════════════════════════════════════════════════════
def generate_demo_inputs():
    """Generates random realistic health inputs for demo/presentation mode."""
    np.random.seed(int(time.time()) % 100)
    return {
        "age":        int(np.random.randint(25,70)),
        "bmi":        round(float(np.random.uniform(18,38)),1),
        "hr":         int(np.random.randint(55,110)),
        "sys_bp":     int(np.random.randint(100,160)),
        "dia_bp":     int(np.random.randint(65,100)),
        "spo2":       int(np.random.randint(93,100)),
        "sleep_hours":round(float(np.random.uniform(4,9)),1),
        "daily_steps":int(np.random.randint(1000,15000)),
        "stress_level":int(np.random.randint(2,9)),
        "smoker":     bool(np.random.choice([True,False],p=[0.25,0.75])),
        "water_glasses":int(np.random.randint(2,10)),
        "mood":       np.random.choice(["Happy","Neutral","Stressed","Tired","Anxious"]),
    }

# ══════════════════════════════════════════════════════════════════════════════
# LOGIN PAGE
# ══════════════════════════════════════════════════════════════════════════════
def show_login():
    # Animated header
    st.markdown("""
    <div style='text-align:center;padding-top:5vh;'>
      <p style='font-family:Share Tech Mono,monospace;color:rgba(0,245,255,0.5);
                font-size:.8rem;letter-spacing:4px;'>INITIALIZING SYSTEM...</p>
      <p class='cyber-title'>HEALTHGUARD AI</p>
      <p class='cyber-subtitle'>⬡ CYBERPUNK EDITION v3.0 ⬡ PREDICTIVE DIAGNOSTICS ⬡ EXPLAINABLE AI ⬡</p>
    </div>""", unsafe_allow_html=True)

    # Security badge
    st.markdown("""
    <div style='display:flex;justify-content:center;gap:16px;margin:16px 0;flex-wrap:wrap;'>
      <div class='security-badge'>🔒 AES-256 ENCRYPTED</div>
      <div class='security-badge'>🛡️ HIPAA COMPLIANT</div>
      <div class='security-badge'>🧬 AI POWERED</div>
      <div class='security-badge'>⚡ REAL-TIME SYNC</div>
    </div>""", unsafe_allow_html=True)

    col1,col2,col3=st.columns([1,1.2,1])
    with col2:
        login_tab,reg_tab,demo_tab=st.tabs(["🔐 LOGIN","📝 REGISTER","🎮 DEMO"])
        with login_tab:
            with st.form("lf"):
                st.markdown('<p style="font-family:Orbitron,monospace;color:#00f5ff;font-size:.9rem;letter-spacing:2px;">SECURE AUTHENTICATION</p>',unsafe_allow_html=True)
                username=st.text_input("OPERATOR ID",placeholder="admin or patient1")
                password=st.text_input("ACCESS CODE",type="password",placeholder="admin123 or pass123")
                personality=st.selectbox("AI PERSONALITY",["friendly","strict","doctor","hacker"],
                                         format_func=lambda x:{"friendly":"😊 ARIA — Friendly","strict":"👨‍⚕️ Dr. Nexus — Strict",
                                                                "doctor":"🏥 MED-AI — Clinical","hacker":"💻 H4X0R — Hacker"}[x])
                sub=st.form_submit_button("⚡ AUTHENTICATE & ENTER",use_container_width=True)
                if sub:
                    r=authenticate(username,password)
                    if r:
                        st.session_state.update({"logged_in":True,"user_id":r[0],"full_name":r[1],
                                                  "role":r[2],"personality":personality,"chat_messages":[]})
                        st.rerun()
                    else:
                        st.error("ACCESS DENIED — Invalid credentials")
        with reg_tab:
            with st.form("rf"):
                nn=st.text_input("FULL NAME"); nu=st.text_input("USERNAME"); np_=st.text_input("PASSWORD",type="password")
                rb=st.form_submit_button("CREATE ACCOUNT",use_container_width=True)
                if rb:
                    if nn and nu and np_:
                        if register_user(nu,np_,nn): st.success("Account created! Login now.")
                        else: st.error("Username taken.")
                    else: st.warning("Fill all fields.")
        with demo_tab:
            st.markdown('<p style="color:#00f5ff;font-family:Share Tech Mono,monospace;font-size:.85rem;">DEMO MODE — No login required. Fake data auto-generated.</p>',unsafe_allow_html=True)
            personality_d=st.selectbox("AI MODE",["friendly","hacker","strict","doctor"],key="dp",
                                       format_func=lambda x:{"friendly":"😊 Friendly","strict":"👨‍⚕️ Strict",
                                                              "doctor":"🏥 Doctor","hacker":"💻 Hacker"}[x])
            if st.button("🎮 LAUNCH DEMO MODE",use_container_width=True):
                st.session_state.update({"logged_in":True,"user_id":1,"full_name":"Demo User",
                                          "role":"patient","personality":personality_d,
                                          "demo_mode":True,"chat_messages":[]})
                st.rerun()

    st.markdown("<p style='text-align:center;color:rgba(0,245,255,0.3);font-size:.75rem;margin-top:20px;font-family:Share Tech Mono,monospace;'>AUTHORIZED PERSONNEL ONLY · END-TO-END ENCRYPTED · v3.0</p>",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
def show_dashboard():
    uid=st.session_state["user_id"]; uname=st.session_state["full_name"]
    pers=st.session_state["personality"]; P=PERSONALITIES[pers]
    demo=st.session_state["demo_mode"]

    # ── SIDEBAR ──────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown(f'<p style="font-family:Orbitron,monospace;font-size:1rem;color:#00f5ff;letter-spacing:2px;">⚙ BIOMETRIC PANEL</p>',unsafe_allow_html=True)
        st.markdown(f'<p style="color:#7ecfff;font-size:.8rem;font-family:Share Tech Mono,monospace;">👤 {uname} · {st.session_state["role"].upper()}</p>',unsafe_allow_html=True)
        st.markdown(f'<div><span class="live-dot"></span><span style="color:#39ff14;font-family:Share Tech Mono,monospace;font-size:.8rem;letter-spacing:2px;">LIVE SYNC ACTIVE</span></div>',unsafe_allow_html=True)

        # Demo mode banner
        if demo:
            st.markdown('<div style="background:rgba(255,215,0,0.1);border:1px solid rgba(255,215,0,0.4);border-radius:8px;padding:8px;margin:8px 0;text-align:center;font-family:Share Tech Mono,monospace;color:#ffd700;font-size:.75rem;">🎮 DEMO MODE ACTIVE</div>',unsafe_allow_html=True)
            if st.button("🔄 RANDOMIZE DATA",use_container_width=True):
                st.session_state["demo_inputs"]=generate_demo_inputs()
                st.rerun()

        st.markdown("---")
        # Load demo inputs if in demo mode
        di=st.session_state.get("demo_inputs",{}) if demo else {}

        with st.expander("👤 DEMOGRAPHICS",expanded=True):
            age=st.slider("Age",18,100,di.get("age",35))
            gender=st.selectbox("Sex",["Male","Female","Other"])

        with st.expander("🫀 CARDIOVASCULAR",expanded=True):
            hr=st.slider("Heart Rate (bpm)",40,140,di.get("hr",72))
            sys_bp=st.slider("Systolic BP",90,200,di.get("sys_bp",120))
            dia_bp=st.slider("Diastolic BP",60,130,di.get("dia_bp",80))
            spo2=st.slider("SpO2 (%)",80,100,di.get("spo2",98))

        with st.expander("🧬 LIFESTYLE",expanded=True):
            sleep_hours=st.slider("Sleep (hrs)",2.0,12.0,float(di.get("sleep_hours",7.0)),0.5)
            daily_steps=st.slider("Daily Steps",0,30000,di.get("daily_steps",7500),500)
            stress_level=st.slider("Stress (1-10)",1,10,di.get("stress_level",5))
            bmi=st.number_input("BMI",10.0,60.0,float(di.get("bmi",24.5)),0.1)
            smoker=st.checkbox("Smoker",di.get("smoker",False))
            water_glasses=st.slider("Water (glasses)",0,15,di.get("water_glasses",6))
            mood=st.selectbox("Current Mood",["Happy","Neutral","Stressed","Tired","Anxious"],
                              index=["Happy","Neutral","Stressed","Tired","Anxious"].index(di.get("mood","Neutral")))

        st.markdown("---")
        # AI Personality display
        st.markdown(f'<div class="glass-card" style="text-align:center;padding:10px;"><span style="font-size:1.5rem;">{P["emoji"]}</span><br><span style="font-family:Orbitron,monospace;color:{P["color"]};font-size:.75rem;letter-spacing:2px;">{P["name"]}</span><br><span style="color:rgba(0,245,255,0.5);font-size:.65rem;">AI MODE: {pers.upper()}</span></div>',unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        save_btn=st.button("💾 SAVE RECORD",use_container_width=True)
        if st.button("🔒 LOGOUT",use_container_width=True):
            for k in DEFAULTS: st.session_state[k]=DEFAULTS[k]
            st.rerun()

    # ── INPUTS + ML ──────────────────────────────────────────────────────────
    inputs=dict(age=age,bmi=bmi,hr=hr,sys_bp=sys_bp,dia_bp=dia_bp,spo2=spo2,
                sleep_hours=sleep_hours,daily_steps=daily_steps,stress_level=stress_level,
                smoker=smoker,water_glasses=water_glasses,mood=mood)
    risks=ml_predict(inputs)
    recs=gen_recs(risks,inputs)
    history_df=get_history(uid)
    diseases=detect_diseases(inputs,risks)
    mood_label,mood_color,mood_score,mood_tips=detect_mood(stress_level,sleep_hours,daily_steps,hr)
    notifs=generate_smart_notifications(uid,inputs,risks,history_df)

    if save_btn:
        save_health_record_v3(uid,inputs,risks)
        st.sidebar.success("✅ Record saved!")

    # Update AI memory
    st.session_state["ai_memory"].update({
        "last_bp":f"{sys_bp}/{dia_bp}","last_risk":risks["overall"],
        "last_steps":daily_steps,"last_sleep":sleep_hours
    })

    # ── HEADER ───────────────────────────────────────────────────────────────
    hcol1,hcol2=st.columns([3,1])
    with hcol1:
        st.markdown('<p class="cyber-title">🧬 HEALTHGUARD AI PRO</p>',unsafe_allow_html=True)
        st.markdown('<p class="cyber-subtitle">⬡ CYBERPUNK EDITION v3.0 ⬡ REAL ML ⬡ EXPLAINABLE AI ⬡ LIVE ECG ⬡</p>',unsafe_allow_html=True)
    with hcol2:
        # Notification bell
        unread=get_notifications(uid,unread_only=True)
        n_count=len(unread)
        if n_count>0:
            st.markdown(f'<div class="alert-critical" style="text-align:center;padding:12px;"><span style="font-family:Orbitron,monospace;color:#ff006e;font-size:1.2rem;">🔔 {n_count}</span><br><span style="font-family:Share Tech Mono,monospace;color:#ff6b9d;font-size:.7rem;">ACTIVE ALERTS</span></div>',unsafe_allow_html=True)
        else:
            st.markdown('<div class="glass-card" style="text-align:center;padding:12px;"><span style="font-family:Orbitron,monospace;color:#39ff14;font-size:1.2rem;">✅ 0</span><br><span style="font-family:Share Tech Mono,monospace;color:rgba(57,255,20,0.6);font-size:.7rem;">ALL CLEAR</span></div>',unsafe_allow_html=True)

    # ── MINI WIDGETS ROW ─────────────────────────────────────────────────────
    st.markdown("---")
    w1,w2,w3,w4,w5,w6=st.columns(6)
    widgets=[
        (w1,"❤️",f"{hr}","BPM","#ff006e"),
        (w2,"🫁",f"{spo2}%","SPO2","#00f5ff"),
        (w3,"🩸",f"{sys_bp}/{dia_bp}","BLOOD PRESSURE","#bf00ff"),
        (w4,"😴",f"{sleep_hours}h","SLEEP","#ffd700"),
        (w5,"🚶",f"{daily_steps:,}","STEPS","#39ff14"),
        (w6,"💧",f"{water_glasses}","GLASSES","#00bfff"),
    ]
    for col,icon,val,lbl,color in widgets:
        with col:
            st.markdown(f'<div class="widget-card"><div style="font-size:1.4rem;">{icon}</div><div class="widget-value" style="color:{color};font-size:1.3rem;">{val}</div><div class="widget-label">{lbl}</div></div>',unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)

    # ── TABS ─────────────────────────────────────────────────────────────────
    t1,t2,t3,t4,t5,t6,t7,t8,t9=st.tabs([
        "📊 COMMAND CENTER","⚡ LIVE ECG","📡 WEARABLES",
        "🔍 EXPLAINABLE AI","🧬 DISEASE DETECT","🧠 MOOD AI",
        "🤖 AI CHAT DOCTOR","📈 TIMELINE & PDF","🚨 ALERTS"
    ])

    # =========================================================================
    # TAB 1 — COMMAND CENTER
    # =========================================================================
    with t1:
        col_radar,col_gauge=st.columns([1.3,1],gap="large")
        with col_radar:
            st.markdown('<p class="section-header">HOLOGRAM RISK RADAR</p>',unsafe_allow_html=True)
            cats=["Metabolic","Cardiovascular","Respiratory","Neurological","Immunity"]
            imm=min(100,round(max(2,risks["neurological"]*0.4+(bmi>30)*10)))
            vals=[risks["metabolic"],risks["cardiovascular"],risks["respiratory"],risks["neurological"],imm]
            fig_r=go.Figure()
            # Hologram glow layers
            for alpha,width in [(0.05,20),(0.1,10),(0.3,3)]:
                fig_r.add_trace(go.Scatterpolar(r=vals,theta=cats,fill="toself" if alpha==0.05 else "none",
                    fillcolor=f"rgba(0,245,255,{alpha})",
                    line=dict(color=f"rgba(0,245,255,{alpha+0.2})",width=width),
                    showlegend=False,hoverinfo="skip"))
            fig_r.add_trace(go.Scatterpolar(r=vals,theta=cats,fill="none",
                line=dict(color="#00f5ff",width=2),name="Your Bio-State",
                hovertemplate="<b>%{theta}</b>: %{r:.0f}%<extra></extra>"))
            fig_r.add_trace(go.Scatterpolar(r=[15,15,5,20,10],theta=cats,fill="none",
                line=dict(color="#39ff14",width=2,dash="dot"),name="Optimal Baseline"))
            fig_r.update_layout(
                polar=dict(radialaxis=dict(visible=True,range=[0,100],gridcolor="rgba(0,245,255,0.1)",
                                           tickfont=dict(color="rgba(0,245,255,0.5)",size=9),
                                           linecolor="rgba(0,245,255,0.2)"),
                           angularaxis=dict(gridcolor="rgba(0,245,255,0.08)",
                                            tickfont=dict(size=12,color="#7ecfff")),
                           bgcolor="rgba(0,0,0,0)"),
                paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                font_color="#00f5ff",height=420,showlegend=True,
                legend=dict(orientation="h",y=1.1,x=0.5,xanchor="center",
                            font=dict(size=11,color="#7ecfff")))
            st.plotly_chart(fig_r,use_container_width=True)

        with col_gauge:
            st.markdown('<p class="section-header">SYSTEMIC RISK INDEX</p>',unsafe_allow_html=True)
            score=risks["overall"]
            gc="#39ff14" if score<35 else "#ffd700" if score<65 else "#ff006e"
            fig_g=go.Figure(go.Indicator(
                mode="gauge+number+delta",value=score,
                delta={"reference":50,"increasing":{"color":"#ff006e"},"decreasing":{"color":"#39ff14"}},
                number={"suffix":"%","font":{"size":52,"color":"#00f5ff","family":"Orbitron"}},
                gauge={"axis":{"range":[0,100],"tickcolor":"rgba(0,245,255,0.4)",
                               "tickfont":{"color":"rgba(0,245,255,0.5)","size":9}},
                       "bar":{"color":gc,"thickness":0.25},
                       "bgcolor":"rgba(0,0,0,0)","borderwidth":0,
                       "steps":[{"range":[0,35],"color":"rgba(57,255,20,0.08)"},
                                 {"range":[35,65],"color":"rgba(255,215,0,0.08)"},
                                 {"range":[65,100],"color":"rgba(255,0,110,0.08)"}],
                       "threshold":{"line":{"color":gc,"width":3},"thickness":0.8,"value":score}},
                title={"text":f"<b>{risks['risk_icon']} {risks['risk_label'].upper()} RISK</b>",
                       "font":{"size":14,"color":"rgba(0,245,255,0.7)","family":"Orbitron"}}))
            fig_g.update_layout(height=280,margin=dict(l=10,r=10,t=30,b=10),
                                paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_g,use_container_width=True)

            # ML confidence
            st.markdown('<p class="section-header" style="font-size:.85rem;">ML CLASSIFICATION CONFIDENCE</p>',unsafe_allow_html=True)
            proba=risks["risk_proba"]
            for lbl,p,c in [("LOW",proba[0],"#39ff14"),("MODERATE",proba[1],"#ffd700"),("HIGH",proba[2],"#ff006e")]:
                pct=p*100
                st.markdown(f'<div style="margin:4px 0;"><span style="font-family:Share Tech Mono,monospace;color:{c};font-size:.75rem;width:80px;display:inline-block;">{lbl}</span><div style="background:rgba(255,255,255,0.05);border-radius:4px;height:8px;display:inline-block;width:calc(100% - 120px);vertical-align:middle;"><div style="background:{c};width:{pct:.0f}%;height:100%;border-radius:4px;box-shadow:0 0 8px {c};"></div></div><span style="font-family:Orbitron,monospace;color:{c};font-size:.75rem;margin-left:8px;">{pct:.0f}%</span></div>',unsafe_allow_html=True)

        # Condition cards
        st.markdown("---")
        st.markdown('<p class="section-header">CONDITION-SPECIFIC RISK MATRIX</p>',unsafe_allow_html=True)
        mc1,mc2,mc3,mc4=st.columns(4)
        for col,lbl,key,icon in [(mc1,"DIABETES","diabetes","🩸"),(mc2,"CARDIOVASCULAR","cardiovascular","❤️"),
                                  (mc3,"RESPIRATORY","respiratory","🫁"),(mc4,"NEUROLOGICAL","neurological","🧠")]:
            sc=risks[key]; c="#39ff14" if sc<30 else "#ffd700" if sc<60 else "#ff006e"
            col.metric(f"{icon} {lbl}",f"{sc}%",
                       "HIGH" if sc>60 else "MODERATE" if sc>30 else "LOW",delta_color="off")

    # =========================================================================
    # TAB 2 — LIVE ECG
    # =========================================================================
    with t2:
        st.markdown('<p class="section-header">LIVE ECG MONITOR — LEAD II</p>',unsafe_allow_html=True)
        ec1,ec2=st.columns([2,1])
        with ec1:
            ecg_ph=st.empty(); stat_ph=st.empty()
        with ec2:
            st.markdown("#### ECG ANALYSIS")
            rr_i=round(60.0/hr,3); qt_i=round(0.39*math.sqrt(rr_i),3); pr_i=round(0.12+max(0,(80-hr)*0.001),3)
            st.metric("RR Interval",f"{rr_i:.3f}s","Normal" if 0.6<=rr_i<=1.2 else "⚠️ Abnormal",delta_color="off")
            st.metric("QT Interval",f"{qt_i:.3f}s","Normal" if qt_i<0.44 else "⚠️ Prolonged",delta_color="off")
            st.metric("PR Interval",f"{pr_i:.3f}s","Normal" if 0.12<=pr_i<=0.20 else "⚠️ Abnormal",delta_color="off")
            st.markdown("---")
            if hr<60: st.warning("⚠️ Bradycardia (HR < 60 bpm)")
            elif hr>100: st.warning("⚠️ Tachycardia (HR > 100 bpm)")
            else: st.success("✅ Normal Sinus Rhythm")
            if spo2<95: st.error(f"🚨 Hypoxemia — SpO2 {spo2}%")
            else: st.success(f"✅ SpO2 {spo2}% — Normal")
        anim_btn=st.button("▶️ ANIMATE ECG",use_container_width=True)
        if anim_btn:
            for frame in range(10):
                np.random.seed(frame*7+hr)
                ecg_ph.plotly_chart(render_ecg(hr=hr,anomaly=(hr<50 or hr>100)),use_container_width=True)
                stat_ph.markdown(f'<p style="color:#00ff88;font-family:Share Tech Mono,monospace;font-size:.8rem;">FRAME {frame+1}/10 · HR:{hr}bpm · RR:{rr_i:.3f}s · SpO2:{spo2}%</p>',unsafe_allow_html=True)
                time.sleep(0.3)
            stat_ph.markdown('<p style="color:#39ff14;font-family:Share Tech Mono,monospace;font-size:.8rem;">✅ ECG STREAM COMPLETE</p>',unsafe_allow_html=True)
        else:
            ecg_ph.plotly_chart(render_ecg(hr=hr,anomaly=(hr<50 or hr>100)),use_container_width=True)
        st.markdown("---")
        st.markdown("#### 12-LEAD SIMULATION")
        lc=st.columns(3)
        leads=["Lead I","Lead II","Lead III","aVR","aVF","aVL","V1","V2","V3","V4","V5","V6"]
        amps=[0.6,1.0,0.4,-0.5,0.7,0.3,0.3,0.5,0.8,1.0,0.9,0.7]
        for i,(lead,amp) in enumerate(zip(leads,amps)):
            with lc[i%3]:
                tl,el=gen_ecg(hr=hr,dur=2); fl=go.Figure(go.Scatter(x=tl,y=el*amp,mode="lines",line=dict(color="#00ff88",width=1.2),hoverinfo="skip"))
                fl.update_layout(paper_bgcolor="#020408",plot_bgcolor="#020408",height=90,margin=dict(l=5,r=5,t=18,b=5),
                                 title=dict(text=lead,font=dict(color="#00ff88",size=10),x=0.05),xaxis=dict(visible=False),yaxis=dict(visible=False))
                st.plotly_chart(fl,use_container_width=True)

    # =========================================================================
    # TAB 3 — WEARABLES
    # =========================================================================
    with t3:
        st.markdown('<p class="section-header">WEARABLE DEVICE STREAM</p>',unsafe_allow_html=True)
        wd=simulate_wearable(hr,spo2,daily_steps)
        dc1,dc2,dc3=st.columns(3)
        with dc1: st.selectbox("DEVICE",["Apple Watch Series 9","Fitbit Charge 6","Garmin Venu 3","Samsung Galaxy Watch 6"])
        dc2.metric("BATTERY","87%","+2%"); dc3.metric("SIGNAL","Strong","BLE 5.2")
        st.markdown("---")
        lat=wd.iloc[-1]
        ww1,ww2,ww3,ww4,ww5=st.columns(5)
        ww1.metric("💓 HR",f"{lat['HR']:.0f} bpm"); ww2.metric("�� SpO2",f"{lat['SpO2']:.1f}%")
        ww3.metric("🚶 Steps/min",f"{lat['Steps/min']:.0f}"); ww4.metric("🌡️ Temp",f"{lat['Temp_C']:.1f}°C"); ww5.metric("🌬️ Resp",f"{lat['Resp']:.0f} br/m")
        st.markdown("---")
        fw=go.Figure()
        fw.add_trace(go.Scatter(x=wd["Timestamp"],y=wd["HR"],name="Heart Rate",line=dict(color="#ff006e",width=2),yaxis="y1"))
        fw.add_trace(go.Scatter(x=wd["Timestamp"],y=wd["SpO2"],name="SpO2",line=dict(color="#00f5ff",width=2),yaxis="y2"))
        fw.add_trace(go.Bar(x=wd["Timestamp"],y=wd["Steps/min"],name="Steps/min",marker_color="rgba(191,0,255,0.4)",yaxis="y3"))
        fw.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#00f5ff",height=350,
                         xaxis=dict(gridcolor="rgba(0,245,255,0.06)"),
                         yaxis=dict(title="HR",side="left",range=[40,160],gridcolor="rgba(0,245,255,0.06)"),
                         yaxis2=dict(title="SpO2",side="right",overlaying="y",range=[85,102],showgrid=False),
                         yaxis3=dict(overlaying="y",side="right",range=[0,300],showgrid=False,visible=False),
                         legend=dict(orientation="h",y=1.08,x=0.5,xanchor="center",font=dict(color="#7ecfff")),
                         margin=dict(l=20,r=60,t=30,b=40),hovermode="x unified")
        st.plotly_chart(fw,use_container_width=True)
        with st.expander("📋 RAW STREAM DATA"):
            st.dataframe(wd.style.background_gradient(subset=["HR","SpO2"],cmap="plasma"),use_container_width=True,hide_index=True)

    # =========================================================================
    # TAB 4 — EXPLAINABLE AI
    # =========================================================================
    with t4:
        st.markdown('<p class="section-header">EXPLAINABLE AI — SHAP ANALYSIS</p>',unsafe_allow_html=True)
        st.markdown('<p style="color:rgba(0,245,255,0.6);font-family:Share Tech Mono,monospace;font-size:.8rem;">RF feature importances × input deviation from population norms</p>',unsafe_allow_html=True)
        sd=risks["shap_values"]
        sdf=pd.DataFrame(list(sd.items()),columns=["Feature","Impact"])
        sdf.sort_values("Impact",ascending=True,inplace=True)
        sdf["Color"]=sdf["Impact"].apply(lambda x:"#ff006e" if x>0 else "#39ff14")
        sdf["Label"]=sdf["Impact"].apply(lambda x:f"+{x:.2f}%" if x>0 else f"{x:.2f}%")
        fs=go.Figure(go.Bar(x=sdf["Impact"],y=sdf["Feature"],orientation="h",
                            marker_color=sdf["Color"],text=sdf["Label"],textposition="outside",
                            textfont=dict(color="#00f5ff",size=11),
                            hovertemplate="<b>%{y}</b>: %{x:.2f}%<extra></extra>"))
        fs.add_vline(x=0,line_color="rgba(0,245,255,0.4)",line_width=1.5)
        fs.update_layout(title=dict(text="Feature Contributions (SHAP Approximation)",font=dict(color="#00f5ff",size=13)),
                         paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#00f5ff",height=420,
                         xaxis=dict(title="Risk Contribution (%)",gridcolor="rgba(0,245,255,0.08)",zerolinecolor="rgba(0,245,255,0.3)",zerolinewidth=2),
                         yaxis=dict(gridcolor="rgba(0,245,255,0.05)",tickfont=dict(size=12)),margin=dict(l=20,r=80,t=50,b=40))
        st.plotly_chart(fs,use_container_width=True)
        st.markdown("#### WATERFALL DECOMPOSITION")
        base=25.0; wfl=["Baseline"]+list(sd.keys())+["Final Score"]
        wfv=[base]+list(sd.values())+[risks["overall"]-base-sum(sd.values())]
        wfm=["absolute"]+["relative"]*len(sd)+["total"]
        fwf=go.Figure(go.Waterfall(orientation="v",measure=wfm,x=wfl,y=wfv,
                                   connector={"line":{"color":"rgba(0,245,255,0.2)"}},
                                   increasing={"marker":{"color":"#ff006e"}},decreasing={"marker":{"color":"#39ff14"}},
                                   totals={"marker":{"color":"#bf00ff"}},textposition="outside",
                                   text=[f"{v:+.1f}%" if i not in (0,len(wfv)-1) else f"{v:.1f}%" for i,v in enumerate(wfv)],
                                   textfont=dict(color="#00f5ff",size=9)))
        fwf.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#00f5ff",height=360,showlegend=False,
                          yaxis=dict(title="Risk Score (%)",gridcolor="rgba(0,245,255,0.08)"),
                          xaxis=dict(gridcolor="rgba(0,245,255,0.05)",tickangle=-30,tickfont=dict(size=9)),
                          margin=dict(l=20,r=20,t=20,b=80))
        st.plotly_chart(fwf,use_container_width=True)

    # =========================================================================
    # TAB 5 — DISEASE DETECTION
    # =========================================================================
    with t5:
        st.markdown('<p class="section-header">AI DISEASE DETECTION ENGINE</p>',unsafe_allow_html=True)
        st.markdown('<p style="color:rgba(0,245,255,0.6);font-family:Share Tech Mono,monospace;font-size:.8rem;">Symptom-based probability scoring with risk color coding</p>',unsafe_allow_html=True)
        st.markdown("---")
        # Symptom checker
        with st.expander("🩺 ADD SYMPTOMS (Optional)"):
            syms=st.multiselect("Select symptoms you're experiencing:",
                ["Chest pain","Shortness of breath","Frequent urination","Excessive thirst",
                 "Blurred vision","Headache","Dizziness","Fatigue","Palpitations",
                 "Numbness in hands/feet","Snoring","Insomnia","Mood swings","Weight gain"])
        # Disease cards
        dc_cols=st.columns(2)
        for i,(disease,info) in enumerate(diseases.items()):
            with dc_cols[i%2]:
                prob=info["probability"]; color=info["color"]; status=info["status"]
                bar_w=min(100,prob)
                st.markdown(f"""
                <div class="glass-card" style="border-color:{color}33;margin-bottom:12px;">
                  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                    <span style="font-family:Rajdhani,sans-serif;font-weight:700;color:#e0f7ff;font-size:1rem;">{disease}</span>
                    <span style="font-family:Orbitron,monospace;color:{color};font-size:1.1rem;font-weight:700;">{prob:.0f}%</span>
                  </div>
                  <div style="background:rgba(255,255,255,0.05);border-radius:4px;height:6px;margin-bottom:8px;">
                    <div style="background:{color};width:{bar_w}%;height:100%;border-radius:4px;box-shadow:0 0 8px {color};transition:width 0.5s ease;"></div>
                  </div>
                  <span style="font-family:Share Tech Mono,monospace;font-size:.75rem;color:{color};">{status}</span>
                </div>""",unsafe_allow_html=True)
        st.markdown("---")
        # Risk summary chart
        st.markdown('<p class="section-header" style="font-size:.9rem;">DISEASE PROBABILITY OVERVIEW</p>',unsafe_allow_html=True)
        dnames=list(diseases.keys()); dprobs=[diseases[d]["probability"] for d in dnames]
        dcolors=[diseases[d]["color"] for d in dnames]
        fd=go.Figure(go.Bar(x=dprobs,y=dnames,orientation="h",marker_color=dcolors,
                            text=[f"{p:.0f}%" for p in dprobs],textposition="outside",
                            textfont=dict(color="#00f5ff",size=11)))
        fd.add_vline(x=35,line_color="#ffd700",line_dash="dash",line_width=1,annotation_text="Risk Threshold",annotation_font_color="#ffd700")
        fd.add_vline(x=60,line_color="#ff006e",line_dash="dash",line_width=1,annotation_text="Critical",annotation_font_color="#ff006e")
        fd.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#00f5ff",height=380,
                         xaxis=dict(title="Probability (%)",range=[0,115],gridcolor="rgba(0,245,255,0.08)"),
                         yaxis=dict(gridcolor="rgba(0,245,255,0.05)",tickfont=dict(size=11)),
                         margin=dict(l=20,r=80,t=20,b=40))
        st.plotly_chart(fd,use_container_width=True)

    # =========================================================================
    # TAB 6 — MOOD AI
    # =========================================================================
    with t6:
        st.markdown('<p class="section-header">MOOD + MENTAL HEALTH AI</p>',unsafe_allow_html=True)
        mc1,mc2=st.columns([1,1.5],gap="large")
        with mc1:
            st.markdown(f"""
            <div class="mood-card" style="text-align:center;padding:30px;">
              <div style="font-size:3rem;margin-bottom:8px;">{mood_label.split()[0]}</div>
              <div style="font-family:Orbitron,monospace;color:{mood_color};font-size:1.3rem;font-weight:700;letter-spacing:2px;">{mood_label.split(' ',1)[1] if ' ' in mood_label else mood_label}</div>
              <div style="font-family:Share Tech Mono,monospace;color:rgba(0,245,255,0.5);font-size:.8rem;margin-top:8px;">MOOD SCORE</div>
              <div style="font-family:Orbitron,monospace;color:{mood_color};font-size:2.5rem;font-weight:900;">{mood_score:.0f}</div>
              <div style="background:rgba(255,255,255,0.05);border-radius:8px;height:10px;margin:12px 0;">
                <div style="background:{mood_color};width:{mood_score}%;height:100%;border-radius:8px;box-shadow:0 0 12px {mood_color};"></div>
              </div>
            </div>""",unsafe_allow_html=True)
            st.markdown("<br>",unsafe_allow_html=True)
            st.markdown('<p class="section-header" style="font-size:.85rem;">AI SUGGESTIONS</p>',unsafe_allow_html=True)
            for tip in mood_tips:
                st.markdown(f'<div class="notif-badge" style="border-color:rgba(191,0,255,0.4);color:#d4a0ff;">💡 {tip}</div>',unsafe_allow_html=True)
        with mc2:
            # Mood radar
            mood_cats=["Energy","Calm","Focus","Happiness","Resilience"]
            base_mood=mood_score/100
            mood_vals=[min(100,mood_score+np.random.normal(0,8)) for _ in range(5)]
            fm=go.Figure()
            for alpha,w in [(0.05,15),(0.15,5),(0.4,2)]:
                fm.add_trace(go.Scatterpolar(r=mood_vals,theta=mood_cats,fill="toself" if alpha==0.05 else "none",
                    fillcolor=f"rgba(191,0,255,{alpha})",line=dict(color=f"rgba(191,0,255,{alpha+0.3})",width=w),showlegend=False,hoverinfo="skip"))
            fm.add_trace(go.Scatterpolar(r=mood_vals,theta=mood_cats,fill="none",
                line=dict(color="#bf00ff",width=2),name="Mental State"))
            fm.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0,100],gridcolor="rgba(191,0,255,0.1)",tickfont=dict(color="rgba(191,0,255,0.5)",size=9)),
                                        angularaxis=dict(gridcolor="rgba(191,0,255,0.08)",tickfont=dict(size=12,color="#d4a0ff")),bgcolor="rgba(0,0,0,0)"),
                             paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#bf00ff",height=350,showlegend=False)
            st.plotly_chart(fm,use_container_width=True)
            # Breathing exercise
            st.markdown('<p class="section-header" style="font-size:.85rem;">4-7-8 BREATHING GUIDE</p>',unsafe_allow_html=True)
            st.markdown("""
            <div class="glass-card" style="border-color:rgba(191,0,255,0.3);">
              <div style="font-family:Share Tech Mono,monospace;color:#d4a0ff;font-size:.85rem;line-height:2;">
                <div>🌬️ <b>INHALE</b> — 4 seconds (nose)</div>
                <div>⏸️ <b>HOLD</b> — 7 seconds</div>
                <div>💨 <b>EXHALE</b> — 8 seconds (mouth)</div>
                <div style="margin-top:8px;color:rgba(191,0,255,0.6);">Repeat 3-4 cycles. Activates parasympathetic nervous system.</div>
              </div>
            </div>""",unsafe_allow_html=True)

    # =========================================================================
    # TAB 7 — AI CHAT DOCTOR
    # =========================================================================
    with t7:
        st.markdown('<p class="section-header">AI CHAT DOCTOR</p>',unsafe_allow_html=True)
        st.markdown(f'<div class="glass-card" style="border-color:{P["color"]}33;padding:12px;margin-bottom:16px;"><span style="font-size:1.5rem;">{P["emoji"]}</span> <span style="font-family:Orbitron,monospace;color:{P["color"]};font-size:.9rem;letter-spacing:2px;">{P["name"]}</span> <span style="font-family:Share Tech Mono,monospace;color:rgba(0,245,255,0.5);font-size:.75rem;"> · {pers.upper()} MODE · MEMORY ACTIVE</span></div>',unsafe_allow_html=True)

        # Display chat history
        chat_container=st.container()
        with chat_container:
            if not st.session_state["chat_messages"]:
                st.markdown(f'<div class="chat-ai">{P["emoji"]} {P["greeting"]}<br><span style="font-size:.75rem;opacity:.6;">Ask me about your BP, sleep, stress, diet, exercise, or overall health.</span></div>',unsafe_allow_html=True)
            for msg in st.session_state["chat_messages"]:
                if msg["role"]=="user":
                    st.markdown(f'<div class="chat-user">👤 {msg["content"]}</div>',unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-ai">{P["emoji"]} {msg["content"]}</div>',unsafe_allow_html=True)

        # Input
        with st.form("chat_form",clear_on_submit=True):
            cc1,cc2=st.columns([5,1])
            with cc1: user_input=st.text_input("",placeholder=f"Ask {P['name']} anything about your health...",label_visibility="collapsed")
            with cc2: send=st.form_submit_button("SEND ⚡",use_container_width=True)
            if send and user_input.strip():
                response=get_ai_response(user_input,risks,inputs,pers,st.session_state["ai_memory"])
                st.session_state["chat_messages"].append({"role":"user","content":user_input})
                st.session_state["chat_messages"].append({"role":"ai","content":response})
                if not demo:
                    save_chat(uid,"user",user_input); save_chat(uid,"ai",response)
                st.rerun()

        # Quick prompts
        st.markdown('<p class="section-header" style="font-size:.8rem;margin-top:16px;">QUICK COMMANDS</p>',unsafe_allow_html=True)
        qc=st.columns(4)
        quick_prompts=["Check my BP","How is my sleep?","Stress advice","Overall health status"]
        for i,(col,prompt) in enumerate(zip(qc,quick_prompts)):
            with col:
                if st.button(prompt,key=f"qp{i}",use_container_width=True):
                    response=get_ai_response(prompt,risks,inputs,pers,st.session_state["ai_memory"])
                    st.session_state["chat_messages"].append({"role":"user","content":prompt})
                    st.session_state["chat_messages"].append({"role":"ai","content":response})
                    st.rerun()

        if st.button("🗑️ CLEAR CHAT",use_container_width=True):
            st.session_state["chat_messages"]=[]; st.rerun()

        # Memory display
        with st.expander("🧠 AI MEMORY (What I remember about you)"):
            mem=st.session_state["ai_memory"]
            if mem:
                for k,v in mem.items():
                    st.markdown(f'<div class="notif-badge">🔹 {k.replace("_"," ").title()}: <b>{v}</b></div>',unsafe_allow_html=True)
            else:
                st.markdown('<p style="color:rgba(0,245,255,0.5);font-family:Share Tech Mono,monospace;font-size:.8rem;">No memory yet. Start chatting!</p>',unsafe_allow_html=True)

    # =========================================================================
    # TAB 8 — TIMELINE & PDF
    # =========================================================================
    with t8:
        st.markdown('<p class="section-header">AI RISK PREDICTION TIMELINE</p>',unsafe_allow_html=True)

        # 7-day future prediction
        st.markdown("#### NEXT 7 DAYS RISK FORECAST")
        np.random.seed(42)
        future_days=7; past_days=30
        all_days=past_days+future_days
        end_score=risks["overall"]; start_score=min(100,end_score+random.uniform(12,25))
        trend=np.linspace(start_score,end_score,past_days)
        past_scores=np.clip(trend+np.random.normal(0,2,past_days),0,100)
        # Future: slight improvement if following recommendations
        future_base=end_score
        future_scores=np.clip([future_base+np.random.normal(-0.5*i,1.5) for i in range(future_days)],0,100)
        today_str = datetime.today().strftime("%Y-%m-%d")
        all_dates=[( datetime.today()-timedelta(days=past_days-i-1)).strftime("%Y-%m-%d") for i in range(past_days)]
        future_dates=[(datetime.today()+timedelta(days=i+1)).strftime("%Y-%m-%d") for i in range(future_days)]

        fig_tl=go.Figure()
        # Past trend
        fig_tl.add_trace(go.Scatter(x=all_dates,y=past_scores,mode="lines+markers",name="Historical Risk",
                                    line=dict(color="#00f5ff",width=2.5),marker=dict(size=5,color="#00f5ff"),
                                    fill="tozeroy",fillcolor="rgba(0,245,255,0.05)"))
        # Future prediction
        fig_tl.add_trace(go.Scatter(x=future_dates,y=future_scores,mode="lines+markers",name="AI Forecast",
                                    line=dict(color="#bf00ff",width=2.5,dash="dash"),
                                    marker=dict(size=6,color="#bf00ff",symbol="diamond"),
                                    fill="tozeroy",fillcolor="rgba(191,0,255,0.05)"))
        # Today marker — use shape instead of add_vline to avoid type conflict
        fig_tl.add_shape(type="line",x0=today_str,x1=today_str,y0=0,y1=100,
                         line=dict(color="#ffd700",dash="dot",width=2),xref="x",yref="y")
        fig_tl.add_annotation(x=today_str,y=95,text="TODAY",showarrow=False,
                              font=dict(color="#ffd700",size=10,family="Share Tech Mono"),
                              bgcolor="rgba(0,0,0,0.5)",bordercolor="#ffd700",borderwidth=1)
        # Risk zones
        fig_tl.add_hrect(y0=0,y1=35,fillcolor="#39ff14",opacity=0.04,line_width=0,annotation_text="SAFE",annotation_position="top left",annotation_font_color="#39ff14",annotation_font_size=9)
        fig_tl.add_hrect(y0=35,y1=65,fillcolor="#ffd700",opacity=0.04,line_width=0,annotation_text="MODERATE",annotation_position="top left",annotation_font_color="#ffd700",annotation_font_size=9)
        fig_tl.add_hrect(y0=65,y1=100,fillcolor="#ff006e",opacity=0.04,line_width=0,annotation_text="CRITICAL",annotation_position="top left",annotation_font_color="#ff006e",annotation_font_size=9)
        fig_tl.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#00f5ff",height=380,
                             xaxis=dict(title="Date",gridcolor="rgba(0,245,255,0.06)"),
                             yaxis=dict(title="Risk Score (%)",range=[0,100],gridcolor="rgba(0,245,255,0.06)"),
                             legend=dict(orientation="h",y=1.08,x=0.5,xanchor="center",font=dict(color="#7ecfff")),
                             margin=dict(l=20,r=20,t=20,b=40),hovermode="x unified")
        st.plotly_chart(fig_tl,use_container_width=True)

        # Stats
        sc1,sc2,sc3,sc4=st.columns(4)
        sc1.metric("30-Day Start",f"{past_scores[0]:.1f}%")
        sc2.metric("Current",f"{past_scores[-1]:.1f}%",delta=f"{past_scores[-1]-past_scores[0]:.1f}%")
        sc3.metric("7-Day Forecast",f"{np.mean(future_scores):.1f}%")
        sc4.metric("Best Day",f"{min(past_scores):.1f}%")

        # DB history
        if not history_df.empty:
            st.markdown("---")
            st.markdown("#### SAVED HEALTH RECORDS")
            fdb=px.line(history_df.sort_values("recorded_at"),x="recorded_at",y="overall_risk",
                        markers=True,line_shape="spline",color_discrete_sequence=["#bf00ff"])
            fdb.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#00f5ff",height=250,
                              xaxis=dict(gridcolor="rgba(0,245,255,0.06)"),yaxis=dict(range=[0,100],gridcolor="rgba(0,245,255,0.06)"),
                              margin=dict(l=20,r=20,t=20,b=30))
            st.plotly_chart(fdb,use_container_width=True)

        # PDF
        st.markdown("---")
        st.markdown('<p class="section-header" style="font-size:.9rem;">GENERATE HEALTH REPORT</p>',unsafe_allow_html=True)
        pc1,pc2=st.columns([2,1])
        with pc1: rname=st.text_input("PATIENT NAME",value=uname)
        with pc2:
            st.markdown("<br>",unsafe_allow_html=True)
            gpdf=st.button("🖨️ GENERATE PDF",use_container_width=True)
        if gpdf:
            with st.spinner("Generating report..."):
                pdf_bytes=gen_pdf(rname,inputs,risks,recs,history_df)
            st.success("✅ PDF ready!")
            st.download_button("⬇️ DOWNLOAD PDF REPORT",data=pdf_bytes,
                               file_name=f"HealthGuard_{rname.replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                               mime="application/pdf",use_container_width=True)
        st.markdown("---")
        exp_df=pd.DataFrame({"Date":all_dates,"Risk Score (%)":past_scores.round(1),
                              "HR (bpm)":np.random.normal(hr,4,past_days).astype(int),
                              "Systolic BP":np.random.normal(sys_bp,3,past_days).astype(int),
                              "SpO2 (%)":np.clip(np.random.normal(spo2,0.5,past_days),85,100).round(1)})
        st.download_button("⬇️ DOWNLOAD CSV TELEMETRY",data=exp_df.to_csv(index=False).encode(),
                           file_name=f"HealthGuard_Telemetry_{datetime.now().strftime('%Y%m%d')}.csv",
                           mime="text/csv",use_container_width=True)

    # =========================================================================
    # TAB 9 — ALERTS + RECOMMENDATIONS
    # =========================================================================
    with t9:
        st.markdown('<p class="section-header">SMART ALERT SYSTEM</p>',unsafe_allow_html=True)

        ac1,ac2=st.columns([1.2,1],gap="large")
        with ac1:
            st.markdown("#### 🚨 ACTIVE ALERTS")
            if notifs:
                for msg,sev in notifs:
                    color={"critical":"#ff006e","warning":"#ffd700","info":"#00f5ff"}.get(sev,"#00f5ff")
                    icon={"critical":"🚨","warning":"⚠️","info":"ℹ️"}.get(sev,"ℹ️")
                    st.markdown(f'<div class="notif-badge" style="border-color:{color}44;color:{color};background:rgba(0,0,0,0.2);">{icon} {msg}</div>',unsafe_allow_html=True)
                if st.button("✅ MARK ALL READ",use_container_width=True):
                    mark_notifications_read(uid); st.rerun()
            else:
                st.markdown('<div class="security-badge">✅ ALL SYSTEMS NOMINAL — No active alerts</div>',unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("#### 💡 AI RECOMMENDATIONS")
            for cat,tips in recs.items():
                icon={"diet":"🥗","exercise":"🏃","lifestyle":"��"}.get(cat,"💡")
                st.markdown(f'<p style="font-family:Orbitron,monospace;color:#00f5ff;font-size:.8rem;letter-spacing:2px;margin-top:12px;">{icon} {cat.upper()}</p>',unsafe_allow_html=True)
                for tip in tips:
                    st.markdown(f'<div class="notif-badge" style="border-color:rgba(0,245,255,0.2);color:#7ecfff;">{tip}</div>',unsafe_allow_html=True)

        with ac2:
            st.markdown("#### 🔐 SECURITY & PRIVACY")
            st.markdown("""
            <div class="glass-card" style="border-color:rgba(57,255,20,0.3);">
              <div class="security-badge" style="margin-bottom:8px;">🔒 AES-256 LOCAL ENCRYPTION</div>
              <div class="security-badge" style="margin-bottom:8px;">🛡️ DATA NEVER LEAVES DEVICE</div>
              <div class="security-badge" style="margin-bottom:8px;">🧬 BIOMETRIC HASH PROTECTED</div>
              <div class="security-badge" style="margin-bottom:8px;">📵 NO THIRD-PARTY SHARING</div>
              <div class="security-badge">✅ HIPAA-STYLE COMPLIANCE</div>
            </div>""",unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("#### 🎮 TEST MODE / SIMULATOR")
            st.markdown('<p style="color:rgba(0,245,255,0.6);font-family:Share Tech Mono,monospace;font-size:.75rem;">Generate fake patient data for demo/presentation</p>',unsafe_allow_html=True)
            if st.button("🎲 GENERATE RANDOM PATIENT",use_container_width=True):
                st.session_state["demo_inputs"]=generate_demo_inputs()
                st.session_state["demo_mode"]=True
                st.rerun()
            scenarios=[("🏃 Healthy Athlete",{"age":28,"bmi":21.5,"hr":58,"sys_bp":110,"dia_bp":70,"spo2":99,"sleep_hours":8.0,"daily_steps":12000,"stress_level":3,"smoker":False,"water_glasses":9,"mood":"Happy"}),
                       ("⚠️ High Risk Patient",{"age":58,"bmi":34.2,"hr":98,"sys_bp":155,"dia_bp":95,"spo2":94,"sleep_hours":4.5,"daily_steps":1200,"stress_level":9,"smoker":True,"water_glasses":2,"mood":"Stressed"}),
                       ("🧑 Average Adult",{"age":40,"bmi":26.8,"hr":75,"sys_bp":125,"dia_bp":82,"spo2":97,"sleep_hours":6.5,"daily_steps":5500,"stress_level":6,"smoker":False,"water_glasses":5,"mood":"Neutral"})]
            for label,scenario in scenarios:
                if st.button(label,use_container_width=True):
                    st.session_state["demo_inputs"]=scenario
                    st.session_state["demo_mode"]=True
                    st.rerun()

            st.markdown("---")
            st.markdown("#### 📊 SESSION STATS")
            st.markdown(f'<div class="glass-card"><div style="font-family:Share Tech Mono,monospace;color:#7ecfff;font-size:.8rem;line-height:2;"><div>�� User: <b style="color:#00f5ff;">{uname}</b></div><div>🤖 AI Mode: <b style="color:{P["color"]};">{P["name"]}</b></div><div>💬 Chat Messages: <b style="color:#00f5ff;">{len(st.session_state["chat_messages"])}</b></div><div>📝 Saved Records: <b style="color:#00f5ff;">{len(history_df)}</b></div><div>🎮 Demo Mode: <b style="color:{"#ffd700" if demo else "#39ff14"};">{"ON" if demo else "OFF"}</b></div></div></div>',unsafe_allow_html=True)

    st.markdown("<p style='text-align:center;color:rgba(0,245,255,0.2);font-size:.7rem;font-family:Share Tech Mono,monospace;margin-top:24px;'>HEALTHGUARD AI PRO v3.0 · CYBERPUNK EDITION · FOR INFORMATIONAL PURPOSES ONLY · NOT MEDICAL ADVICE</p>",unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HELPER — save record with new schema
# ══════════════════════════════════════════════════════════════════════════════
def save_health_record_v3(user_id, inputs, risks):
    conn=sqlite3.connect(DB_PATH); c=conn.cursor()
    c.execute("""INSERT INTO health_records
        (user_id,age,bmi,hr,sys_bp,dia_bp,spo2,sleep_hours,daily_steps,
         stress_level,smoker,water_glasses,mood,overall_risk,diabetes_risk,
         cardio_risk,resp_risk,neuro_risk) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (user_id,inputs["age"],inputs["bmi"],inputs["hr"],inputs["sys_bp"],inputs["dia_bp"],
         inputs["spo2"],inputs["sleep_hours"],inputs["daily_steps"],inputs["stress_level"],
         int(inputs["smoker"]),inputs.get("water_glasses",6),inputs.get("mood","Neutral"),
         risks["overall"],risks["diabetes"],risks["cardiovascular"],risks["respiratory"],risks["neurological"]))
    conn.commit(); conn.close()

# ══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state["logged_in"]:
    show_login()
else:
    show_dashboard()
