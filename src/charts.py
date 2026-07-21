# pyrefly: ignore [missing-import]
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import urllib.request

CHART_TEMPLATE = "plotly_dark"
LABEL_COMMON = {
    "Tahun": "Tahun",
    "Jumlah Pengangguran": "Jumlah Pengangguran (Orang)",
    "Pendidikan": "Tingkat Pendidikan",
}
LAYOUT_BASE = dict(
    template=CHART_TEMPLATE,
    height=520,
    margin=dict(t=60, b=20, l=20, r=20),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#d0e0ff"),
    hoverlabel=dict(bgcolor="#1e2a3a", font_color="#e0eaff", bordercolor="#4a9eff"),
)

def plot_line_chart(df_filtered: pd.DataFrame, rentang_tahun: tuple[int, int]):
    """Membuat Line Chart tren pengangguran (Dark Mode)."""
    fig = px.line(
        df_filtered,
        x="Tahun", y="Jumlah Pengangguran", color="Pendidikan",
        markers=True,
        title=f"Tren Pengangguran per Tingkat Pendidikan ({rentang_tahun[0]}–{rentang_tahun[1]})",
        labels=LABEL_COMMON,
    )
    fig.update_traces(
        line=dict(width=2.5),
        marker=dict(size=6),
        hovertemplate="<b>%{fullData.name}</b><br>Tahun: %{x}<br>Jumlah: %{y:,.0f} orang<extra></extra>",
    )
    fig.update_layout(
        **LAYOUT_BASE,
        hovermode="x unified",
        xaxis=dict(tickmode="linear", dtick=2, gridcolor="#1e3050"),
        yaxis=dict(gridcolor="#1e3050"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="center", x=0.5),
    )
    return fig

def plot_horizontal_bar(df_filtered: pd.DataFrame, rentang_tahun: tuple[int, int]):
    """Membuat Horizontal Bar Chart untuk perbandingan kategori (Dark Mode)."""
    df_bar = (
        df_filtered.groupby("Pendidikan", as_index=False)["Jumlah Pengangguran"]
        .sum()
        .sort_values("Jumlah Pengangguran")
    )
    fig = px.bar(
        df_bar,
        x="Jumlah Pengangguran", y="Pendidikan",
        color="Pendidikan",
        orientation="h",
        text="Jumlah Pengangguran",
        title=f"Perbandingan Total Pengangguran per Kategori ({rentang_tahun[0]}–{rentang_tahun[1]})",
        labels=LABEL_COMMON,
    )
    fig.update_traces(
        texttemplate="%{x:,.0f}",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Total: %{x:,.0f} orang<extra></extra>",
    )
    fig.update_layout(
        **LAYOUT_BASE,
        showlegend=False,
        xaxis=dict(gridcolor="#1e3050"),
        yaxis=dict(gridcolor="rgba(0,0,0,0)"),
    )
    return fig

def plot_treemap(df_filtered: pd.DataFrame, rentang_tahun: tuple[int, int]):
    """Membuat Treemap untuk komposisi kontribusi pengangguran (Dark Mode)."""
    df_tree = (
        df_filtered.groupby("Pendidikan", as_index=False)["Jumlah Pengangguran"].sum()
    )
    fig = px.treemap(
        df_tree,
        path=["Pendidikan"],
        values="Jumlah Pengangguran",
        color="Pendidikan",
        title=f"Komposisi Pengangguran per Kategori ({rentang_tahun[0]}–{rentang_tahun[1]})",
    )
    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Total: %{value:,.0f} orang<br>Porsi: %{percentRoot:.1%}<extra></extra>",
        textinfo="label+percent root",
        textfont=dict(size=14),
    )
    fig.update_layout(
        template=CHART_TEMPLATE,
        height=520,
        margin=dict(t=60, b=20, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#d0e0ff"),
        hoverlabel=dict(bgcolor="#1e2a3a", font_color="#e0eaff", bordercolor="#4a9eff"),
    )
    return fig

def plot_bubble_scatter(df_filtered: pd.DataFrame, rentang_tahun: tuple[int, int]):
    """Membuat Bubble Scatter plot kepadatan pengangguran (Dark Mode)."""
    fig = px.scatter(
        df_filtered,
        x="Tahun", y="Pendidikan",
        size="Jumlah Pengangguran",
        color="Pendidikan",
        title=f"Kepadatan Pengangguran per Kategori & Tahun ({rentang_tahun[0]}–{rentang_tahun[1]})",
        labels=LABEL_COMMON,
        size_max=45,
    )
    fig.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>Tahun: %{x}<br>Jumlah: %{marker.size:,.0f} orang<extra></extra>",
    )
    fig.update_layout(
        **LAYOUT_BASE,
        hovermode="closest",
        xaxis=dict(tickmode="linear", dtick=2, gridcolor="#1e3050"),
        yaxis=dict(gridcolor="rgba(0,0,0,0)"),
        showlegend=False,
    )
    return fig


