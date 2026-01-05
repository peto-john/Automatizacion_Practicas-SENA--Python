import os      #  - 'os'     => Nos permite interactuar con el sistema operativo (archivos, rutas, etc.)
import shutil  #  - 'shutil' => Nos permite realizar operaciones de alto nivel con archivos y carpetas (como copiar o Eliminar Carpetas Completas)
import time    #  - 'time'   => se usa para pausar el TIEMPO un instante 

import zipfile
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


#========================================================================================================================================================================================#
#                                      FUNCION PARA ELIMINAR LA CARPETA TraficoAniscopio y TraficoAniscopio.zip CUANDO YA SE ENVIEN LOS ARCHIVOS                                                                                                                             #
#========================================================================================================================================================================================#

def borrar_carpeta():

    """
    Definimos las rutas (ubicaciones en el disco) de los archivos que queremos eliminar.
    # ruta_traficoAniscopio_zip → ruta del archivo comprimido (.zip)
    # ruta_traficoAniscopio → ruta de la carpeta que se quiere eliminar
    """
    ruta_actual = os.getcwd()  # OBTENEMOS LA RUTA ACTUAL
    ruta_traficoAniscopio_zip = os.path.join(ruta_actual, "TraficoAniscopio.zip")  # RUTA DINAMICA POR SI EL ARCHIVO CAMBIA DE LUGAR NO FALLE
    ruta_traficoAniscopio = os.path.join(ruta_actual, "TraficoAniscopio")    # RUTA DINAMICA POR SI EL ARCHIVO CAMBIA DE LUGAR NO FALLE

    #ruta_traficoAniscopio_zip = r"C:\Bitacoras_Sena\CapturasAPI\proyecto\TraficoAniscopio.zip"
    #ruta_traficoAniscopio = r"C:\Bitacoras_Sena\CapturasAPI\proyecto\TraficoAniscopio"

    # ---------------------------------------------------------------------
    # ELIMINAR ARCHIVO ZIP
    # ---------------------------------------------------------------------

    # Verificamos si el archivo ZIP existe en la ruta indicada
    if os.path.exists(ruta_traficoAniscopio_zip):
        # Si existe, lo eliminamos con os.remove()
        os.remove(ruta_traficoAniscopio_zip)
        print(f"Eliminado Archivo Comprimido: TraficoAniscopio.zip")
    else:
        # Si no existe, mostramos un mensaje indicando que no se encontró el archivo
        print(f"No existe el archivo en la ruta: {ruta_traficoAniscopio_zip}")  

    # ---------------------------------------------------------------------
    # ELIMINAR CARPETA
    # ---------------------------------------------------------------------

    # Verificamos si la carpeta existe en la ruta indicada
    if os.path.exists(ruta_traficoAniscopio):
        # Si existe, la eliminamos completamente (con todo su contenido) usando shutil.rmtree()
        shutil.rmtree(ruta_traficoAniscopio)
        print(f"Eliminada carpeta: TraficoAniscopio")
    else:
        # Si no existe, mostramos un mensaje indicando que no se encontró la carpeta
        print(f"No existe la carpeta en la ruta: {ruta_traficoAniscopio}")





#========================================================================================================================================================================================#
#                                                 FUNCION PARA COMPRIMIR LA CARPETA                                                                                                                                     #
#========================================================================================================================================================================================#

# **** COMPRIMIR CARPETA EN .ZIP ****
def comprimir_carpeta(carpeta, nombre_zip):
    
    # CREA UN NUEVO ARCHIVO ZIP EN MODO ESCRITURA
    # zipfile.ZIP_DEFLATED REDUCE EL TAMAÑO DEL ARCHIVO
    with zipfile.ZipFile("TraficoAniscopio.zip", "w", zipfile.ZIP_DEFLATED) as fzip:
        
        # RECORRE TODOS LOS ARCHIVOS DENTRO DE ESTA CARPETA 
        for raiz, _ , archivos in os.walk(carpeta):
            # PARA CADA ARCHIVO ENCONTRADO 
            for file in archivos:
                ruta_completa = os.path.join(raiz, file)  # --> ESTA ES LA RUTA COMPLETA EN EL SISTEMA
                ruta_relativa = os.path.relpath(ruta_completa, carpeta) # --> CREA RUTA RELATIVA PARA QUE APARESCA SOLO LA CARPETA BASE
                fzip.write(ruta_completa, ruta_relativa)    # AGREGA EL ARCHIVO ZIP CON LA RUTA RELATIVA
        print(f"*** Se Comprimio la carpeta {carpeta} en {nombre_zip} ***")

    return nombre_zip



#========================================================================================================================================================================================#
#                                                 FUNCION PARA ENVIAR POR CORREO CON EL ARCHIVO ADJUNTO                                                                                                                                       #
#========================================================================================================================================================================================#

