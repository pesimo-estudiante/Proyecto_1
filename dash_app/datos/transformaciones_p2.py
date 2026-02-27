# data/transforms_q2.py
import pandas as pd


COL_PUNT = "punt_global"
COL_MUN = "cole_mcpio_ubicacion"         
COL_ZONA = "cole_area_ubicacion"         
COL_NAT = "cole_naturaleza"         

VAL_URB = "URBANO"
VAL_RUR = "RURAL"
VAL_OFI = "OFICIAL"
VAL_NOF = "NO OFICIAL"
# ===========================================

def _normalize_text(s: pd.Series) -> pd.Series:
    return s.astype(str).str.strip()

def build_p2_tables(df: pd.DataFrame):
    """
    Retorna:
      - gp_mun: promedio por municipio (para opción 1)
      - gp_gap_ur: brecha URBANO - RURAL por municipio (opción 2)
      - gp_gap_of: brecha OFICIAL - NO OFICIAL por municipio (opción 3)
      - municipios: lista ordenada de municipios (para dropdown/slider)
    """

    d = df.copy()

    # Normalizar texto
    d[COL_MUN] = _normalize_text(d[COL_MUN])
    d[COL_ZONA] = _normalize_text(d[COL_ZONA])
    d[COL_NAT] = _normalize_text(d[COL_NAT])

    # -----------------------------
    # (1) Puntaje promedio por municipio
    # -----------------------------
    gp_mun = (
        d.groupby(COL_MUN, dropna=False)
        .agg(
            promedio=(COL_PUNT, "mean"),
            desvest=(COL_PUNT, "std"),
            n=(COL_PUNT, "size")
        )
        .reset_index()
        .sort_values("promedio", ascending=False)
        .rename(columns={COL_MUN: "municipio"})
    )
    gp_mun["cv"] = gp_mun["desvest"] / gp_mun["promedio"]

    # -----------------------------
    # (2) Brecha Urbano - Rural por municipio
    # -----------------------------
    piv_zona = (
        d.pivot_table(index=COL_MUN, columns=COL_ZONA, values=COL_PUNT, aggfunc="mean")
        .reset_index()
        .rename(columns={COL_MUN: "municipio"})
    )

    # gap = urbano - rural (si falta alguna categoría, quedará NaN)
    if VAL_URB in piv_zona.columns and VAL_RUR in piv_zona.columns:
        piv_zona["gap_urb_rur"] = piv_zona[VAL_URB] - piv_zona[VAL_RUR]
    else:
        piv_zona["gap_urb_rur"] = pd.NA

    gp_gap_ur = piv_zona[["municipio", "gap_urb_rur"]].sort_values("gap_urb_rur", ascending=False)

    # -----------------------------
    # (3) Brecha Oficial - No oficial por municipio
    # -----------------------------
    piv_nat = (
        d.pivot_table(index=COL_MUN, columns=COL_NAT, values=COL_PUNT, aggfunc="mean")
        .reset_index()
        .rename(columns={COL_MUN: "municipio"})
    )

    if VAL_OFI in piv_nat.columns and VAL_NOF in piv_nat.columns:
        piv_nat["gap_ofi_nof"] = piv_nat[VAL_OFI] - piv_nat[VAL_NOF]
    else:
        piv_nat["gap_ofi_nof"] = pd.NA

    gp_gap_of = piv_nat[["municipio", "gap_ofi_nof"]].sort_values("gap_ofi_nof", ascending=False)

    # Lista ordenada de municipios (la usamos para slider y dropdown)
    municipios = gp_mun["municipio"].tolist()

    return gp_mun, gp_gap_ur, gp_gap_of, municipios