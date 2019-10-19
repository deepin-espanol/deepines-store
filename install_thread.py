import subprocess
# Importamos las librerias necesarias
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
import time


# Creamos la clase y heredamos de QThread
class External(QObject):
    start = pyqtSignal(object)
    finish = pyqtSignal()
    complete = pyqtSignal()
    error = pyqtSignal()
    
    def __init__(self, app):
        super(External, self).__init__()
        self.app = app

    @pyqtSlot()
    def run(self):
        for elemento in self.app:
            try:
            	# Iniciamos la instalacion
            	# Enviamos la señal
                self.start.emit(elemento)
                # comandos para instalar la app
                comando = 'sudo apt install {}'.format(elemento)
#                subprocess.call(comando, shell=True)
            except:
                self.error.emit()
                print("Algo a fallado")
            finally:
                self.finish.emit()
                print("Proceso finalizado")
        else:
            self.complete.emit()
