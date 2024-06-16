__author__ = "TP2-G023"

ISO_3166_2_AR_DIGITS = "ABCDEFGHJKLMNPQRSTUVWXYZ"

ISO_3166_2_AR_DIGITS_NAMES = (
    ("A", "Salta"),
    ("B", "Provincia de Buenos Aires"),
    ("C", "Ciudad Autónoma de Buenos Aires"),
    ("D", "San Luis"),
    ("E", "Entre Ríos"),
    ("F", "La Rioja"),
    ("G", "Santiago del Estero"),
    ("H", "Chaco"),
    ("J", "San Juan"),
    ("K", "Catamarca"),
    ("L", "La Pampa"),
    ("M", "Mendoza"),
    ("N", "Misiones"),
    ("P", "Formosa"),
    ("Q", "Neuquén"),
    ("R", "Río Negro"),
    ("S", "Santa Fe"),
    ("T", "Tucumán"),
    ("U", "Chubut"),
    ("V", "Tierra del Fuego"),
    ("W", "Corrientes"),
    ("X", "Córdoba"),
    ("Y", "Jujuy"),
    ("Z", "Santa Cruz"),
)

MONTOS_ENVIOS = (
    (0, 1100),
    (1, 1800),
    (2, 2450),
    (3, 8300),
    (4, 10900),
    (5, 14300),
    (6, 17900),
)

def get_envios(file_name, action):
    archivo = open(file_name, action)

    envios_string = archivo.read()

    archivo.close()

    return envios_string

envios = get_envios("envios.txt", "rt")

def detectar_tipo_control(tiene_hc):
    if tiene_hc:
        return "Hard Control"

    return "Soft Control"

def get_tipo_mayor(ccs, ccc, cce):
    if ccs > ccc:
        if ccs > cce:
            return "Carta Simple"
        else:
            return "Carta Expresa"
    elif ccc > cce:
        return "Carta Certificada"
    else:
        return "Carta Expresa"

def cp_is_argentina(cp):
    return ((len(cp) == 8 and
                   (cp[0].upper() in ISO_3166_2_AR_DIGITS) and
                   len(cp[1:5]) == 4 and
                   cp[1:5].isdigit() and
                   len(cp[5:]) == 3) and
                   cp[5:].isalpha())
    
def cp_is_bolivia(cp):
    return len(cp) == 4 and cp.isdigit()

def cp_is_brasil(cp):
    return len(cp) == 9 and cp[:5].isdigit() and cp[5] == "-" and cp[6:].isdigit()

def cp_is_chile(cp):
    return len(cp) == 7 and cp.isdigit()

def cp_is_paraguay(cp):
    return len(cp) == 6 and cp.isdigit()

def cp_is_uruguay(cp):
    return len(cp) == 5 and cp.isdigit()

# Seteo el país de destino según el formato del código postal.
def setear_destino(cp):
    isArgentina = cp_is_argentina(cp)
    isBolivia = cp_is_bolivia(cp)
    isBrasil = cp_is_brasil(cp)
    isChile = cp_is_chile(cp)
    isParaguay = cp_is_paraguay(cp)
    isUruguay = cp_is_uruguay(cp)

    if isArgentina:
        return "Argentina"

    if isBolivia:
        return "Bolivia"

    if isBrasil:
        return "Brasil"

    if isChile:
        return "Chile"

    if isParaguay:
        return "Paraguay"

    if isUruguay:
        return "Uruguay"

    return "Otro"

# Elijo la provincia(en caso de ser envio en argentina) según el código postal.
def set_provincia(cp):
    primer_digito_o_letra = cp[0]

    is_argentina = cp_is_argentina(cp)
    provincia = "No aplica"

    if is_argentina:
        for iso_digit_name in ISO_3166_2_AR_DIGITS_NAMES:
            if primer_digito_o_letra == iso_digit_name[0]:
                provincia = iso_digit_name[1]

    return provincia

