# figures/question3_figures.py
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def empty_hist_figure(title="Histograma"):
    fig = go.Figure()
    fig.update_layout(
        title=title, template="plotly_white",
        xaxis_title="Puntaje", yaxis_title="Frecuencia",
        height=320, margin=dict(l=40, r=20, t=45, b=40),
        annotations=[dict(
            text="Selecciona un grupo en el gráfico superior para visualizar el histograma",
            x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False, font=dict(size=13)
        )]
    )
    return fig

def histogram_fixed(df_sub, x_col, title, x_range=(100, 420), nbins=20):
    fig = px.histogram(df_sub, x=x_col, nbins=nbins, range_x=x_range, title=title)
    fig.update_layout(
        template="plotly_white",
        xaxis_title=x_col,
        yaxis_title="Frecuencia",
        height=320,
        margin=dict(l=40, r=20, t=45, b=40),
    )
    fig.update_xaxes(range=list(x_range))
    return fig

def _highlight_bars(fig, selected_label=None, base_color="#2c7fb8", highlight_color="crimson"):
    if not fig.data:
        return fig
    tr = fig.data[0]
    labels = list(tr.x)
    n = len(labels)
    if selected_label is None or str(selected_label) not in [str(x) for x in labels]:
        tr.marker.color = [base_color] * n
        tr.marker.opacity = [0.90] * n
        tr.marker.line = dict(color=[base_color] * n, width=[0] * n)
        return fig

    idx = [str(x) for x in labels].index(str(selected_label))
    colors, op, lc, lw = [], [], [], []
    for i in range(n):
        if i == idx:
            colors.append(base_color); op.append(1.0); lc.append(highlight_color); lw.append(2)
        else:
            colors.append(base_color); op.append(0.25); lc.append(base_color); lw.append(0)
    tr.marker.color = colors
    tr.marker.opacity = op
    tr.marker.line = dict(color=lc, width=lw)
    return fig

def bar_window_municipios(df_plot, x_col, y_col, title, start=0, window=20, selected_mun=None):
    start = max(0, int(start))
    window = max(5, int(window))
    end = min(len(df_plot), start + window)
    view = df_plot.iloc[start:end].copy()

    fig = px.bar(view, x=x_col, y=y_col, title=title, text=view[y_col].round(2))
    fig.update_traces(customdata=np.stack([view[x_col].astype(str)], axis=-1))
    fig.update_layout(
        template="plotly_white",
        height=520,
        margin=dict(l=50, r=20, t=55, b=40),
        xaxis_title="Municipio",
        yaxis_title="Promedio",
        clickmode="event+select",
    )
    fig.update_xaxes(tickangle=45)
    return _highlight_bars(fig, selected_label=selected_mun)

def heatmap_window(df_gap, municipios_orden, techs_sel, start=0, window=25):
    # construye matriz: filas=municipio (ventana), cols=tech
    start = max(0, int(start))
    window = max(5, int(window))
    end = min(len(municipios_orden), start + window)
    mun_view = municipios_orden[start:end]

    d = df_gap[df_gap["municipio"].isin(mun_view)].copy()
    if techs_sel:
        d = d[d["tech"].isin(techs_sel)]

    pivot = d.pivot_table(index="municipio", columns="tech", values="gap", aggfunc="mean")
    pivot = pivot.reindex(mun_view)  # respeta orden ventana

    fig = px.imshow(
        pivot,
        aspect="auto",
        title="Mapa de calor - Brecha digital (Con acceso - Sin acceso)",
        labels=dict(x="Tecnología", y="Municipio", color="Brecha"),
    )
    fig.update_layout(template="plotly_white", height=520, margin=dict(l=120, r=20, t=55, b=40))
    return fig

def boxplot_area(area_tech_df, areas_sel, techs_sel):
    d = area_tech_df.copy()
    if areas_sel:
        d = d[d["area"].isin(areas_sel)]
    if techs_sel:
        d = d[d["tech"].isin(techs_sel)]
    d = d.dropna(subset=["score", "area", "tech", "access"])

    if d.empty:
        fig = go.Figure()
        fig.update_layout(
            template="plotly_white", height=520, margin=dict(l=60, r=20, t=55, b=40),
            title="Desempeño por área (sin datos para filtros)"
        )
        return fig

    # color por acceso; facet por tech si hay varias
    facet = "tech" if len(d["tech"].unique()) > 1 else None
    fig = px.box(
        d,
        x="area",
        y="score",
        color="access",
        facet_col=facet,
        points="outliers",
        title="Desempeño por área académica según acceso tecnológico"
    )
    fig.update_layout(template="plotly_white", height=520, margin=dict(l=60, r=20, t=55, b=40))
    fig.update_xaxes(tickangle=25)
    return fig