import streamlit as st

st.set_page_config(page_title="Sistem Antrian Tol", page_icon="🛣️", layout="wide")

st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #0F172A; }

/* Sembunyikan elemen bawaan streamlit yang tidak perlu */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem !important; padding-bottom: 2rem !important; }

/* Brand header */
.brand-wrap {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 1.5rem;
}
.brand-inner { display: flex; align-items: center; gap: 12px; }
.brand-icon {
    width: 40px; height: 40px; border-radius: 10px;
    background: #1E293B; display: flex; align-items: center;
    justify-content: center; font-size: 22px;
}
.brand-title { font-size: 17px; font-weight: 600; color: #F8FAFC;; margin: 0; }
.brand-sub   { font-size: 12px; color: #888; margin: 0; }

/* Stat cards */
.stat-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 10px; margin-bottom: 1.25rem; }
.scard {
    background: #1E293B; border: 0.5px solid rgba(0,0,0,0.1);
    border-radius: 10px; padding: 14px 16px;
}
.scard-icon { font-size: 20px; margin-bottom: 6px; }
.scard-val  { font-size: 26px; font-weight: 600; color: #1a1a1a; line-height: 1; }
.scard-lbl  { font-size: 11px; color: #888; margin-top: 3px; }

/* Input panel */
.input-panel {
    background: #1E293B; border: 0.5px solid rgba(0,0,0,0.1);
    border-radius: 12px; padding: 1rem 1.25rem; margin-bottom: 1.25rem;
}

/* Lane cards */
.lane {
    background: #1E293B; border: 0.5px solid rgba(0,0,0,0.1);
    border-radius: 12px; overflow: hidden; height: 100%;
}
.lane-hdr {
    padding: 12px 14px; border-bottom: 0.5px solid rgba(0,0,0,0.08);
    display: flex; align-items: center; justify-content: space-between;
}
.lane-title { font-size: 13px; font-weight: 600; display: flex; align-items: center; gap: 8px; }
.dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; flex-shrink: 0; }
.lane-badge { font-size: 11px; font-weight: 500; padding: 2px 9px; border-radius: 6px; }
.lane-body  { padding: 10px 12px; min-height: 180px; }
.chip {
    display: flex; align-items: center; gap: 8px;
    padding: 7px 10px; border-radius: 8px; margin-bottom: 6px;
    border: 0.5px solid rgba(0,0,0,0.09);
    font-family: 'JetBrains Mono', monospace;
}
.chip-num  { font-size: 11px; color: #aaa; min-width: 16px; }
.chip-name { font-size: 13px; color: #1a1a1a; flex: 1; }
.chip-front { font-size: 10px; font-weight: 600; padding: 2px 7px; border-radius: 5px; margin-left: auto; }
.empty-lane { text-align: center; padding: 2.5rem 0; color: #bbb; font-size: 13px; }
.bar-wrap { padding: 0 12px 12px; }
.bar-bg   { height: 4px; background: #f0f0f0; border-radius: 2px; overflow: hidden; }
.bar-fill { height: 4px; border-radius: 2px; transition: width .3s; }

/* Log */
.log-wrap {
    background: #fff; border: 0.5px solid rgba(0,0,0,0.1);
    border-radius: 12px; overflow: hidden; margin-top: 1.25rem;
}
.log-hdr {
    padding: 10px 14px; border-bottom: 0.5px solid rgba(0,0,0,0.08);
    font-size: 12px; font-weight: 500; color: #888;
}
.log-row {
    display: flex; align-items: center; gap: 10px;
    padding: 6px 14px; font-family: 'JetBrains Mono', monospace; font-size: 12px;
}
.log-row:hover { background: #fafafa; }
.log-time { color: #bbb; min-width: 64px; }
.log-pill { font-size: 10px; font-weight: 600; padding: 1px 7px; border-radius: 5px; min-width: 44px; text-align: center; }
.log-msg  { color: #444; flex: 1; }
.pill-in  { background: #EAF3DE; color: #27500A; }
.pill-out { background: #FAEEDA; color: #633806; }
.pill-err { background: #FCEBEB; color: #791F1F; }
.pill-sys { background: #F1EFE8; color: #444441; }
.no-log   { text-align: center; padding: 20px; font-size: 13px; color: #bbb; }

/* Override tombol Streamlit */
.stButton > button {
    border-radius: 8px !important; font-size: 13px !important;
    font-weight: 500 !important; height: 36px !important;
    padding: 0 16px !important; transition: opacity .15s !important;
}
.stButton > button:hover { opacity: .85 !important; }

div[data-testid="stTextInput"] input {
    border-radius: 8px !important; font-size: 13px !important;
    font-family: 'JetBrains Mono', monospace !important;
    background: #fff !important; border: 0.5px solid rgba(0,0,0,0.2) !important;
}
div[data-testid="stSelectbox"] > div > div {
    border-radius: 8px !important; font-size: 13px !important;
    background: #fff !important; border: 0.5px solid rgba(0,0,0,0.2) !important;
}
</style>
""", unsafe_allow_html=True)


# ── Data ────────────────────────────────────────────────────────────────────
class Queue:
    def __init__(self):
        self.data = []
    def enqueue(self, k): self.data.append(k)
    def dequeue(self):
        return self.data.pop(0) if self.data else None
    def size(self): return len(self.data)
    def display(self): return self.data.copy()

class MultiQueueTol:
    def __init__(self):
        self.tol = [Queue(), Queue(), Queue()]

    def masuk_tol(self, kendaraan):
        sizes = [q.size() for q in self.tol]
        lane = sizes.index(min(sizes))
        self.tol[lane].enqueue(kendaraan)
        return lane + 1

    def keluar_tol(self, nomor):
        return self.tol[nomor - 1].dequeue()

    def lihat_antrian(self):
        return {i+1: self.tol[i].display() for i in range(3)}

    def total(self):
        return sum(q.size() for q in self.tol)


# ── Session State ────────────────────────────────────────────────────────────
if "tol"        not in st.session_state: st.session_state.tol = MultiQueueTol()
if "log"        not in st.session_state: st.session_state.log = []
if "total_masuk"  not in st.session_state: st.session_state.total_masuk = 0
if "total_keluar" not in st.session_state: st.session_state.total_keluar = 0

tol   = st.session_state.tol
antrian = tol.lihat_antrian()

LANE_COLORS = [
    {"dot": "#378ADD", "bg": "#E6F1FB", "txt": "#0C447C", "bar": "#378ADD",
     "front_bg": "#E6F1FB", "front_txt": "#0C447C"},
    {"dot": "#1D9E75", "bg": "#E1F5EE", "txt": "#085041", "bar": "#1D9E75",
     "front_bg": "#E1F5EE", "front_txt": "#085041"},
    {"dot": "#7F77DD", "bg": "#EEEDFE", "txt": "#3C3489", "bar": "#7F77DD",
     "front_bg": "#EEEDFE", "front_txt": "#3C3489"},
]

from datetime import datetime
def now(): return datetime.now().strftime("%H:%M:%S")

def add_log(tipe, pesan):
    st.session_state.log.insert(0, {"time": now(), "type": tipe, "msg": pesan})
    if len(st.session_state.log) > 50:
        st.session_state.log.pop()


# ── Brand Header ─────────────────────────────────────────────────────────────
col_brand, col_reset = st.columns([5, 1])
with col_brand:
    st.markdown("""
    <div class="brand-wrap">
      <div class="brand-inner">
        <div class="brand-icon">🛣️</div>
        <div>
          <p class="brand-title">Sistem antrian tol</p>
          <p class="brand-sub">Multi-lane queue management</p>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
with col_reset:
    st.markdown("<div style='margin-top:1.1rem'>", unsafe_allow_html=True)
    if st.button("↺ Reset", use_container_width=True):
        st.session_state.tol = MultiQueueTol()
        st.session_state.total_masuk = 0
        st.session_state.total_keluar = 0
        add_log("sys", "Semua antrian direset")
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# ── Stat Cards ───────────────────────────────────────────────────────────────
antrian = tol.lihat_antrian()
sizes   = [len(antrian[i]) for i in [1,2,3]]
mx_idx  = sizes.index(max(sizes))
sibuk   = f"Tol {mx_idx+1}" if max(sizes) > 0 else "—"

st.markdown(f"""
<div class="stat-grid">
  <div class="scard">
    <div class="scard-icon" style="color:#0C447C">🚗</div>
    <div class="scard-val">{tol.total()}</div>
    <div class="scard-lbl">Total antrian</div>
  </div>
  <div class="scard">
    <div class="scard-icon" style="color:#27500A">⬇</div>
    <div class="scard-val">{st.session_state.total_masuk}</div>
    <div class="scard-lbl">Total masuk</div>
  </div>
  <div class="scard">
    <div class="scard-icon" style="color:#633806">⬆</div>
    <div class="scard-val">{st.session_state.total_keluar}</div>
    <div class="scard-lbl">Total keluar</div>
  </div>
  <div class="scard">
    <div class="scard-icon" style="color:#791F1F">🔥</div>
    <div class="scard-val">{sibuk}</div>
    <div class="scard-lbl">Tersibuk</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── Input Panel ──────────────────────────────────────────────────────────────
st.markdown('<div class="input-panel">', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns([3, 1.2, 2, 1.2])
with c1:
    nama = st.text_input("Nama / plat kendaraan", placeholder="cth: B 1234 XY",
                         label_visibility="visible", key="inp_nama")
with c2:
    st.markdown("<div style='margin-top:1.65rem'>", unsafe_allow_html=True)
    if st.button("＋ Masukkan", use_container_width=True, type="primary"):
        v = nama.strip().upper()
        if v:
            lane_no = tol.masuk_tol(v)
            st.session_state.total_masuk += 1
            add_log("in", f"{v} masuk ke Tol {lane_no}")
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
with c3:
    antrian = tol.lihat_antrian()
    opts = {f"Tol {i} ({len(antrian[i])} kendaraan)": i for i in [1,2,3]}
    pilihan = st.selectbox("Jalur keluar", list(opts.keys()), label_visibility="visible")
with c4:
    st.markdown("<div style='margin-top:1.65rem'>", unsafe_allow_html=True)
    if st.button("⬆ Proses", use_container_width=True):
        nomor = opts[pilihan]
        hasil = tol.keluar_tol(nomor)
        if hasil:
            st.session_state.total_keluar += 1
            add_log("out", f"{hasil} keluar dari Tol {nomor}")
        else:
            add_log("err", f"Tol {nomor} sedang kosong")
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# ── Lane Cards ───────────────────────────────────────────────────────────────
antrian = tol.lihat_antrian()
max_size = max(1, max(len(v) for v in antrian.values()))

lane_cols = st.columns(3, gap="small")
for idx, (lane_num, col) in enumerate(zip([1,2,3], lane_cols)):
    c = LANE_COLORS[idx]
    vehicles = antrian[lane_num]
    pct = int(len(vehicles) / max_size * 100) if vehicles else 0

    chips_html = ""
    if vehicles:
        for pos, v in enumerate(vehicles):
            front = (f'<span class="chip-front" style="background:{c["front_bg"]};color:{c["front_txt"]}">depan</span>'
                     if pos == 0 else "")
            chips_html += (f'<div class="chip">'
                           f'<span class="chip-num">{pos+1}</span>'
                           f'<span style="color:{c["dot"]};font-size:15px">🚗</span>'
                           f'<span class="chip-name">{v}</span>{front}</div>')
    else:
        chips_html = '<div class="empty-lane">🚧 Jalur kosong</div>'

    col.markdown(f"""
    <div class="lane">
      <div class="lane-hdr">
        <div class="lane-title">
          <span class="dot" style="background:{c['dot']}"></span>
          Tol {lane_num}
        </div>
        <span class="lane-badge" style="background:{c['bg']};color:{c['txt']}">
          {len(vehicles)} kendaraan
        </span>
      </div>
      <div class="lane-body">{chips_html}</div>
      <div class="bar-wrap">
        <div class="bar-bg">
          <div class="bar-fill" style="width:{pct}%;background:{c['bar']}"></div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ── Log Aktivitas ─────────────────────────────────────────────────────────────
pill_map = {"in": "pill-in", "out": "pill-out", "err": "pill-err", "sys": "pill-sys"}
lbl_map  = {"in": "masuk",   "out": "keluar",   "err": "error",    "sys": "sistem"}

if st.session_state.log:
    rows = "".join(
        f'<div class="log-row">'
        f'<span class="log-time">{l["time"]}</span>'
        f'<span class="log-pill {pill_map[l["type"]]}">{lbl_map[l["type"]]}</span>'
        f'<span class="log-msg">{l["msg"]}</span>'
        f'</div>'
        for l in st.session_state.log[:25]
    )
else:
    rows = '<div class="no-log">Belum ada aktivitas</div>'

st.markdown(f"""
<div class="log-wrap">
  <div class="log-hdr">📋 Log aktivitas</div>
  {rows}
</div>
""", unsafe_allow_html=True)