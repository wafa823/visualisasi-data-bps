# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
import os
from src.styles import apply_custom_css
from src.data_processing import load_and_clean, fmt_number
from src.charts import (
    plot_line_chart,
    plot_horizontal_bar,
    plot_treemap,
    plot_bubble_scatter,
)

# ── Konfigurasi Halaman ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard Pengangguran BPS",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)



# ── Muat Daftar Dataset ──────────────────────────────────────────────────────
DATA_DIR  = os.path.join(os.path.dirname(__file__), "Data")
csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]

if not csv_files:
    st.error("❌ Tidak ada file CSV di folder **Data**.")
    st.stop()

# ── Sidebar: Panel Filter & Kontrol ──────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎛️ Panel Kontrol")
    st.markdown("---")
    
    # Pilih Tema
    theme = st.selectbox("🎨 Pilih Tema:", ["Dark Mode", "Light Mode"])
    st.markdown("---")

    # Pilih file
    selected_file = st.selectbox("📁 Pilih File CSV:", csv_files)
    file_path = os.path.join(DATA_DIR, selected_file)

    try:
        df_raw, df_long = load_and_clean(file_path)
    except Exception as e:
        st.error(f"❌ Gagal memuat data: {e}")
        st.stop()

    st.markdown("---")
    st.markdown("### 🔍 Filter Data")

    # 1. Filter Kategori Pendidikan
    semua_kategori = sorted(df_long["Pendidikan"].unique().tolist())
    pilihan_pendidikan = st.multiselect(
        "🎓 Kategori Pendidikan:",
        options=semua_kategori,
        default=semua_kategori,
        help="Pilih satu atau beberapa kategori pendidikan.",
    )
    if not pilihan_pendidikan:
        pilihan_pendidikan = semua_kategori

    # 2. Slider Rentang Tahun
    tahun_min = int(df_long["Tahun"].min())
    tahun_max = int(df_long["Tahun"].max())
    rentang_tahun = st.slider(
        "📅 Rentang Tahun:",
        min_value=tahun_min,
        max_value=tahun_max,
        value=(tahun_min, tahun_max),
        step=1,
    )

    st.markdown("---")
    st.markdown("### 📊 Pilih Visualisasi")

    # 3. Varian grafik
    VARIAN_LIST = [
        "Line Chart (Tren)",
        "Horizontal Bar Chart (Perbandingan)",
        "Treemap (Komposisi)",
        "Bubble Scatter (Korelasi Kepadatan)",
    ]
    varian = st.selectbox("📊 Pilih Varian Grafik:", VARIAN_LIST)

    st.markdown("---")
    st.caption("📂 Data: BPS — Pengangguran Terbuka 1986–2024")

# ── Terapkan CSS Kustom ──────────────────────────────────────────────────────
apply_custom_css(theme)


# ── Filter Data Sesuai Input User ────────────────────────────────────────────
df_filtered = df_long[
    df_long["Pendidikan"].isin(pilihan_pendidikan)
    & (df_long["Tahun"] >= rentang_tahun[0])
    & (df_long["Tahun"] <= rentang_tahun[1])
].copy()


# ── Halaman Utama: Header ────────────────────────────────────────────────────
st.title("📊 Dashboard Pengangguran Terbuka Indonesia")
st.markdown("<hr class='thin-divider'>", unsafe_allow_html=True)


# ── Ringkasan Metrik (KPIs) ──────────────────────────────────────────────────
total_kasus      = df_filtered["Jumlah Pengangguran"].sum()
rata_per_tahun   = df_filtered.groupby("Tahun")["Jumlah Pengangguran"].sum().mean()
tertinggi_series = df_filtered.groupby("Pendidikan")["Jumlah Pengangguran"].sum()
tertinggi_nama   = tertinggi_series.idxmax() if not tertinggi_series.empty else "-"
tertinggi_val    = tertinggi_series.max()    if not tertinggi_series.empty else 0
terendah_nama    = tertinggi_series.idxmin() if not tertinggi_series.empty else "-"

st.markdown(f"""
<div style="display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin:18px 0 24px 0;">

  <div class="metric-card metric-card-blue">
    <div class="metric-label">📌 Total Pengangguran</div>
    <div class="metric-value">{fmt_number(total_kasus)}</div>
    <div class="metric-sub">Kumulatif semua periode &amp; kategori</div>
  </div>

  <div class="metric-card metric-card-green">
    <div class="metric-label">📅 Rata-rata per Tahun</div>
    <div class="metric-value">{fmt_number(rata_per_tahun)}</div>
    <div class="metric-sub">Rentang {rentang_tahun[0]} – {rentang_tahun[1]}</div>
  </div>

  <div class="metric-card metric-card-orange">
    <div class="metric-label">🔺 Kategori Tertinggi</div>
    <div class="metric-value-text">{tertinggi_nama}</div>
    <div class="metric-sub">Total: {fmt_number(tertinggi_val)}</div>
  </div>

  <div class="metric-card metric-card-purple">
    <div class="metric-label">🔻 Kategori Terendah</div>
    <div class="metric-value-text">{terendah_nama}</div>
    <div class="metric-sub">Kontribusi terkecil di periode ini</div>
  </div>

</div>
""", unsafe_allow_html=True)


