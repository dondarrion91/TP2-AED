import controles
import montos

def get_envios(file_name, action):
    archivo = open(file_name, action)

    envios_string = archivo.read()

    archivo.close()

    return envios_string


def handle_envio(direccion, control):
    # Caso Soft Control
    direccion_es_valida = True

    if control == "Hard Control":
        direccion_es_valida = controles.validar_direccion(direccion)
    
    return direccion_es_valida

# def handle_envio_valido(cedvalid, cedinvalid, imp_acu_total, cp, pago, tipo, direccion_es_valida):
#     if direccion_es_valida:
#         # Punto 2
#         cedvalid += 1
        
#         # Punto 4
#         # Elimino los espacios del código postal.
#         local_cp = ""

#         for car in cp:
#             if car != " ":
#                 local_cp += car

#         inicial = montos.set_monto_inicial(local_cp, tipo)
#         final = montos.set_monto_final(inicial, pago)
        
#         local_cp = ""

#         imp_acu_total += final
#     else:
#         # Punto 3
#         cedinvalid += 1
    
#     return cedvalid, cedinvalid, imp_acu_total