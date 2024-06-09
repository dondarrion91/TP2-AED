__author__ = "TP2-G023"

import controles
import envio
import montos

# Flag para detectar si es la primer linea del archivo de texto.
primera_linea = True
direccion_es_valida = True

# Outputs variables
control = None
cedvalid = 0
cedinvalid = 0
imp_acu_total = 0
ccs = 0
ccc = 0
cce = 0
primer_cp = None
cant_primer_cp = 0
menimp = None
mencp = None
porc = None
prom = None

imp_acu_bsas = 0
cant_envios_totales = 0
cant_envios_prov_bsas = 0
cant_exterior = 0
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
        if not control:
            # Punto 1
            control = controles.detectar_tipo_control(timestamp)

        primera_linea = False

        # Reset variables
        cp = ""
        direccion = ""
        tipo = ""
        pago = ""
        posicion = 0
    elif not primera_linea and posicion <= 9:
        cp += envio_car
    elif not primera_linea and posicion > 9 and posicion < 30:
        direccion += envio_car
    elif not primera_linea and posicion == 30:
        tipo = int(envio_car)
    elif posicion == 31 or has_ended:
        pago = int(envio_car)
        direccion_es_valida = envio.handle_envio(direccion, control)
        
        # Elimino los espacios del código postal.
        cp_sin_espacios = ""

        for car in cp:
            if car != " ":
                cp_sin_espacios += car

        # Punto 10
        if (primer_cp is not None) and (cp_sin_espacios == primer_cp):
            cant_primer_cp += 1

        # Punto 9
        if primer_cp is None:
            primer_cp = cp_sin_espacios
            cant_primer_cp += 1

        # Punto 4
        inicial = montos.set_monto_inicial(cp_sin_espacios, tipo)
        final = montos.set_monto_final(inicial, pago)

        if direccion_es_valida:
            # Punto 2
            cedvalid += 1

            # Punto 8
            if tipo in (0, 1, 2):
                ccs += 1
            elif tipo in (3, 4):
                ccc += 1
            elif tipo in (5, 6):
                cce += 1
            
            # Punto 13
            is_argentina = montos.cp_is_argentina(cp_sin_espacios)
            
            if not is_argentina:
                cant_exterior += 1
            else:
                # Punto 14
                provincia = montos.set_provincia(cp_sin_espacios)

                if provincia == "Provincia de Buenos Aires":
                    cant_envios_prov_bsas += 1
                    imp_acu_bsas += final

            cp_sin_espacios = ""

            imp_acu_total += final
        else:
            # Punto 3
            cedinvalid += 1
        
        # Punto 11 y 12
        es_brasil = montos.cp_is_brasil(cp_sin_espacios)

        if es_brasil:
            if menimp is None or (final < menimp):
                menimp = final
                mencp = cp_sin_espacios

        cant_envios_totales += 1

        cp_sin_espacios = ""

    cantidad_caracteres += 1
    posicion += 1

# punto 8
tipo_mayor = controles.get_tipo_mayor(ccs, ccc, cce)

# Punto 13
if cant_envios_totales == 0:
    porc = 0
else:
    porc = int((cant_exterior * 100) / cant_envios_totales)

if cant_envios_prov_bsas == 0:
    prom = 0
else:
    # Punto 14
    prom = imp_acu_bsas // cant_envios_prov_bsas


print(' (r1) - Tipo de control de direcciones:', control)
print(' (r2) - Cantidad de envios con direccion valida:', cedvalid)
print(' (r3) - Cantidad de envios con direccion no valida:', cedinvalid)
print(' (r4) - Total acumulado de importes finales:', imp_acu_total)
print(' (r5) - Cantidad de cartas simples:', ccs)
print(' (r6) - Cantidad de cartas certificadas:', ccc)
print(' (r7) - Cantidad de cartas expresas:', cce)
print(' (r8) - Tipo de carta con mayor cantidad de envios:', tipo_mayor)
print(' (r9) - Codigo postal del primer envio del archivo:', primer_cp)
print('(r10) - Cantidad de veces que entro ese primero:', cant_primer_cp)
print('(r11) - Importe menor pagado por envios a Brasil:', menimp)
print('(r12) - Codigo postal del envio a Brasil con importe menor:', mencp)
print('(r13) - Porcentaje de envios al exterior sobre el total:', porc)
print('(r14) - Importe final promedio de los envios Buenos Aires:', prom)