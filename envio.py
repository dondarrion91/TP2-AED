import controles

def get_envios(file_name, action):
    archivo = open(file_name, action)

    envios_string = archivo.read()

    archivo.close()

    return envios_string


def handle_envio(cp, direccion, control):
    # Caso Soft Control
    direccion_es_valida = True
    local_cp = ""
    
    # Elimino los espacios del código postal.
    for car in cp:
        if car != " ":
            local_cp += car

    if control == "Hard Control":
        direccion_es_valida = controles.validar_direccion(direccion)
    
    return direccion_es_valida
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