def enviar_correo(destinatario, asunto, cuerpo, archivo_adj):

    remitente = "petohackgonzalez@gmail.com"  ####### =====> AQUI SE PONE EL CORREO REMITENTE CON CREDENCIALES DE APLICACION <===== #######
    contrasena = "ywybnhefqqkqkdcb"    # ES RECOMENDABLE USAR UNA CONTRASEÑA DE APLICACION 

    mensaje = MIMEMultipart()
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto

    # ADJUNTAR EL ARCHIVO .ZIP
    with open(archivo_adj, "rb") as adj:
        parte = MIMEBase("application", "octet-stream")
        parte.set_payload(adj.read())
        encoders.encode_base64(parte)
        parte.add_header("Content-Disposition", f"attachment; filename={os.path.basename(archivo_adj)}")
        mensaje.attach(parte)

    try:
        servidor = smtplib.SMTP("smtp.gmail.com", 587)   ####### =====> AQUI SE PONE EL PROVEDOR DEL SERVIDOR DE CORREO ELECTRONICO QUE USA EL REMITENTE <===== #######
        servidor.starttls()
        servidor.login(remitente, contrasena)
        servidor.sendmail(remitente, destinatario, mensaje.as_string())
        servidor.quit()
    except Exception as e:
        print(f"Error Enviando Correo : {e}")



#========================================================================================================================================================================================#
#    ********************  FUNCION PRINCIPAL PARA ENVIAR, COMPRIMIR SI HOY ES EL DIA INDICADO O SI YA SE TERMINO EL MES ACTUAL ENVIE LO ULTIMO QUE SE DESCARGO   ********************                                                                                                                            #
#========================================================================================================================================================================================#

def dia_envio_correo(dia_objetivo, mes_pasado): 
     
    dia_semana = datetime.now().weekday() # Obtiene el Dia Actual De la Semana ( DONDE " 0 = LUNES, 1 = MARTES, 2 = MIERCOLES, 3 = JUEVES, 4 = VIERNES, 5 = SABADO, 6 = DOMINGO " )
    mes_actual = datetime.now().strftime("%m") # OBTENEMOS EL MES ATUAL PARA LA COMPARACION CON EL MES QUE LLEGA COMO PARAMETRO 

    ruta_actual = os.getcwd()
    ruta_carpeta = os.path.join(ruta_actual, "TraficoAniscopio/2025")    # RUTA DINAMICA POR SI EL ARCHIVO CAMBIA DE LUGAR NO FALLE
    ruta_zip_salida = os.path.join(ruta_actual, "TraficoAniscopio.zip")  # RUTA DINAMICA POR SI EL ARCHIVO CAMBIA DE LUGAR NO FALLE


    if dia_semana == dia_objetivo or mes_actual != mes_pasado:
        carpeta = ruta_carpeta    # IMPORTANTE --> RUTA COMPLETA DONDE SE DESCARGA EL ARCHIVO ORIGINAL EN ( VARIABLE )
        zip_salida = ruta_zip_salida

        # ****** SE COMPRIME LA CARPETA ANTES DE ENVIAR POR CORREO *******
        archivo_zip = comprimir_carpeta(carpeta, zip_salida)
     
        # SE LLAMA A LA FUNCION PARA ENVIAR POR CORREO
        enviar_correo(
            
            destinatario = "peto--john19@hotmail.com",   ####### =====> AQUI SE PONE EL CORREO AL QUE SE DESEA ENVIAR EL ARCHIVO COMPRIMIDO EN ( .ZIP ) <===== #######

            asunto = f"Respaldo Diario de Trafico Aniscopio de los Ultimos 7 Dias de Esta Semana",
            cuerpo = "Adjunto Encontraras el Respaldo en un Archivo Comprimido ( .zip )",
            archivo_adj = archivo_zip
            )
        print(f"\n*** Hoy Es Dia LUNES, O SE TERMINO EL MES ACTUAL. La Tarea De Enviar El Archivo Trafico Aniscopio Programada Para Este DIA. Se Envio Por Correo Electronico Al Destino Programado. ***\n")

        print(f"\nEn los Siguientes Segundo Se Eliminara la Carpeta TraficoAniscopio y el Archivo TraficoAniscopio.zip")

        # TEMPORIZADOR ANTES DE LA ELIMINACION TOTAL DE LOS ARCHIVOS TraficoAniscopio y TraficoAniscopio.zip
        for i in range(5, -1, -1):
            print(f"BORRAR EN {i} Segundos...", end="\r")
            time.sleep(1)
        print()
        borrar_carpeta()  # LLAMADO A LA FUNCION QUE ELIMINA LOS ARCHIVOS TraficoAniscopio y TraficoAniscopio.zip DEPUES DE ENVIARSE POR CORREO ELECTRONICO
        
    else:
        print(f"\n*** HOY NO Hay Tareas Programadas. La Tarea De Enviar El Archivo Trafico Aniscopio Por Correo Electronico Esta Programada Para Ejecutarse Los DIAS LUNES De Cada MES ***.\n")