# ── GeoJSON Indonesia (cache di module level) ─────────────────────────────────
_GEOJSON_URL = (
    "https://raw.githubusercontent.com/superpikar/indonesia-geojson/"
    "master/indonesia.geojson"
)
_geojson_cache: dict | None = None

def _get_indonesia_geojson() -> dict:
    global _geojson_cache
    if _geojson_cache is None:
        with urllib.request.urlopen(_GEOJSON_URL, timeout=15) as resp:
            _geojson_cache = json.loads(resp.read().decode())
    return _geojson_cache


_PROVINCE_LABOR_FORCE = {
    "Aceh": 2600000,
    "Sumatera Utara": 7900000,
    "Sumatera Barat": 2900000,
    "Riau": 3300000,
    "Jambi": 1900000,
    "Sumatera Selatan": 4500000,
    "Bengkulu": 1100000,
    "Lampung": 4600000,
    "Bangka-Belitung": 800000,
    "Kepulauan Riau": 1100000,
    "Jakarta Raya": 5400000,
    "Jawa Barat": 25400000,
    "Jawa Tengah": 19800000,
    "Yogyakarta": 2300000,
    "Jawa Timur": 23400000,
    "Banten": 6400000,
    "Bali": 2600000,
    "Nusa Tenggara Barat": 2800000,
    "Nusa Tenggara Timur": 2900000,
    "Kalimantan Barat": 2700000,
    "Kalimantan Tengah": 1400000,
    "Kalimantan Selatan": 2300000,
    "Kalimantan Timur": 1900000,
    "Kalimantan Utara": 400000,
    "Sulawesi Utara": 1300000,
    "Sulawesi Tengah": 1600000,
    "Sulawesi Selatan": 4400000,
    "Sulawesi Tenggara": 1400000,
    "Gorontalo": 600000,
    "Sulawesi Barat": 700000,
    "Maluku": 900000,
    "Maluku Utara": 650000,
    "Papua Barat": 550000,
    "Papua": 1100000,
    "Papua Barat Daya": 300000,
    "Papua Selatan": 250000,
    "Papua Tengah": 600000,
    "Papua Pegunungan": 650000,
}


