from dash import Dash, html, dcc
from datos.cargar_datos import load_data
from datos.transformaciones import build_summary_tables
from callbacks.router import register_router_callbacks
from callbacks.pregunta_1_callback import register_question1_callbacks


# =====================================
# Crear aplicación
# =====================================

def create_app():
    app = Dash(
        __name__,
        suppress_callback_exceptions=True,
        title="Resultados Saber 11 - Santander"
    )

    # ==============================
    # Cargar datos UNA sola vez
    # ==============================
    df = load_data()
    gp_est, gp_mad, gp_pad, gp_cond = build_summary_tables(df)

    # Guardar en memoria del servidor
    app.server.config.update({
        "DF": df,
        "GP_EST": gp_est,
        "GP_MAD": gp_mad,
        "GP_PAD": gp_pad,
        "GP_COND": gp_cond
    })

    # ==============================
    # Layout
    # ==============================
    app.layout = build_layout()

    # ==============================
    # Registrar callbacks
    # ==============================
    register_router_callbacks(app)
    register_question1_callbacks(app)

    return app


# =====================================
# Layout base
# =====================================

def build_layout():
    return html.Div(
        className="background",
        children=[

            dcc.Location(id="url", refresh=False),
            dcc.Store(id="store-q1-selection", storage_type="session"),

            html.Div(
                className="main-container",
                children=[

                    html.H1(
                        "Resultados Saber 11 - Santander",
                        className="main-title"
                    ),

                    html.P(
                        "Análisis interactivo de desempeño académico",
                        className="subtitle"
                    ),

                    html.Hr(),

                    html.Div(
                        id="page-content",
                        className="page-content"
                    )
                ]
            )
        ]
    )


# =====================================
# Ejecutar servidor
# =====================================

app = create_app()
server = app.server

if __name__ == "__main__":
    app.run(debug=True)