from dash import Dash, html, dcc
from datos.cargar_datos import load_data
from datos.transformaciones import build_summary_tables
from callbacks.router import register_router_callbacks
from callbacks.pregunta_1_callback import register_question1_callbacks

app = Dash(__name__, suppress_callback_exceptions=True)
app.title = "Resultados Saber 11 - Santander"
server = app.server


# Se cargan los datos una sola vez
df = load_data()
gp_est, gp_mad, gp_pad, gp_cond = build_summary_tables(df)

# Guardamos dataframes en app.server.config para acceso en callbacks
app.server.config["DF"] = df
app.server.config["GP_EST"] = gp_est
app.server.config["GP_MAD"] = gp_mad
app.server.config["GP_PAD"] = gp_pad
app.server.config["GP_COND"] = gp_cond


# Layout base
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),

    # Store para selección actual de la Pregunta 1
    dcc.Store(id="store-q1-selection", storage_type="session"),

    html.Div(id="page-content")
])

# Registrar callbacks

register_router_callbacks(app)
register_question1_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)