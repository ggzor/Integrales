from sys import stderr
from sympy import latex

from aserciones import Resultado
from interpretacion import interpretar_integral
from validacion import validar_particiones

from atexit import register
from subprocess import Popen

class Funciones:
    def generar_visualizacion(self, parametros):
        try:
            integral = interpretar_integral(parametros['funcion'], parametros['intervalo'])
            if isinstance(integral, Resultado):
                return {
                    'esValido': True,
                    'latex': latex(integral.valor)
                }
            else:
                return {
                    'esValido': False,
                    'errores': integral.errores
                }
        except Exception as e:
            print(e, file=stderr)
            return {
                'esValido': False,
                'errores': [
                    {
                        'propiedad': 'funcion',
                        'mensaje': 'La función no se pudo interpretar.'
                    }
                ]
            }

    def validar_particiones(self, parametros):
        valor = validar_particiones(parametros['particiones'], parametros['metodo'])

        if isinstance(valor, Resultado):
            return {
                'esValido': True
            }
        else:
            return {
                'esValido': False,
                'errores': valor.errores
            }

    def mostrar_resultados(self, parametros):
        valores = [parametros['funcion'], parametros['intervalo'], parametros['metodo'], parametros['particiones']]
        procesos = ['graficar', 'mostrarResultados']

        for p in procesos:
            proceso = Popen(['python3', '{}.py'.format(p)] + valores)
            register(proceso.kill)
