from aserciones import realizar_aserciones

def puede_convertirse_entero(numero):
    try:
        int(numero)
        return True
    except ValueError:
        return False

def validar_particiones(particiones, metodo):
    particiones = particiones.strip()
    metodo = metodo.strip()
    valor = lambda: int(particiones)
    aserciones = [
        (
            particiones == '',
            'Debe especificar un número de particiones.'
        ),
        (
            not puede_convertirse_entero(particiones),
            'La cantidad de particiones debe ser un número.'
        ),
        (
            lambda: valor() <= 0,
            'La cantidad de particiones debe ser un numero mayor que 0.'
        ),
        (
            lambda:  metodo == 'simpson' and valor() % 2 == 1,
            'La cantidad de particiones para el método de Simpson debe ser un número par.'
        )
    ]

    return realizar_aserciones(aserciones, 'particiones', valor)