import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# Utilidades de estilo de selección
# -----------------------------
def _apply_selected_style_bar(fig, selected_idx=None, selected_color="#2c7fb8", highlight_color="crimson"):
    """
    Resalta una barra (bar/barh) sin usar selected/unselected (más robusto entre versiones de Plotly).
    """
    if not fig.data:
        return fig

    trace = fig.data[0]
    n = len(trace.x) if trace.x is not None else len(trace.y)

    # Sin selección: estilo uniforme
    if selected_idx is None:
        trace.marker.color = [selected_color] * n
        trace.marker.opacity = 0.9
        # borde uniforme (opcional)
        trace.marker.line = dict(color=[selected_color] * n, width=[0] * n)
        return fig

    # Con selección: resaltar una barra y atenuar las demás
    colors = []
    opacities = []
    line_colors = []
    line_widths = []

    for i in range(n):
        if i == selected_idx:
            colors.append(selected_color)
            opacities.append(1.0)
            line_colors.append(highlight_color)
            line_widths.append(2)
        else:
            colors.append(selected_color)
            opacities.append(0.25)
            line_colors.append(selected_color)
            line_widths.append(0)

    trace.marker.color = colors
    trace.marker.opacity = opacities
    trace.marker.line = dict(color=line_colors, width=line_widths)

    return fig

def _apply_selected_style_scatter_trace(fig, trace_index, selected_idx=None, highlight_color="crimson"):
    """
    Resalta un punto de un trace scatter de forma manual (sin selected/unselected),
    para evitar errores de compatibilidad entre versiones de Plotly.
    """
    if not fig.data or trace_index >= len(fig.data):
        return fig

    trace = fig.data[trace_index]

    # Número de puntos del trace
    n = len(trace.x) if trace.x is not None else 0
    if n == 0:
        return fig

    # Estilo base (sin selección)
    sizes = [8] * n
    opacities = [0.85] * n
    line_colors = ["rgba(0,0,0,0)"] * n
    line_widths = [0] * n

    # Si hay selección, resaltamos ese punto y atenuamos los demás
    if selected_idx is not None and 0 <= selected_idx < n:
        opacities = [0.25] * n
        sizes = [8] * n
        line_colors = ["rgba(0,0,0,0)"] * n
        line_widths = [0] * n

        sizes[selected_idx] = 12
        opacities[selected_idx] = 1.0
        line_colors[selected_idx] = highlight_color
        line_widths[selected_idx] = 2

    # Aplicar a marcadores
    trace.marker.size = sizes
    trace.marker.opacity = opacities
    trace.marker.line = dict(color=line_colors, width=line_widths)

    return fig

# -----------------------------
# Figuras base
# -----------------------------
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
            text="Selecciona una categoría en la gráfica superior para visualizar el histograma",
            x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False, font=dict(size=13)
        )]
    )
    return fig

def histogram_fixed(df_sub, title, x_range=(100, 420), nbins=20):
    fig = px.histogram(
        df_sub,
        x="PUNT_GLOBAL",
        nbins=nbins,
        range_x=x_range,
        title=title
    )
    fig.update_layout(
        template="plotly_white",
        xaxis_title="Puntaje global",
        yaxis_title="Frecuencia",
        height=320,
        margin=dict(l=40, r=20, t=45, b=40)
    )
    fig.update_xaxes(range=list(x_range))
    return fig

# -----------------------------
# Estrato
# -----------------------------
def fig_estrato(gp_est, selected_label=None):
    fig = px.bar(
        gp_est,
        x="Fami_Estrato",
        y="promedio",
        text=gp_est["promedio"].round(1),
        title="Puntaje global promedio por estrato",
    )
    fig.update_traces(customdata=np.stack([gp_est["Fami_Estrato"]], axis=-1))
    fig.update_layout(
        template="plotly_white",
        xaxis_title="Estrato",
        yaxis_title="Promedio Puntaje Global",
        height=300,
        margin=dict(l=40, r=20, t=45, b=40),
        clickmode="event+select",
    )

    selected_idx = None
    if selected_label is not None:
        labels = gp_est["Fami_Estrato"].astype(str).tolist()
        if str(selected_label) in labels:
            selected_idx = labels.index(str(selected_label))

    return _apply_selected_style_bar(fig, selected_idx)

