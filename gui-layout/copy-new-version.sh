#!/bin/bash

DST=../src
NAMES=("mpadd" "mpgui")

for name in ${NAMES[@]} ; do
  cp -t ${DST} ${name}.py ${name}_ui.py
  chmod u+rw ${DST}/${name}_ui.py
done
