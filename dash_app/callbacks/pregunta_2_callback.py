# callbacks/question2.py
from dash import Input, Output, State, no_update, html, ctx
from flask import current_app

from figures.figures_pregunta_2 import barh_window, histogram_fixed, empty_hist_figure


COL_PUNT = "punt_global"
COL_MUN = "cole_mcpio_ubicacion"

def _get_q2():
    cfg = current_app.config
    return (
        cfg["DF_P2"],
        cfg["Q2_GP_MUN"],
        cfg["Q2_GP_UR"],
        cfg["Q2_GP_OF"],
        cfg["Q2_MUNICIPIOS"]
    )

def _badge(text):
    return html.Div(
        text,
        style={
            "padding":"8px 10px",
            "border":"1px solid #222",
            "backgroundColor":"#fff",
            "display":"inline-block",
            "fontSize":"14px"
        }
    )

def register_question2_callbacks(app):

    # ==========================================
    # Inicialización de sliders + dropdowns
    # ==========================================
    @app.callback(
        Output("q2-mun-slider", "max"),
        Output("q2-mun-dd", "options"),
        Input("url", "pathname"),
        prevent_initial_call=False
    )
    def init_mun_controls(path):
        if path != "/pregunta-2/municipio":
            return no_update, no_update
        _, _, _, _, municipios = _get_q2()
        opts = [{"label": m, "value": m} for m in municipios]
        maxv = max(0, len(municipios) - 1)
        return maxv, opts

    @app.callback(
        Output("q2-ur-slider", "max"),
        Output("q2-ur-dd", "options"),
        Input("url", "pathname"),
        prevent_initial_call=False
    )
    def init_ur_controls(path):
        if path != "/pregunta-2/rural-urbano":
            return no_update, no_update
        _, _, _, _, municipios = _get_q2()
        opts = [{"label": m, "value": m} for m in municipios]
        maxv = max(0, len(municipios) - 1)
        return maxv, opts

    @app.callback(
        Output("q2-of-slider", "max"),
        Output("q2-of-dd", "options"),
        Input("url", "pathname"),
        prevent_initial_call=False
    )
    def init_of_controls(path):
        if path != "/pregunta-2/oficiales-nooficiales":
            return no_update, no_update
        _, _, _, _, municipios = _get_q2()
        opts = [{"label": m, "value": m} for m in municipios]
        maxv = max(0, len(municipios) - 1)
        return maxv, opts

    # ==========================================
    # Store selección por vista
    # ==========================================

    # Click municipio
    @app.callback(
        Output("store-q2-selection", "data", allow_duplicate=True),
        Input("q2-mun-main", "clickData"),
        Input("q2-mun-clear", "n_clicks"),
        prevent_initial_call=True
    )
    def store_sel_mun(clickData, n_clear):
        if ctx.triggered_id == "q2-mun-clear":
            return {"view": "municipio", "selected": None}
        if not clickData:
            return no_update
        p = clickData["points"][0]
        mun = p["customdata"][0] if p.get("customdata") is not None else p.get("y")
        return {"view": "municipio", "selected": mun}

    # Click urbano-rural
    @app.callback(
        Output("store-q2-selection", "data", allow_duplicate=True),
        Input("q2-ur-main", "clickData"),
        Input("q2-ur-clear", "n_clicks"),
        prevent_initial_call=True
    )
    def store_sel_ur(clickData, n_clear):
        if ctx.triggered_id == "q2-ur-clear":
            return {"view": "rural_urbano", "selected": None}
        if not clickData:
            return no_update
        p = clickData["points"][0]
        mun = p["customdata"][0] if p.get("customdata") is not None else p.get("y")
        return {"view": "rural_urbano", "selected": mun}

    # Click oficial-no oficial
    @app.callback(
        Output("store-q2-selection", "data", allow_duplicate=True),
        Input("q2-of-main", "clickData"),
        Input("q2-of-clear", "n_clicks"),
        prevent_initial_call=True
    )
    def store_sel_of(clickData, n_clear):
        if ctx.triggered_id == "q2-of-clear":
            return {"view": "oficial_no", "selected": None}
        if not clickData:
            return no_update
        p = clickData["points"][0]
        mun = p["customdata"][0] if p.get("customdata") is not None else p.get("y")
        return {"view": "oficial_no", "selected": mun}

    # ==========================================
    # Dropdown => mover slider y guardar selección
    # ==========================================
    @app.callback(
        Output("q2-mun-slider", "value"),
        Output("store-q2-selection", "data", allow_duplicate=True),
        Input("q2-mun-dd", "value"),
        State("store-q2-selection", "data"),
        prevent_initial_call=True
    )
    def dd_to_slider_mun(mun, store):
        if mun is None:
            return no_update, no_update
        _, _, _, _, municipios = _get_q2()
        if mun in municipios:
            idx = municipios.index(mun)
            return idx, {"view": "municipio", "selected": mun}
        return no_update, no_update

    @app.callback(
        Output("q2-ur-slider", "value"),
        Output("store-q2-selection", "data", allow_duplicate=True),
        Input("q2-ur-dd", "value"),
        prevent_initial_call=True
    )
    def dd_to_slider_ur(mun):
        if mun is None:
            return no_update, no_update
        _, _, _, _, municipios = _get_q2()
        if mun in municipios:
            idx = municipios.index(mun)
            return idx, {"view": "rural_urbano", "selected": mun}
        return no_update, no_update

    @app.callback(
        Output("q2-of-slider", "value"),
        Output("store-q2-selection", "data", allow_duplicate=True),
        Input("q2-of-dd", "value"),
        prevent_initial_call=True
    )
    def dd_to_slider_of(mun):
        if mun is None:
            return no_update, no_update
        _, _, _, _, municipios = _get_q2()
        if mun in municipios:
            idx = municipios.index(mun)
            return idx, {"view": "oficial_no", "selected": mun}
        return no_update, no_update

    # ==========================================
    # Render MAIN FIG 
    # slider controla start de la ventana
    # ==========================================
    WINDOW = 20

    @app.callback(
        Output("q2-mun-main", "figure"),
        Input("url", "pathname"),
        Input("q2-mun-slider", "value"),
        Input("store-q2-selection", "data"),
        prevent_initial_call=False
    )
    def render_main_mun(path, start, store):
        if path != "/pregunta-2/municipio":
            return no_update
        _, gp_mun, _, _, _ = _get_q2()
        sel = store.get("selected") if store and store.get("view") == "municipio" else None

        df_plot = gp_mun.rename(columns={"municipio":"municipio", "promedio":"valor"}).copy()
        # para municipio, orden desc por promedio
        df_plot = df_plot.sort_values("valor", ascending=False)

        return barh_window(
            df_plot=df_plot,
            y_col="municipio",
            x_col="valor",
            title="Puntaje promedio por municipio",
            start=start or 0,
            window=WINDOW,
            selected_label=sel,
            xaxis_title="Promedio PUNT_GLOBAL"
        )

    @app.callback(
        Output("q2-ur-main", "figure"),
        Input("url", "pathname"),
        Input("q2-ur-slider", "value"),
        Input("store-q2-selection", "data"),
        prevent_initial_call=False
    )
    def render_main_ur(path, start, store):
        if path != "/pregunta-2/rural-urbano":
            return no_update
        _, _, gp_ur, _, _ = _get_q2()
        sel = store.get("selected") if store and store.get("view") == "rural_urbano" else None

        df_plot = gp_ur.rename(columns={"gap_urb_rur":"valor"}).copy()
        df_plot = df_plot.sort_values("valor", ascending=False)

        return barh_window(
            df_plot=df_plot,
            y_col="municipio",
            x_col="valor",
            title="Brecha Urbano - Rural (URBANO - RURAL)",
            start=start or 0,
            window=WINDOW,
            selected_label=sel,
            xaxis_title="Brecha de puntaje"
        )

    @app.callback(
        Output("q2-of-main", "figure"),
        Input("url", "pathname"),
        Input("q2-of-slider", "value"),
        Input("store-q2-selection", "data"),
        prevent_initial_call=False
    )
    def render_main_of(path, start, store):
        if path != "/pregunta-2/oficiales-nooficiales":
            return no_update
        _, _, _, gp_of, _ = _get_q2()
        sel = store.get("selected") if store and store.get("view") == "oficial_no" else None

        df_plot = gp_of.rename(columns={"gap_ofi_nof":"valor"}).copy()
        df_plot = df_plot.sort_values("valor", ascending=False)

        return barh_window(
            df_plot=df_plot,
            y_col="municipio",
            x_col="valor",
            title="Brecha Oficial - No Oficial (OFICIAL - NO OFICIAL)",
            start=start or 0,
            window=WINDOW,
            selected_label=sel,
            xaxis_title="Brecha de puntaje"
        )

    # ==========================================
    # Render HIST + badge 
    # Histograma siempre del municipio seleccionado
    # ==========================================
    @app.callback(
        Output("q2-mun-hist", "figure"),
        Output("q2-mun-selection", "children"),
        Input("url", "pathname"),
        Input("store-q2-selection", "data"),
        prevent_initial_call=False
    )
    def render_hist_mun(path, store):
        if path != "/pregunta-2/municipio":
            return no_update, no_update
        df, *_ = _get_q2()

        if not store or store.get("view") != "municipio" or not store.get("selected"):
            return empty_hist_figure("Histograma municipio"), _badge("Sin selección")

        mun = store["selected"]
        df_sub = df[df[COL_MUN].astype(str) == str(mun)]
        return histogram_fixed(df_sub, f"Histograma del municipio: {mun}", x_range=(100, 420), nbins=20), _badge(f"Selección actual: {mun}")

    @app.callback(
        Output("q2-ur-hist", "figure"),
        Output("q2-ur-selection", "children"),
        Input("url", "pathname"),
        Input("store-q2-selection", "data"),
        prevent_initial_call=False
    )
    def render_hist_ur(path, store):
        if path != "/pregunta-2/rural-urbano":
            return no_update, no_update
        df, *_ = _get_q2()

        if not store or store.get("view") != "rural_urbano" or not store.get("selected"):
            return empty_hist_figure("Histograma municipio"), _badge("Sin selección")

        mun = store["selected"]
        df_sub = df[df[COL_MUN].astype(str) == str(mun)]
        return histogram_fixed(df_sub, f"Histograma del municipio: {mun}", x_range=(100, 420), nbins=20), _badge(f"Selección actual: {mun}")

    @app.callback(
        Output("q2-of-hist", "figure"),
        Output("q2-of-selection", "children"),
        Input("url", "pathname"),
        Input("store-q2-selection", "data"),
        prevent_initial_call=False
    )
    def render_hist_of(path, store):
        if path != "/pregunta-2/oficiales-nooficiales":
            return no_update, no_update
        df, *_ = _get_q2()

        if not store or store.get("view") != "oficial_no" or not store.get("selected"):
            return empty_hist_figure("Histograma municipio"), _badge("Sin selección")

        mun = store["selected"]
        df_sub = df[df[COL_MUN].astype(str) == str(mun)]
        return histogram_fixed(df_sub, f"Histograma del municipio: {mun}", x_range=(100, 420), nbins=20), _badge(f"Selección actual: {mun}")