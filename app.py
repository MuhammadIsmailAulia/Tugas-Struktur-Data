import streamlit as st
from datetime import datetime

# ── Konfigurasi Halaman ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sistem Antrian Tol",
    page_icon="🛣️",
    layout="wide"
)

# ── Styling ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #f3f2ef; }

/* Sembunyikan elemen bawaan streamlit */
#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
}

/* Brand header */
.brand-wrap { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.5rem; }
.brand-inner { display: flex; align-items: center; gap: 12px; }
.brand-icon { width: 40px; height: 40px; border-radius: 10px; background: #E6F1FB; display: flex; align-items: center; justify-content: center; font-size: 22px; }
.brand-title { font-size: 17px; font-weight: 600; color: #1a1a1a; margin: 0; }
.brand-sub { font-size: 12px; color: #888; margin: 0; }

/* Stat cards */
.stat-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 10px; margin-bottom: 1.25rem; }
.scard { background: #fff; border: 0.5px solid rgba(0,0,0,0.1); border-radius: 10px; padding: 14px 16px; }
.scard-icon { font-size: 20px; margin-bottom: 6px; }
.scard-val { font-size: 26px; font-weight: 600; color: #1a1a1a; line-height: 1; }
.scard-lbl { font-size: 11px; color: #888; margin-top: 3px; }

/* Input panel */
.input-panel { background: #fff; border: 0.5px solid rgba(0,0,0,0.1); border-radius: 12px; padding: 1rem 1.25rem; margin-bottom: 1.25rem; }

/* Lane cards */
.lane { background: #fff; border: 0.5px solid rgba(0,0,0,0.1); border-radius: 12px; overflow: hidden; height: 100%; }
.lane-hdr { padding: 12px 14px; border-bottom: 0.5px solid rgba(0,0,0,0.08); display: flex; align-items: center; justify-content: space-between; }
.lane-title { font-size: 13px; font-weight: 600; display: flex; align-items: center; gap: 8px; }
.dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; flex-shrink: 0; }
.lane-badge { font-size: 11px; font-weight: 500; padding: 2px 9px; border-radius: 6px; }
.lane-body { padding: 10px 12px; min-height: 180px; }
.chip { display: flex; align-items: center; gap: 8px; padding: 7px 10px; border-radius: 8px; margin-bottom: 6px; border: 0.5px solid rgba(0,0,0,0.09); font-family: 'JetBrains Mono', monospace; }
.chip-num { font-size: 11px; color: #aaa; min-width: 16px; }
.chip-name { font-size: 13px; color: #1a1a1a; flex: 1; }
.chip-front { font-size: 10px; font-weight: 600; padding: 2px 7px; border-radius: 5px; margin-left: auto; }
.empty-lane { text-align: center; padding: 2.5rem 0; color: #bbb; font-size: 13px; }
.bar-wrap { padding: 0 12px 12px; }
.bar-bg { height: 4px; background: #f0f0f0; border-radius: 2px; overflow: hidden; }
.bar-fill { height: 4px; border-radius: 2px; transition: width .3s; }

/* Log */
.log-wrap { background: #fff; border: 0.5px solid rgba(0,0,0,0.1); border-radius: 12px; overflow: hidden; margin-top: 1.25rem; }
.log-hdr { padding: 10px 14px; border-bottom: 0.5px solid rgba(0,0,0,0.08); font-size: 12px; font-weight: 500; color: #888; }
.log-row { display: flex; align-items: center; gap: 10px; padding: 6px 14px; font-family: 'JetBrains Mono', monospace; font-size: 12px; }
.log-row:hover { background: #fafafa; }
.log-time { color: #bbb; min-width: 64px; }
.log-pill { font-size: 10px; font-weight: 600; padding: 1px 7px; border-radius: 5px; min-width: 44px; text-align: center; }
.log-msg { color: #444; flex: 1; }
.pill-in { background: #EAF3DE; color: #27500A; }
.pill-out { background: #FAEEDA; color: #633806; }
.pill-err { background: #FCEBEB; color: #791F1F; }
.pill-sys { background: #F1EFE8; color: #444441; }
.no-log { text-align: center; padding: 20px; font-size: 13px; color: #bbb; }

/* Override tombol Streamlit */
.stButton > button {
    border-radius: 8px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    height: 36px !important;
    padding: 0 16px !important;
    transition: opacity .15s !important;
}
.stButton > button:hover { opacity: .85 !important; }

div[data-testid