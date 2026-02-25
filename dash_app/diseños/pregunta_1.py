from dash import html, dcc
from user_interface.estilos import box_style, button_style
from user_interface.componentes import layout_shell, footer_signature, nav_top

def question1_menu_layout():
    titulo = (
        "¿Qué grupos estudiantiles deberían ser el foco de la inversión educativa "
        "para mejorar los resultados nacionales de las Pruebas Saber Pro, "
        "considerando las disparidades asociadas a las condiciones económicas y familiares?"
    )

    return layout_shell([
        nav_top(show_home=True, back_href="/"),

        html.Div(
            html.Div(titulo, style={"fontSize": "20px", "lineHeight": "1.45", "textAlign": "center"}),
            style=box_style(height="150px", padding="18px")
        ),

        html.Div("Seleccione una variable para revisar el análisis",
                 style={"margin": "18px 4px", "fontSize": "16px"}),

        html.Div(
            [
                dcc.Link(html.Div("Por Estrato Familiar", style=button_style()), href="/pregunta-1/estrato"),
                dcc.Link(html.Div("Por Nivel de educación Padres", style=button_style()), href="/pregunta-1/padres"),
                dcc.Link(html.Div("Por Cuartos/ Personas que conviven en el hogar", style=button_style()), href="/pregunta-1/cuartos-personas"),
            ],
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(3, 1fr)",
                "gap": "80px",
                "padding": "0 80px"
            }
        ),

        footer_signature()
    ])