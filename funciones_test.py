import pytest
from funciones import Funciones

def generar_visualizacion(funcion='x', intervalo='[0, 1]'):
    f = Funciones()
    parametros = {
        'funcion': funcion,
        'intervalo': intervalo
    }
    return f.generar_visualizacion(parametros)

def tiene_error(resultado, propiedad):
    return any([error['propiedad'] == propiedad for error in resultado['errores']])

def tiene_error_cuando_intervalo_es(intervalo): 
    return tiene_error(generar_visualizacion(intervalo=intervalo), 'intervalo')

def test_deberiaRegresar_funcionInterpretada_cuandoFuncionValida():
    assert generar_visualizacion()['esValido']

@pytest.mark.parametrize('intervalo', [
    pytest.param('0, 1', id='Intervalo no inicia o termina con corchetes'),
    pytest.param('[23]', id='Intervalo no tiene dos valores'),
    pytest.param('[23,]', id='Intervalo no tiene dos valores, pero sí coma.'),
    pytest.param('[lambda, 1]', id='Limite inferior no se puede interpretar'),
    pytest.param('0, lambda', id='Limite superior no se puede interpretar'),
    pytest.param('[x, 1]', id='Limite inferior no es un número real'),
    pytest.param('[0, x]', id='Limite superior no es un número real'),
    pytest.param('[34, 34]', id='Límites son iguales'),
])
def test_deberiaRegresar_errorEnPropiedadIntervalo_cuandoIntervaloTieneErrores(intervalo):
    assert tiene_error_cuando_intervalo_es(intervalo)


@pytest.mark.parametrize('funcion', [
    pytest.param('', id='Función vacía'),
    pytest.param('x^', id='Funcion inválida'),
    pytest.param('y', id='Función con otra variable'),
    pytest.param('sec', id="Función trigronométrica"), # BUG: Funciones planas
])
def test_deberiaRegresar_errorEnPropiedadFuncion_cuandoFuncionTieneErrores(funcion):
    assert tiene_error(generar_visualizacion(funcion=funcion), 'funcion')

@pytest.mark.parametrize('particiones, metodo', [
    pytest.param('', 'trapecio', id='Particiones vacías en trapecio'),
    pytest.param('', 'simpson', id='Particiones vacías en trapecio'),
    pytest.param('ab', 'trapecio', id='No número'),
    pytest.param('ab', 'simpson', id='No número'),
    pytest.param('-3', 'trapecio', id='Números negativos'),
    pytest.param('-3', 'simpson', id='Números negativos'),
    pytest.param('1', 'simpson', id='Simpson requiere >= 2'),
    pytest.param('3', 'simpson', id='Simpson requere número par'),
    pytest.param('3000', 'trapecio', id='Menos de 3000'),
])
def test_deberiaRegresar_errorEnPropiedadParticion_cuandoParticionTieneErrores(particiones, metodo):
    f = Funciones()
    parametros = {
        'particiones': particiones,
        'metodo': metodo
    }
    assert tiene_error(f.validar_particiones(parametros), 'particiones')


@pytest.mark.parametrize('particiones, metodo', [
    pytest.param('1', 'trapecio', id='Trapecio válido'),
    pytest.param('2', 'simpson', id='Simpson válido')
])
def test_deberiaRegresar_valido_cuandoParticionesYMetodoSonValidos(particiones, metodo):
    f = Funciones()
    parametros = {
        'particiones': particiones,
        'metodo': metodo
    }
    assert f.validar_particiones(parametros)['esValido']