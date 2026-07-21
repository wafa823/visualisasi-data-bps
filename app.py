# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
import os
from src.styles import apply_custom_css
from src.data_processing import load_and_clean, load_geo_data, fmt_number
from src.charts import (
    plot_line_chart,
    plot_horizontal_bar,
    plot_treemap,
    plot_bubble_scatter,
    plot_choropleth_map,
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
xlsx_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".xlsx")]

if not csv_files:
    st.error("❌ Tidak ada file CSV di folder **Data**.")
    st.stop()

# Muat data geografis (xlsx) jika tersedia
df_geo = None
if xlsx_files:
    xlsx_path = os.path.join(DATA_DIR, xlsx_files[0])
    try:
        df_geo = load_geo_data(xlsx_path)
    except Exception:
        df_geo = None

# ── Sidebar: Panel Filter & Kontrol ──────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎛️ Panel Kontrol")
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
    st.caption("📂 Data: BPS — Pengangguran Terbuka 1986–2024")

# ── Terapkan CSS Kustom ──────────────────────────────────────────────────────
apply_custom_css()

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
<div class="metrics-grid">

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


# ── Peta Geografis (setelah KPI, sebelum tabs) ───────────────────────────────
if df_geo is not None and not df_geo.empty:
    st.markdown("""
    <div class="chart-section-header" style="margin-top:24px;">
        <span class="chart-badge badge-teal">🗺️ Persebaran Geografis</span>
        <h2 class="chart-section-title">Peta Choropleth</h2>
    </div>
    <p class="chart-desc">
        Peta choropleth menampilkan <strong>distribusi TPT secara geografis</strong> per provinsi.
        Semakin terang warnanya, semakin tinggi Tingkat Pengangguran Terbuka (TPT).
        Hover pada provinsi untuk melihat nilai detail.
    </p>
    """, unsafe_allow_html=True)
    try:
        fig_map = plot_choropleth_map(df_geo)
        st.plotly_chart(fig_map, use_container_width=True)

        with st.expander("💡 Insight — Persebaran Geografis", expanded=False):
            prov_tertinggi = df_geo.loc[df_geo["TPT"].idxmax()]
            prov_terendah  = df_geo.loc[df_geo["TPT"].idxmin()]
            rata_tpt       = df_geo["TPT"].mean()
            st.markdown(f"""
**🔴 Provinsi TPT Tertinggi:** `{prov_tertinggi['Provinsi']}` — **{prov_tertinggi['TPT']:.2f}%**

**🟢 Provinsi TPT Terendah:** `{prov_terendah['Provinsi']}` — **{prov_terendah['TPT']:.2f}%**

**📊 Rata-rata TPT Nasional:** **{rata_tpt:.2f}%** (dari {len(df_geo)} provinsi)

> 💬 *Peta choropleth memungkinkan identifikasi kesenjangan regional — daerah yang butuh intervensi kebijakan ketenagakerjaan terlihat langsung.*
            """)
    except Exception as e:
        st.warning(f"⚠️ Peta tidak dapat dimuat: {e}")

