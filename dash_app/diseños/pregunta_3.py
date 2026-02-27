# layouts/question3.py
from dash import html, dcc
from user_interface.estilos import box_style, button_style
from user_interface.componentes import layout_shell, footer_signature, nav_top

def question3_menu_layout():
    titulo = ("¿Existen diferencias significativas en los resultados de las Pruebas Saber 11 entre estudiantes "
              "con y sin acceso a computador e internet en el hogar, y qué tan asociadas están estas diferencias "
              "a otras características socioeconómicas y educativas?")

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
                dcc.Link(html.Div("Acceso tecnológico por municipio y tecnología", style=button_style()),
                         href="/pregunta-3/municipio-tecnologia"),

                dcc.Link(html.Div("Brecha digital por municipio", style=button_style()),
                         href="/pregunta-3/brecha-digital"),

                dcc.Link(html.Div("Desempeño por área académica según acceso tecnológico", style=button_style()),
                         href="/pregunta-3/desempeno-area"),
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