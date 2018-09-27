import webview
import threading
from sys import argv

def principal():
    with open('ayuda.html') as archivo:
        html = archivo.read()
        webview.load_html(html)

if __name__ == '__main__':
    t = threading.Thread(target=principal)
    t.start()

    webview.create_window("Ayuda", width=400, height=640, resizable=False)