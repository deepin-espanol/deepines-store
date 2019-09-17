import sys
# Importamos las librerias necesarias
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
import time


# Creamos la clase y heredamos de QThread
class External(QObject):
    start = pyqtSignal(object)
    finish = pyqtSignal(object)
    error = pyqtSignal(object)
    
    def __init__(self, app: str, parent=None):
        super(External, self).__init__(parent)
        self.app = app

    @pyqtSlot()
    def run(self):
        try:
        	# Iniciamos la instalacion
        	# Enviamos la señal
            self.start.emit(self.app)
            # comandos para instalar la app
            print("Comenzando Instalacion de la aplicacion")
            comando = 'apt install {}'.format(self.app)
            print(comando)
            #os.system(comando)
            time.sleep(6)
        except:
            self.error.emit(self.app)
            print("Algo a fallado")
        finally:
            self.finish.emit(self.app)
            print("Proceso finalizado")