# Calculo el monto inicial a pagar según el tipo de envio y cp
def set_monto_inicial(cp, tipo):
    primer_digito_o_letra = cp[0]
    inicial = 0

    for monto in MONTOS_ENVIOS:
        if tipo == monto[0]:
            inicial = monto[1]

    isArgentina = cp_is_argentina(cp)
    isBolivia = cp_is_bolivia(cp)
    isBrasil = cp_is_brasil(cp)
    isChile = cp_is_chile(cp)
    isParaguay = cp_is_paraguay(cp)
    isUruguay = cp_is_uruguay(cp)

    if isArgentina:
        return inicial

    if (isBolivia or isParaguay or (isUruguay and int(primer_digito_o_letra) == 1) or
            (isBrasil and int(primer_digito_o_letra) in (8, 9))):
        return int(inicial * 1.20)

    if (isChile or (isUruguay and int(primer_digito_o_letra) != 1) or
          (isBrasil and int(primer_digito_o_letra) in (0, 1, 2, 3))):
        return int(inicial * 1.25)

    if isBrasil and int(primer_digito_o_letra) in (4, 5, 6, 7):
        return int(inicial * 1.30)

    return int(inicial * 1.50)

# Calculo monto final según el metodo de pago del envio.
def set_monto_final(inicial, pago):
    if pago == 1:
        return int(inicial * 0.90)
    
    return inicial

def get_porcentaje_exterior(cant_envios_totales, cant_exterior):
    if cant_envios_totales == 0:
        return 0
    return int((cant_exterior * 100) / cant_envios_totales)

def get_promedio_bsas(cant_envios_prov_bsas, imp_acu_bsas):
    if cant_envios_prov_bsas == 0:
        return 0

    return imp_acu_bsas // cant_envios_prov_bsas

def validar_direccion(all_alfa_digit, cant_uppers_palabra, cant_todos_digitos, control):
    if control == "Hard Control":
        return all_alfa_digit and (cant_uppers_palabra == 0) and (cant_todos_digitos >= 1)

    return True

def contar_tipo_cartas(tipo, ccs, ccc, cce):
    if tipo in (0, 1, 2):
        # simples
        ccs += 1
    elif tipo in (3, 4):
        # certificadas
        ccc += 1
    elif tipo in (5, 6):
        # expresas
        cce += 1
    
    return ccs, ccc, cce

def contar_envios_exterior_y_bsas(cp, cant_exterior, cant_envios_prov_bsas, imp_acu_bsas, final):
    is_argentina = cp_is_argentina(cp)

    if not is_argentina:
        cant_exterior += 1
    else:
        provincia = set_provincia(cp)

        if provincia == "Provincia de Buenos Aires":
            cant_envios_prov_bsas += 1
            imp_acu_bsas += final
    
    return cant_exterior, cant_envios_prov_bsas, imp_acu_bsas

def detectar_hc(envio_car, tiene_h, tiene_hc):
    if envio_car.lower() == "h" and not tiene_h:
        tiene_h = True
    elif envio_car.lower() == "c" and tiene_h:
        tiene_hc = True
    else:
        tiene_h = False

    return tiene_h, tiene_hc

