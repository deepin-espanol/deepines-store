import sys, os, subprocess, cgitb
import time
from threading import Thread, Lock
from messageg import Ui_Dialog

bloque = Lock()

class Installacion_App(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name,
                         daemon=daemon)
        self.arg1 = args

    def run(self):
        bloque.acquire()
        
        try:
            # comandos para instalar la app
            print("Comenzando Instalacion de %s" % self.arg1)
            comando = 'apt install %s' % self.arg1
            #os.system(comando)
        except:
            print("Algo a fallado")
        finally:
            bloque.release()
            print("Proceso finalizado")