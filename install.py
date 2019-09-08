import sys
# Importamos las librerias necesarias
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
import time

# Creamos la clase y heredamos de QThread
class External(QObject):
    finished = pyqtSignal()
    intReady = pyqtSignal(int, str)
    
    def __init__(self, app: str, parent=None):
        super(External, self).__init__(parent)
        #finished = pyqtSignal()
        self.app = app

    @pyqtSlot()
    def run(self):
        try:
            self.intReady.emit(1, self.app)
            # comandos para instalar la app
            print("Comenzando Instalacion de la aplicacion")
            comando = 'apt install {}'.format(self.app)
            print(comando)
            #os.system(comando)
            time.sleep(5)
        except:
            self.intReady.emit(0, self.app)
            print("Algo a fallado")
        finally:
            self.intReady.emit(2, self.app)
            self.finished.emit()
            #self.finished.emit()
            print("Proceso finalizado")