# -----------------------------
# Educación padres
# -----------------------------
def fig_padres(gp_mad, gp_pad, selected_role=None, selected_label=None):
    fig = go.Figure()

    # Trace Madre
    fig.add_trace(go.Scatter(
        x=gp_mad["_educacion_MADRE"].astype(str),
        y=gp_mad["promedio"],
        mode="lines+markers",
        name="Madre",
        marker=dict(size=8),
        customdata=np.stack(
            [gp_mad["_educacion_MADRE"].astype(str), np.array(["MADRE"] * len(gp_mad))],
            axis=-1
        )
    ))

    # Trace Padre
    fig.add_trace(go.Scatter(
        x=gp_pad["_educacion_PADRE"].astype(str),
        y=gp_pad["promedio"],
        mode="lines+markers",
        name="Padre",
        marker=dict(size=8),
        customdata=np.stack(
            [gp_pad["_educacion_PADRE"].astype(str), np.array(["PADRE"] * len(gp_pad))],
            axis=-1
        )
    ))

    fig.update_layout(
        title="Puntaje promedio según educación de los padres",
        template="plotly_white",
        xaxis_title="Nivel educativo",
        yaxis_title="Promedio puntaje global",
        height=300,
        margin=dict(l=40, r=20, t=45, b=40),
        clickmode="event+select",
    )

    # Estilo base por si no hay selección
    fig.data[0].opacity = 0.95
    fig.data[1].opacity = 0.95

    # Aplicar resaltado manual
    if selected_role is not None and selected_label is not None:
        mad_labels = gp_mad["_educacion_MADRE"].astype(str).tolist()
        pad_labels = gp_pad["_educacion_PADRE"].astype(str).tolist()

        if selected_role == "MADRE":
            idx_rel = mad_labels.index(str(selected_label)) if str(selected_label) in mad_labels else None

            # Resaltar punto en Madre
            _apply_selected_style_scatter_trace(fig, 0, idx_rel)

            # Atenuar trace Padre completo
            fig.data[1].opacity = 0.35
            _apply_selected_style_scatter_trace(fig, 1, None)

        elif selected_role == "PADRE":
            idx_rel = pad_labels.index(str(selected_label)) if str(selected_label) in pad_labels else None

            # Resaltar punto en Padre
            _apply_selected_style_scatter_trace(fig, 1, idx_rel)

            # Atenuar trace Madre completo
            fig.data[0].opacity = 0.35
            _apply_selected_style_scatter_trace(fig, 0, None)

    return fig

# -----------------------------
# Cuartos / Personas
# -----------------------------
def _top_bottom_cond(gp_cond):
    tb = px.data.tips()  # placeholder para no repetir warning, se reemplaza de inmediato
    tb = None
    tb = (
        np.nan  # dummy
    )
    # calculamos y devolvemos DataFrame real
    import pandas as pd
    out = pd.concat([gp_cond.nsmallest(5, "promedio"), gp_cond.nlargest(5, "promedio")]).copy()
    out = out.drop_duplicates(subset=["cond_est"]).sort_values("promedio")
    return out

def fig_condiciones(gp_cond, selected_label=None):
    tb = _top_bottom_cond(gp_cond)

    fig = px.bar(
        tb,
        x="promedio",
        y="cond_est",
        orientation="h",
        text=tb["promedio"].round(1),
        title="Condiciones del hogar (5 menores y 5 mayores promedios)"
    )
    fig.update_traces(customdata=np.stack([tb["cond_est"]], axis=-1))
    fig.update_layout(
        template="plotly_white",
        xaxis_title="Promedio Puntaje Global",
        yaxis_title="Cuartos_Personas",
        height=320,
        margin=dict(l=80, r=20, t=45, b=40),
        clickmode="event+select",
    )

    selected_idx = None
    if selected_label is not None:
        labels = tb["cond_est"].astype(str).tolist()
        if str(selected_label) in labels:
            selected_idx = labels.index(str(selected_label))

    return _apply_selected_style_bar(fig, selected_idx)