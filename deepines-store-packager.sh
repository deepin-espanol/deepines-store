#!/bin/sh

Main() {
    unset VER MANUAL AUTO
    while getopts ":v:ma" OPTION >/dev/null 2>&1; do
        case $OPTION in
        v) VER=$OPTARG ;;
        m) MANUAL=true ;;
        a) AUTO=true ;;
        :) echo >&2 "Option '$OPTARG' requires a version to be specified." && exit 1 ;;
        *) echo >&2 "Unknown option: '$OPTARG'." && echo "Usage: ${0##*/} [-v 'version'] [-m] [-a]" && exit 1 ;;
        esac
    done
    if [ -z "$VER" ]; then
        echo >&2 "The '-v' option is mandatory and requires a version to be specified." && exit 1
    fi
    SetVariables
    if [ "$AUTO" = true ]; then
        echo "Starting automatic mode."
        ShowDetails
    else
        Welcome
    fi
}

Cleanup() { rm -R "$TEMP_DIR" >/dev/null 2>&1; }
CleanupAndExit() {
    Cleanup
    exit 130
}
trap "CleanupAndExit" INT

SetVariables() {
    PKG_NAME=deepines-store
    PKG_VER=$VER
    PKG_DEV="Deepin en Español <soporte@deepines.com>"
    PKG_ARCH=all
    PKG_FULL_NAME=${PKG_NAME}_${PKG_VER}_${PKG_ARCH}
    PKG_SRC="https://github.com/deepin-espanol/deepines-store"
    PKG_BUGS="$PKG_SRC/issues"
    SH_DIR="$(pwd -P)"
    TEMP_DIR="$(mktemp -d)"
    WORK_DIR="$TEMP_DIR/$PKG_FULL_NAME"
}

# shellcheck disable=SC2016
PREINSTSCRIPT='#!/bin/sh

set -e

CNFMOD="/usr/share/debconf/confmodule"
if [ -f "${CNFMOD}" ]; then
	. "${CNFMOD}"
fi

SEPARATOR="=============================================================="
COMPATIBLE_VERSIONS="Deepines Store is only compatible with Deepin 20 and Deepin 23"
WE_RECOMMEND="  We recommend installing a recent version of Deepin. If you
  are using Deepin 20, check that the configuration of the
  repositories does not contain errors."

case "${LANGUAGE:-$LANG}" in
es*)
	COMPATIBLE_VERSIONS="Tienda Deepines sólo es compatible con Deepin 20 y Deepin 23"
	WE_RECOMMEND=" Recomendamos instalar una versión reciente de Deepin. Si está
 usando Deepin 20, compruebe que la configuración de 
 los repositorios no contiene errores."
	;;
esac

UnsupportedOS() {
	echo >&2 "$SEPARATOR"
	echo >&2 "$COMPATIBLE_VERSIONS"
	echo >&2
	echo >&2 "$WE_RECOMMEND"
	echo >&2 "$SEPARATOR"
	db_go || true
	exit 1
}

CheckSupportedOS() {
	DIST_ID=$(lsb_release -is)
	REL_NUM=$(lsb_release -rs)
	if [ "$DIST_ID" = "Deepin" ]; then
		case $REL_NUM in
		20 | 20.*) ;;
		"23 Nightly" | 23 | 23.*) ;;
		*) UnsupportedOS ;;
		esac
	else
		UnsupportedOS
	fi
}

case "$1" in
install | upgrade)
	CheckSupportedOS
	;;
esac

exit 0
'

# shellcheck disable=SC2016
POSTINSTSCRIPT='#!/bin/sh

set -e

CNFMOD="/usr/share/debconf/confmodule"
if [ -f "${CNFMOD}" ]; then
	. "${CNFMOD}"
fi

Fmt="printf"

SOURCES_DIR=/etc/apt/sources.list.d
REPO="deb http://repositorio.deepines.com/pub/deepines/%d/ stable main"

