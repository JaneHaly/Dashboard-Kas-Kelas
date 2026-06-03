# Dashboard Keuangan Kelas (Python OOP + Streamlit + Pandas + Plotly)
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime


# =========================================
# CLASS USER
# =========================================
class User:
    def __init__(self, id_user, nama, kelas, role):
        self.id_user = id_user
        self.nama = nama
        self.kelas = kelas
        self.role = role

    def login(self):
        return f"{self.nama} login sebagai {self.role}"


# =========================================
# CLASS PENGURUS (Admin)
# =========================================
class Pengurus(User):
    def __init__(self, id_user, nama, kelas, username, password):
        super().__init__(id_user, nama, kelas, "Pengurus")
        self.username = username
        self.password = password

    def tambah_transaksi(self, dashboard, transaksi):
        dashboard.tambah_transaksi(transaksi)

    def hapus_transaksi(self, dashboard, id_transaksi):
        dashboard.hapus_transaksi(id_transaksi)

    def edit_transaksi(self, dashboard, id_transaksi, field, nilai_baru):
        dashboard.edit_transaksi(id_transaksi, field, nilai_baru)

    def hapus_saran(self, kotak_saran, index):
        kotak_saran.hapus_saran(index)


# =========================================
# CLASS ANGGOTA
# =========================================
class Anggota(User):
    def __init__(self, id_user, nama, kelas, username, password):
        super().__init__(id_user, nama, kelas, "Anggota")
        self.username = username
        self.password = password

    def kirim_saran(self, kotak_saran, isi_saran):
        kotak_saran.kirim_saran(isi_saran, self.nama)


# =========================================
# CLASS TRANSAKSI
# =========================================
class Transaksi:
    def __init__(self, id_transaksi, tanggal, jenis, jumlah, keterangan):
        self.id_transaksi = id_transaksi
        self.tanggal = tanggal
        self.jenis = jenis
        self.jumlah = jumlah
        self.keterangan = keterangan

    def to_dict(self):
        return {
            "ID": self.id_transaksi,
            "Tanggal": self.tanggal,
            "Jenis": self.jenis,
            "Jumlah": self.jumlah,
            "Keterangan": self.keterangan
        }

# =========================================
# CLASS PEMASUKAN
# =========================================
class Pemasukan(Transaksi):
    def __init__(self, id_transaksi, tanggal, jumlah, keterangan, sumber_dana):
        super().__init__(id_transaksi, tanggal, "Pemasukan", jumlah, keterangan)
        self.sumber_dana = sumber_dana

    def to_dict(self):
        d = super().to_dict()
        d["Sumber Dana"] = self.sumber_dana
        return d


# =========================================
# CLASS PENGELUARAN
# =========================================
class Pengeluaran(Transaksi):
    def __init__(self, id_transaksi, tanggal, jumlah, keterangan, kategori):
        super().__init__(id_transaksi, tanggal, "Pengeluaran", jumlah, keterangan)
        self.kategori = kategori

    def to_dict(self):
        d = super().to_dict()
        d["Sumber Dana"] = self.kategori
        return d


# =========================================
# CLASS KOTAK SARAN
# =========================================
class KotakSaran:
    def __init__(self):
        self.daftar_saran = []

    def kirim_saran(self, isi_saran, pengirim="Anonim"):
        self.daftar_saran.append({
            "Tanggal": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Pengirim": pengirim,
            "Saran": isi_saran
        })

    def hapus_saran(self, index):
        if 0 <= index < len(self.daftar_saran):
            self.daftar_saran.pop(index)

    def get_dataframe(self):
        return pd.DataFrame(self.daftar_saran)


