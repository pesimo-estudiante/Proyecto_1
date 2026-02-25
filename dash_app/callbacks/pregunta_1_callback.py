from dash import Input, Output, State, no_update, html, ctx
from flask import current_app

from figures.figures_pregunta_1 import (
    fig_estrato, fig_padres, fig_condiciones,
    histogram_fixed, empty_hist_figure
)

# ============================================================
# Helpers de acceso a dataframes
# ============================================================

def _get_data():
    cfg = current_app.config
    return (
        cfg["DF"],
        cfg["GP_EST"],
        cfg["GP_MAD"],
        cfg["GP_PAD"],
        cfg["GP_COND"],
    )

def _badge_text(text):
    return html.Div(
        text,
        style={
            "padding": "8px 10px",
            "border": "1px solid #222",
            "backgroundColor": "#fff",
            "display": "inline-block",
            "fontSize": "14px"
        }
    )

# ============================================================
# Registro de callbacks
# ============================================================

def register_question1_callbacks(app):

    # -----------------------------------------
    # 1) Guardar selección en store (estrato)
    # -----------------------------------------
    @app.callback(
        Output("store-q1-selection", "data", allow_duplicate=True),
        Input("graph-estrato-main", "clickData"),
        Input("btn-clear-estrato", "n_clicks"),
        prevent_initial_call=True
    )
    def store_selection_estrato(clickData, n_clear):
        trigger = ctx.triggered_id
        if trigger == "btn-clear-estrato":
            return {"view": "estrato", "selected": None}

        if not clickData:
            return no_update

        p = clickData["points"][0]
        label = p["customdata"][0] if p.get("customdata") is not None else p["x"]

        return {
            "view": "estrato",
            "selected": {"label": label}
        }

    # -----------------------------------------
    # 2) Guardar selección en store (padres)
    # -----------------------------------------
    @app.callback(
        Output("store-q1-selection", "data", allow_duplicate=True),
        Input("graph-padres-main", "clickData"),
        Input("btn-clear-padres", "n_clicks"),
        prevent_initial_call=True
    )
    def store_selection_padres(clickData, n_clear):
        trigger = ctx.triggered_id
        if trigger == "btn-clear-padres":
            return {"view": "padres", "selected": None}

        if not clickData:
            return no_update

        p = clickData["points"][0]
        if p.get("customdata") is not None:
            nivel = p["customdata"][0]
            rol = p["customdata"][1]   # MADRE / PADRE
        else:
            nivel = p["x"]
            rol = "MADRE"

        return {
            "view": "padres",
            "selected": {"label": nivel, "role": rol}
        }

    # -----------------------------------------
    # 3) Guardar selección en store (cuartos)
    # -----------------------------------------
    @app.callback(
        Output("store-q1-selection", "data", allow_duplicate=True),
        Input("graph-cuartos-main", "clickData"),
        Input("btn-clear-cuartos", "n_clicks"),
        prevent_initial_call=True
    )
    def store_selection_cuartos(clickData, n_clear):
        trigger = ctx.triggered_id
        if trigger == "btn-clear-cuartos":
            return {"view": "cuartos", "selected": None}

        if not clickData:
            return no_update

        p = clickData["points"][0]
        label = p["customdata"][0] if p.get("customdata") is not None else p["y"]

        return {
            "view": "cuartos",
            "selected": {"label": label}
        }

    # ============================================================
    # Render de figuras principales con resaltado de selección
    # ============================================================

    @app.callback(
        Output("graph-estrato-main", "figure"),
        Input("url", "pathname"),
        Input("store-q1-selection", "data"),
        prevent_initial_call=False
    )
    def render_estrato_main(pathname, store_data):
        if pathname != "/pregunta-1/estrato":
            return no_update

        _, gp_est, _, _, _ = _get_data()

        selected_label = None
        if store_data and store_data.get("view") == "estrato" and store_data.get("selected"):
            selected_label = store_data["selected"]["label"]

        return fig_estrato(gp_est, selected_label=selected_label)

    @app.callback(
        Output("graph-padres-main", "figure"),
        Input("url", "pathname"),
        Input("store-q1-selection", "data"),
        prevent_initial_call=False
    )
    def render_padres_main(pathname, store_data):
        if pathname != "/pregunta-1/padres":
            return no_update

        _, _, gp_mad, gp_pad, _ = _get_data()

        selected_label = None
        selected_role = None
        if store_data and store_data.get("view") == "padres" and store_data.get("selected"):
            selected_label = store_data["selected"]["label"]
            selected_role = store_data["selected"]["role"]

        return fig_padres(gp_mad, gp_pad, selected_role=selected_role, selected_label=selected_label)

    @app.callback(
        Output("graph-cuartos-main", "figure"),
        Input("url", "pathname"),
        Input("store-q1-selection", "data"),
        prevent_initial_call=False
    )
    def render_cuartos_main(pathname, store_data):
        if pathname != "/pregunta-1/cuartos-personas":
            return no_update

        _, _, _, _, gp_cond = _get_data()

        selected_label = None
        if store_data and store_data.get("view") == "cuartos" and store_data.get("selected"):
            selected_label = store_data["selected"]["label"]

        return fig_condiciones(gp_cond, selected_label=selected_label)

    # ============================================================
    # Histograma + texto de selección (estrato)
    # ============================================================

    @app.callback(
        Output("graph-estrato-hist", "figure"),
        Output("txt-estrato-selection", "children"),
        Input("url", "pathname"),
        Input("store-q1-selection", "data"),
        prevent_initial_call=False
    )
    def render_hist_estrato(pathname, store_data):
        if pathname != "/pregunta-1/estrato":
            return no_update, no_update

        df, *_ = _get_data()

        if not store_data or store_data.get("view") != "estrato" or not store_data.get("selected"):
            return empty_hist_figure("Histograma por estrato"), _badge_text("Sin selección")

        label = store_data["selected"]["label"]
        df_sub = df[df["Fami_Estrato"] == label]

        fig = histogram_fixed(df_sub, f"Histograma estrato: {label}", x_range=(100, 420), nbins=20)
        return fig, _badge_text(f"Selección actual: {label}")

    # ============================================================
    # Histograma + texto de selección (padres)
    # ============================================================

    @app.callback(
        Output("graph-padres-hist", "figure"),
        Output("txt-padres-selection", "children"),
        Input("url", "pathname"),
        Input("store-q1-selection", "data"),
        prevent_initial_call=False
    )
    def render_hist_padres(pathname, store_data):
        if pathname != "/pregunta-1/padres":
            return no_update, no_update

        df, *_ = _get_data()

        if not store_data or store_data.get("view") != "padres" or not store_data.get("selected"):
            return empty_hist_figure("Histograma por educación de padres"), _badge_text("Sin selección")

        label = store_data["selected"]["label"]
        role = store_data["selected"]["role"]

        if role == "MADRE":
            df_sub = df[df["_educacion_MADRE"] == label]
            title = f"Histograma nivel académico (Madre): {label}"
            badge = f"Selección actual: Madre - {label}"
        else:
            df_sub = df[df["_educacion_PADRE"] == label]
            title = f"Histograma nivel académico (Padre): {label}"
            badge = f"Selección actual: Padre - {label}"

        fig = histogram_fixed(df_sub, title, x_range=(100, 420), nbins=20)
        return fig, _badge_text(badge)

    # ============================================================
    # Histograma + texto de selección (cuartos/personas)
    # ============================================================

    @app.callback(
        Output("graph-cuartos-hist", "figure"),
        Output("txt-cuartos-selection", "children"),
        Input("url", "pathname"),
        Input("store-q1-selection", "data"),
        prevent_initial_call=False
    )
    def render_hist_cuartos(pathname, store_data):
        if pathname != "/pregunta-1/cuartos-personas":
            return no_update, no_update

        df, *_ = _get_data()

        if not store_data or store_data.get("view") != "cuartos" or not store_data.get("selected"):
            return empty_hist_figure("Histograma por categoría de cuartos/personas"), _badge_text("Sin selección")

        label = store_data["selected"]["label"]
        df_sub = df[df["cond_est"] == label]

        fig = histogram_fixed(
            df_sub,
            f"Histograma categoría cuartos/personas: {label}",
            x_range=(100, 420),
            nbins=20
        )
        return fig, _badge_text(f"Selección actual: {label}")