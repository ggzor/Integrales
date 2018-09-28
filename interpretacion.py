from sympy import sympify, Integral
from sympy.abc import x

from functools import lru_cache
from aserciones import Error, Resultado, realizar_aserciones, combinar_errores

memoizar = lru_cache(1)

def transformar_mensaje_error(error):
    if 'EOF' in error:
        return 'expresión incompleta' 
    if 'unmatched left parent':
        return 'paréntesis faltantes'

    return error

def interpretar_expresion(expresion):
    try:
        return Resultado(sympify(expresion, evaluate=False))
    except ValueError as e:
        return Error([transformar_mensaje_error(str(e))])


def interpretar_intervalo(intervalo):
    intervalo = intervalo.strip()
    intervalos = memoizar(lambda: [s.strip() for s in intervalo[1:-1].split(',')])
    inferior = memoizar(lambda: interpretar_expresion(intervalos()[0]))
    superior = memoizar(lambda: interpretar_expresion(intervalos()[1]))

    aserciones = [
        (
            intervalo == '',
            'Debe especificar un intervalo de integración.'
        ),
        (
            not intervalo.startswith('[') or not intervalo.endswith(']'),
            'El intervalo de integración debe estar encerrado entre corchetes.'
        ),
        (
            lambda: not len(intervalos()) == 2 or any([s == '' for s in intervalos()]),
            'El intervalo debe tener exactamente dos valores.'
        ),
        (
            lambda: isinstance(inferior(), Error),
            lambda: 'No se pudo interpretar el intervalo inferior: {}.'.format(inferior().errores[0])
        ), 
        (
            lambda: isinstance(superior(), Error),
            lambda: 'No se pudo interpretar el intervalo superior: {}.'.format(superior().errores[0])
        ),
        (
            lambda: inferior().valor.is_real != True,
            'El límite inferior no es un número real.'
        ),
        (
            lambda: superior().valor.is_real != True,
            'El límite superior no es un número real.'
        ),
        (
            lambda: inferior() == superior(),
            'Los límites deben ser distintos.'
        )
    ]

    return realizar_aserciones(aserciones, 'intervalo', lambda: [inferior(), superior()])

def interpretar_funcion(expresion):
    expresion = expresion.strip()
    funcion = memoizar(lambda: interpretar_expresion(expresion))

    aserciones = [
        (
            expresion == '',
            'Debe especificar una función para integrar.'
        ),
        (
            lambda: isinstance(funcion(), Error),
            lambda: 'No se pudo interpretar la función: {}.'.format(funcion().errores[0])
        ),
        (
            lambda: isinstance(funcion(), Resultado) and not isinstance(funcion().valor.free_symbols, set),
            lambda: 'La función no está parametrizada.'
        ),
        (
            lambda: funcion().valor.free_symbols - {x} != set(),
            'La función debe estar completamente en términos de x.'
        )
    ]

    return realizar_aserciones(aserciones, 'funcion', lambda: funcion().valor)

def interpretar_integral(funcion, intervalo):
    funcion = interpretar_funcion(funcion)
    intervalo = interpretar_intervalo(intervalo)

    if isinstance(intervalo, Resultado) and isinstance(funcion, Resultado):
        funcion = funcion.valor
        inferior, superior = intervalo.valor

        return Resultado(Integral(funcion, (x, inferior, superior)))
    else:
        return Error(combinar_errores(funcion, intervalo))
