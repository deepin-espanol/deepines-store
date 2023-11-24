#!/usr/bin/env python3
import os
from subprocess import Popen, PIPE, check_output, CalledProcessError
import platform

from deepinesStore.core import lang, default_env


def get_real_uid():
	uid = os.geteuid()
	if uid == 0:
		if 'SUDO_UID' in default_env:
			return default_env["SUDO_UID"]
		elif 'PKEXEC_UID' in default_env:
			return default_env["PKEXEC_UID"]
		else:
			return uid
	else:
		return uid


def set(uid: int, gid: int):
	def new_ids():
		os.setgid(gid)
		os.setuid(uid)
	return new_ids


class UserDefault:
	def __init__(self, uid: int):
		import pwd
		self.uid = uid
		self.user = pwd.getpwuid(uid)
		self.name = self.user.pw_name
		self.gid = self.user.pw_gid
		self.home = self.user.pw_dir
		self.env = {**default_env, 'USER': self.name, 'LOGNAME': self.name, 'PWD': os.getcwd(), 'HOME': self.home,
		'LANG': lang, 'LANGUAGE': lang, 'DBUS_SESSION_BUS_ADDRESS': f'unix:path=/run/user/{uid}/bus'}


def run_cmd(user: UserDefault, cmd):
	return Popen(cmd, env=user.env, preexec_fn=set(user.uid, user.gid), stderr=PIPE, stdout=PIPE, encoding='utf8', universal_newlines=True)


if platform.system() == 'Windows':
	pass
else:
	UID = int(get_real_uid())
	DEF = UserDefault(UID)


def get_flatpak_info_cmd():
	p = ""
	try:
		p = check_output(['flatpak', 'remote-ls', 'flathub', '--app', '--columns=application,version'], text=True, env=DEF.env, preexec_fn=set(DEF.uid, DEF.gid))
	except CalledProcessError:
		print("Couldn't get flatpak app info: Error running flatpak command!")
	return p