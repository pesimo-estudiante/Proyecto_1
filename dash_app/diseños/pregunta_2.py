from dash import html, dcc
from user_interface.estilos import box_style, button_style
from user_interface.componentes import layout_shell, footer_signature, nav_top

def question2_menu_layout():
    titulo = (
        "¿Existen diferencias significativas en el desempeño académico entre los"
        "municipios del departamento de Santander, y en qué medida estas diferencias"
        "podrían estar asociadas a características institucionales como naturaleza "
        "del colegio y ubicación rural o urbana?"
    )

    return layout_shell([
        nav_top(show_home=True, back_href="/"),

        html.Div(
            html.Div(titulo, style={"fontSize": "20px", "lineHeight": "1.45", "textAlign": "center"}),
            style=box_style(height="150px", padding="18px")
        ),

        html.Div("Seleccione el tipo de análisis que quiere revisar",
                 style={"margin": "18px 4px", "fontSize": "16px"}),

        html.Div(
            [
                dcc.Link(html.Div("Puntaje promedio por Municipio", style=button_style()), href="/pregunta-2/municipio"),
                dcc.Link(html.Div("Brecha rural vs urbano ", style=button_style()), href="/pregunta-2/rural-urbano"),
                dcc.Link(html.Div("Colegios oficiales vs no oficiales", style=button_style()), href="/pregunta-2/oficiales-nooficiales"),
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