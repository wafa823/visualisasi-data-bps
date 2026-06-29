# pyrefly: ignore [missing-import]
import plotly.express as px
import pandas as pd

LABEL_COMMON = {
    "Tahun": "Tahun",
    "Jumlah Pengangguran": "Jumlah Pengangguran (Orang)",
    "Pendidikan": "Tingkat Pendidikan",
}

def _get_layout(theme: str, height=520, has_legend=True):
    """Kembalikan layout dictionary Plotly kustom berdasarkan tema."""
    is_dark = (theme == "Dark Mode")
    
    chart_template = "plotly_dark" if is_dark else "plotly_white"
    text_color = "#d0e0ff" if is_dark else "#0f172a"
    grid_color = "#1e3050" if is_dark else "#e2e8f0"
    
    hover_bg = "#1e2a3a" if is_dark else "#ffffff"
    hover_text = "#e0eaff" if is_dark else "#0f172a"
    hover_border = "#4a9eff" if is_dark else "#2563eb"
    
    layout = dict(
        template=chart_template,
        height=height,
        margin=dict(t=60, b=20, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=text_color),
        hoverlabel=dict(bgcolor=hover_bg, font_color=hover_text, bordercolor=hover_border),
    )
    
    if has_legend:
        layout["legend"] = dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="center", x=0.5)
        
    return layout, grid_color


def plot_line_chart(df_filtered: pd.DataFrame, rentang_tahun: tuple[int, int], theme: str):
    """Membuat Line Chart tren pengangguran dengan tema dinamis."""
    layout, grid_color = _get_layout(theme)
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
        **layout,
        hovermode="x unified",
        xaxis=dict(tickmode="linear", dtick=2, gridcolor=grid_color),
        yaxis=dict(gridcolor=grid_color),
    )
    return fig

def plot_horizontal_bar(df_filtered: pd.DataFrame, rentang_tahun: tuple[int, int], theme: str):
    """Membuat Horizontal Bar Chart untuk perbandingan dengan tema dinamis."""
    layout, grid_color = _get_layout(theme, has_legend=False)
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
        **layout,
        showlegend=False,
        xaxis=dict(gridcolor=grid_color),
        yaxis=dict(gridcolor="rgba(0,0,0,0)"),
    )
    return fig

def plot_treemap(df_filtered: pd.DataFrame, rentang_tahun: tuple[int, int], theme: str):
    """Membuat Treemap untuk komposisi kontribusi dengan tema dinamis."""
    is_dark = (theme == "Dark Mode")
    chart_template = "plotly_dark" if is_dark else "plotly_white"
    text_color = "#d0e0ff" if is_dark else "#0f172a"
    hover_bg = "#1e2a3a" if is_dark else "#ffffff"
    hover_text = "#e0eaff" if is_dark else "#0f172a"
    hover_border = "#4a9eff" if is_dark else "#2563eb"
    
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
        template=chart_template,
        height=520,
        margin=dict(t=60, b=20, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=text_color),
        hoverlabel=dict(bgcolor=hover_bg, font_color=hover_text, bordercolor=hover_border),
    )
    return fig

def plot_bubble_scatter(df_filtered: pd.DataFrame, rentang_tahun: tuple[int, int], theme: str):
    """Membuat Bubble Scatter plot dengan tema dinamis."""
    layout, grid_color = _get_layout(theme, has_legend=False)
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
        **layout,
        hovermode="closest",
        xaxis=dict(tickmode="linear", dtick=2, gridcolor=grid_color),
        yaxis=dict(gridcolor="rgba(0,0,0,0)"),
        showlegend=False,
    )
    return fig
