import pandas as pd
import psycopg2


df = pd.read_excel("septiembre2025.xlsx")


df = df.rename(columns={
    "Nº (ORDEN)": "id_orden",
    "FECHA": "fecha_registro",
    "HORA": "hora_registro",
    "DIRECCIÓN DE LA INFRACCIÓN": "direccion",
    "LATITUD (X)": "latitud",   
    "LONGITUD (Y)": "longitud",     
    "ZONA (SEGÚN SENPLADES)": "zona",
    "PROVINCIA": "provincia",
    "CANTÓN": "canton",
    "DISTRITO": "distrito",
    "CIRCUITO": "circuito",
    "SUBCIRCUITO": "subcircuito",
    "PARROQUIA": "parroquia",
    "Tipo de delito": "tipo_delito",
    "Subtipo_de_delito (pj)": "subtipo_delito",
    "DELITO DNPJ": "delito_dnpj",
    "CODIGO PENAL (DELITOS)": "codigo_penal",
    "MODALIDAD (MODUS OPERANDI)": "modalidad"
})


df['id_orden'] = df['id_orden'].astype('Int64') 
df['id_orden'] = df['id_orden'].fillna(0).astype(int)  

df['latitud'] = df['latitud'].astype(str).str.replace(" ", "").str.replace(",", ".")
df['longitud'] = df['longitud'].astype(str).str.replace(" ", "").str.replace(",", ".")


df['latitud'] = df['latitud'].astype(float)
df['longitud'] = df['longitud'].astype(float)

df = df[(df['latitud'] >= -90) & (df['latitud'] <= 90)]
df = df[(df['longitud'] >= -180) & (df['longitud'] <= 180)]


df.to_csv("temp.csv", index=False, header=True, quoting=1)


conn = psycopg2.connect(
    dbname="",
    user="postgres",
    password="",
    host="",
    port=""
)
cur = conn.cursor()


with open("temp.csv", "r", encoding="utf-8") as f:
    next(f)  
    cur.copy_expert("""
    COPY detalle (
        id_orden, fecha_registro, hora_registro, direccion,
        latitud, longitud, zona, provincia, canton, distrito,
        circuito, subcircuito, parroquia, tipo_delito, subtipo_delito,
        delito_dnpj, codigo_penal, modalidad
    )
    FROM STDIN WITH CSV HEADER
    """, f)

conn.commit()
cur.close()
conn.close()