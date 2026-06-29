# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd

@st.cache_data
def load_and_clean(file_path: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Baca CSV BPS dan kembalikan (df_raw, df_long)."""
    df_raw = pd.read_csv(file_path, skiprows=2)

    pendidikan_col = df_raw.columns[1]
    df_clean = df_raw.dropna(subset=[pendidikan_col]).copy()
    df_clean = df_clean[df_clean[pendidikan_col].astype(str).str.strip() != "Total"]

    year_cols = [c for c in df_clean.columns if str(c).strip().isdigit()]
    df_clean = df_clean[[pendidikan_col] + year_cols].rename(
        columns={pendidikan_col: "Pendidikan"}
    )

    df_long = df_clean.melt(
        id_vars=["Pendidikan"], var_name="Tahun", value_name="Jumlah Pengangguran"
    )
    df_long["Tahun"] = pd.to_numeric(df_long["Tahun"], errors="coerce").astype("Int64")
    df_long["Jumlah Pengangguran"] = pd.to_numeric(
        df_long["Jumlah Pengangguran"], errors="coerce"
    )
    df_long = (
        df_long.dropna(subset=["Jumlah Pengangguran"])
        .sort_values(["Pendidikan", "Tahun"])
        .reset_index(drop=True)
    )
    return df_raw, df_long


def fmt_number(n: float) -> str:
    """Format angka besar menjadi ribuan/jutaan."""
    if n >= 1_000_000:
        return f"{n/1_000_000:.2f} Jt"
    if n >= 1_000:
        return f"{n/1_000:.1f} Rb"
    return str(int(n))
