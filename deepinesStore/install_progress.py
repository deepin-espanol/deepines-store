# sudo apt install python3-apt
# paste in your venv
# sudo cp -r /usr/lib/python3/dist-packages/apt* ~/.virtualenvs/deepines/lib/python3.11/site-packages/
import apt
import apt.progress.base
import subprocess as sp
from PyQt5.QtCore import QThread, pyqtSignal
from deepinesStore.app_info import AppType

class ProgressHandler(apt.progress.base.AcquireProgress):
    def __init__(self, update_signal):
        super().__init__()
        self.update_signal = update_signal

    def pulse(self, owner):
        current = self.current_bytes / 1024 / 1024  # Convertir a MB
        total = self.total_bytes / 1024 / 1024  # Convertir a MB
        if total > 0:
            percent = int(current / total * 100)
            self.update_signal.emit(f"Descargando... {percent}% ({current:.2f}/{total:.2f} MB)")
        return True

    def start(self):
        self.update_signal.emit("Iniciando descarga...")

    def stop(self):
        self.update_signal.emit("Descarga completada")

class UpdateProgress(apt.progress.base.OpProgress):
    def __init__(self, update_signal):
        super().__init__()
        self.update_signal = update_signal

    def update(self, percent=None):
        if percent:
            self.update_signal.emit(f"Actualizando caché... {percent:.2f}%")
        else:
            self.update_signal.emit("Actualizando caché...")

class InstallProgressHandler(apt.progress.base.InstallProgress):
    def __init__(self, update_signal):
        super().__init__()
        self.update_signal = update_signal

    def status_change(self, pkg, percent, status):
        self.update_signal.emit(f"Instalando: {status} - {percent}%")

class InstallThread(QThread):
    update_signal = pyqtSignal(str)
    name_process_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool)

    def __init__(self, package_list):
        super().__init__()
        self.package_list = package_list
        self._is_running = True
        self.first_update = True

    def run(self):
        try:
            for package in self.package_list:
                if not self._is_running:
                    break
                if package.type == AppType.DEB_PACKAGE:
                    if self.first_update:
                        cache = apt.Cache()
                        self.name_process_signal.emit("Actualizando lista de paquetes...")
                        self.update_signal.emit("Actualizando lista de paquetes...")
                        try:
                            cache.update(fetch_progress=ProgressHandler(self.update_signal))
                        except apt.cache.FetchFailedException as e:
                            error_msg = f"Error durante la actualización del caché: {str(e)}"
                            print(error_msg)
                            self.update_signal.emit(error_msg)
                            self.finished_signal.emit(False)
                            return
                        self.first_update = False
                    cache.open(progress=UpdateProgress(self.update_signal))
                    package_name = package.id
                    self.name_process_signal.emit(f'Instalando: {package.name} desde repositorio Deepines')
                    self.update_signal.emit(f"Buscando paquete {package_name}...")
                    if package_name not in cache:
                        error_msg = f"Paquete {package_name} no encontrado"
                        print(error_msg)
                        self.update_signal.emit(error_msg)
                        self.finished_signal.emit(False)
                        return
                    
                    pkg = cache[package_name]
                    if pkg.is_installed:
                        self.update_signal.emit(f"{package_name} ya está instalado.")
                    else:
                        try:
                            self.update_signal.emit(f"Marcando {package_name} para instalación...")
                            pkg.mark_install()
                        except apt.cache.DependencyCache.DependencyError as e:
                            error_msg = f"Error de dependencias para {package_name}: {str(e)}"
                            print(error_msg)
                            self.update_signal.emit(error_msg)
                            self.finished_signal.emit(False)
                            return
                        
                        self.update_signal.emit(f"Descargando e instalando {package_name}...")
                        try:
                            cache.commit(fetch_progress=ProgressHandler(self.update_signal),
                                         install_progress=InstallProgressHandler(self.update_signal))
                            
                            # Verificar si el paquete se instaló correctamente
                            cache.open(progress=UpdateProgress(self.update_signal))
                            if cache[package_name].is_installed:
                                self.update_signal.emit(f"{package_name} se ha instalado correctamente.")
                            else:
                                error_msg = f"{package_name} no se pudo instalar correctamente, posiblemente debido a errores de dependencias."
                                print(error_msg)
                                self.update_signal.emit(error_msg)
                                self.finished_signal.emit(False)
                                return
                        except apt.cache.LockFailedException as e:
                            error_msg = f"Error de bloqueo durante la instalación: {str(e)}"
                            print(error_msg)
                            self.update_signal.emit(error_msg)
                            self.finished_signal.emit(False)
                            return
                        except apt.cache.FetchFailedException as e:
                            error_msg = f"Error de descarga durante la instalación: {str(e)}"
                            print(error_msg)
                            self.update_signal.emit(error_msg)
                            self.finished_signal.emit(False)
                            return
                        except apt.cache.FetchCancelledException as e:
                            error_msg = f"Descarga cancelada: {str(e)}"
                            print(error_msg)
                            self.update_signal.emit(error_msg)
                            self.finished_signal.emit(False)
                            return
                        except apt.cache.InstallFailedException as e:
                            error_msg = f"Error durante la instalación: {str(e)}"
                            print(error_msg)
                            self.update_signal.emit(error_msg)
                            self.finished_signal.emit(False)
                            return
                        except SystemError as e:
                            error_msg = f"Error del sistema durante la instalación: {str(e)}"
                            print(error_msg)
                            self.update_signal.emit(error_msg)
                            self.finished_signal.emit(False)
                            return
                        except Exception as e:
                            error_msg = f"Error inesperado: {str(e)}"
                            print(error_msg)
                            self.update_signal.emit(error_msg)
                            self.finished_signal.emit(False)
                            return

                elif package.type == AppType.FLATPAK_APP:
                    app_id = package.id
                    self.name_process_signal.emit(f"Instalando {app_id} desde Flathub...")
                    self.update_signal.emit(f"Instalando {app_id} desde Flathub...")

                    process = sp.Popen(['flatpak', 'install', '-y', 'flathub', app_id], stdout=sp.PIPE, stderr=sp.PIPE, text=True)

                    while True:
                        if not self._is_running:
                            process.terminate()
                            break
                        output = process.stdout.readline()
                        if output == '' and process.poll() is not None:
                            break
                        if output:
                            print(output.strip())
                            self.update_signal.emit(output.strip())

                    stderr = process.communicate()[1]
                    if stderr:
                        print(stderr.strip())
                        self.update_signal.emit(stderr.strip())

                    if process.returncode == 0:
                        self.update_signal.emit(f"{app_id} se ha instalado correctamente.")
                    else:
                        error_msg = f"Error instalando {app_id}: {stderr}"
                        print(error_msg)
                        self.update_signal.emit(error_msg)
                        self.finished_signal.emit(False)
                        return
            
            if self._is_running:
                print("Instalación completada con éxito.")
                self.finished_signal.emit(True)

        except Exception as e:
            import traceback
            error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            self.update_signal.emit(error_msg)
            self.finished_signal.emit(False)

    def stop(self):
        self._is_running = False
        self.wait()
