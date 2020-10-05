import pandas as pd
import numpy as np

def generate_table(file):
    date = file[-9:]
    Tabla = pd.read_csv(file, index_col = "county_name")
    Tabla.columns = ['Prevalencia', 'Tasa %', 'R_e', 'Activos', 'Probables',
           'Mortalidad', 'Viajes', 'Movilidad']
    Probables = Tabla['Probables'].copy()
    print(Probables.apply(lambda x: x.split('~')) )

    Tabla.drop('Probables', axis= 'columns', inplace = True)
    #Cambiar caracteres
    Tabla = Tabla.apply(lambda x: x.astype(str).str.replace(',','.'))
    Tabla = Tabla.apply(lambda x: x.astype(str).str.replace('ND','0'))
    Tabla = Tabla.apply(lambda x: x.astype(str).str.replace('%',''))
    print(Tabla)

    # Pasar de string a float
    columns = Tabla.columns
    for column in columns:

        Tabla[column] = pd.to_numeric(Tabla[column])

    #Renombrar columna
    Tabla = Tabla.rename(columns={'Tasa': 'Tasa %'})
    print(date)
    Tabla.to_csv('Tables/Tabla_'+date)

if __name__ == "__main__":
    generate_table("display_22_09.csv")
