# pyrefly: ignore [missing-import]
import streamlit as st

def apply_custom_css():
    """Terapkan semua CSS kustom untuk mempercantik UI dan menambahkan animasi (Dark Mode)."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

        /* ── HTML Metric Cards (Gelap) ── */
        .metric-card {
            background: linear-gradient(135deg, #0f2035, #132840) !important;
            border: 1px solid #1e3a5c !important;
            border-radius: 12px !important;
            padding: 18px 20px !important;
        }
        .metric-card-blue   { border-top: 3px solid #4a9eff !important; }
        .metric-card-green  { border-top: 3px solid #3ecf8e !important; }
        .metric-card-orange { border-top: 3px solid #f4a44a !important; }
        .metric-card-purple { border-top: 3px solid #a78bfa !important; }

        .metric-label {
            font-size: 0.72rem !important;
            color: #6a9abf !important;
            letter-spacing: 0.06em !important;
            text-transform: uppercase !important;
            margin-bottom: 8px !important;
            font-weight: 600 !important;
        }
        .metric-value {
            font-size: 1.75rem !important;
            font-weight: 800 !important;
            color: #dff0ff !important;
            line-height: 1.1 !important;
        }
        .metric-value-text {
            font-size: 1.1rem !important;
            font-weight: 700 !important;
            color: #dff0ff !important;
            line-height: 1.3 !important;
            margin-top: 2px !important;
        }
        .metric-sub {
            font-size: 0.73rem !important;
            color: #4a7aa0 !important;
            margin-top: 5px !important;
        }

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
        @keyframes fadeSlideUp {
            from { opacity: 0; transform: translateY(22px); }
            to   { opacity: 1; transform: translateY(0);    }
        }
        @keyframes pulseGlow {
            0%, 100% { text-shadow: 0 0 0px rgba(74,158,255,0); }
            50%       { text-shadow: 0 0 14px rgba(74,158,255,0.55); }
        }
        @keyframes fadeInLeft {
            from { opacity: 0; transform: translateX(-18px); }
            to   { opacity: 1; transform: translateX(0);     }
        }

        h1 {
            animation: fadeInLeft 0.55s ease both;
        }

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

        .metric-value {
            animation: pulseGlow 3s ease-in-out infinite;
        }

        [data-testid="stTabs"] {
            animation: fadeSlideUp 0.5s ease 0.4s both;
        }
        [data-testid="stSidebar"] > div {
            animation: fadeSlideUp 0.6s ease 0.1s both;
        }

        [data-testid="stExpander"] {
            border-left: 3px solid #1e3a5c;
            transition: border-color 0.3s;
        }
        [data-testid="stExpander"]:hover {
            border-left-color: #4a9eff;
        }
    </style>
    """, unsafe_allow_html=True)
