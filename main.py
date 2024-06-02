__author__ = "TP2-G023"

cp = input("Ingrese el código postal del lugar de destino: ")
direccion = input("Dirección del lugar de destino: ")
tipo = int(input("Tipo de envío (id entre 0 y 6 - ver tabla 2 en el enunciado): "))
pago = int(input("Forma de pago (1: efectivo - 2: tarjeta): "))
inicial = 0

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

# Punto 1)
isArgentina = ((len(cp) == 8 and
               (cp[0].upper() in ISO_3166_2_AR_DIGITS) and
               len(cp[1:5]) == 4 and
               cp[1:5].isdigit() and
               len(cp[5:]) == 3) and
               cp[5:].isalpha())

isBolivia = len(cp) == 4 and cp.isdigit()

isBrasil = len(cp) == 9 and cp[:5].isdigit() and cp[5] == "-" and cp[6:].isdigit()

isChile = len(cp) == 7 and cp.isdigit()

isParaguay = len(cp) == 6 and cp.isdigit()

isUruguay = len(cp) == 5 and cp.isdigit()


if isArgentina:
    destino = "Argentina"
elif isBolivia:
    destino = "Bolivia"
elif isBrasil:
    destino = "Brasil"
elif isChile:
    destino = "Chile"
elif isParaguay:
    destino = "Paraguay"
elif isUruguay:
    destino = "Uruguay"
else:
    destino = "Otro"

# Punto 2)
primer_digito_o_letra = cp[0]

provincia = "No aplica"

if isArgentina:
    for iso_digit_name in ISO_3166_2_AR_DIGITS_NAMES:
        if primer_digito_o_letra == iso_digit_name[0]:
            provincia = iso_digit_name[1]

# Punto 3)
for monto in MONTOS_ENVIOS:
    if tipo == monto[0]:
        inicial = monto[1]

if not isArgentina:
    if (isBolivia or isParaguay or (isUruguay and int(primer_digito_o_letra) == 1) or
            (isBrasil and int(primer_digito_o_letra) in (8, 9))):
        inicial = int(inicial * 1.20)
    elif (isChile or (isUruguay and int(primer_digito_o_letra) != 1) or
          (isBrasil and int(primer_digito_o_letra) in (0, 1, 2, 3))):
        inicial = int(inicial * 1.25)
    elif isBrasil and int(primer_digito_o_letra) in (4, 5, 6, 7):
        inicial = int(inicial * 1.30)
    else:
        inicial = int(inicial * 1.50)

# Punto 4)
final = inicial

if pago == 1:
    final = int(inicial * 0.90)


print("País de destino del envío:", destino)
print("Provincia destino:", provincia)
print("Importe inicial a pagar:", inicial)
print("Importe final a pagar:", final)