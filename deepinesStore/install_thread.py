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
    error = pyqtSignal(object)
    
    def __init__(self, app):
        super(External, self).__init__()
        self.app = app
        self.errores = ('Err:', 
            'fallo temporal al resolver «mirror.deepines.com»',
            '101: La red es inaccesible', '101: network is unreachable')

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
            """
            error = 0 -> sin error
            error = 1 -> excepcion no controlada
            error = 2 -> error en red de internet
            error = 3 -> error en apt
            """
            error = 0
            try:
            	# Iniciamos la instalacion
            	# Enviamos la señal
                self.start.emit(elemento)
                # comandos para instalar la app
                comando = ["sudo", "DEBIAN_FRONTEND=noninteractive",
                 "apt", "-q", "-y","install", elemento]
                        
                ejecucion = subprocess.Popen(comando, 
                            stdout=subprocess.PIPE, universal_newlines=True)
                while not ejecucion.poll():
                    line = ejecucion.stdout.readline()
                    if line != '\n':
                        for err in self.errores:
                            if err in line:
                                line = ""
                        self.progress.emit(line)
                    
                    if ('101: La red es inaccesible' in line or 
                    '101: network is unreachable'): error = 2


                    if not line:
                        if error == 0: 
                            self.finish.emit(elemento)
                        break

            except:
                # Ocurre algun error
                self.error.emit(0)
        else:
            # Termino del ciclo for
            if error == 0:
                self.complete.emit()
            else:
                self.error.emit(error)

