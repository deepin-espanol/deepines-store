#!/bin/bash

# Las rutas de las carpetas deben terminar con '/'
CARPETA_DE_TRABAJO="/usr/share/deepines/deepinesStore/resources/apps/"
CARPETA_GUARDAR_LISTA_SVG="/home/jaca/desarrollo/github/store_deepines/server/"
NOMBRE_ARCHIVO_LISTA_SVG="svg_checksum"


echo Creando lista md5sums de los archivos SVG de la Tienda Deepines


cd $CARPETA_DE_TRABAJO

# Borrar la lista antes de volver a crearla
echo $CARPETA_GUARDAR_LISTA_SVG$NOMBRE_ARCHIVO_LISTA_SVG
cat /dev/null > $CARPETA_GUARDAR_LISTA_SVG$NOMBRE_ARCHIVO_LISTA_SVG

# Listar solo los archivos .svg
LISTA_ARCHIVOS=$(find ./ -type f -name  "*.svg" )

for i in $LISTA_ARCHIVOS; do

	echo $i
	md5sum "$(echo $i | sed "s/^\.\///")" >> $CARPETA_GUARDAR_LISTA_SVG$NOMBRE_ARCHIVO_LISTA_SVG

done

