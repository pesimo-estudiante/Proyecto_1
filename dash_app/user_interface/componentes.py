from dash import html, dcc
from user_interface.estilos import COLORS, BASE_FONT, small_button_style

def nav_top(show_home=True, back_href=None):
    buttons = []
    if show_home:
        buttons.append(dcc.Link(html.Button("Inicio", style=small_button_style()), href="/"))
    if back_href:
        buttons.append(dcc.Link(html.Button("Volver", style=small_button_style()), href=back_href))
    return html.Div(buttons, style={"marginBottom": "10px"})

def footer_signature():
    return html.Div(
        "Desarrollado por: Alison - Jairo - Nicolas",
        style={"textAlign": "right", "marginTop": "12px", "fontSize": "14px"}
    )

def layout_shell(content):
    return html.Div(
        [
            html.Div(
                content,
                style={
                    "maxWidth": "1180px",
                    "margin": "14px auto",
                    "padding": "12px",
                    "border": f"2px solid {COLORS['border']}",
                    "backgroundColor": COLORS["bg"],
                    **BASE_FONT
                }
            )
        ],
        style={"backgroundColor": "#dddddd", "minHeight": "100vh", "padding": "6px"}
    )

def selection_badge(text="Sin selección"):
    return html.Div(
        text,
        style={
            "padding": "8px 10px",
            "border": f"1px solid {COLORS['border']}",
            "backgroundColor": "#ffffff",
            "display": "inline-block",
            "fontSize": "14px",
            "marginBottom": "8px"
        }
    )