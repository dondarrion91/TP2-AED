def detectar_hc(cad):
    tiene_h = False
    tiene_hc = False

    for car in cad:
        if car.lower() == "h" and not tiene_h:
            tiene_h = True
        elif car.lower() == "c" and tiene_h:
            tiene_hc = True
        else:
            tiene_h = False

    return tiene_hc

def detectar_tipo_control(cad):
    tiene_hc = detectar_hc(cad)
    
    if tiene_hc:
        return "Hard Control"

    return "Soft Control"

"""
HC: En cada envío del archivo de entrada, se debe controlar que la dirección de
destino tenga solo letras y dígitos, y que no haya dos mayúsculas seguidas, y que haya al menos una
palabra compuesta sólo por dígitos. Será considerado válido el envío solo si pasa la verificación
indicada aquí.
"""

def validar_caract_digitos(direccion):
    termino_palabra = False
    todos_digitos = True
    todos_alfa = True
    is_valid_direccion = True
    
    anterior_car = None
    cant_uppers_palabra = 0
    cant_todos_digitos = 0

    for car in direccion:
        if not is_valid_direccion:
            return False

        if not termino_palabra and (car == " " or car == "."):
            is_valid_direccion = todos_digitos or todos_alfa
            
            if todos_digitos:
                cant_todos_digitos += 1
            
            todos_digitos = True
            todos_alfa = True

            if car == ".":
                termino_palabra = True
        elif not termino_palabra:
            if todos_digitos and not car.isdigit():
                todos_digitos = False

            if todos_alfa and not car.isalpha():
                todos_alfa = False

            if anterior_car is not None:
                ant_car_is_alpha = anterior_car.isalpha() and car.isalpha()
                dos_uppers_seguidos = anterior_car.upper() == anterior_car and car.upper() == car

                if ant_car_is_alpha and dos_uppers_seguidos:
                    cant_uppers_palabra += 1

        anterior_car = car

    return is_valid_direccion and (cant_uppers_palabra == 0) and (cant_todos_digitos >= 1)

def validar_direccion(direccion):
    is_caract_digitos_validos = validar_caract_digitos(direccion)

    return is_caract_digitos_validos