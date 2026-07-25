#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os
import json

FORWARDED_ENV_NAMES = {
	"DBUS_SESSION_BUS_ADDRESS", "DESKTOP_SESSION", "DISPLAY", "GDK_DPI_SCALE",
	"GDK_SCALE", "GTK_THEME", "HTTP_PROXY", "HTTPS_PROXY", "LANG", "LANGUAGE",
	"NO_PROXY", "QT_AUTO_SCREEN_SCALE_FACTOR", "QT_FONT_DPI", "QT_QPA_PLATFORM",
	"QT_SCALE_FACTOR", "QT_SCREEN_SCALE_FACTORS", "QT_STYLE_OVERRIDE",
	"WAYLAND_DISPLAY", "XAUTHORITY", "XDG_CURRENT_DESKTOP", "XDG_DATA_DIRS",
	"XDG_SESSION_DESKTOP", "XDG_SESSION_TYPE", "http_proxy", "https_proxy",
	"no_proxy",
}
forwarded_env = {
	key: value for key, value in os.environ.items()
	if key in FORWARDED_ENV_NAMES or key.startswith("LC_")
}
cmd = ["pkexec", "/usr/share/deepines/deepines", "--env", json.dumps(forwarded_env)]

subprocess.run(cmd, check=True)
