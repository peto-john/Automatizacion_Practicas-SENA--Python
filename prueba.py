# API CON EL MODULO FastAPI DE PYTHON QUE AUTOMATIZA LA DESCARGA DEL ANISCOPIO EN FORMATO ( SEPARADO POR COMA " .csv ") DE LA PAGINA WEB EasyRoad ( PEAJES )
# ELABORADO POR :   --> CRISTIAN      //      --> JOHN PACHECO

from barra_progreso import barra_progreso # Es una Animacion de Porcentaje de DESCARGA Solo Usando PYTHON
from eliminar_fila import eliminar_fila_csv # IMPORTAMOS MODULO ELIMINAR FILA
from backup import dia_envio_correo  #comprimir_carpeta # IMPORTAMOS MODULO COMPRIMIR CARPETA

from fastapi import FastAPI, Request
from contextlib import asynccontextmanager  # Esta Libreria de fastAPI permite Ejecutar cosas al INICIO ( before yield) y al CIERRE ( after yield)
from datetime import datetime, timedelta # Para manipular la Fecha Actual Y PASADA (AYER) ( AÑO/MES/DIA)
import requests # Importa la librería 'requests' para hacer peticiones HTTP GET, POST, UPDATE, DELETE

# RENDERIZAR PAGINA WEB ( FRONTEND Mediante jinja2 ) CON TEMPLATES Y STATIC 
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import os   # Funciones del Sistema Operativo
import sys  # para usar sys.exit()
import time # PARA QUE EL CMD O TERMINAL ESPERE UN TIMPO ANTES DE SALIR Y USAR ( EL METODO sleep() )


app = FastAPI()


# Ruta absoluta del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Montar carpeta static
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Templates
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


# CONFIGURACION DE LA FECHA
fecha_ayer = datetime.now() - timedelta(days=1)  # FECHA DE AYER /  AÑO/MES/DIA

anio = fecha_ayer.strftime("%Y")  # CON LETRAS MAYUSCULA RETORNA AÑO EN 4 DIGITOS
mes = fecha_ayer.strftime("%m")   # CON LETRAS MINUSCULAS RETORNA MES Y DIA   2 DIGITOS
dia = fecha_ayer.strftime("%d")

# FORMATEO LOS MESES DE NUMEROS A STRING PARA EL NOMBRE DE LAS CARPETAS DEL MES
MESES = {"01" : "ENERO", "02" : "FEBRERO", "03" : "MARZO", "04" : "ABRIL", "05" : "MAYO", "06" : "JUNIO",
         "07" : "JULIO", "08" : "AGOSTO", "09" : "SEPTIEMBRE", "10" : "OCTUBRE", "11" : "NOVIEMBRE", "12" : "DICCIEMBRE"
        }

for m in MESES:
    if m == mes:
        MESES=MESES[m]


