#!/bin/sh

UpdTS() {
    SRC_FILES='deepinesStore/*.py'
    TS_FILES='translations/*.ts'
    TR_FUNCTION="__tr"
    pylupdate5 $SRC_FILES -ts $TS_FILES -tr-function $TR_FUNCTION
}

GenQM() {
    TS_d="translations"
    TS_DIR=${1:-$TS_d}
    QM_d="deepinesStore/translations"
    QM_DIR=${2:-$QM_d}
    mkdir -p $QM_DIR
    for ts_file in "$TS_DIR"/*.ts; do
    lconvert -i "$ts_file" -o "$QM_DIR"/"$(basename "$ts_file" .ts).qm"
    done
}

Run() {
    case $1 in
    update-ts) UpdTS ;;
    generate-qm) GenQM ;;
    *) echo >&2 "Specify update-ts or generate-qm." && exit 1 ;;
    esac
    echo "Done!"
    exit
}

Main() {
    unset VER MANUAL AUTO
    while getopts ":v:mar" OPTION >/dev/null 2>&1; do
        case $OPTION in
        v) VER=$OPTARG ;;
        m) MANUAL=true ;;
        a) AUTO=true ;;
        r) Run "$2" ;;
        :) echo >&2 "Option '$OPTARG' requires a version to be specified." && exit 1 ;;
        *) echo >&2 "Unknown option: '$OPTARG'." && echo "Usage: ${0##*/} [-v 'version'] [-m] [-a] [-r]" && exit 1 ;;
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
# shellcheck disable=SC2329
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
rsync -aqr --exclude='translations' --exclude="config" --exclude="remote_svg.txt" \
    --exclude="*.pyc" --exclude='__pycache__' --exclude='svg_checksum' \
    "$SH_DIR/deepinesStore" usr/share/deepines
cp -a "$SH_DIR/deepines.py" usr/share/deepines/deepines

echo "Updating user interface version..."
sed -i "s/[[]VERSION[]]/$PKG_VER/" usr/share/deepines/deepinesStore/core.py

echo "Copying main binary..."
mkdir -p usr/bin
cp -a "$SH_DIR/loader.py" usr/bin/deepines

echo "Generating app translations..."
GenQM "$SH_DIR"/translations "usr/share/deepines/deepinesStore/translations"

echo "Generating .desktop:"
mkdir -p usr/share/applications
deepin-desktop-ts-convert ts2desktop "$SH_DIR/data/desktop/deepines.desktop" \
    "$SH_DIR/data/desktop/translations" usr/share/applications/deepines.desktop

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

echo "Generating Polkit action:"
mkdir -p usr/share/polkit-1/actions
deepin-policy-ts-convert ts2policy "$SH_DIR/data/pkexec/org.freedesktop.deepines.policy" \
    "$SH_DIR/data/pkexec/translations" usr/share/polkit-1/actions/org.freedesktop.deepines.policy

echo "Writing 'preinst' script..."
cat "$SH_DIR/data/control/preinst" >DEBIAN/preinst
chmod 755 DEBIAN/preinst

echo "Writing 'postinst' script..."
cat "$SH_DIR/data/control/postinst" >DEBIAN/postinst
chmod 755 DEBIAN/postinst

echo "Writing 'postrm' script..."
cat "$SH_DIR/data/control/postrm" >DEBIAN/postrm
chmod 755 DEBIAN/postrm

YEAR="2025"

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
gzip -9n <"$SH_DIR/changelog" >usr/share/doc/$PKG_NAME/changelog.Debian.gz

BIN_UPPER=$(echo "deepines" | tr '[:lower:]' '[:upper:]')

MakeManPage() {
	cat <<EOF | gzip -9n
.TH $BIN_UPPER 1 "February 2022"

.SH NAME
deepines \- Install applications from the Deepines repository

.SH HOMEPAGE
.I $PKG_SRC
EOF
}

echo "Generating manual page..."
mkdir -p usr/share/man/man1 &&
MakeManPage >usr/share/man/man1/deepines.1.gz

# Generate md5sums.
find . -not \( -path ./DEBIAN -prune \) -type f -exec md5sum {} \; |
    sed "s|\./||" >DEBIAN/md5sums

# Get 'Installed-Size' variable (used in GenerateControl).
# shellcheck disable=SC2034
INSIZE=$(du -s --exclude='DEBIAN/*' | grep -Eo "[0-9]*")
Open "./DEBIAN/" # (-m) Manually update preinst, postinst, etc.

GenerateControl() {
    eval "cat <<EOF
$(cat "$SH_DIR/data/control/control.in")
EOF"
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
fakeroot dpkg-deb -Z xz --build "$WORK_DIR" "$SH_DIR" || {
    Cleanup
    exit 1
}

echo "Finished!"
Cleanup
exit 0
