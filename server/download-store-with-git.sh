#!/bin/sh

Fmt="printf"

WORK_DIR=~/temp
REPO_NAME=deepines-store
REPO_URL="https://github.com/deepin-espanol/$REPO_NAME"
BRANCH=nightly

FOLDER_EXISTS="La carpeta '%s' existe.\n"
FOLDER_NO_EXISTS="La carpeta '%s' no existe.\n"

Directory() {
	[ -d "$1" ] || {
		$Fmt "$FOLDER_NO_EXISTS" "$1"
		return 1
	}
	$Fmt "$FOLDER_EXISTS" "$1"
	return 0
}

# Check if git is installed.
if [ -z "$(which git)" ]; then
	echo "Para descargar la tienda ($REPO_URL) es necesario instalar primero Git."
	echo "Instale Git con el siguiente comando:"
	echo "sudo apt install git"
	exit 1
fi

if ! Directory $WORK_DIR; then
	echo "Creando '$WORK_DIR'."
	mkdir $WORK_DIR
fi

cd $WORK_DIR || exit 1

if ! Directory "$WORK_DIR/$REPO_NAME"; then
	echo "Usando repositorio '$REPO_URL'..."
	git clone $REPO_URL
fi

cd "$WORK_DIR/$REPO_NAME" || exit 1

git checkout $BRANCH # Switch to the branch with the most recent files.
git pull             # Download new files.