def start():
    # Flag para detectar si es la primer linea del archivo de texto.
    primera_linea = True
    direccion_es_valida = True

    # Outputs
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

    # Variables auxiliares para los outputs
    tiene_h = False
    tiene_hc = False
    imp_acu_bsas = 0
    cant_envios_totales = 0
    cant_envios_prov_bsas = 0
    cant_exterior = 0
    posicion = 0
    cantidad_caracteres = 0

    # Variables de calculo de montos
    cp = ""
    tipo = ""
    pago = ""

    # Variables para validar direcciones
    anterior = None
    todos_digitos = True
    todos_alfa = True
    all_alfa_digit = True
    cant_uppers_palabra = 0
    cant_todos_digitos = 0

    for envio_car in envios:
        has_ended = cantidad_caracteres == (len(envios) - 1)

        if primera_linea and envio_car != "\n":
            # Punto 1
            tiene_h, tiene_hc = detectar_hc(envio_car, tiene_h, tiene_hc)
        elif envio_car == "\n":
            if not control:
                control = detectar_tipo_control(tiene_hc)

            # Detecto si ya no estoy recorriendo la primera linea.
            primera_linea = False

            # Reset variables
            cp = ""
            tipo = ""
            pago = ""
            posicion = 0
        elif not primera_linea and posicion <= 9:
            cp += envio_car
        elif not primera_linea and posicion > 9 and posicion < 30:
            if control == "Hard Control":
                if envio_car == " " or envio_car == ".":
                    all_alfa_digit = todos_digitos or todos_alfa
                    # Si la direccion no es valida en esta iteracion
                    # Termino el ciclo y retorno False
                    if not all_alfa_digit:
                        direccion_es_valida = False
                    else:
                        if todos_digitos:
                            cant_todos_digitos += 1

                        todos_digitos = True
                        todos_alfa = True
                else:
                    if todos_digitos and not envio_car.isdigit():
                        todos_digitos = False

                    if todos_alfa and not envio_car.isalpha():
                        todos_alfa = False

                    if anterior is not None:
                        ant_car_is_alpha = anterior.isalpha() and envio_car.isalpha()
                        dos_uppers_seguidos = anterior.upper() == anterior and envio_car.upper() == envio_car

                        if ant_car_is_alpha and dos_uppers_seguidos:
                            cant_uppers_palabra += 1
                anterior = envio_car
        elif not primera_linea and posicion == 30:
            tipo = int(envio_car)
        elif posicion == 31 or has_ended:
            # Termino de recorrer la linea del archivo.
            direccion_es_valida = validar_direccion(all_alfa_digit, cant_uppers_palabra, cant_todos_digitos, control)

            # Elimino los espacios del código postal.
            cp_sin_espacios = cp.strip()
            pago = int(envio_car)

            # Punto 10
            if (primer_cp is not None) and (cp_sin_espacios == primer_cp):
                cant_primer_cp += 1

            # Punto 9
            if primer_cp is None:
                primer_cp = cp_sin_espacios
                cant_primer_cp += 1

            # Punto 4
            inicial = set_monto_inicial(cp_sin_espacios, tipo)
            final = set_monto_final(inicial, pago)

            if direccion_es_valida:
                # Punto 2
                cedvalid += 1

                # Punto 8
                ccs, ccc, cce = contar_tipo_cartas(tipo, ccs, ccc, cce)

                # Punto 13 y 14
                cant_exterior, cant_envios_prov_bsas, imp_acu_bsas = contar_envios_exterior_y_bsas(
                    cp_sin_espacios,
                    cant_exterior,
                    cant_envios_prov_bsas,
                    imp_acu_bsas,
                    final
                )

                imp_acu_total += final
            else:
                # Punto 3
                cedinvalid += 1

            # Punto 11 y 12
            es_brasil = cp_is_brasil(cp_sin_espacios)

            if es_brasil:
                if menimp is None or (final < menimp):
                    menimp = final
                    mencp = cp_sin_espacios

            # Contador necesario para calcular porcentaje de punto 13
            cant_envios_totales += 1

            # Reseteo codigo postal
            cp_sin_espacios = ""

            # Reset variables para la validacion de direccion
            todos_digitos = True
            todos_alfa = True
            all_alfa_digit = True
            cant_uppers_palabra = 0
            cant_todos_digitos = 0

        cantidad_caracteres += 1
        posicion += 1

    # punto 8
    tipo_mayor = get_tipo_mayor(ccs, ccc, cce)

    # Punto 13
    porc = get_porcentaje_exterior(cant_envios_totales, cant_exterior)
    
    # Punto 14
    prom = get_promedio_bsas(cant_envios_prov_bsas, imp_acu_bsas)
    
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

# Cuerpo principal del script
if __name__ == "__main__":
    start()