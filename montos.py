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