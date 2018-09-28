from sys import argv

from sympy import abc, lambdify, latex, sympify

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

def convertir_numero(valor):
    return lambdify((), sympify(valor))()

def parabola_puntos(p1, p2, p3):
    from sympy.abc import x 
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    func = y1 * (((x - x2) * (x - x3)) / ((x1 - x2) * (x1 - x3))) + \
           y2 * (((x - x1) * (x - x3)) / ((x2 - x1) * (x2 - x3))) + \
           y3 * (((x - x1) * (x - x2)) / ((x3 - x1) * (x3 - x2)))
    
    return lambdify(x, func)

def graficar(expr, intervalo, metodo, particiones):
    expr = sympify(expr, evaluate=False)
    func = lambdify(abc.x, expr)
    particiones = convertir_numero(particiones)
    intervalo = a, b = list(sorted([convertir_numero(limite) for limite in intervalo]))
    
    fig, ax = plt.subplots()

    def establecer_interfaz():
        # Establecer título
        fig.canvas.set_window_title('{}, {}'.format(expr, intervalo))
        # Escribir función
        plt.text((a + b) / 2, func((a + b) / 2), '${}$'.format(latex(expr)),
                horizontalalignment='center', fontsize=20)

    def graficar_funcion():
        x = np.arange(a, b, 0.001)
        y = func(x)
        plt.plot(x, y, '#FE4A49')

    def graficar_trapecio():
        x = np.linspace(a, b, particiones + 1)
        y = func(x)
        puntos = list(zip(x, y)) 

        for i in range(particiones):
            x1, _ = puntos[i]
            x2, _ = puntos[i + 1]
            vertices = [(x1, 0), puntos[i], puntos[i + 1], (x2, 0)]
            poligono = Polygon(vertices, facecolor='#F26430' if i % 2 == 0 else '#F48055', edgecolor='#F26430')
            ax.add_patch(poligono)

    def graficar_simpson():
        def graficar_parabola(p1, p2, p3, obscuro):
            inicio = p1[0]
            fin = p3[0]

            func = parabola_puntos(p1, p2, p3)
            x = np.arange(inicio, fin, 0.001)
            y = func(x)

            vertices = [(inicio, 0)] + list(zip(x, y)) + [(fin, 0)]
            poligono = Polygon(vertices, facecolor='#009FB7' if obscuro else '#7FC0CA', edgecolor='#009FB7')
            ax.add_patch(poligono)

        x = np.linspace(a, b, particiones + 1)
        y = func(x)
        puntos = list(zip(x, y))

        for i in range(particiones // 2):
            graficar_parabola(puntos[2 * i], puntos[2 * i + 1], puntos[2 * i + 2], i % 2 == 0)

    def graficar_area_bajo_curva():
        x = np.arange(a, b, 0.001)
        y = func(x)

        vertices = [(a, 0)] + list(zip(x, y)) + [(b, 0)]
        poligono = Polygon(vertices, facecolor='#009FB7', edgecolor='#009FB7')
        ax.add_patch(poligono)

    establecer_interfaz()
    graficar_funcion()
    if particiones > 1000:
        graficar_area_bajo_curva()
    else:
        if metodo == 'trapecio':
            graficar_trapecio()
        else:
            graficar_simpson()

    plt.show()


if __name__ == '__main__':
    intervalo = [s.strip() for s in argv[2][1:-1].split(',')]
    graficar(argv[1], intervalo, argv[3], argv[4])
