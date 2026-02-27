# figures/question2_figures.py
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def empty_hist_figure(title="Histograma"):
    fig = go.Figure()
    fig.update_layout(
        title=title,
        template="plotly_white",
        xaxis_title="Puntaje global",
        yaxis_title="Frecuencia",
        height=320,
        margin=dict(l=40, r=20, t=45, b=40),
        annotations=[dict(
            text="Selecciona un municipio en la gráfica superior para visualizar el histograma",
            x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False, font=dict(size=13)
        )]
    )
    return fig

def histogram_fixed(df_sub, title, x_range=(100, 420), nbins=20):
    fig = px.histogram(df_sub, x="punt_global", nbins=nbins, range_x=x_range, title=title)
    fig.update_layout(
        template="plotly_white",
        xaxis_title="Puntaje global",
        yaxis_title="Frecuencia",
        height=320,
        margin=dict(l=40, r=20, t=45, b=40),
    )
    fig.update_xaxes(range=list(x_range))
    return fig

def _highlight_barh(fig, selected_label=None, base_color="#2c7fb8", highlight_color="crimson"):
    if not fig.data:
        return fig

    trace = fig.data[0]
    labels = list(trace.y)  # en barh, y son los municipios (categorías)

    n = len(labels)
    if selected_label is None or str(selected_label) not in [str(x) for x in labels]:
        trace.marker.color = [base_color] * n
        trace.marker.opacity = [0.90] * n
        trace.marker.line = dict(color=[base_color] * n, width=[0] * n)
        return fig

    sel_idx = [str(x) for x in labels].index(str(selected_label))

    colors, opacities, line_colors, line_widths = [], [], [], []
    for i in range(n):
        if i == sel_idx:
            colors.append(base_color)
            opacities.append(1.0)
            line_colors.append(highlight_color)
            line_widths.append(2)
        else:
            colors.append(base_color)
            opacities.append(0.25)
            line_colors.append(base_color)
            line_widths.append(0)

    trace.marker.color = colors
    trace.marker.opacity = opacities
    trace.marker.line = dict(color=line_colors, width=line_widths)
    return fig

def barh_window(df_plot, y_col, x_col, title, start=0, window=20, selected_label=None, xaxis_title="Valor"):
    """
    df_plot: DataFrame ya ordenado (desc o asc) con columnas y_col (municipio) y x_col (valor)
    start: índice inicio de la ventana
    window: tamaño de ventana visible
    """
    start = max(0, int(start))
    window = max(5, int(window))
    end = min(len(df_plot), start + window)

    view = df_plot.iloc[start:end].copy()

    fig = px.bar(
        view,
        x=x_col,
        y=y_col,
        orientation="h",
        title=title,
        text=view[x_col].round(2) if np.issubdtype(view[x_col].dtype, np.number) else None,
    )
    fig.update_traces(customdata=np.stack([view[y_col].astype(str)], axis=-1))

    fig.update_layout(
        template="plotly_white",
        height=520,
        margin=dict(l=140, r=20, t=55, b=40),
        xaxis_title=xaxis_title,
        yaxis_title="Municipio",
        clickmode="event+select",
    )

    # Para que el mejor quede arriba, invertimos yaxis
    fig.update_yaxes(autorange="reversed")

    return _highlight_barh(fig, selected_label=selected_label)