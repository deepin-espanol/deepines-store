#!/usr/bin/env python3
import os
from subprocess import Popen, PIPE, check_output, CalledProcessError
import platform
import threading
from pathlib import Path


def get_real_uid():
	uid = os.geteuid()
	if uid == 0:
		if 'SUDO_UID' in os.environ:
			return os.environ["SUDO_UID"]
		elif 'PKEXEC_UID' in os.environ:
			return os.environ["PKEXEC_UID"]
		else:
			return uid
	else:
		return uid


class UserDefault:
	def __init__(self, uid: int):
		import pwd
		self.uid = uid
		self.user = pwd.getpwuid(uid)
		self.name = self.user.pw_name
		self.gid = self.user.pw_gid
		self.home = self.user.pw_dir
		self.env = {**os.environ, 'USER': self.name, 'LOGNAME': self.name, 'PWD': os.getcwd(), 'HOME': self.home,
		'DBUS_SESSION_BUS_ADDRESS': f'unix:path=/run/user/{uid}/bus'}


def run_cmd(user: UserDefault, cmd):
	return Popen(cmd, env=user.env, user=user.uid, group=user.gid, stderr=PIPE, stdout=PIPE, encoding='utf8', universal_newlines=True)


def get_user_home_path() -> Path:
	return Path.home()


if platform.system() == 'Windows':
	pass
else:
	UID = int(get_real_uid())
	DEF = UserDefault(UID)
	# This is the "real" home, not the one from the user running the command
	# (which is probably root)
	HOME = Path(DEF.home)


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
	if platform.system() != 'Linux':
		return False
	try:
		p = check_output(["xdg-mime", "query", "default", "x-scheme-handler/tg"], env=DEF.env, user=DEF.uid, group=DEF.gid)
	except CalledProcessError as e:
		if e.returncode != 1:
			return True # May fail with 2 and still ok!
		return False
	if p.strip():
		return True
	return False


def create_folder(path: Path):
	if platform.system() == 'Linux':
		run_cmd(DEF, ['mkdir', '-p', str(path)])
	else:
		path.mkdir(parents=True, exist_ok=True)


def write_file(b, to):
	with open(to, 'wb') as ftw:
		ftw.write(b.content)
	if platform.system() == 'Linux':
		try:
			os.chown(str(to), DEF.uid, DEF.gid)
		except Exception:
			pass


def get_user_home():
	if platform.system() == 'Linux':
		return DEF.env['HOME']
	else:
		return str(get_user_home_path())


config_dir = Path(get_user_home()) / '.config' / 'deepines-store'

def create_config_dir():
	create_folder(config_dir)
	return config_dir


def get_resource(res_name, dir='', ext='.svg'):
	from os.path import join, abspath, dirname
	write_only_path = abspath(join(dirname(__file__), 'resources', dir, res_name + ext))
	user_config_path = abspath(join(config_dir, dir, res_name + ext))
	if Path(user_config_path).exists():
		return user_config_path
	elif Path(write_only_path).exists():
		return write_only_path
	else:
		return None

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


def notify(desc='Working!', app_name="Deepines Store", title="Title", icon='deepines', actions=None, timeout=0, handler=None):
	if platform.system() == 'Windows':
		pass
	else:
		if actions:
			# Start a background listener for the action signal
			def listen():
				cmd = ['dbus-monitor', "interface='org.freedesktop.Notifications',member='ActionInvoked'"]
				proc = run_cmd(DEF, cmd)
				for line in proc.stdout:
					line = line.strip()
					for action_key, _ in actions:
						if action_key in line:
							if handler:
								handler(action_key)
							return
			thread = threading.Thread(target=listen)
			thread.daemon = True
			thread.start()
			# Send the notification via D-Bus
			actions_list = []
			for key, label in actions:
				actions_list.extend([key, label])
			actions_str = str(actions_list)
			hints_str = "{'urgency': <byte 1>}"
			cmd = ['gdbus', 'call', '--session', '--dest', 'org.freedesktop.Notifications', '--object-path', '/org/freedesktop/Notifications', '--method', 'org.freedesktop.Notifications.Notify', app_name, '0', icon, title, desc, actions_str, hints_str, str(timeout)]
			run_cmd(DEF, cmd)
		else:
			run_cmd(DEF, ['notify-send', '-a', app_name, '-i', icon, title, desc])
