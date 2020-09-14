#! /bin/sh

FILE1="/etc/apt/trusted.gpg.d/deepines.asc"
FILE2="/etc/apt/sources.list.d/deepines.list"
FILE3="/usr/share/doc/deepines-store/copyright"
FILE4="/usr/share/deepines/deepinesStore/"
for F in "${FILE1}" "${FILE2}" "${FILE3}" "${FILE4}"; do
if [ -f "${F}" ]; then
  echo $F exite
elif [ -d "${F}"  ]; then
  echo $F exite
fi
done