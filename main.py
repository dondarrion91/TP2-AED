__author__ = "TP2-G023"

import montos
import controles

envios = open("envios.txt", "rt")

# Flag para detectar si es la primer linea del archivo de texto.
primera_linea = True
direccion_es_valida = True
control = None
cedvalid = 0
cedinvalid = 0

# Cuerpo principal del script
for envio_cad in envios:
    if not primera_linea:
        cp = ""
        direccion = envio_cad[9:29]
        tipo = int(envio_cad[29])
        pago = int(envio_cad[30])

        # Elimino los espacios del código postal.
        for car in envio_cad[0:9]:
            if car != " ":
                cp += car

        if control == "Hard Control":
            direccion_es_valida = controles.validar_direccion(direccion)
        
        if direccion_es_valida:
            cedvalid += 1
        else:
            cedinvalid += 1

        # destino = montos.setear_destino(cp)
        # provincia = montos.set_provincia(cp)
        # inicial = montos.set_monto_inicial(cp, tipo)
        # final = montos.set_monto_final(inicial, pago)

        # print("\nCodigo postal", cp)
        # print("Direccion:", direccion)
        # print("Tipo de envio:", tipo)
        # print("Forma de pago:", pago)
        # print("Destino:", destino)
        # print("Provincia:", provincia)
        # print("Monto incial:", inicial)
        # print("Monto final:", final)
    else:
        control = controles.detectar_tipo_control(envio_cad)

    primera_linea = False

print(' (r1) - Tipo de control de direcciones:', control)
print(' (r2) - Cantidad de envios con direccion valida:', cedvalid)
print(' (r3) - Cantidad de envios con direccion no valida:', cedinvalid)