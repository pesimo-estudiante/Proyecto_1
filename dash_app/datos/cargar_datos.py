import pandas as pd

def load_data():
    df = pd.read_csv(r"C:\Users\ching\OneDrive\Documentos\Maestría\Analítica computacional para la toma de decisiones\Proyecto_1\dash_app\datos\data_sample.csv")
    return df