def plot_choropleth_map(df_geo: pd.DataFrame) -> go.Figure:
    """Membuat Choropleth Map TPT per Provinsi Indonesia (Dark Mode)."""
    geojson = _get_indonesia_geojson()
    df_clean = df_geo.copy()

    # Ambil field name dari GeoJSON untuk mencocokkan provinsi
    # GeoJSON superpikar menggunakan key 'state'
    sample_props = geojson["features"][0]["properties"]
    for candidate in ["state", "Propinsi", "name", "NAME_1"]:
        if candidate in sample_props:
            geo_key = candidate
            break
    else:
        geo_key = list(sample_props.keys())[0]

    rename_map = {
        "Aceh": "Aceh",
        "Sumatera Utara": "Sumatera Utara",
        "Sumatera Barat": "Sumatera Barat",
        "Riau": "Riau",
        "Jambi": "Jambi",
        "Sumatera Selatan": "Sumatera Selatan",
        "Bengkulu": "Bengkulu",
        "Lampung": "Lampung",
        "Kep. Bangka Belitung": "Bangka-Belitung",
        "Kep. Riau": "Kepulauan Riau",
        "Dki Jakarta": "Jakarta Raya",
        "Jawa Barat": "Jawa Barat",
        "Jawa Tengah": "Jawa Tengah",
        "Di Yogyakarta": "Yogyakarta",
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
        "Papua Barat Daya": "Papua Barat Daya",
        "Papua Selatan": "Papua Selatan",
        "Papua Tengah": "Papua Tengah",
        "Papua Pegunungan": "Papua Pegunungan",
    }
    df_clean["Provinsi"] = df_clean["Provinsi"].map(rename_map).fillna(df_clean["Provinsi"])

    # Hitung estimasi jumlah pengangguran absolut
    df_clean["LaborForce"] = df_clean["Provinsi"].map(_PROVINCE_LABOR_FORCE).fillna(1000000)
    df_clean["Jumlah_Pengangguran"] = (df_clean["TPT"] / 100 * df_clean["LaborForce"]).round(0)
    df_clean["Jumlah_Fmt"] = df_clean["Jumlah_Pengangguran"].apply(lambda x: f"{x:,.0f}".replace(",", "."))

    fig = px.choropleth(
        df_clean,
        geojson=geojson,
        locations="Provinsi",
        featureidkey=f"properties.{geo_key}",
        color="TPT",
        color_continuous_scale=[
            [0.0,  "#0a1628"],
            [0.2,  "#0d2d5e"],
            [0.4,  "#1a5fa8"],
            [0.6,  "#2e8fd4"],
            [0.8,  "#56c0f0"],
            [1.0,  "#b4f0ff"],
        ],
        range_color=(df_clean["TPT"].min(), df_clean["TPT"].max()),
        labels={"TPT": "TPT (%)"},
        title="Sebaran Tingkat Pengangguran Terbuka (TPT) per Provinsi — Februari 2026",
        hover_name="Provinsi",
        custom_data=["Jumlah_Fmt"]
    )

    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>TPT: %{z:.2f}%<br>Estimasi Pengangguran: %{customdata[0]} orang<extra></extra>",
        marker_line_color="#0d2030",
        marker_line_width=0.6,
        selector=dict(type="choropleth")
    )

    # Hitung centroids untuk menampilkan label teks provinsi di peta
    centroids = {}
    for feature in geojson["features"]:
        name = feature["properties"][geo_key]
        geom = feature["geometry"]
        lons, lats = [], []
        if geom["type"] == "Polygon":
            for ring in geom["coordinates"]:
                for pt in ring:
                    lons.append(pt[0])
                    lats.append(pt[1])
        elif geom["type"] == "MultiPolygon":
            for poly in geom["coordinates"]:
                for ring in poly:
                    for pt in ring:
                        lons.append(pt[0])
                        lats.append(pt[1])
        if lons and lats:
            centroids[name] = (sum(lons)/len(lons), sum(lats)/len(lats))

    # Tampilkan label singkat teks (Nama Provinsi) di peta
    label_lons = []
    label_lats = []
    label_texts = []
    
    for idx, row in df_clean.iterrows():
        prov = row["Provinsi"]
        if prov in centroids:
            lon, lat = centroids[prov]
            # Singkatkan nama provinsi yang terlalu panjang jika diperlukan agar tidak bertumpuk
            short_names = {
                "Kepulauan Riau": "Kep. Riau",
                "Bangka-Belitung": "Babel",
                "Nusa Tenggara Barat": "NTB",
                "Nusa Tenggara Timur": "NTT",
                "Sulawesi Tenggara": "Sultra",
                "Sulawesi Utara": "Sulut",
                "Sulawesi Selatan": "Sulsel",
                "Sulawesi Tengah": "Sulteng",
                "Sulawesi Barat": "Sulbar",
                "Kalimantan Timur": "Kaltim",
                "Kalimantan Barat": "Kalbar",
                "Kalimantan Tengah": "Kalteng",
                "Kalimantan Selatan": "Kalsel",
                "Kalimantan Utara": "Kaltara",
                "Sumatera Utara": "Sumut",
                "Sumatera Barat": "Sumbar",
                "Sumatera Selatan": "Sumsel",
                "Jakarta Raya": "DKI Jakarta",
            }
            display_name = short_names.get(prov, prov)
            label_lons.append(lon)
            label_lats.append(lat)
            label_texts.append(display_name)

    fig.add_trace(go.Scattergeo(
        lon=label_lons,
        lat=label_lats,
        text=label_texts,
        mode="text",
        textfont=dict(size=8, color="#cbd5e1", family="Inter, sans-serif"),
        hoverinfo="skip",
        showlegend=False
    ))

    fig.update_geos(
        fitbounds="locations",
        visible=True,
        showland=False,
        showcoastlines=False,
        showlakes=False,
        showcountries=False,
        showocean=False,
        bgcolor="rgba(0,0,0,0)",
    )

    fig.update_layout(
        template=CHART_TEMPLATE,
        height=560,
        margin=dict(t=60, b=10, l=0, r=0),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#d0e0ff"),
        hoverlabel=dict(bgcolor="#1e2a3a", font_color="#e0eaff", bordercolor="#4a9eff"),
        coloraxis_colorbar=dict(
            title=dict(
                text="TPT (%)",
                font=dict(color="#a0c4e8"),
            ),
            tickfont=dict(color="#a0c4e8"),
            bgcolor="rgba(10,22,40,0.7)",
            bordercolor="#1a3050",
            borderwidth=1,
            thickness=14,
            len=0.75,
        ),
        geo=dict(bgcolor="rgba(0,0,0,0)"),
    )

    return fig

