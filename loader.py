#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import locale

cmd = f"pkexec /usr/share/deepines/deepines -l '{locale.getdefaultlocale()[0]}' -d $XDG_CURRENT_DESKTOP"
subprocess.check_call(cmd, shell=True)
