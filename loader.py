#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os
import json
import locale

cmd = ["pkexec", "/usr/share/deepines/deepines", "-l", locale.getdefaultlocale()[0], "--env", json.dumps(os.environ.copy())]

subprocess.run(cmd, check=True)