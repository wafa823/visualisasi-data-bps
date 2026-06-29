# pyrefly: ignore [missing-import]
import plotly.express as px
import pandas as pd

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
