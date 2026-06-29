# pyrefly: ignore [missing-import]
import streamlit as st

def apply_custom_css():
    """Terapkan semua CSS kustom untuk mempercantik UI dan menambahkan animasi."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

        /* ── Metric cards ── */
        [data-testid="stMetric"] {
            background: linear-gradient(135deg, #1a2535 0%, #1e2f45 100%);
            border: 1px solid #2a4060;
            border-radius: 14px;
            padding: 18px 22px;
            box-shadow: 0 4px 20px rgba(74,158,255,0.08);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        [data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 28px rgba(74,158,255,0.18);
        }
        [data-testid="stMetricLabel"] { font-size: 0.80rem; color: #7da8d4; letter-spacing: 0.04em; }
        [data-testid="stMetricValue"] { font-size: 1.65rem; color: #dff0ff; font-weight: 800; }
        [data-testid="stMetricDelta"] { font-size: 0.76rem; }

        /* ── Sidebar ── */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0b1623 0%, #0f1e2e 100%);
            border-right: 1px solid #1a3050;
        }
        [data-testid="stSidebar"] h2 { color: #7eb8f7; letter-spacing: 0.02em; }
        [data-testid="stSidebar"] h3 { color: #5a9fd4; font-size: 0.9rem; }

        /* ── Tab aktif ── */
        button[data-baseweb="tab"][aria-selected="true"] {
            border-bottom: 3px solid #4a9eff !important;
            color: #4a9eff !important;
            font-weight: 700 !important;
        }

        /* ── Divider tipis ── */
        .thin-divider {
            border: none;
            border-top: 1px solid #1a3050;
            margin: 18px 0;
        }

        /* ── Section label ── */
        .section-label {
            font-size: 0.72rem; font-weight: 700; letter-spacing: 0.10em;
            color: #4a9eff; text-transform: uppercase; margin-bottom: 10px;
        }

        /* ── Download button ── */
        [data-testid="stDownloadButton"] > button {
            background: linear-gradient(135deg, #1b3a5c, #1e4a72);
            color: #7eb8f7; border: 1px solid #2a5a8a;
            border-radius: 8px; font-weight: 600;
            transition: all 0.2s;
        }
        [data-testid="stDownloadButton"] > button:hover {
            background: linear-gradient(135deg, #1e4a72, #2460a0);
            box-shadow: 0 0 12px rgba(74,158,255,0.25);
            color: #c0deff;
        }

        /* ═══════════════════════════════════════════
           ANIMASI
        ═══════════════════════════════════════════ */

        /* 1. Fade + slide dari bawah */
        @keyframes fadeSlideUp {
            from { opacity: 0; transform: translateY(22px); }
            to   { opacity: 1; transform: translateY(0);    }
        }

        /* 2. Shimmer sweep border-top */
        @keyframes shimmerBorder {
            0%   { background-position: -200% center; }
            100% { background-position:  200% center; }
        }

        /* 3. Pulse glow angka besar */
        @keyframes pulseGlow {
            0%, 100% { text-shadow: 0 0 0px rgba(74,158,255,0); }
            50%       { text-shadow: 0 0 14px rgba(74,158,255,0.55); }
        }

        /* 4. Judul utama fade-in dari kiri */
        @keyframes fadeInLeft {
            from { opacity: 0; transform: translateX(-18px); }
            to   { opacity: 1; transform: translateX(0);     }
        }

        /* ── Terapkan ke judul halaman ── */
        h1 {
            animation: fadeInLeft 0.55s ease both;
        }

        /* ── Terapkan ke kartu metric HTML kustom ── */
        .metric-card {
            animation: fadeSlideUp 0.5s ease both;
            transition: transform 0.25s ease, box-shadow 0.25s ease;
        }
        .metric-card:hover {
            transform: translateY(-4px) scale(1.01);
            box-shadow: 0 10px 32px rgba(74,158,255,0.22) !important;
        }
        .metric-card:nth-child(1) { animation-delay: 0.05s; }
        .metric-card:nth-child(2) { animation-delay: 0.15s; }
        .metric-card:nth-child(3) { animation-delay: 0.25s; }
        .metric-card:nth-child(4) { animation-delay: 0.35s; }

        /* ── Nilai angka besar punya pulse glow ── */
        .metric-value {
            animation: pulseGlow 3s ease-in-out infinite;
        }

        /* ── Tab bar fade in ── */
        [data-testid="stTabs"] {
            animation: fadeSlideUp 0.5s ease 0.4s both;
        }

        /* ── Sidebar items fade in ── */
        [data-testid="stSidebar"] > div {
            animation: fadeSlideUp 0.6s ease 0.1s both;
        }

        /* ── Expander smooth expand (border accent) ── */
        [data-testid="stExpander"] {
            border-left: 3px solid #1e3a5c;
            transition: border-color 0.3s;
        }
        [data-testid="stExpander"]:hover {
            border-left-color: #4a9eff;
        }
    </style>
    """, unsafe_allow_html=True)
