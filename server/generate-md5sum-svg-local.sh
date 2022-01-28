#!/bin/sh

# shellcheck disable=SC1007
SH_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
REPO_DIR="$SH_DIR/.."
SVG_DIR="$REPO_DIR/deepinesStore/resources/apps"
SVG_LIST_DIR="$REPO_DIR/deepinesStore/config"
SVG_LIST_NAME=svg_checksum

echo "Creando lista md5sum de archivos SVG de la Tienda Deepines."

cd "$SVG_LIST_DIR" || { echo "No se encontró la carpeta de scripts '$SVG_LIST_DIR'." && exit 1; }
cd "$SVG_DIR" || { echo "No se encontró la carpeta de SVG '$SVG_DIR'." && exit 1; }

echo "$SVG_LIST_DIR/$SVG_LIST_NAME"

find . -type f -name "*.svg" -exec md5sum {} \; |
	sed "s|\./||" >"$SVG_LIST_DIR/$SVG_LIST_NAME"