INSTALLING_DEEPINES="Installing Deepines %d repository and key..."
INSTALLING_DONE=" done.\n"
INSTALLING_FAILED=" failed:\n"

case "${LANGUAGE:-$LANG}" in
es*)
	INSTALLING_DEEPINES="Instalando repositorio y clave de Deepines %d..."
	INSTALLING_DONE=" hecho.\n"
	INSTALLING_FAILED=" falló:\n"
	;;
esac

TRUSTED_DIR=/etc/apt/trusted.gpg.d
SOURCES_DIR=/etc/apt/sources.list.d
DEEPINES_LIST=$SOURCES_DIR/deepines.list
DEEPINES_KEY=$TRUSTED_DIR/deepines.asc

MakeRepoKey() {
	cat <<EOF
-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: GnuPG v1

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
TGGtKg==
=ym7H
-----END PGP PUBLIC KEY BLOCK-----
EOF
}

InstallFiles() {
	REPO="deb http://repositorio.deepines.com/pub/deepines/%d/ stable main"
	mkdir -p $TRUSTED_DIR
	mkdir -p $SOURCES_DIR
	$Fmt "${REPO}\n" "$1" >$DEEPINES_LIST
	MakeRepoKey >$DEEPINES_KEY
}

InstallDeepinesRepository() {
	$Fmt "${INSTALLING_DEEPINES}" "$1" && RepoInstallationResult=$(
		InstallFiles "$1" 2>&1
	) || {
		$Fmt "$INSTALLING_FAILED"
		echo "$RepoInstallationResult"
		db_go || true
		exit 1
	} && $Fmt "$INSTALLING_DONE"
}

InstallDeepines() {
	REL_NUM=$(lsb_release -rs)
	case $REL_NUM in
	20 | 20.*) InstallDeepinesRepository 4 ;;
	"23 Nightly" | 23 | 23.*) InstallDeepinesRepository 5 ;;
	esac
}

case "$1" in
configure)
	InstallDeepines
	;;
esac

exit 0
'

# shellcheck disable=SC2016
POSTRMSCRIPT='#!/bin/sh

set -e

CNFMOD="/usr/share/debconf/confmodule"
if [ -f "${CNFMOD}" ]; then
	. "${CNFMOD}"
fi

DeleteFiles() {
	FILE1="/etc/apt/trusted.gpg.d/deepines.asc"
	FILE2="/etc/apt/sources.list.d/deepines.list"
	FILE3="/usr/share/doc/deepines-store/"
	FILE4="/usr/share/deepines/deepinesStore/"
	for F in "${FILE1}" "${FILE2}" "${FILE3}" "${FILE4}"; do
		if [ -f "${F}" ]; then
			rm -f "${F}"
		elif [ -d "${F}" ]; then
			rm -rf "${F}"
		fi
	done
}

case "$1" in
remove | purge | abort-upgrade)
	DeleteFiles
	db_purge
	;;
abort-install)
	db_purge
	;;
esac

exit 0
'

ShowDetails() {
    echo "Packaging details:
Name: $PKG_NAME
Version: $PKG_VER
Architecture: $PKG_ARCH
Final package name: $PKG_FULL_NAME.deb
"
}

Welcome() {
    echo "Welcome to '$PKG_NAME' packaging assistant!" && sleep 1
    echo "This script will help you in the packaging process." && sleep 1
    echo "Press Ctrl+C at any time to cancel the process."
    echo
    ShowDetails
    printf "%s" 'Starting in ' && i=5 && while [ $i -gt 0 ]; do
        printf "%u... " "$i" && i=$((i - 1)) && sleep 1
    done && printf "%s\n" 'Now!'
    echo
}

Open() { # Create file (if needed), open and wait to finish...
    if [ "$MANUAL" = true ]; then
        touch "$1" >/dev/null 2>&1
        echo "Manually checking '$1'..."
        mimeopen -n "$1" >/dev/null 2>&1
    fi
}

Main "$@"

mkdir -p "$WORK_DIR/DEBIAN"
cd "$WORK_DIR" || exit 1

