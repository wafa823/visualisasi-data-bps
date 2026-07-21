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


@st.cache_data
def load_geo_data(file_path: str) -> pd.DataFrame:
    """Baca file Excel TPT per Provinsi dan kembalikan DataFrame bersih."""
    df = pd.read_excel(file_path, header=None)

    # Cari baris data: kolom 0 berisi nama provinsi (bukan NaN, bukan 'INDONESIA')
    data_rows = []
    for _, row in df.iterrows():
        provinsi = str(row.iloc[0]).strip()
        nilai    = row.iloc[1]
        if (
            provinsi not in ["nan", "INDONESIA", ""]
            and str(nilai).replace(".", "").isdigit()
        ):
            try:
                tpt = float(nilai)
                data_rows.append({"Provinsi": provinsi.title(), "TPT": tpt})
            except (ValueError, TypeError):
                continue

    df_clean = pd.DataFrame(data_rows)

    # Normalisasi nama agar cocok persis dengan GeoJSON (key: 'state')
    rename_map = {
        "Aceh": "Aceh",
        "Sumatera Utara": "Sumatera Utara",
        "Sumatera Barat": "Sumatera Barat",
        "Riau": "Riau",
        "Jambi": "Jambi",
        "Sumatera Selatan": "Sumatera Selatan",
        "Bengkulu": "Bengkulu",
        "Lampung": "Lampung",
        "Kep. Bangka Belitung": "Bangka-Belitung",   # GeoJSON: "Bangka-Belitung"
        "Kep. Riau": "Kepulauan Riau",
        "Dki Jakarta": "Jakarta Raya",               # GeoJSON: "Jakarta Raya"
        "Jawa Barat": "Jawa Barat",
        "Jawa Tengah": "Jawa Tengah",
        "Di Yogyakarta": "Yogyakarta",               # GeoJSON: "Yogyakarta"
        "Jawa Timur": "Jawa Timur",
        "Banten": "Banten",
        "Bali": "Bali",
        "Nusa Tenggara Barat": "Nusa Tenggara Barat",
        "Nusa Tenggara Timur": "Nusa Tenggara Timur",
        "Kalimantan Barat": "Kalimantan Barat",
        "Kalimantan Tengah": "Kalimantan Tengah",
        "Kalimantan Selatan": "Kalimantan Selatan",
        "Kalimantan Timur": "Kalimantan Timur",
        "Kalimantan Utara": "Kalimantan Utara",
        "Sulawesi Utara": "Sulawesi Utara",
        "Sulawesi Tengah": "Sulawesi Tengah",
        "Sulawesi Selatan": "Sulawesi Selatan",
        "Sulawesi Tenggara": "Sulawesi Tenggara",
        "Gorontalo": "Gorontalo",
        "Sulawesi Barat": "Sulawesi Barat",
        "Maluku": "Maluku",
        "Maluku Utara": "Maluku Utara",
        "Papua Barat": "Papua Barat",
        "Papua": "Papua",
        # Provinsi baru (pemekaran 2022) - belum ada di GeoJSON
        "Papua Barat Daya": "Papua Barat Daya",
        "Papua Selatan": "Papua Selatan",
        "Papua Tengah": "Papua Tengah",
        "Papua Pegunungan": "Papua Pegunungan",
    }
    df_clean["Provinsi"] = df_clean["Provinsi"].map(rename_map).fillna(df_clean["Provinsi"])
    return df_clean


def fmt_number(n: float) -> str:
    """Format angka besar menjadi ribuan/jutaan."""
    if n >= 1_000_000:
        return f"{n/1_000_000:.2f} Jt"
    if n >= 1_000:
        return f"{n/1_000:.1f} Rb"
    return str(int(n))