# =========================================
# CLASS DASHBOARD
# =========================================
class Dashboard:
    def __init__(self):
        self.transaksi_list = []

    def tambah_transaksi(self, transaksi):
        self.transaksi_list.append(transaksi)

    def hapus_transaksi(self, id_transaksi):
        self.transaksi_list = [
            trx for trx in self.transaksi_list
            if trx.id_transaksi != id_transaksi
        ]

    def edit_transaksi(self, id_transaksi, field, nilai_baru):
        for trx in self.transaksi_list:
            if trx.id_transaksi == id_transaksi:
                setattr(trx, field, nilai_baru)
                break

    def get_dataframe(self):
        data = [trx.to_dict() for trx in self.transaksi_list]
        return pd.DataFrame(data)

    def get_pemasukan_df(self):
        data = [trx.to_dict() for trx in self.transaksi_list if trx.jenis == "Pemasukan"]
        return pd.DataFrame(data)

    def get_pengeluaran_df(self):
        data = [trx.to_dict() for trx in self.transaksi_list if trx.jenis == "Pengeluaran"]
        return pd.DataFrame(data)

    def hitung_saldo(self):
        pemasukan = sum(
            trx.jumlah for trx in self.transaksi_list
            if trx.jenis == "Pemasukan"
        )
        pengeluaran = sum(
            trx.jumlah for trx in self.transaksi_list
            if trx.jenis == "Pengeluaran"
        )
        saldo = pemasukan - pengeluaran
        return pemasukan, pengeluaran, saldo


# =========================================
# USER DATABASE
# =========================================
USER_DB = {
    "Ahmad Jaka": Pengurus(1, "Ahmad Jaka", " ", " ", "pengurus123"),
    "Andika": Pengurus(2, "Andika", "TI-F", "pengurus1", "pengurus123"),
    "Nabil Lingga": Anggota(3, "Nabil Lingga", "TI-F", "anggota1", "anggota123"),
    "Rafiul": Anggota(4, "Rafiul Zuhri", "TI-F", "anggota2", "anggota123"),
}


# =========================================
# STREAMLIT CONFIG & STYLING
# =========================================
st.set_page_config(
    page_title="Kas Kelas — TI-F",
    page_icon=" ",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500&display=swap');

/* DEFAULT: LIGHT MODE VARIABLES */
:root {
    --bg: #f8f9fa;
    --surface: #ffffff;
    --surface2: #f1f3f5;
    --border: #dee2e6;
    --accent: #c9a84c;
    --accent2: #b59334;
    --green: #2b8a3e;
    --red: #e03131;
    --text: #212529;
    --muted: #6c757d;
    --radius: 14px;
}

/* AUTOMATIC DARK MODE OVERRIDE */
@media (prefers-color-scheme: dark) {
    :root {
        --bg: #0f0f13;
        --surface: #18181f;
        --surface2: #1e1e27;
        --border: #2a2a38;
        --accent: #c9a84c;
        --accent2: #e8c86d;
        --green: #3ecf72;
        --red: #ffffff;
        --text: #e8e6e0;
        --muted: #7a7888;
    }
}

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* Hide default Streamlit elements, KECUALI header agar tombol sidebar tidak hilang */
#MainMenu, footer {visibility: hidden;}
[data-testid="stHeader"] { background: transparent !important; }
.block-container {padding: 2rem 2rem 4rem;}

/* Page heading */
h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--accent2);
    letter-spacing: 0.01em;
    margin-bottom: 0.1rem;
}
h2, h3 {
    font-family: 'Playfair Display', serif;
    color: var(--text);
}
h2 { font-size: 1.3rem; font-weight: 600; }
h3 { font-size: 1.05rem; font-weight: 600; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: var(--muted) !important;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

/* Metric cards */
[data-testid="metric-container"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius);
    padding: 1.4rem 1.6rem !important;
    transition: border-color 0.2s;
}
[data-testid="metric-container"]:hover {
    border-color: var(--accent) !important;
}
[data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; }
[data-testid="stMetricValue"] { font-family: 'Playfair Display', serif; color: var(--text) !important; font-size: 1.6rem !important; }

/* Custom Adaptive Box for Cards */
.custom-card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.2rem;
}