echo "Copying scripts..."
mkdir -p usr/share/deepines/deepinesStore
rsync -aqr --exclude='translations' --exclude="remote_svg.txt" \
    --exclude="*.pyc" --exclude='__pycache__' --exclude='svg_checksum' \
    "$SH_DIR/deepinesStore" usr/share/deepines
cp -a "$SH_DIR/deepines.py" usr/share/deepines/deepines

echo "Updating user interface version..."
sed -i "s/[[]VERSION[]]/$PKG_VER/" usr/share/deepines/deepinesStore/maing.py

GenerateMainBinary() {
    cat <<EOF
#!/bin/sh
pkexec /usr/share/deepines/deepines
EOF
}

echo "Generating main binary..."
mkdir -p usr/bin
GenerateMainBinary >usr/bin/deepines

echo "Generating translations..."
mkdir -p usr/share/deepines/deepinesStore/translations
for ts_file in "$SH_DIR"/translations/*.ts; do
    lconvert -i "$ts_file" -o "usr/share/deepines/deepinesStore/translations/$(basename "$ts_file" .ts).qm"
done

MakeDesktop() {
    cat <<EOF
[Desktop Entry]
Name=Deepines Store
Name[es]=Tienda Deepines
Version=1.1
Exec=deepines
Comment=Application store for the deepines repository
Comment[es]=Tienda de aplicaciones para el repositorio de deepines
Icon=deepines
Type=Application
Terminal=false
StartupNotify=true
Encoding=UTF-8
Categories=System;
EOF
}

echo "Generating .desktop..."
mkdir -p usr/share/applications
MakeDesktop >usr/share/applications/deepines.desktop

echo "Generating icons..."
HICOLORPATH="usr/share/icons/hicolor"
RESSVG="usr/share/deepines/deepinesStore/resources/deepines.svg"
ICONSVG="$HICOLORPATH/scalable/apps/deepines.svg"
mkdir -p $HICOLORPATH/scalable/apps
mv "$RESSVG" "$ICONSVG"
ICONS="16:24:32:48:64:128"
CDR="${ICONS}:"
while [ -n "$CDR" ]; do
    ICONSZ=${CDR%%:*}
    mkdir -p $HICOLORPATH/${ICONSZ}x${ICONSZ}/apps
    rsvg-convert -w "$ICONSZ" "$ICONSVG" -o $HICOLORPATH/${ICONSZ}x${ICONSZ}/apps/deepines.png ||
        echo >&2 "Couldn't found the icon to convert!"
    CDR=${CDR#*:}
done
unset ICONSZ CDR
ln -sf "../../../icons/hicolor/scalable/apps/deepines.svg" "$RESSVG"

MakePolkitPolicy() {
    cat <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE policyconfig PUBLIC
 "-//freedesktop//DTD PolicyKit Policy Configuration 1.0//EN"
 "http://www.freedesktop.org/standards/PolicyKit/1/policyconfig.dtd">

<policyconfig>
    <vendor>DeepinenEspañol</vendor>
    <vendor_url>https://deepinenespañol.org/</vendor_url>
    <icon_name>deepines</icon_name>
    <action id="deepines">
        <description>Allows the installation of applications stored in the deepines repository</description>
        <description xml:lang="es">Permite la instalación de aplicaciones almacenadas en el repositorio de deepines</description>
        <message>Deepines Store requires authentication</message>
        <message xml:lang="es">Tienda Deepines requiere autenticación</message>
        <defaults>
          <allow_any>auth_admin</allow_any>
          <allow_inactive>auth_admin</allow_inactive>
          <allow_active>auth_admin</allow_active>
        </defaults>
        <annotate key="org.freedesktop.policykit.exec.path">/usr/share/deepines/deepines</annotate>
        <annotate key="org.freedesktop.policykit.exec.allow_gui">true</annotate>
  </action>

</policyconfig>
EOF
}

echo "Generating Polkit action..."
mkdir -p usr/share/polkit-1/actions
MakePolkitPolicy >usr/share/polkit-1/actions/org.freedesktop.deepines.policy

echo "Generating 'preinst' script..."
printf "%s" "$PREINSTSCRIPT" >DEBIAN/preinst
chmod 755 DEBIAN/preinst

echo "Generating 'postinst' script..."
printf "%s" "$POSTINSTSCRIPT" >DEBIAN/postinst
chmod 755 DEBIAN/postinst

echo "Generating 'postrm' script..."
printf "%s" "$POSTRMSCRIPT" >DEBIAN/postrm
chmod 755 DEBIAN/postrm

SY="2020"
CY=$(date +%Y)
YEAR=$(if [ "$SY" = "$CY" ]; then echo "$CY"; else echo "$SY-$CY"; fi)

MakeCopyright() {
    cat <<EOF
Format: http://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: $PKG_NAME
Upstream-Contact: $PKG_BUGS
Source: $PKG_SRC
License: Apache-2.0

Files: *
Copyright: $YEAR $PKG_DEV
License: Apache-2.0
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
 http://www.apache.org/licenses/LICENSE-2.0
 .
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 .
 On Debian systems, the complete text of the Apache version 2.0
 license can be found in "/usr/share/common-licenses/Apache-2.0".
EOF
}

echo "Generating copyright file..."
mkdir -p usr/share/doc/$PKG_NAME
MakeCopyright >usr/share/doc/$PKG_NAME/copyright

echo "Generating changelog..."
Open "$SH_DIR/changelog" # (-m) Manually update the changelog file.
# TODO: Use dch (devscripts package) if available.
gzip -9n <"$SH_DIR/changelog" >usr/share/doc/$PKG_NAME/changelog.gz

# Generate md5sums.
find . -not \( -path ./DEBIAN -prune \) -type f -exec md5sum {} \; |
    sed "s|\./||" >DEBIAN/md5sums

# Generate 'Installed-Size' variable.
INSIZE=$(du -s --exclude='DEBIAN/*' | grep -Eo "[0-9]*")
Open "./DEBIAN/" # (-m) Manually update preinst, postinst, etc.

P3=python3

GenerateControl() {
    cat <<EOF
Package: $PKG_NAME
Version: $PKG_VER
Architecture: $PKG_ARCH
Installed-Size: $INSIZE
Section: admin
Maintainer: $PKG_DEV
Homepage: $PKG_SRC
Priority: optional
Pre-Depends: debconf (>= 0.5)
Depends: $P3, $P3-pyqt5, $P3-requests, $P3-bs4, libqt5designer5, libqt5help5, $P3-certifi, $P3-html5lib, $P3-idna, $P3-lxml, $P3-sip, $P3-soupsieve, $P3-urllib3, $P3-webencodings
Replaces: deepines-repository (<= 1:4.1), deepines-store:amd64 (<= 1.3.3)
Description: Deepines repository, key and Store
 Deepines unofficial repository and Store by deepinenespañol.org
EOF
}

echo "Generating control file..."
GenerateControl >DEBIAN/control
Open "./DEBIAN/control" # (-m) Manually update the control file.

echo "Fixing permissions..."                     # For lintian mainly.
find . -type d -exec chmod 755 {} \;             # Set all directory permissions to 755 (non-standard-dir-perm).
find . -executable -type f -exec chmod 755 {} \; # Set all executable files permissions to 755 (non-standard-executable-perm).
find usr/share -type f -exec chmod 644 {} \;     # Set all usr/share file permissions to 644 (non-standard-file-perm).
find usr/bin -type f -exec chmod +x {} \;        # Mark each script as executable.
chmod +x usr/share/deepines/deepines             # Mark main script as executable (script-not-executable).

echo "Build package..."
# Should use "dpkg-buildpackage -rfakeroot" instead, but no.
fakeroot dpkg-deb --build "$WORK_DIR" "$SH_DIR" || {
    Cleanup
    exit 1
}

echo "Finished!"
Cleanup
exit 0
