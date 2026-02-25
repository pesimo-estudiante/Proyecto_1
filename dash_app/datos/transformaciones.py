import pandas as pd

ORDER_ESTRATO = ["Estrato 1", "Estrato 2", "Estrato 3", "Estrato >=4"]
ORDER_EDU = [
    "Ninguno", "Primaria", "No sabe", "Bachiller",
    "Tecnico/Tecnologico", "Profesional", "Postgrado"
]

def build_summary_tables(df_input: pd.DataFrame):
    gp_est = (
        df_input.groupby("Fami_Estrato", dropna=False)
        .agg(promedio=("PUNT_GLOBAL", "mean"), desvest=("PUNT_GLOBAL", "std"))
        .reset_index()
    )
    gp_est["cv"] = gp_est["desvest"] / gp_est["promedio"]
    gp_est["Fami_Estrato"] = pd.Categorical(gp_est["Fami_Estrato"], categories=ORDER_ESTRATO, ordered=True)
    gp_est = gp_est.sort_values("Fami_Estrato")

    gp_mad = (
        df_input.groupby("_educacion_MADRE", dropna=False)
        .agg(promedio=("PUNT_GLOBAL", "mean"), desvest=("PUNT_GLOBAL", "std"))
        .reset_index()
    )
    gp_mad["cv"] = gp_mad["desvest"] / gp_mad["promedio"]
    gp_mad["_educacion_MADRE"] = pd.Categorical(gp_mad["_educacion_MADRE"], categories=ORDER_EDU, ordered=True)
    gp_mad = gp_mad.sort_values("_educacion_MADRE")

    gp_pad = (
        df_input.groupby("_educacion_PADRE", dropna=False)
        .agg(promedio=("PUNT_GLOBAL", "mean"), desvest=("PUNT_GLOBAL", "std"))
        .reset_index()
    )
    gp_pad["cv"] = gp_pad["desvest"] / gp_pad["promedio"]
    gp_pad["_educacion_PADRE"] = pd.Categorical(gp_pad["_educacion_PADRE"], categories=ORDER_EDU, ordered=True)
    gp_pad = gp_pad.sort_values("_educacion_PADRE")

    gp_cond = (
        df_input.groupby("cond_est", dropna=False)
        .agg(promedio=("PUNT_GLOBAL", "mean"), desvest=("PUNT_GLOBAL", "std"))
        .reset_index()
        .sort_values("promedio")
    )
    gp_cond["cv"] = gp_cond["desvest"] / gp_cond["promedio"]

    return gp_est, gp_mad, gp_pad, gp_cond