st.markdown("<hr class='thin-divider'>", unsafe_allow_html=True)

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

    if df_filtered.empty:
        st.warning("⚠️ Tidak ada data untuk ditampilkan dengan filter saat ini.")
    else:
        # ════════════════════════════════════════════════════════════════
        # VISUALISASI 1 — LINE CHART (TREN TEMPORAL)
        # ════════════════════════════════════════════════════════════════
        st.markdown("""
        <div class="chart-section-header">
            <span class="chart-badge badge-blue">📈 Tren Waktu</span>
            <h2 class="chart-section-title">Line Chart</h2>
        </div>
        <p class="chart-desc">
            Line chart digunakan untuk menampilkan <strong>perubahan data sepanjang waktu (temporal)</strong>.
            Setiap garis mewakili satu kategori pendidikan dan memperlihatkan naik-turunnya
            jumlah pengangguran dari tahun ke tahun.
        </p>
        """, unsafe_allow_html=True)

        fig_line = plot_line_chart(df_filtered, rentang_tahun)
        st.plotly_chart(fig_line, use_container_width=True)

        with st.expander("💡 Insight — Tren Waktu", expanded=False):
            per_tahun   = df_filtered.groupby("Tahun")["Jumlah Pengangguran"].sum()
            tahun_puncak   = int(per_tahun.idxmax())
            nilai_puncak   = per_tahun.max()
            tahun_terendah = int(per_tahun.idxmin())
            nilai_terendah = per_tahun.min()
            st.markdown(f"""
**📅 Tahun puncak pengangguran:** `{tahun_puncak}` — total **{nilai_puncak:,.0f} orang**.

**📅 Tahun terendah pengangguran:** `{tahun_terendah}` — total **{nilai_terendah:,.0f} orang**.

> 💬 *Line chart menunjukkan pola tren dari waktu ke waktu, memudahkan identifikasi periode kritis.*
            """)

        st.markdown("<hr class='thin-divider'>", unsafe_allow_html=True)

        # ════════════════════════════════════════════════════════════════
        # VISUALISASI 2 — HORIZONTAL BAR CHART (PERBANDINGAN ANTARKATEGORI)
        # ════════════════════════════════════════════════════════════════
        st.markdown("""
        <div class="chart-section-header">
            <span class="chart-badge badge-green">📊 Perbandingan Kategori</span>
            <h2 class="chart-section-title">Horizontal Bar Chart</h2>
        </div>
        <p class="chart-desc">
            Horizontal bar chart digunakan untuk <strong>membandingkan nilai antar kategori</strong>
            secara langsung. Panjang batang merepresentasikan besaran total pengangguran
            per kategori pendidikan, sehingga mudah melihat mana yang paling dominan.
        </p>
        """, unsafe_allow_html=True)

        fig_bar = plot_horizontal_bar(df_filtered, rentang_tahun)
        st.plotly_chart(fig_bar, use_container_width=True)

        with st.expander("💡 Insight — Perbandingan Kategori", expanded=False):
            per_kategori  = df_filtered.groupby("Pendidikan")["Jumlah Pengangguran"].sum()
            kat_tertinggi = per_kategori.idxmax()
            val_tertinggi = per_kategori.max()
            kat_terendah  = per_kategori.idxmin()
            val_terendah  = per_kategori.min()
            pct_tertinggi = (val_tertinggi / per_kategori.sum() * 100) if per_kategori.sum() > 0 else 0
            st.markdown(f"""
**🔺 Kategori terbesar:** `{kat_tertinggi}` — **{val_tertinggi:,.0f} orang** ({pct_tertinggi:.1f}% dari total).

**🔻 Kategori terkecil:** `{kat_terendah}` — **{val_terendah:,.0f} orang**.

> 💬 *Horizontal bar memudahkan perbandingan langsung tanpa perlu melihat sumbu vertikal yang panjang.*
            """)

        st.markdown("<hr class='thin-divider'>", unsafe_allow_html=True)

        # ════════════════════════════════════════════════════════════════
        # VISUALISASI 3 — TREEMAP (KOMPOSISI / PROPORSI)
        # ════════════════════════════════════════════════════════════════
        st.markdown("""
        <div class="chart-section-header">
            <span class="chart-badge badge-orange">🗺️ Komposisi Proporsi</span>
            <h2 class="chart-section-title">Treemap</h2>
        </div>
        <p class="chart-desc">
            Treemap menampilkan <strong>proporsi atau komposisi bagian dari keseluruhan</strong>.
            Luas setiap kotak sebanding dengan jumlah pengangguran kategori tersebut terhadap total,
            sehingga terlihat jelas dominasi relatif setiap kategori pendidikan.
        </p>
        """, unsafe_allow_html=True)

        fig_tree = plot_treemap(df_filtered, rentang_tahun)
        st.plotly_chart(fig_tree, use_container_width=True)

        with st.expander("💡 Insight — Komposisi", expanded=False):
            per_kategori  = df_filtered.groupby("Pendidikan")["Jumlah Pengangguran"].sum()
            total_semua   = per_kategori.sum()
            top3 = per_kategori.sort_values(ascending=False).head(3)
            pct_top3 = top3.sum() / total_semua * 100 if total_semua > 0 else 0
            st.markdown(f"""
**🏆 3 Kategori Dominan:** {", ".join([f"`{k}`" for k in top3.index.tolist()])}
— mencakup **{pct_top3:.1f}%** dari total pengangguran.

> 💬 *Treemap ideal untuk memahami kontribusi relatif setiap bagian terhadap keseluruhan data.*
            """)

        st.markdown("<hr class='thin-divider'>", unsafe_allow_html=True)

        # ════════════════════════════════════════════════════════════════
        # VISUALISASI 4 — BUBBLE SCATTER (KORELASI DUA DIMENSI)
        # ════════════════════════════════════════════════════════════════
        st.markdown("""
        <div class="chart-section-header">
            <span class="chart-badge badge-purple">🔵 Distribusi & Kepadatan</span>
            <h2 class="chart-section-title">Bubble Scatter</h2>
        </div>
        <p class="chart-desc">
            Bubble scatter digunakan untuk melihat <strong>distribusi data pada dua dimensi sekaligus</strong>
            (waktu dan kategori), dengan ukuran gelembung yang merepresentasikan besaran nilai.
            Cocok untuk mengidentifikasi periode dan kategori mana yang paling menonjol secara bersamaan.
        </p>
        """, unsafe_allow_html=True)

        fig_bubble = plot_bubble_scatter(df_filtered, rentang_tahun)
        st.plotly_chart(fig_bubble, use_container_width=True)

        with st.expander("💡 Insight — Distribusi & Kepadatan", expanded=False):
            top_row = df_filtered.loc[df_filtered["Jumlah Pengangguran"].idxmax()]
            st.markdown(f"""
**📍 Titik paling menonjol:** Kategori `{top_row['Pendidikan']}` pada tahun `{int(top_row['Tahun'])}`
— **{top_row['Jumlah Pengangguran']:,.0f} orang**.

> 💬 *Bubble scatter memperlihatkan pola distribusi dua variabel sekaligus — sangat berguna untuk menemukan outlier atau konsentrasi data.*
            """)

