"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""

import pandas as pd
import numpy as np
import os
import re
import nltk

def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    input_path = "files/input/solicitudes_de_credito.csv"
    df = pd.read_csv(input_path, sep=";", index_col=0, encoding="utf-8")
    #df = df.copy()

    df['sexo']=df['sexo'].str.lower().str.strip()
    df['tipo_de_emprendimiento']=df['tipo_de_emprendimiento'].str.lower().str.strip()
    df['idea_negocio']=df['idea_negocio'].str.replace('-',' ').str.replace('_',' ').str.lower().str.strip()
    df['barrio']=df['barrio'].str.replace('-',' ').str.replace('_',' ').str.lower()
    df['barrio'] = df['barrio'].str.replace(r'no\.\s*(\d+)', r'no\1', regex=True)
    df['estrato']=df['estrato'].astype(int)
    df['comuna_ciudadano']=df['comuna_ciudadano'].astype(int)

    from datetime import datetime

    def parse_date(date_str):
        for fmt in ('%d/%m/%Y', '%Y/%m/%d', '%Y/%d/%m'):
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                pass
        return None

    df['fecha_de_beneficio'] = df['fecha_de_beneficio'].apply(parse_date)
    df['fecha_de_beneficio'] = df['fecha_de_beneficio'].dt.strftime('%d/%m/%Y')

    df['monto_del_credito']=df['monto_del_credito'].replace({'\$':'',',':'',' ':''},regex=True).astype(float)
    df['línea_credito']=df['línea_credito'].str.replace('-',' ').str.replace('_',' ').str.lower().str.strip()

    df.dropna(inplace=True)    
    df.drop_duplicates(inplace=True)  

    output_path = "files/output/solicitudes_de_credito.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, sep=";", index=False, encoding="utf-8")

    #INTENTO 1
    # stemmer = nltk.PorterStemmer()

    # def create_normalized_key(df, col):
    #     """
    #     Crea una nueva columna 'key_<col>' a partir de df[col].
    #     Normaliza el texto para generar una clave única (firma textual).
    #     """
    #     df = df.copy()

    #     df[f"key_{col}"] = (
    #         df[col]
    #         .astype(str)
    #         .str.strip()
    #         .str.lower()
    #         .str.replace("-", " ", regex=False)
    #     )

    #     df[f"key_{col}"] = df[f"key_{col}"].str.replace(r"[^a-z0-9\s]", " ", regex=True)

    #     # Tokenizar, aplicar stemming y eliminar duplicados
    #     df[f"key_{col}"] = df[f"key_{col}"].str.split()
    #     df[f"key_{col}"] = df[f"key_{col}"].apply(
    #         lambda tokens: sorted(set(stemmer.stem(w) for w in tokens))
    #     )
    #     df[f"key_{col}"] = df[f"key_{col}"].str.join(" ")

    #     return df
    
    # def generate_cleaned_text(df, col):
    #     temp = df.copy()
    #     temp = temp.sort_values(by=[f"key_{col}", col])
    #     temp = temp.drop_duplicates(subset=f"key_{col}", keep="first")

    #     mapping = dict(zip(temp[f"key_{col}"], temp[col]))
    #     df[f"clean_{col}"] = df[f"key_{col}"].map(mapping)

    #     return df


    # # 1. Leer el archivo
    # input_path = "files/input/solicitudes_de_credito.csv"
    # output_path = "files/output/solicitudes_de_credito.csv"
    # os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # df = pd.read_csv(input_path, sep=";", encoding="utf-8")
    # df = df.copy()

    # # 2. Eliminar filas con datos faltantes
    # df = df.dropna()

    # # 4. Limpieza de sexo y tipo de emprendimiento
    # df["sexo"] = (df["sexo"].astype(str).str.strip().str.lower())
    # df["tipo_de_emprendimiento"] = (df["tipo_de_emprendimiento"].astype(str).str.strip().str.lower())

    # # 5. Limpieza de monto del crédito, comuna y estrato
    # df["monto_del_credito"] = (
    #     df["monto_del_credito"]
    #     .astype(str)
    #     .str.strip()
    #     .str.replace(r"[^\d,\.]", "", regex=True) #quitar cualquier símbolo que no sea dígito, coma o punto
    #     .str.replace(",", "", regex=False)  #quitar separador de miles 
    #     .replace("", np.nan)
    #     .astype(float)
    # )
    # # Limpieza fecha de beneficio
    # from datetime import datetime

    # def parse_date(date_str):
    #     for fmt in ('%d/%m/%Y', '%Y/%m/%d', '%Y/%d/%m'):
    #         try:
    #             return datetime.strptime(date_str, fmt)
    #         except ValueError:
    #             pass
    #     return np.nan
    
    # df["fecha_de_beneficio"] = df["fecha_de_beneficio"].apply(parse_date)
    # df['fecha_de_beneficio'] = df['fecha_de_beneficio'].dt.strftime('%d/%m/%Y')


    # # 6. Limpieza de idea negocio, barrio y línea de crédito
    # text_cols_for_key = [c for c in ["idea_negocio", "barrio", "línea_credito"] if c in df.columns]
    # for col in text_cols_for_key:
    #     df = create_normalized_key(df, col)
    #     df = generate_cleaned_text(df, col)
    #     df[col] = df[f"clean_{col}"]

    # # 7. Quitar columnas auxiliares (key_ y clean_)
    # df = df[[c for c in df.columns if not c.startswith("key_") and not c.startswith("clean_")]]

    # # Eliminar columnas con datos faltantes 
    # df = df.dropna()

    # # Eliminar duplicados exactos
    # df = df.drop_duplicates()

    # # 8. Guardar resultado  
    # df.to_csv(output_path, sep=";", index=False, encoding="utf-8")

    # return df

pregunta_01()
