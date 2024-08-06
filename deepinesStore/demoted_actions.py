#!/usr/bin/env python3
import os
from subprocess import Popen, PIPE, check_output, CalledProcessError
import platform

from deepinesStore.core import default_env


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
		'DBUS_SESSION_BUS_ADDRESS': f'unix:path=/run/user/{uid}/bus'}


def run_cmd(user: UserDefault, cmd):
	return Popen(cmd, env=user.env, preexec_fn=set(user.uid, user.gid), stderr=PIPE, stdout=PIPE, encoding='utf8', universal_newlines=True)


if platform.system() == 'Windows':
	pass
else:
	UID = int(get_real_uid())
	DEF = UserDefault(UID)


def browse(uri: str):
	if platform.system() == 'Linux':
		run_cmd(DEF, ['xdg-open', uri])
	else:
		import webbrowser
		try:
			webbrowser.open(uri)
			return True
		except webbrowser.Error:
			return False


def check_tg_handler():
	p = b""
	try:
		p = check_output(["xdg-mime", "query", "default", "x-scheme-handler/tg"], env=DEF.env, preexec_fn=set(DEF.uid, DEF.gid))
	except CalledProcessError as e:
		if e.returncode != 1:
			return True # May fail with 2 and still ok!
	if p.strip():
		return True
	else:
		return False


def open_telegram_link(username: str):
	tg = f'tg://resolve?domain={username}'
	web = f'https://t.me/{username}'

	if platform.system() == 'Linux':
		if check_tg_handler(): # FIXME: Really slow
			browse(tg)
		else:
			browse(web)
	else:
		if not browse(tg):
			browse(web)


def notify(desc='Working!', app_name="Deepines Store", title="Title", icon='deepines'):
	icon = icon
	title = title
	desc = desc
	if platform.system() == 'Windows':
		pass
	else:
		run_cmd(DEF, ['notify-send', '-a', app_name, '-i', icon, title, desc])
