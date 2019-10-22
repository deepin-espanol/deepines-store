#!/usr/bin/python3
# -*- coding: utf-8 -*-
import subprocess
from os.path import join, abspath, dirname

def resolver_ruta():

    ruta = '/usr/share/deepines/main.py'
    comando = 'pkexec env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY python3 ' + ruta

    return comando

subprocess.run(resolver_ruta(), shell=True)