# ── Tabs Tampilan ────────────────────────────────────────────────────────────
tab_mentah, tab_bersih = st.tabs(["📁 Data Mentah BPS", "✨ Data Setelah Cleaning"])

# ── Tab 1: Data Mentah BPS
with tab_mentah:
    st.subheader("📁 Data Mentah BPS")
    st.markdown(
        f"**Jumlah baris:** {df_raw.shape[0]} &nbsp;|&nbsp; **Jumlah kolom:** {df_raw.shape[1]}"
    )
    st.dataframe(df_raw, use_container_width=True)

# ── Tab 2: Data Setelah Cleaning
with tab_bersih:
    st.subheader("✨ Data Setelah Cleaning & Visualisasi")

    st.info(
        f"🔍 Menampilkan **{len(pilihan_pendidikan)} kategori** · "
        f"Tahun **{rentang_tahun[0]} – {rentang_tahun[1]}** · "
        f"**{df_filtered.shape[0]} baris** data",
        icon=None,
    )

    # Expander Data Table + Download CSV
    with st.expander("📋 Lihat Tabel Data Bersih", expanded=False):
        st.markdown(
            f"**Jumlah baris:** {df_filtered.shape[0]} &nbsp;|&nbsp; "
            f"**Jumlah kolom:** {df_filtered.shape[1]}"
        )
        st.dataframe(df_filtered, use_container_width=True)

        st.markdown("")
        csv_bytes = df_filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Unduh Data Bersih (.csv)",
            data=csv_bytes,
            file_name=f"data_bersih_{rentang_tahun[0]}_{rentang_tahun[1]}.csv",
            mime="text/csv",
            help="Download tabel yang sedang ditampilkan dalam format CSV",
        )

    st.markdown("<hr class='thin-divider'>", unsafe_allow_html=True)
    st.markdown(f"<p class='section-label'>Visualisasi Aktif</p>", unsafe_allow_html=True)
    st.subheader(f"📊 {varian}")

    # Expander Insight Otomatis
    with st.expander("💡 Lihat Analisis Ringkas & Insight Data", expanded=False):
        if df_filtered.empty:
            st.warning("Tidak ada data untuk ditampilkan dengan filter saat ini.")
        else:
            per_tahun = df_filtered.groupby("Tahun")["Jumlah Pengangguran"].sum()
            tahun_puncak    = int(per_tahun.idxmax())
            nilai_puncak    = per_tahun.max()
            tahun_terendah  = int(per_tahun.idxmin())
            nilai_terendah  = per_tahun.min()

            per_kategori    = df_filtered.groupby("Pendidikan")["Jumlah Pengangguran"].sum()
            kat_tertinggi   = per_kategori.idxmax()
            val_tertinggi   = per_kategori.max()
            kat_terendah    = per_kategori.idxmin()
            val_terendah    = per_kategori.min()

            pct_tertinggi   = (val_tertinggi / per_kategori.sum() * 100) if per_kategori.sum() > 0 else 0

            st.markdown(f"""
**📅 Tahun dengan Pengangguran Tertinggi:** `{tahun_puncak}`
— total **{nilai_puncak:,.0f} orang** pada periode yang dipilih.

**📅 Tahun dengan Pengangguran Terendah:** `{tahun_terendah}`
— total **{nilai_terendah:,.0f} orang**.

**🔺 Kategori Penyumbang Terbesar:** `{kat_tertinggi}`
— berkontribusi **{pct_tertinggi:.1f}%** dari total dengan **{val_tertinggi:,.0f} orang**.

**🔻 Kategori Penyumbang Terkecil:** `{kat_terendah}`
— total **{val_terendah:,.0f} orang** dalam periode ini.

> 💬 *Insight dihasilkan secara otomatis berdasarkan data yang sedang difilter.*
            """)

    st.markdown("")

    # Render Grafik Sesuai Varian Terpilih
    fig = None
    if varian == "Line Chart (Tren)":
        fig = plot_line_chart(df_filtered, rentang_tahun, theme)
    elif varian == "Horizontal Bar Chart (Perbandingan)":
        fig = plot_horizontal_bar(df_filtered, rentang_tahun, theme)
    elif varian == "Treemap (Komposisi)":
        fig = plot_treemap(df_filtered, rentang_tahun, theme)
    else:
        fig = plot_bubble_scatter(df_filtered, rentang_tahun, theme)

    if fig:
        st.plotly_chart(fig, use_container_width=True)
