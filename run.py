#!/usr/bin/python3
# Ejecutar con python3 run.py
import subprocess, os, sys

def resolver_ruta(ruta_relativa):
    global ruta
    if hasattr(sys, '_MEIPASS'):
        ruta = sys._MEIPASS
        return os.path.join(sys._MEIPASS, ruta_relativa)
    return os.path.join(os.path.abspath('.'), ruta_relativa)

subprocess.call(['gksudo', 'python3 ' + resolver_ruta('main.py'), "-D"
" le permite instalar las aplicaiones"
" de una manera grafica, estas son las que el equipo"
" de deepin en español tiene en su repositorio"])