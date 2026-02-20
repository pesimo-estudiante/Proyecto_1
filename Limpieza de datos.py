import pandas as pd
import numpy as np

df = pd.read_csv("C:/Users/pinil/OneDrive/Escritorio/Analitica computacional/Proyecto/subconjunto.csv")

#Info sin limpiar 
df.info()
df.isna().sum()

#Eliminar datos que no tiene valor en puntaje global
df = df.dropna(subset=["punt_global"])

#Se verifica
df.isna().sum()

#Si esta vacio por No reporta, como otra categoria
cols_cat = [
    "fami_estratovivienda",
    "fami_tienecomputador",
    "fami_tieneinternet"
]

df[cols_cat] = df[cols_cat].fillna("NO REPORTA")

#Se muestra que no hay errores
df.isna().sum()

#Se crea el nuevo archivo csv para trabajar
df.to_csv("C:/Users/pinil/OneDrive/Escritorio/Analitica computacional/Proyecto//saber11_santander_clean.csv", index=False)