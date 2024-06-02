__author__ = "TP2-G023"

import montos

envios = open("envios.txt", "rt")

# Flag para detectar si es la primer linea del archivo de texto.
primera_linea = True

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

        destino = montos.setear_destino(cp)
        provincia = montos.set_provincia(cp)
        inicial = montos.set_monto_inicial(cp, tipo)
        final = montos.set_monto_final(inicial, pago)

        print("\nCodigo postal", cp)
        print("Direccion:", direccion)
        print("Tipo de envio:", tipo)
        print("Forma de pago:", pago)
        print("Destino:", destino)
        print("Provincia:", provincia)
        print("Monto incial:", inicial)
        print("Monto final:", final)

    primera_linea = False