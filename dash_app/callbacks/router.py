from dash import Output, Input, html
from diseños.home import home_layout
from diseños.pregunta_1 import question1_menu_layout
from diseños.pregunta_2 import question2_menu_layout
from diseños.pregunta_3 import question3_menu_layout
from diseños.paginas_variables import diseño_variable_p1
from diseños.pagina_variables_p2 import diseño_variable_p2
from diseños.pagina_variables_p3 import diseño_p3_2_checklist, diseño_p3_slider_checklist
from user_interface.componentes import layout_shell, nav_top, footer_signature


def _placeholder_layout(title):
    return layout_shell([
        nav_top(show_home=True, back_href="/"),
        html.Div(title, style={"fontSize": "24px", "marginBottom": "12px"}),
        html.Div("Esta sección está en construcción."),
        footer_signature()
    ])

def _page_p1_estrato():
    return diseño_variable_p1(
        title="Estrato Familiar",
        subtitle="Para visualizar el histograma de un estrato específico, dé clic sobre la barra correspondiente.",
        main_graph_id="graph-estrato-main",
        hist_graph_id="graph-estrato-hist",
        selection_text_id="txt-estrato-selection",
        clear_btn_id="btn-clear-estrato"
    )

def _page_p1_padres():
    return diseño_variable_p1(
        title="Educación Padres",
        subtitle="Para visualizar el histograma de un nivel académico específico, dé clic sobre el punto correspondiente.",
        main_graph_id="graph-padres-main",
        hist_graph_id="graph-padres-hist",
        selection_text_id="txt-padres-selection",
        clear_btn_id="btn-clear-padres"
    )

def _page_p1_cuartos():
    return diseño_variable_p1(
        title="Cuartos/Personas que conviven en el hogar",
        subtitle="Para visualizar el histograma de una categoría específica, dé clic sobre la barra correspondiente.",
        main_graph_id="graph-cuartos-main",
        hist_graph_id="graph-cuartos-hist",
        selection_text_id="txt-cuartos-selection",
        clear_btn_id="btn-clear-cuartos"
    )

def _page_p2_municipio():
    return diseño_variable_p2(
        title="Puntaje promedio por municipio",
        main_graph_id="q2-mun-main",
        hist_graph_id="q2-mun-hist",
        dropdown_id="q2-mun-dd",
        slider_id="q2-mun-slider",
        selection_id="q2-mun-selection",
        clear_btn_id="q2-mun-clear"
    )

def _page_p2_rural_urbano():
    return diseño_variable_p2(
        title="Brecha Urbano-Rural por municipio",
        main_graph_id="q2-ur-main",
        hist_graph_id="q2-ur-hist",
        dropdown_id="q2-ur-dd",
        slider_id="q2-ur-slider",
        selection_id="q2-ur-selection",
        clear_btn_id="q2-ur-clear"
    )

def _page_p2_oficial_nooficial():
    return diseño_variable_p2(
        title="Brecha Oficial-No oficial por municipio",
        main_graph_id="q2-of-main",
        hist_graph_id="q2-of-hist",
        dropdown_id="q2-of-dd",
        slider_id="q2-of-slider",
        selection_id="q2-of-selection",
        clear_btn_id="q2-of-clear"
    )

def _page_p3_municipio_tecnologia():
    return diseño_p3_slider_checklist(
        title="Puntaje promedio por municipio y acceso tecnológico",
        main_graph_id="q3-mt-main",
        slider_id="q3-mt-slider",
        dropdown_id="q3-mt-dd",
        tech_check_id="q3-mt-tech",
        selection_id="q3-mt-selection",
        hist_graph_id="q3-mt-hist",
        clear_btn_id="q3-mt-clear",
    )

def _page_p3_brecha_digital():
    return diseño_p3_slider_checklist(
        title="Brecha digital por municipio",
        main_graph_id="q3-bd-main",
        slider_id="q3-bd-slider",
        dropdown_id="q3-bd-dd",
        tech_check_id="q3-bd-tech",
        selection_id="q3-bd-selection",
        hist_graph_id="q3-bd-hist",
        clear_btn_id="q3-bd-clear",
    )

def _page_p3_desempeno_area():
    return diseño_p3_2_checklist(
        title="Desempeño por área académica según acceso tecnológico",
        main_graph_id="q3-da-main",
        area_check_id="q3-da-area",
        tech_check_id="q3-da-tech",
        selection_id="q3-da-selection",
        hist_graph_id="q3-da-hist",
        clear_btn_id="q3-da-clear",
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
            return question2_menu_layout()
        if pathname == "/pregunta-2/municipio":
            return _page_p2_municipio()
        if pathname == "/pregunta-2/rural-urbano":
            return _page_p2_rural_urbano()
        if pathname == "/pregunta-2/oficiales-nooficiales":
            return _page_p2_oficial_nooficial()
        if pathname == "/pregunta-3":
            return question3_menu_layout()
        if pathname == "/pregunta-3/municipio-tecnologia":
            return _page_p3_municipio_tecnologia()
        if pathname == "/pregunta-3/brecha-digital":
            return _page_p3_brecha_digital()
        if pathname == "/pregunta-3/desempeno-area":
            return _page_p3_desempeno_area()