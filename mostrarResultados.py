from sys import argv
from os import mkdir, system
from subprocess import Popen
from atexit import register
from pathlib import Path
from datetime import datetime
from sympy import lambdify, sympify, latex, Integral
from sympy.abc import x
import numpy as np

def convertir_numero(valor):
    return lambdify((), sympify(valor))()

carpeta = 'resultados'
if not Path(carpeta).exists():
    mkdir(carpeta)

def crear_archivo(expr, intervalo, metodo, particiones):
    funcion = sympify(expr, evaluate=False)
    func = lambdify(x, funcion)
    particiones = convertir_numero(particiones)
    a, b = list(sorted([convertir_numero(limite) for limite in intervalo]))
    valores = np.linspace(a, b, particiones + 1)

    def escribir_numeros(w, inicio, fin):
        for i in range(inicio, fin):
            valor = i * ((b - a) / particiones) + a
            w(
"""
          <tr>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
          </tr>
"""
                .format(i, valor, func(valor))
            )

    def escribir_resultado(w):
        resultado = func(a) + func(b)
        if metodo == 'trapecio':
            for i in range(1, particiones):
                resultado += 2 * func(valores[i])
            resultado *= (b - a) / (2 * particiones)
        else:
            for i in range(1, particiones):
                if i % 2 == 1:
                    resultado += 4 * func(valores[i])
                else:
                    resultado += 2 * func(valores[i]) 
            resultado *= (b - a) / (3 * particiones)
        w(str(resultado) + '\n')

    funcion_nombre = ''.join(x for x in expr if x.isalnum() or x in '() ')
    nombre_archivo = datetime.now().strftime(
        './resultados/%Y-%m-%d %H.%M.%S {} {}.html'.format(funcion_nombre, metodo)
    )

    with open(nombre_archivo, 'w') as f, open('plantilla.html') as p:
        w = f.write

        for l in p.readlines():
            if '{{ valores1 }}' in l:
                escribir_numeros(w, 0, particiones // 2 + 1)
            elif '{{ valores2 }}' in l:
                escribir_numeros(w, particiones // 2 + 1, particiones + 1)
            elif '{{ resultado }}' in l:
                escribir_resultado(w)
            elif '{{ metodo }}' in l:
                w(metodo.capitalize())
            elif '{{ funcion }}' in l:
                w('$$' + latex(Integral(funcion, (x, sympify(intervalo[0]), sympify(intervalo[1])))) + '$$')
            elif '{{ particiones }}' in l:
                w(str(particiones))
            else:
                w(l)

    return nombre_archivo

if __name__ == '__main__':
    intervalo = [s.strip() for s in argv[2][1:-1].split(',')]
    nombre = crear_archivo(argv[1], intervalo, argv[3], argv[4])

    proceso = Popen(['python3', 'tabla.py', nombre])
    register(proceso.kill)
    proceso.wait()