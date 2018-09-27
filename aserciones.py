from collections import namedtuple

Resultado = namedtuple('Resultado', ['valor'])
Error = namedtuple('Error', ['errores'])

def obtener_errores(resultado):
    if isinstance(resultado, Error):
        return resultado.errores
    else:
        return []

def combinar_errores(intento1, intento2) -> list:
    return obtener_errores(intento1) + obtener_errores(intento2)

def realizar_aserciones(aserciones, propiedad, resultado):
    for asercion, mensaje in aserciones:
        if asercion() if callable(asercion) else asercion:
            return Error([{
                'propiedad': propiedad,
                'mensaje': mensaje() if callable(mensaje) else mensaje
            }])

    return Resultado(resultado() if callable(resultado) else resultado)