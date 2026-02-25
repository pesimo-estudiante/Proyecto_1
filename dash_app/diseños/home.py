from dash import html, dcc
from user_interface.estilos import box_style, button_style
from user_interface.componentes import layout_shell, footer_signature

def home_layout():
    return layout_shell([
        html.Div(
            [
                html.H1("Resultados Saber 11", style={"margin": "4px 0", "fontSize": "28px"}),
                html.H2("Departamento de Santander", style={"margin": "4px 0", "fontSize": "24px", "fontWeight": "500"}),
            ],
            style={**box_style(height="130px"), "display": "flex", "flexDirection": "column", "justifyContent": "center"}
        ),

        html.Div("Para empezar, seleccione una de las preguntas dando clic sobre ella",
                 style={"margin": "20px 4px", "fontSize": "16px"}),

        html.Div(
            [
                dcc.Link(html.Div("Pregunta 1", style=button_style()), href="/pregunta-1"),
                dcc.Link(html.Div("Pregunta 2", style=button_style()), href="/pregunta-2"),
                dcc.Link(html.Div("Pregunta 3", style=button_style()), href="/pregunta-3"),
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