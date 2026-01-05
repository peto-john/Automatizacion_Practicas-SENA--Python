"""
Muestra una barra de progreso animada en la consola.

La función simula un proceso en ejecución actualizando una barra
con caracteres "#" y "-" junto con el porcentaje completado.
Pausa brevemente entre actualizaciones para generar el efecto visual.
"""

def barra_progreso():  #  Definimos una función llamada "barra_progreso"
    
    import sys, time  # sys → permite escribir directamente en la consola sin saltar de línea
                      # time → se usa para pausar un instante entre actualizaciones

    total = 30  # Cuántas veces se actualizará la barra (control del bucle)

    # Iniciamos un bucle que va de 0 hasta 30
    for i in range(total + 1):

        # Calculamos cuántos caracteres de la barra deben estar "rellenos" con #
        llenado = int((i/total) * 20)  # ← 20 es el ancho visual de la barra / Ejemplo: si i = 15 (mitad del total), llenado = 10

        # Construimos la barra con dos partes: // "#" → parte completada  "-" → parte restante
        barra = "#" * llenado + "-" * (20 - llenado)

        # Mostramos la barra en la misma línea usando \r (retorno de carro)
        # \r mueve el cursor al inicio de la línea, así sobrescribe el texto anterior
        sys.stdout.write(f"\rProgreso: [{barra}] {i*100//total}%")

        # Forzamos a que se muestre inmediatamente (sin esperar al buffer)
        sys.stdout.flush()

        # Pausamos 0.08 segundos antes de la siguiente actualización (efecto animado)
        time.sleep(0.08)

    # Cuando termina el bucle, imprimimos un mensaje final
    print("   ---> !! COMPLETADO <--- ¡¡ ")



