from dash import Dash, html, dcc
from datos.cargar_datos import load_data
from datos.transformaciones import build_summary_tables
from datos.transformaciones_p2 import build_p2_tables
from datos.transformaciones_p3 import build_p3_tables
from callbacks.router import register_router_callbacks
from callbacks.pregunta_1_callback import register_question1_callbacks
from callbacks.pregunta_2_callback import register_question2_callbacks
from callbacks.pregunta_3_callback import register_question3_callbacks

app = Dash(__name__, suppress_callback_exceptions=True)
app.title = "Resultados Saber 11 - Santander"
server = app.server

# Se cargan los datos una sola vez
df_p1, df_p2, df_p3 = load_data()
gp_est, gp_mad, gp_pad, gp_cond = build_summary_tables(df_p1)
gp_mun, gp_gap_ur, gp_gap_of, municipios= build_p2_tables(df_p2)
p3 = build_p3_tables(df_p3)


# Guardamos dataframes en app.server.config para acceso en callbacks
app.server.config["DF"] = df_p1
app.server.config["GP_EST"] = gp_est
app.server.config["GP_MAD"] = gp_mad
app.server.config["GP_PAD"] = gp_pad
app.server.config["GP_COND"] = gp_cond
app.server.config["DF_P2"] = df_p2
app.server.config["Q2_GP_MUN"] = gp_mun
app.server.config["Q2_GP_UR"] = gp_gap_ur
app.server.config["Q2_GP_OF"] = gp_gap_of
app.server.config["Q2_MUNICIPIOS"] = municipios
app.server.config["DF3"]= df_p3
app.server.config["Q3"] = p3

# Layout base
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),

    # Store para selección actual de la Pregunta 1
    dcc.Store(id="store-q1-selection", storage_type="session"),
    # Store para selección actual de la Pregunta 2
    dcc.Store(id="store-q2-selection", storage_type="session"),
    # Store para selección actual de la Pregunta 3
    dcc.Store(id="store-q3-selection", storage_type="session"),

    html.Div(id="page-content")
])

# Registrar callbacks

register_router_callbacks(app)
register_question1_callbacks(app)
register_question2_callbacks(app)
register_question3_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)