#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess

command = f'pkexec /usr/share/deepines/deepines'
subprocess.check_call(command, shell=True)