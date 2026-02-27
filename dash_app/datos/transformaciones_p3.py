import pandas as pd
import numpy as np

COL_MUN = "cole_mcpio_ubicacion"          
COL_PUNT_GLOBAL = "punt_global"


TECH_COLS = {
    "Computador": "fami_tienecomputador",   
    "Internet": "fami_tieneinternet"        
}

AREA_SCORE_COLS = {
    "Lectura crítica": "punt_lectura_critica",
    "Matemáticas": "punt_matematicas",
    "C. Naturales": "punt_c_naturales",
    "Sociales": "punt_sociales_ciudadanas",
    "Inglés": "punt_ingles"
}
# =======================================================


def build_p3_tables(df: pd.DataFrame):
    d = df.copy()

    # 1) crear ID único por fila (si ya tienes uno real, úsalo)
    d = d.reset_index().rename(columns={"index": "__row_id"})
    d[COL_MUN] = d[COL_MUN].astype(str).str.strip()

    municipios = sorted(d[COL_MUN].dropna().unique().tolist())
    techs = list(TECH_COLS.keys())
    areas = list(AREA_SCORE_COLS.keys())

    # 2) tech_long (a nivel estudiante)
    tech_long_parts = []
    for tech_name, col in TECH_COLS.items():
        if col not in d.columns:
            continue
        tmp = d[["__row_id", COL_MUN, COL_PUNT_GLOBAL, col]].copy()
        tmp["tech"] = tech_name
        tmp["access"] = np.where(tmp[col]== "Si", "Con acceso", "Sin acceso")
        tmp = tmp.drop(columns=[col])
        tech_long_parts.append(tmp)

    tech_long = (
        pd.concat(tech_long_parts, ignore_index=True)
        if tech_long_parts
        else pd.DataFrame(columns=["__row_id", COL_MUN, COL_PUNT_GLOBAL, "tech", "access"])
    )

    # 3) gp_bar (promedio por municipio/tech/access)
    gp_bar = (tech_long.groupby([COL_MUN, "tech", "access"])
                     .agg(promedio=(COL_PUNT_GLOBAL, "mean"), n=(COL_PUNT_GLOBAL, "size"))
                     .reset_index()
                     .rename(columns={COL_MUN: "municipio"}))

    # 4) gp_gap (brecha: con - sin)
    piv = (gp_bar.pivot_table(index=["municipio", "tech"], columns="access", values="promedio", aggfunc="first")
                .reset_index())
    if "Con acceso" in piv.columns and "Sin acceso" in piv.columns:
        piv["gap"] = piv["Con acceso"] - piv["Sin acceso"]
    else:
        piv["gap"] = pd.NA
    gp_gap = piv[["municipio", "tech", "gap"]].copy()

    # 5) area_long (a nivel estudiante)
    area_long_parts = []
    for area_name, col_score in AREA_SCORE_COLS.items():
        if col_score not in d.columns:
            continue
        tmp = d[["__row_id", COL_MUN, col_score]].copy()
        tmp = tmp.rename(columns={COL_MUN: "municipio", col_score: "score"})
        tmp["area"] = area_name
        area_long_parts.append(tmp)

    area_long = (
        pd.concat(area_long_parts, ignore_index=True)
        if area_long_parts
        else pd.DataFrame(columns=["__row_id", "municipio", "score", "area"])
    )
    tech_sel = tech_long[["__row_id", "tech", "access"]].copy()
    area_tech = area_long.merge(tech_sel, on="__row_id", how="left")
    

    return {
        "municipios": municipios,
        "techs": techs,
        "areas": areas,
        "gp_bar": gp_bar,
        "gp_gap": gp_gap,
        "area_tech": area_tech,
        "cfg": {"COL_MUN": COL_MUN, "COL_PUNT_GLOBAL": COL_PUNT_GLOBAL}
    }