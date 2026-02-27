# callbacks/question3.py
from dash import Input, Output, State, no_update, html, ctx
from flask import current_app

from figures.figures_pregunta_3 import (
    bar_window_municipios, heatmap_window, boxplot_area,
    histogram_fixed, empty_hist_figure
)

WINDOW_BAR = 20
WINDOW_HEAT = 25

def _get_q3():
    cfg = current_app.config
    return cfg["DF3"], cfg["Q3"]

def _badge(text):
    return html.Div(text, style={"padding":"8px 10px","border":"1px solid #222","backgroundColor":"#fff","display":"inline-block","fontSize":"14px"})

def register_question3_callbacks(app):
    # ==========================================
    # Inicialización controles (Municipio-Tecnología)
    # ==========================================
    @app.callback(
        Output("q3-mt-slider", "max"),
        Output("q3-mt-dd", "options"),
        Output("q3-mt-tech", "options"),
        Input("url", "pathname"),
        prevent_initial_call=False
    )
    def init_mt(path):
        if path != "/pregunta-3/municipio-tecnologia":
            return no_update, no_update, no_update
        _, q3 = _get_q3()
        maxv = max(0, len(q3["municipios"]) - 1)
        dd = [{"label": m, "value": m} for m in q3["municipios"]]
        tech = [{"label": t, "value": t} for t in q3["techs"]]
        return maxv, dd, tech

    # ==========================================
    # Inicialización controles (Brecha digital)
    # ==========================================
    @app.callback(
        Output("q3-bd-slider", "max"),
        Output("q3-bd-dd", "options"),
        Output("q3-bd-tech", "options"),
        Input("url", "pathname"),
        prevent_initial_call=False
    )
    def init_bd(path):
        if path != "/pregunta-3/brecha-digital":
            return no_update, no_update, no_update
        _, q3 = _get_q3()
        maxv = max(0, len(q3["municipios"]) - 1)
        dd = [{"label": m, "value": m} for m in q3["municipios"]]
        tech = [{"label": t, "value": t} for t in q3["techs"]]
        return maxv, dd, tech

    # ==========================================
    # Inicialización controles (Desempeño área)
    # ==========================================
    @app.callback(
        Output("q3-da-area", "options"),
        Output("q3-da-tech", "options"),
        Input("url", "pathname"),
        prevent_initial_call=False
    )
    def init_da(path):
        if path != "/pregunta-3/desempeno-area":
            return no_update, no_update
        _, q3 = _get_q3()
        areas = [{"label": a, "value": a} for a in q3["areas"]]
        tech = [{"label": t, "value": t} for t in q3["techs"]]
        return areas, tech

    # ==========================================
    # Store selección por vista
    # ==========================================
    @app.callback(
        Output("store-q3-selection", "data", allow_duplicate=True),
        Input("q3-mt-main", "clickData"),
        Input("q3-mt-clear", "n_clicks"),
        prevent_initial_call=True
    )
    def store_mt_click(clickData, nclear):
        if ctx.triggered_id == "q3-mt-clear":
            return {"view":"mt", "municipio":None}
        if not clickData:
            return no_update
        p = clickData["points"][0]
        mun = p["customdata"][0] if p.get("customdata") is not None else p.get("x")
        return {"view":"mt", "municipio": mun}

    @app.callback(
        Output("store-q3-selection", "data", allow_duplicate=True),
        Input("q3-bd-dd", "value"),
        Input("q3-bd-clear", "n_clicks"),
        prevent_initial_call=True
    )
    def store_bd_select(mun, nclear):
        if ctx.triggered_id == "q3-bd-clear":
            return {"view":"bd", "municipio":None}
        if mun is None:
            return no_update
        return {"view":"bd", "municipio": mun}

    @app.callback(
        Output("store-q3-selection", "data", allow_duplicate=True),
        Input("q3-da-main", "clickData"),
        Input("q3-da-clear", "n_clicks"),
        prevent_initial_call=True
    )
    def store_da_click(clickData, nclear):
        if ctx.triggered_id == "q3-da-clear":
            return {"view":"da", "area":None, "tech":None, "access":None}
        if not clickData:
            return no_update
        p = clickData["points"][0]
        area = p.get("x")
        return {"view":"da", "area": area}
    
    # ==========================================
    # Dropdown municipio => mover slider (MT)
    # ==========================================
    @app.callback(
        Output("q3-mt-slider", "value"),
        Output("store-q3-selection", "data", allow_duplicate=True),
        Input("q3-mt-dd", "value"),
        prevent_initial_call=True
    )
    def mt_dd_to_slider(mun):
        if mun is None:
            return no_update, no_update
        _, q3 = _get_q3()
        if mun in q3["municipios"]:
            idx = q3["municipios"].index(mun)
            return idx, {"view":"mt", "municipio": mun}
        return no_update, no_update

    # ==========================================
    # Render MAIN (MT: barras)
    # ==========================================
    @app.callback(
        Output("q3-mt-main", "figure"),
        Input("url", "pathname"),
        Input("q3-mt-slider", "value"),
        Input("q3-mt-tech", "value"),
        Input("store-q3-selection", "data"),
        prevent_initial_call=False
    )
    def render_mt_main(path, start, techs_sel, store):
        if path != "/pregunta-3/municipio-tecnologia":
            return no_update
        _, q3 = _get_q3()

        d = q3["gp_bar"].copy()
        if techs_sel:
            d = d[d["tech"].isin(techs_sel)]
        d = d[d["access"] == "Con acceso"]

        d = (d.groupby("municipio", as_index=False)
               .agg(valor=("promedio", "mean"))
               .sort_values("valor", ascending=False))

        sel = store.get("municipio") if store and store.get("view") == "mt" else None

        return bar_window_municipios(
            df_plot=d, x_col="municipio", y_col="valor",
            title="Puntaje promedio por municipio (Con acceso)",
            start=start or 0, window=WINDOW_BAR, selected_mun=sel
        )

    # ==========================================
    # Render HIST (MT)
    # ==========================================
    @app.callback(
        Output("q3-mt-hist", "figure"),
        Output("q3-mt-selection", "children"),
        Input("url", "pathname"),
        Input("store-q3-selection", "data"),
        prevent_initial_call=False
    )
    def render_mt_hist(path, store):
        if path != "/pregunta-3/municipio-tecnologia":
            return no_update, no_update
        df, q3 = _get_q3()
        col_mun = q3["cfg"]["COL_MUN"]
        col_punt = q3["cfg"]["COL_PUNT_GLOBAL"]

        if not store or store.get("view") != "mt" or not store.get("municipio"):
            return empty_hist_figure("Histograma municipio"), _badge("Sin selección")

        mun = store["municipio"]
        df_sub = df[df[col_mun].astype(str) == str(mun)]
        return histogram_fixed(df_sub, col_punt, f"Histograma del municipio: {mun}", x_range=(100, 420), nbins=20), _badge(f"Selección actual: {mun}")

    # ==========================================
    # Render MAIN (BD: heatmap)
    # ==========================================
    @app.callback(
        Output("q3-bd-main", "figure"),
        Input("url", "pathname"),
        Input("q3-bd-slider", "value"),
        Input("q3-bd-tech", "value"),
        prevent_initial_call=False
    )
    def render_bd_main(path, start, techs_sel):
        if path != "/pregunta-3/brecha-digital":
            return no_update
        _, q3 = _get_q3()
        return heatmap_window(q3["gp_gap"], q3["municipios"], techs_sel or q3["techs"], start=start or 0, window=WINDOW_HEAT)

    # ==========================================
    # Render HIST (BD)
    # ==========================================
    @app.callback(
        Output("q3-bd-hist", "figure"),
        Output("q3-bd-selection", "children"),
        Input("url", "pathname"),
        Input("store-q3-selection", "data"),
        prevent_initial_call=False
    )
    def render_bd_hist(path, store):
        if path != "/pregunta-3/brecha-digital":
            return no_update, no_update
        df, q3 = _get_q3()
        col_mun = q3["cfg"]["COL_MUN"]
        col_punt = q3["cfg"]["COL_PUNT_GLOBAL"]

        if not store or store.get("view") != "bd" or not store.get("municipio"):
            return empty_hist_figure("Histograma municipio"), _badge("Sin selección")

        mun = store["municipio"]
        df_sub = df[df[col_mun].astype(str) == str(mun)]
        return histogram_fixed(df_sub, col_punt, f"Histograma del municipio: {mun}", x_range=(100, 420), nbins=20), _badge(f"Selección actual: {mun}")

    # ==========================================
    # Render MAIN (DA: boxplot)
    # ==========================================
    @app.callback(
        Output("q3-da-main", "figure"),
        Input("url", "pathname"),
        Input("q3-da-area", "value"),
        Input("q3-da-tech", "value"),
        prevent_initial_call=False
    )
    def render_da_main(path, areas_sel, techs_sel):
        if path != "/pregunta-3/desempeno-area":
            return no_update
        _, q3 = _get_q3()
        return boxplot_area(q3["area_tech"], areas_sel or q3["areas"], techs_sel or q3["techs"])

    # ==========================================
    # Render HIST (DA) - por área seleccionada (click)
    # ==========================================
    @app.callback(
        Output("q3-da-hist", "figure"),
        Output("q3-da-selection", "children"),
        Input("url", "pathname"),
        Input("store-q3-selection", "data"),
        Input("q3-da-area", "value"),
        Input("q3-da-tech", "value"),
        prevent_initial_call=False
    )
    def render_da_hist(path, store, areas_sel, techs_sel):
        if path != "/pregunta-3/desempeno-area":
            return no_update, no_update
        _, q3 = _get_q3()

        if not store or store.get("view") != "da" or not store.get("area"):
            return empty_hist_figure("Histograma (área)"), _badge("Sin selección")

        area = store["area"]
        d = q3["area_tech"].copy()
        d = d[d["area"].astype(str) == str(area)]
        if techs_sel:
            d = d[d["tech"].isin(techs_sel)]
        # si el usuario también filtró áreas con checklist, respetarlo
        if areas_sel:
            d = d[d["area"].isin(areas_sel)]

        if d.empty:
            return empty_hist_figure("Histograma (área)"), _badge("Sin datos para la selección")

        return histogram_fixed(d, "score", f"Histograma del área: {area}", x_range=(0, 100), nbins=20), _badge(f"Selección actual: {area}")