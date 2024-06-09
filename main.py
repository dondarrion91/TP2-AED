__author__ = "TP2-G023"

import controles
import envio

# Flag para detectar si es la primer linea del archivo de texto.
primera_linea = True
direccion_es_valida = True
control = None
cedvalid = 0
cedinvalid = 0
posicion = 0
cantidad_caracteres = 0

cp = ""
direccion = ""
tipo = ""
pago = ""
timestamp = ""

envios = envio.get_envios("envios.txt", "rt")

# Cuerpo principal del script
for envio_car in envios:
    has_ended = cantidad_caracteres == (len(envios) - 1)

    if primera_linea and envio_car != "\n":
        timestamp += envio_car
    elif envio_car == "\n":
        control = controles.detectar_tipo_control(timestamp)
        primera_linea = False
        posicion = 0
    elif not primera_linea and posicion <= 9:
        cp += envio_car
    elif not primera_linea and posicion > 9 and posicion < 30:
        direccion += envio_car
    elif not primera_linea and posicion == 30:
        tipo = envio_car
    elif posicion == 31 or has_ended:
        pago = envio_car
        direccion_es_valida = envio.handle_envio(cp, direccion, control)
        
        if direccion_es_valida:
            cedvalid += 1
        else:
            cedinvalid += 1

        # Reset variables
        cp = ""
        direccion = ""
        tipo = ""
        pago = ""

    cantidad_caracteres += 1
    posicion += 1

print(' (r1) - Tipo de control de direcciones:', control)
print(' (r2) - Cantidad de envios con direccion valida:', cedvalid)
print(' (r3) - Cantidad de envios con direccion no valida:', cedinvalid)