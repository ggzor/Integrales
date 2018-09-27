import webview
import threading
from subprocess import Popen
from funciones import Funciones
from atexit import register

def principal():
    with open('index.html') as archivo:
        html = archivo.read()
        webview.load_html(html)


if __name__ == '__main__':
    t = threading.Thread(target=principal)
    t.start()

    proceso = Popen(['python3', 'ayuda.py'])
    register(proceso.kill)

    webview.create_window(
        "Integrales", 
        width=500, height=640, resizable=True, 
        js_api=Funciones())
