from dash import html, dcc
from user_interface.estilos import box_style
from user_interface.componentes import layout_shell, footer_signature, nav_top, selection_badge

def variable_page_layout(title, subtitle, main_graph_id, hist_graph_id, selection_text_id, clear_btn_id):
    return layout_shell([
        nav_top(show_home=True, back_href="/pregunta-1"),

        html.Div(
            title,
            style={**box_style(height="70px"), "display":"flex","justifyContent":"center","alignItems":"center","fontSize":"20px"}
        ),

        html.Div(subtitle, style={"margin": "18px 4px 8px 4px", "fontSize": "16px"}),

        dcc.Graph(id=main_graph_id, config={"displayModeBar": False}),

        html.Div([
            html.Div(id=selection_text_id, children=selection_badge("Sin selección")),
            html.Button("Limpiar selección", id=clear_btn_id, n_clicks=0, style={"marginLeft": "8px"})
        ], style={"display": "flex", "alignItems": "center", "gap": "8px", "margin": "8px 4px 14px 4px"}),

        html.Div(
            dcc.Graph(id=hist_graph_id, config={"displayModeBar": False}),
            style=box_style(height=None, padding="8px")
        ),

        footer_signature()
    ])