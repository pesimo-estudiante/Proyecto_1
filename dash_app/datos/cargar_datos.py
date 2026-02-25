import pandas as pd

def load_data():
    df = pd.read_csv(r"C:/Users/pinil/OneDrive/Escritorio/Proyecto__1/Proyecto_1/dash_app/datos/data_sample.csv")
    return df