# --- Función que Descarga el .CSV Automaticamente al Iniciar el Servidor ---
def descargar_archivo(anio, mes, dia):

    
    login = "http://DOMINIO O IP/easyroad/usuarios/login"  # Variable Con la Ruta de la Pagina Web del Login EasyRoad

    usuario = " USUARIO "
    contrasenas = ["CONTRASEÑA 1" , "CONTRASEÑA 2"]  # Lista de contraseñas a probar

    # Iniciar sesión con varias contraseñas
    login_exitoso = False

    for contrasena in contrasenas:

        sesion = requests.Session() # Iniciar sesion con EasyRoad

        credenciales = {
            "data[Usuarios][username]":usuario,      # Variable con los parametros de la Pagina y Credenciales Tipo Diccionario para hacer Login
            "data[Usuarios][password]":contrasena
        }

        respuesta = sesion.post(login, data=credenciales)   # Inicia la sesion por Metodo POST de la URL login y con el PARAMETRO data manda la VARIABLE con el DIC de las CREDENCIALES

        # Validar el login según el estado y el contenido
        if respuesta.status_code == 200 and ("Cerrar sesión" in respuesta.text or "logout" in respuesta.text):
            print(f"✅ Login exitoso con la contraseña: {contrasena}")
            login_exitoso = True
            break


    if not login_exitoso:
        print("\n[-] Ninguna contraseña funcionó, *** VERIFIQUE CREDENCIALES EN ( EasyRoad ). ***\n")

        # TEMPORIZADOR ANTES DEL CIERRE TOTAL
        for i in range(5, 0, -1):
            print(f"Saliendo en {i} Segundos...", end="\r")
            time.sleep(1)
        sys.exit()
            
    else:
        print("\n[+] Continuando Con La Descarga De Archivos Trafico Aniscopio ...\n")

        # LLAMAMOS A LA FUNCION PARA MOSTARAR LA BARRA DE PROGRESO ( VISUAL )
        barra_progreso()

        # Crear Carpeta Si No Existe por fecha y Ruta para guardar los Archivos Descargados
        carpeta = os.path.join("TraficoAniscopio", anio, MESES , dia)
        os.makedirs(carpeta, exist_ok=True)

        dia = int(dia) # Convertir de Numero String  A  Numero Entero
        
        # Genera el Reporte
        reporte_url = "http://DOMINIO/RUTA-FORM/traficoaniscopio"
        parametros = {
            "_method": "POST",
            "data[CommonReport][diario]": 1,
            "data[CommonReport][Mhora]": 0,
            "data[CommonReport][fechaInicial]": f"{anio}-{mes}-{dia}",
            "data[CommonReport][horainicio]": "00:00:00",
            "data[CommonReport][fechaFinal]": f"{anio}-{mes}-{int(dia)+1}",
            "data[CommonReport][horafin]": "23:59:59",
            "data[CommonReport][codigoPeaje]": 55,
            "data[CommonReport][carril]": 0,
            "data[CommonReport][sentido]": 0,
            "data[CommonReport][turnopeaje]": 0,
            "data[CommonReport][selturno]": 0,
            "data[CommonReport][fechaturno]": 0,
            "data[CommonReport][criterio]": 0,
            "data[CommonReport][modificar]": 0,
            "data[CommonReport][placa]": 0,
            "data[CommonReport][formapago]": -1,
            "data[CommonReport][tipoespecial]": 0,
            "data[CommonReport][Tipovista]": 0,
            "data[CommonReport][tipoReporte]": 1,   #  Nombre y valor correctos
            "data[CommonReport][conciliado]": 2,    #  Valor correcto (no la forma)
            "data[CommonReport][tipoturno]": 1,
            "data[CommonReport][formato]": "csv"    # Exportación CSV
        }

        # se guarda en la Variable " res " la Respuest de la peticion a la url con estos parametros del formulario EasyRoad
        res = sesion.post(reporte_url, data=parametros, stream=True)

        if res.status_code == 200:

            nombre_archivo = os.path.join(carpeta, f"trafico_carrils.csv")   # CONCATENA LA RUTA DE LA CARPETA DONDE SE VA A GUARDAR

            # Guardar el Documento en la Ruta Actual o Carpeta
            with open(nombre_archivo, "wb") as f:
                for chunk in res.iter_content(chunk_size=2000):
                    if chunk:
                        f.write(chunk)
            
            print(f"\n[+] Descargado Automáticamente : {nombre_archivo}")

            # **** Llamado a la Funcion eliminar_fila_csv para ELIMINAR FILAS ESPECIFICAS DESPUES DE GUARDAR ****
            eliminar_fila_csv(nombre_archivo, ["EG","ER","EA","EC"])

        else:
            print(f"\n*** Error al Descargar el Archivo : {res.status_code} ***\n")
            

        return nombre_archivo  # Se Retorna el NOMBRE del ARCHIVO en str


# ==== RUTA HOME (renderiza tu HTML) ====
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# === TRABAJANDO EN EL SERVIDOR ( API ) PARA UN POSIBLE FRONTEND / 28-NOVIEMBRE-2025 ===
# Ruta Para Descargar Todo el Archivo ( get )
@app.get("/descargar_csv")
async def descargar_csv():
    ruta_archivo = descargar_archivo(anio, mes, dia)

    if not ruta_archivo or not os.path.isfile(ruta_archivo):
        return {"error": "No se pudo generar el archivo"}

    return FileResponse(
        ruta_archivo,
        media_type="text/csv",
        filename="trafico_aniscopio.csv"
    )
    
    
# LINEA NECESARIA PARA CONVERTIR EN EJECUTABLE DE WINDOWS LLAMANDO AL PROGRAMA PRIMCIPAL CON LO NECESARIO PARA QUE NO FALLE ( LA FECHA QUE SE LE PASA ALA FUNCION descargar_archivos)
    
if __name__ == "__main__":
    import os

    DIA_SEMANA = 0 # DIA OBJETIVO DE LA SEMANA PARA EL ENVIO DEL CORREO ELECTRONICO AUTOMATICAMETE ( DONDE " 0 = LUNES, 1 = MARTES, 2 = MIERCOLES, 3 = JUEVES, 4 = VIERNES, 5 = SABADO, 6 = DOMINGO " )

    MES_PASADO = mes #  CONTROLA QUE SE ENVIEN LOS ARCHIVOS SI YA SE TERMINA EL MES ACTUAL

    try:
        
        descargar_archivo(anio,mes,dia)
        dia_envio_correo(DIA_SEMANA, MES_PASADO) ## SE PASAN POR PARAMETROS LOS VALORES DE LAS VARIABLES CONSTANTES A LA FUNCION

        print("\nDescarga Completada Con Exito...")
        
    except Exception as e:
        print("Error",e)

    
