from pathlib import Path
import pandas as pd

HERE= Path(__file__).resolve().parent
ROOT= HERE.parent.parent

def load_data():
    path_p1= HERE/"data_sample.csv"
    path_p2= ROOT/"saber11_pregunta_2.csv"
    path_p3= ROOT/"saber11_pregunta_3.csv"
    df1 = pd.read_csv(path_p1)
    df2 = pd.read_csv(path_p2)
    df3 = pd.read_csv(path_p3)
    return df1, df2, df3