/* Buttons */
.stButton > button {
    background: var(--accent) !important;
    color: #0f0f13 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    padding: 0.5rem 1.4rem !important;
    letter-spacing: 0.04em;
    transition: background 0.2s, transform 0.1s !important;
}
.stButton > button:hover {
    background: var(--accent2) !important;
    transform: translateY(-1px) !important;
}

button[kind="secondary"] {
    background: transparent !important;
    color: var(--red) !important;
    border: 1px solid var(--red) !important;
}

/* Input fields */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stDateInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Labels */
.stTextInput label, .stNumberInput label, .stDateInput label,
.stTextArea label, .stSelectbox label {
    color: var(--muted) !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    overflow: hidden;
}

/* Divider */
hr { border-color: var(--border) !important; }

/* Badges */
.role-badge-pengurus {
    display: inline-block;
    background: rgba(201,168,76,0.15);
    color: var(--accent2);
    border: 1px solid var(--accent);
    border-radius: 20px;
    padding: 2px 12px;
    font-size: 0.72rem;
    font-weight: 500;
    text-transform: uppercase;
}
.role-badge-anggota {
    display: inline-block;
    background: rgba(62,207,114,0.1);
    color: var(--green);
    border: 1px solid rgba(62,207,114,0.4);
    border-radius: 20px;
    padding: 2px 12px;
    font-size: 0.72rem;
    font-weight: 500;
    text-transform: uppercase;
}
.section-header {
    border-left: 3px solid var(--accent);
    padding-left: 0.8rem;
    margin: 1.5rem 0 1rem;
}
</style>
""", unsafe_allow_html=True)


# =========================================
# SESSION STATE INIT
# =========================================
if "dashboard" not in st.session_state:
    st.session_state.dashboard = Dashboard()

if "kotak_saran" not in st.session_state:
    st.session_state.kotak_saran = KotakSaran()

if "user" not in st.session_state:
    st.session_state.user = None

if "login_error" not in st.session_state:
    st.session_state.login_error = ""


# =========================================
# LOGIN FUNCTION
# =========================================
def do_login(username, password):
    user = USER_DB.get(username)
    if user and user.password == password:
        st.session_state.user = user
        st.session_state.login_error = ""
    else:
        st.session_state.login_error = "Username atau password salah."

def do_logout():
    st.session_state.user = None


# =========================================
# LOGIN PAGE
# =========================================
if st.session_state.user is None:
    col_l, col_c, col_r = st.columns([1, 1.4, 1])
    with col_c:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='text-align:center; margin-bottom: 2rem;'>
            <div style='font-size:2.8rem; margin-bottom:0.3rem;'>💎</div>
            <h1>Kas Kelas</h1>
            <p style='color:var(--muted); font-size:0.85rem; letter-spacing:0.5em; text-transform:uppercase;'>TI-F — Sistem Keuangan</p>
        </div>
        """, unsafe_allow_html=True)

        with st.container():
            username_input = st.text_input("Username", placeholder="Masukkan username")
            password_input = st.text_input("Password", type="password", placeholder="Masukkan password")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Masuk", use_container_width=True):
                do_login(username_input, password_input)
                st.rerun()

            if st.session_state.login_error:
                st.error(st.session_state.login_error)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="custom-card">
            <p style='color:var(--muted); font-size:0.72rem; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.6rem;'>Demo Akun</p>
            <p style='font-size:0.8rem; margin:0.2rem 0;'>🔑 <b>Ahmad Jaka</b> / pengurus123 &nbsp;<span style='color:var(--accent); font-size:0.7rem;'>Pengurus 1</span></p>
            <p style='font-size:0.8rem; margin:0.2rem 0;'>🔑 <b>Andika</b> / pengurus123 &nbsp;<span style='color:var(--accent); font-size:0.7rem;'>Pengurus 2</span></p>
            <p style='font-size:0.8rem; margin:0.2rem 0;'>👤 <b>Nabil Lingga</b> / anggota123 &nbsp;<span style='color:var(--green); font-size:0.7rem;'>Anggota</span></p>
            <p style='font-size:0.8rem; margin:0.2rem 0;'>👤 <b>Rafiul</b> / anggota123 &nbsp;<span style='color:var(--green); font-size:0.7rem;'>Anggota</span></p>
        </div>
        """, unsafe_allow_html=True)

    st.stop()


# =========================================
# SIDEBAR (after login)
# =========================================
user = st.session_state.user
dashboard = st.session_state.dashboard
kotak_saran = st.session_state.kotak_saran

with st.sidebar:
    st.markdown(f"""
    <div style='padding: 1rem 0 1.5rem;'>
        <div style='font-family: Playfair Display, serif; font-size:1.3rem; color:var(--accent2); font-weight:700; margin-bottom:0.2rem;'>💰 Kas Kelas</div>
        <div style='color:var(--muted); font-size:0.72rem; text-transform:uppercase; letter-spacing:0.1em;'>TI-F</div>
    </div>
    <hr style='margin-bottom:1.2rem;'>
    <div style='margin-bottom:1.5rem;'>
        <div style='font-size:0.9rem; font-weight:500; margin-bottom:0.3rem;'>{user.nama}</div>
        <span class='role-badge-{"pengurus" if user.role == "Pengurus" else "anggota"}'>{user.role}</span>
    </div>
    """, unsafe_allow_html=True)

    if user.role == "Pengurus":
        menu_options = ["Dashboard Utama", "Pemasukan", "Pengeluaran", "Kotak Saran"]
    else:
        menu_options = ["Dashboard Utama", "Kotak Saran"]

    menu = st.selectbox("Navigasi", menu_options, label_visibility="collapsed")

    st.markdown("<br>" * 8, unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    if st.button("Keluar", use_container_width=True):
        do_logout()
        st.rerun()


# =========================================
# PLOTLY THEME HELPER (Adaptive)
# =========================================
# Menghapus 'color' hardcoded agar Plotly otomatis mengikuti tema Streamlit (Light/Dark)
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans"),
    margin=dict(t=40, b=20, l=10, r=10),
)
COLOR_SEQ = ["#fa0000", "#26ff04", "#3ecf72", "#5a9cf0", "#c05af0"]


# =========================================
# DASHBOARD UTAMA
# =========================================
if menu == "Dashboard Utama":
    st.markdown("<h1>Dashboard Keuangan</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:var(--muted); margin-top:-0.4rem; margin-bottom:1.5rem; font-size:0.85rem;'>{datetime.now().strftime('%A, %d %B %Y')}</p>", unsafe_allow_html=True)

    pemasukan, pengeluaran, saldo = dashboard.hitung_saldo()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Pemasukan", f"Rp {pemasukan:,.0f}")
    col2.metric("Total Pengeluaran", f"Rp {pengeluaran:,.0f}")
    col3.metric("Saldo", f"Rp {saldo:,.0f}", delta=f"{'Surplus' if saldo >= 0 else 'Defisit'}")

    st.markdown("<br>", unsafe_allow_html=True)
    df = dashboard.get_dataframe()

    if not df.empty:
        col_g1, col_g2 = st.columns(2)

        with col_g1:
            st.markdown("<div class='section-header'><h3>Distribusi Keuangan</h3></div>", unsafe_allow_html=True)
            fig_pie = go.Figure(data=[go.Pie(
                labels=["Pemasukan", "Pengeluaran"],
                values=[pemasukan, pengeluaran],
                hole=0.55,
                marker=dict(colors=["#00ff00", "#ff0000"]),
            )])
            fig_pie.update_layout(**PLOTLY_LAYOUT,
                annotations=[dict(text=f"Rp {saldo:,.0f}", x=0.5, y=0.5,
                                  font=dict(size=13, family="Playfair Display", color="#ffffff"),
                                  showarrow=False)])
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_g2:
            st.markdown("<div class='section-header'><h3>Riwayat Transaksi</h3></div>", unsafe_allow_html=True)
            df_chart = df.copy()
            df_chart["Tanggal"] = pd.to_datetime(df_chart["Tanggal"])
            df_chart = df_chart.sort_values("Tanggal")
            fig_bar = px.bar(df_chart, x="Tanggal", y="Jumlah", color="Jenis",
                             color_discrete_map={"Pemasukan": "#00ff00", "Pengeluaran": "#ff0000"})
            fig_bar.update_layout(**PLOTLY_LAYOUT)
            st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("<div class='section-header'><h3>Semua Transaksi</h3></div>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Belum ada transaksi. Pengurus dapat menambahkan transaksi melalui menu Pemasukan / Pengeluaran.")


# =========================================
# PEMASUKAN PAGE (Pengurus only)
# =========================================
elif menu == "Pemasukan":
    st.markdown("<h1>Pemasukan</h1>", unsafe_allow_html=True)

    df_p = dashboard.get_pemasukan_df()

    total_masuk = sum(trx.jumlah for trx in dashboard.transaksi_list if trx.jenis == "Pemasukan")
    col_a, col_b = st.columns([1, 3])
    col_a.metric("Total Pemasukan", f"Rp {total_masuk:,.0f}")

    st.markdown("<div class='section-header'><h3>Data Pemasukan</h3></div>", unsafe_allow_html=True)
    if not df_p.empty:
        st.dataframe(df_p, use_container_width=True, hide_index=True)
    else:
        st.info("Belum ada data pemasukan.")

    st.markdown("---")

    st.markdown("<div class='section-header'><h3>Tambah Pemasukan</h3></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        id_trx = st.number_input("ID Transaksi", min_value=1, step=1, key="p_id")
        tanggal = st.date_input("Tanggal", key="p_tgl")
        jumlah = st.number_input("Jumlah (Rp)", min_value=0, step=1000, key="p_jml")
    with c2:
        keterangan = st.text_input("Keterangan", key="p_ket")
        sumber = st.text_input("Sumber Dana", key="p_sumber")

    if st.button("＋ Simpan Pemasukan"):
        trx = Pemasukan(id_trx, str(tanggal), jumlah, keterangan, sumber)
        user.tambah_transaksi(dashboard, trx)
        st.success(f"Pemasukan Rp {jumlah:,} berhasil ditambahkan.")
        st.rerun()

    if not df_p.empty:
        st.markdown("---")
        st.markdown("<div class='section-header'><h3>Hapus Pemasukan</h3></div>", unsafe_allow_html=True)
        id_hapus = st.number_input("ID Transaksi yang dihapus", min_value=1, step=1, key="p_hapus")
        if st.button("🗑 Hapus", key="btn_hapus_p"):
            user.hapus_transaksi(dashboard, id_hapus)
            st.success("Transaksi berhasil dihapus.")
            st.rerun()


# =========================================
# PENGELUARAN PAGE (Pengurus only)
# =========================================
elif menu == "Pengeluaran":
    st.markdown("<h1>Pengeluaran</h1>", unsafe_allow_html=True)

    df_k = dashboard.get_pengeluaran_df()

    total_keluar = sum(trx.jumlah for trx in dashboard.transaksi_list if trx.jenis == "Pengeluaran")
    col_a, col_b = st.columns([1, 3])
    col_a.metric("Total Pengeluaran", f"Rp {total_keluar:,.0f}")

    st.markdown("<div class='section-header'><h3>Data Pengeluaran</h3></div>", unsafe_allow_html=True)
    if not df_k.empty:
        st.dataframe(df_k, use_container_width=True, hide_index=True)

        # df_k["Sumber Dana"] = df_k["Sumber Dana"].fillna("Lainnya")
        # fig_kat = px.pie(df_k, names="Sumber Dana", values="Jumlah",
        #                 color_discrete_sequence=COLOR_SEQ,
        #                 title="Pengeluaran per Kategori")
        # fig_kat.update_layout(**PLOTLY_LAYOUT)
        # st.plotly_chart(fig_kat, use_container_width=True)

    else:
        st.info("Belum ada data pengeluaran.")

    st.markdown("---")

    st.markdown("<div class='section-header'><h3>Tambah Pengeluaran</h3></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        id_trx2 = st.number_input("ID Transaksi", min_value=1, step=1, key="k_id")
        tanggal2 = st.date_input("Tanggal", key="k_tgl")
    with c2:
        keterangan2 = st.text_input("Keterangan", key="k_ket")
        kategori = "Kas Kelas"
        jumlah2 = st.number_input("Jumlah (Rp)", min_value=0, step=1000, key="k_jml")

    if st.button("＋ Simpan Pengeluaran"):
        trx = Pengeluaran(id_trx2, str(tanggal2), jumlah2, keterangan2, kategori)
        user.tambah_transaksi(dashboard, trx)
        st.success(f"Pengeluaran Rp {jumlah2:,} berhasil ditambahkan.")
        st.rerun()

    if not df_k.empty:
        st.markdown("---")
        st.markdown("<div class='section-header'><h3>Hapus Pengeluaran</h3></div>", unsafe_allow_html=True)
        id_hapus2 = st.number_input("ID Transaksi yang dihapus", min_value=1, step=1, key="k_hapus")
        if st.button("🗑 Hapus", key="btn_hapus_k"):
            user.hapus_transaksi(dashboard, id_hapus2)
            st.success("Transaksi berhasil dihapus.")
            st.rerun()


# =========================================
# KOTAK SARAN PAGE
# =========================================
elif menu == "Kotak Saran":
    st.markdown("<h1>Kotak Saran</h1>", unsafe_allow_html=True)

    if user.role == "Anggota":
        st.markdown("<div class='section-header'><h3>Kirim Saran</h3></div>", unsafe_allow_html=True)
        isi_saran = st.text_area("Apa yang ingin kamu sampaikan?", height=130, placeholder="Tulis saranmu di sini...")
        if st.button("📨 Kirim Saran"):
            if isi_saran.strip():
                user.kirim_saran(kotak_saran, isi_saran)
                st.success("Saran berhasil dikirim. Terima kasih!")
                st.rerun()
            else:
                st.warning("Saran tidak boleh kosong.")

    df_saran = kotak_saran.get_dataframe()

    st.markdown("<div class='section-header'><h3>Daftar Saran Masuk</h3></div>", unsafe_allow_html=True)
    if not df_saran.empty:
        if user.role == "Pengurus":
            for i, row in df_saran.iterrows():
                with st.container():
                    col_text, col_btn = st.columns([5, 1])
                    with col_text:
                        st.markdown(f"""
                        <div class="custom-card" style="margin-bottom: 0.6rem;">
                            <div style='display:flex; justify-content:space-between; margin-bottom:0.4rem;'>
                                <span style='font-size:0.8rem; color:var(--accent); font-weight:500;'>{row.get("Pengirim","Anonim")}</span>
                                <span style='font-size:0.75rem; color:var(--muted);'>{row["Tanggal"]}</span>
                            </div>
                            <div style='font-size:0.88rem;'>{row["Saran"]}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_btn:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("🗑", key=f"del_saran_{i}"):
                            user.hapus_saran(kotak_saran, i)
                            st.rerun()
        else:
            saran_saya = df_saran[df_saran["Pengirim"] == user.nama]
            if not saran_saya.empty:
                st.markdown(f"<p style='color:var(--muted); font-size:0.8rem;'>Kamu telah mengirim {len(saran_saya)} saran.</p>", unsafe_allow_html=True)
                for _, row in saran_saya.iterrows():
                    st.markdown(f"""
                    <div class="custom-card" style="margin-bottom: 0.6rem;">
                        <div style='font-size:0.75rem; color:var(--muted); margin-bottom:0.3rem;'>{row["Tanggal"]}</div>
                        <div style='font-size:0.88rem;'>{row["Saran"]}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Kamu belum mengirim saran.")
    else:
        st.info("Belum ada saran masuk.")