import subprocess
# Importamos las librerias necesarias
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
import time


# Creamos la clase y heredamos de QThread
class External(QObject):
    start = pyqtSignal(object)
    progress = pyqtSignal(object)
    finish = pyqtSignal(object)
    complete = pyqtSignal()
    update = pyqtSignal()
    error = pyqtSignal()
    
    def __init__(self, app):
        super(External, self).__init__()
        self.app = app

    @pyqtSlot()
    def run(self):
        self.update.emit()
        update = subprocess.Popen(["sudo", "apt", "update"], 
                 stdout=subprocess.PIPE, universal_newlines=True)
        while not update.poll():
            line = update.stdout.readline()
            if line != '\n':
                self.progress.emit(line)
            if not line:
                break

        for elemento in self.app:
            try:
            	# Iniciamos la instalacion
            	# Enviamos la señal
                self.start.emit(elemento)
                # comandos para instalar la app
                comando = ["sudo", "apt", "install", elemento, "-y"]
                        
                ejecucion = subprocess.Popen(comando, 
                            stdout=subprocess.PIPE, universal_newlines=True)
                while not ejecucion.poll():
                    line = ejecucion.stdout.readline()
                    if line != '\n':
                        self.progress.emit(line)
                    
                    if not line:
                        break
            except:
                # Ocurre algun error
                self.error.emit()
            finally:
                # Finaliza correctamente
                self.finish.emit(elemento)
        else:
            # Termino del ciclo for
            self.complete.emit()