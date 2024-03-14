#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os
import json

cmd = ["pkexec", "/usr/share/deepines/deepines", "--env", json.dumps(os.environ.copy())]

subprocess.run(cmd, check=True)