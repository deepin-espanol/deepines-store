#!/usr/bin/env python3
import os
import threading
import time

from demoted_actions import notify, run_cmd, DEF

DESC = os.environ.get('DEEPINES_NOTIFY_DESC')
TITLE = os.environ.get('DEEPINES_NOTIFY_TITLE')
LATER = os.environ.get('DEEPINES_NOTIFY_LATER')
RESTART = os.environ.get('DEEPINES_NOTIFY_RESTART')

# If the installer PID was passed, wait for it to exit before showing the notification.
# So the notification appears only after the invoker (installer) has finished...
gp_env = os.environ.get('DEEPINES_INSTALLER_PID')
if gp_env:
	try:
		gp_pid = int(gp_env)
	except Exception:
		gp_pid = None
	else:
		# Busy-wait until /proc/<pid> disappears!
		while gp_pid > 0 and os.path.exists(f'/proc/{gp_pid}'):
			time.sleep(0.25)

e = threading.Event()

def handler(action):
	if action == 'restart':
		run_cmd(DEF, ['dbus-send', '--session', '--print-reply', '--dest=com.deepin.dde.shutdownFront', '/com/deepin/dde/shutdownFront', 'com.deepin.dde.shutdownFront.Restart'])
	e.set()

notify(desc=DESC, title=TITLE, actions=[('later', LATER), ('restart', RESTART)], handler=handler)
e.wait()
