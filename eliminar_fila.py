import pandas as pd

# --- Función que Elimina varias Filas del Archivo .CSV Automaticamente al Iniciar el Servidor ---  
def eliminar_fila_csv(nombre_archivo, categorias_a_eliminar):

    # CONDICION QUE VALIDA SI PASAN UN SOLO VALOR, CONVERTIRLO EN LISTA
    if isinstance(categorias_a_eliminar, str):
        categorias_a_eliminar = [categorias_a_eliminar]


    try:
        df = pd.read_csv(nombre_archivo, 
                         sep=";",
                         header=None,            # LEE EL ARCHIVO .CSV COMO TEXTO SIN CABECERAS
                         dtype=str, 
                         encoding="utf-8", 
                         on_bad_lines="skip")   


        if df.empty:
            print(f"\n*** El Archivo  {nombre_archivo}  Esta Vacio ***\n")
            return
        
        #col_index = 3 if df.shape[1] > 3 else df.shape[1] -1

        df[3] = df[3].astype(str).str.strip().str.replace('"', '')   # REVISA COLUMNA ' D '  ( INDICE 3 )
        categorias_a_eliminar = [c.strip().upper() for c in categorias_a_eliminar]  # NORMALIZAMOS LAS CATEGORIAS A ELIMINAR QUITANDO. COMA, ESPACIOS, COMILLAS Y TODO A MAYUSCULAS

        #print(df[3].unique())
        
        df_filtrado = df[~df[3].isin(categorias_a_eliminar) ]  # FILTRA Y QUITA " CUALQUIER CATEGORIA SEA UNA SOLA O VARIAS EN LISTA " 

        df_filtrado.to_csv(nombre_archivo, 
                           sep=";", 
                           index=False,             # SOBRESCRIBIR EL ARCHIVO CSV SIN INDICE NI CABECERA Y CON PUNTO Y COMA (;)
                           header=False, 
                           encoding="utf-8")     

        print(f"\n*** Se Elimino Todas Las Filas Con Categorias {categorias_a_eliminar} De Los Carriles 1,2,3,4 De Peaje De ROZO  ***\n ")

    except Exception as e:
        print(f"\n*** Error Eliminando Fila {categorias_a_eliminar} en {nombre_archivo} : {e} ***\n")

