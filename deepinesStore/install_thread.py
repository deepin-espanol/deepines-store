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
        self.errores = ('Err:', 'Ign:',
            'Fallo temporal al resolver',
            'No se pudieron obtener algunos archivos',
            '101: La red es inaccesible', '101: network is unreachable',
            'dependencias inclumplidas',
            'No se pudo bloquear', 'Unable to acquire the dpkg')

    @pyqtSlot()
    def run(self):
        validacion = True # Comprobar si es posible usar apt
        self.update.emit()
        # TODO: Don't use Popen!!
        update = subprocess.Popen(["sudo", "apt", "update"], 
                 stdout=subprocess.PIPE, universal_newlines=True)
        try:
            while not update.poll():
                line = update.stdout.readline()
                
                if line != '\n':
                    self.progress.emit(line)

                if not line:
                    break
        except:
            # Ocurre algun error no controlado
            self.error.emit(1)

        for elemento in self.app:
            error = 0
            """
            error = 0 -> sin error
            error = 1 -> excepcion no controlada
            error = 2 -> error en red de internet
            error = 3 -> error de dependencias
            error = 4 -> apt en uso por otra app
            """
            try:
            	# Iniciamos la instalacion
                self.start.emit(elemento)
            	# Enviamos la señal
                # comandos para instalar la app
                comando = ["sudo", "DEBIAN_FRONTEND=noninteractive",
                 "apt", "-q", "-y","install", elemento]
                        
                ejecucion = subprocess.Popen(comando, 
                            stdout=subprocess.PIPE, universal_newlines=True)
                while not ejecucion.poll():
                    line = ejecucion.stdout.readline()
                    # Caso de que la primera linea este vacia
                    if validacion and not line:
                        error = 4
                    # Cambiamos el validador para que no vuelva a ingresar
                    validacion = False
                    print(f"linea: {line}")
                    if line != '\n':
                        if ('101: La red es inaccesible' in line or 
                            '101: network is unreachable' in line or 
                            'Fallo temporal al resolver' in line or
                            'No se pudieron obtener algunos archivos' in line):
                            error = 2

                        if ('dependencias incumplidas' in line): error = 3

                        if ('No se pudo bloquear' in line or
                            'Unable to acquire the dpkg' in line):
                            error = 4
                        
                        for err in self.errores:
                            if err in line:
                                line = ""
                        
                        self.progress.emit(line)
                    
                    if not line:
                        break
                    
                else:
                    if error == 0: 
                        self.finish.emit(elemento)

                    else:
                        self.error.emit(error)
                        return 0
                        
            except:
                # Ocurre algun error no controlado
                self.error.emit(1)
                return 0
        else:
            # Termino del ciclo for
            self.complete.emit()


