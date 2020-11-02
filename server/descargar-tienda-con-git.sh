#!/bin/bash

CARPETA_TRABAJO=~/temp
URL_REPOSITORIO="https://github.com/s384/store_deepines.git"  #repositorio en github
NOMBRE_REPOSITORIO=$(echo $URL_REPOSITORIO | cut -d / -f5 | sed "s|.git||")
RAMA=Develop

#Comprobar si git está instalado
if [[ -z $(which git) ]]; then
	#statements
	echo "El comando git es necesario para descargar la tienda desde $URL_REPOSITORIO"
	echo "Instale git con el siguiente comando"
	echo "sudo apt install git"

	exit 1
fi

if [[ -d $CARPETA_TRABAJO ]]; then

	echo "La carpeta $CARPETA_TRABAJO existe"

else

	echo "La carpeta $CARPETA_TRABAJO no existe"
	echo "Creando $CARPETA_TRABAJO"
	mkdir $CARPETA_TRABAJO

fi

cd $CARPETA_TRABAJO

if [[ -d $CARPETA_TRABAJO/$NOMBRE_REPOSITORIO ]]; then

	echo "La carpeta $CARPETA_TRABAJO/$NOMBRE_REPOSITORIO existe"

else

	echo "La carpeta $CARPETA_TRABAJO/$NOMBRE_REPOSITORIO no existe"
	echo "Cloando repositorio $URL_REPOSITORIO"
	git clone $URL_REPOSITORIO

fi

cd $NOMBRE_REPOSITORIO

#cambiar a la rama con los archivos mas recientes
git checkout $RAMA

#descargar archivos nuevos
git pull