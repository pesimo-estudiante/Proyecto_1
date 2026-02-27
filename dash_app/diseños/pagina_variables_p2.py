# layouts/question2_variable_pages.py
from dash import html, dcc
from user_interface.estilos import box_style
from user_interface.componentes import layout_shell, footer_signature, nav_top, selection_badge

def diseño_variable_p2(title, main_graph_id, hist_graph_id, dropdown_id, slider_id, selection_id, clear_btn_id):
    return layout_shell([
        nav_top(show_home=True, back_href="/pregunta-2"),

        html.Div(
            title,
            style={**box_style(height="70px"), "display":"flex","justifyContent":"center","alignItems":"center","fontSize":"20px"}
        ),

        html.Div(
            "Utilice la barra lateral para desplazarse a través del gráfico",
            style={"margin": "14px 4px 6px 4px", "fontSize": "16px"}
        ),

        html.Div(
            [
                # Controles
                html.Div(
                    [
                        html.Div("Barra para desplazarse por el gráfico", style={"fontSize": "14px", "marginBottom": "6px"}),
                        dcc.Slider(
                            id=slider_id,
                            min=0,
                            max=0,         
                            step=1,
                            value=0,
                            updatemode="drag"
                        ),

                        html.Div(style={"height":"16px"}),

                        html.Div("Buscar municipio", style={"fontSize": "14px", "marginBottom": "6px"}),
                        dcc.Dropdown(
                            id=dropdown_id,
                            options=[],
                            value=None,
                            clearable=True,
                            searchable=True,
                            placeholder="Escriba para buscar..."
                        ),
                    ],
                    style={"flex":"0 0 360px", "padding":"8px", "boxSizing":"border-box"}
                ),

                # Gráfica principal
                html.Div(
                    dcc.Graph(id=main_graph_id, config={"displayModeBar": False}),
                    style={"flex":"1", "padding":"8px", "boxSizing":"border-box"}
                )
            ],
            style={
                "display":"flex",
                "gap":"10px",
                "alignItems":"stretch"
            }
        ),

        # Selección + limpiar
        html.Div(
            [
                html.Div(id=selection_id, children=selection_badge("Sin selección")),
                html.Button("Limpiar selección", id=clear_btn_id, n_clicks=0, style={"marginLeft": "8px"})
            ],
            style={"display":"flex", "alignItems":"center", "gap":"8px", "margin":"10px 4px 12px 4px"}
        ),

        html.Div(
            dcc.Graph(id=hist_graph_id, config={"displayModeBar": False}),
            style=box_style(padding="8px")
        ),

        footer_signature()
    ])