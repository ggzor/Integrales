import webview
import threading
from sys import argv

def principal(nombre):
    with open(nombre) as archivo:
        html = archivo.read()
        webview.load_html(html)

if __name__ == '__main__':
    t = threading.Thread(target=principal, args=[argv[1]])
    t.start()

    webview.create_window("Resultados", width=500, height=500, resizable=True)