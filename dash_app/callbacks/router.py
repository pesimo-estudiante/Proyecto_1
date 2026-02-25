from dash import Output, Input, html
from diseños.home import home_layout
from diseños.pregunta_1 import question1_menu_layout
from diseños.paginas_variables import variable_page_layout
from user_interface.componentes import layout_shell, nav_top, footer_signature
from figures.figures_pregunta_1 import empty_hist_figure

def _placeholder_layout(title):
    return layout_shell([
        nav_top(show_home=True, back_href="/"),
        html.Div(title, style={"fontSize": "24px", "marginBottom": "12px"}),
        html.Div("Esta sección está en construcción."),
        footer_signature()
    ])

def _page_p1_estrato():
    return variable_page_layout(
        title="Estrato Familiar",
        subtitle="Para visualizar el histograma de un estrato específico, dé clic sobre la barra correspondiente.",
        main_graph_id="graph-estrato-main",
        hist_graph_id="graph-estrato-hist",
        selection_text_id="txt-estrato-selection",
        clear_btn_id="btn-clear-estrato"
    )

def _page_p1_padres():
    return variable_page_layout(
        title="Educación Padres",
        subtitle="Para visualizar el histograma de un nivel académico específico, dé clic sobre el punto correspondiente.",
        main_graph_id="graph-padres-main",
        hist_graph_id="graph-padres-hist",
        selection_text_id="txt-padres-selection",
        clear_btn_id="btn-clear-padres"
    )

def _page_p1_cuartos():
    return variable_page_layout(
        title="Cuartos/Personas que conviven en el hogar",
        subtitle="Para visualizar el histograma de una categoría específica, dé clic sobre la barra correspondiente.",
        main_graph_id="graph-cuartos-main",
        hist_graph_id="graph-cuartos-hist",
        selection_text_id="txt-cuartos-selection",
        clear_btn_id="btn-clear-cuartos"
    )

def register_router_callbacks(app):
    @app.callback(Output("page-content", "children"), Input("url", "pathname"))
    def route_pages(pathname):
        if pathname in (None, "", "/"):
            return home_layout()
        if pathname == "/pregunta-1":
            return question1_menu_layout()
        if pathname == "/pregunta-1/estrato":
            return _page_p1_estrato()
        if pathname == "/pregunta-1/padres":
            return _page_p1_padres()
        if pathname == "/pregunta-1/cuartos-personas":
            return _page_p1_cuartos()
        if pathname == "/pregunta-2":
            return _placeholder_layout("Pregunta 2")
        if pathname == "/pregunta-3":
            return _placeholder_layout("Pregunta 3")
        return _placeholder_layout("404 - Página no encontrada")