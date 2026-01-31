#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys
import tempfile


# Messages
INSTALLING_FLATHUB = "Adding Flathub repository..."
INSTALLING_DONE = " done.\n"
INSTALLING_FAILED = " failed:\n"
FLATHUB_NOT_FOUND = "flatpak not found, skipping Flathub setup.\n"
FLATHUB_CONTINUE = "Continuing without Flathub.\n"

RECOMMENDATION = "It is recommended to reboot your computer for .desktop entries to appear in the launcher."
RESTART_TITLE = "Reboot Required"
LATER_LABEL = "Later"
RESTART_LABEL = "Reboot"
_lang = (os.environ.get("LANGUAGE") or os.environ.get("LANG") or "").lower()
if _lang.startswith("es"):
	INSTALLING_FLATHUB = "Añadiendo repositorio de Flathub..."
	INSTALLING_DONE = " hecho.\n"
	INSTALLING_FAILED = " falló:\n"
	FLATHUB_NOT_FOUND = "flatpak no encontrado, omitiendo configuración de Flathub.\n"
	FLATHUB_CONTINUE = "Continuando sin Flathub.\n"
	
	RECOMMENDATION = "Se recomienda reiniciar el equipo para que los accesos .desktop se muestren en el lanzador."
	RESTART_TITLE = "Reinicio requerido"
	LATER_LABEL = "Más tarde"
	RESTART_LABEL = "Reiniciar"
elif _lang.startswith("pt"):
	INSTALLING_FLATHUB = "Adicionando repositório do Flathub..."
	INSTALLING_DONE = " concluído.\n"
	INSTALLING_FAILED = " falhou:\n"
	FLATHUB_NOT_FOUND = "flatpak não encontrado, ignorando configuração do Flathub.\n"
	FLATHUB_CONTINUE = "Continuando sem o Flathub.\n"

	RECOMMENDATION = "Recomenda-se reiniciar o computador para que os atalhos .desktop apareçam no iniciador."
	RESTART_TITLE = "Reinício necessário"
	LATER_LABEL = "Mais tarde"
	RESTART_LABEL = "Reiniciar"

def main() -> int:
	print(INSTALLING_FLATHUB, end="", flush=True)

	if shutil.which("flatpak") is None:
		print(INSTALLING_FAILED)
		print(FLATHUB_NOT_FOUND)
		return 0

	# Capture flatpak output to a temp file so we can show it on failure
	tmp = tempfile.NamedTemporaryFile(delete=False)
	tmpname = tmp.name
	tmp.close()

	def append_cmd_output(cmd):
		try:
			with open(tmpname, "ab") as f:
				f.write(("$ %s\n" % (" ".join(cmd))).encode())
				p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
				f.write(p.stdout)
				return p.returncode
		except Exception as exc:
			try:
				with open(tmpname, "ab") as f:
					f.write((b"ERROR: %s\n" % str(exc).encode()))
			except Exception:
				pass
			return 1

	# Run cmds; failures shouldn't abort the installer (postinst handles errors)
	append_cmd_output(["flatpak", "remote-add", "--if-not-exists", "flathub", "https://dl.flathub.org/repo/flathub.flatpakrepo"])
	append_cmd_output(["flatpak", "update", "--appstream", "--assumeyes"])
	append_cmd_output([
		"flatpak",
		"install",
		"flathub",
		"org.gtk.Gtk3theme.deepin",
		"org.gtk.Gtk3theme.deepin-dark",
		"--assumeyes",
	])

	captured = ""
	try:
		with open(tmpname, "rb") as f:
			captured = f.read().decode(errors="replace")
	except Exception:
		captured = "(failed to read captured output)"
	try:
		os.remove(tmpname)
	except Exception:
		pass

	try:
		p = subprocess.run(["flatpak", "remote-list"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
		remotes = p.stdout.decode(errors="replace").splitlines()
	except Exception:
		remotes = []

	if any(line.startswith("flathub") for line in remotes):
		print(INSTALLING_DONE)
	else:
		print(INSTALLING_FAILED)
		print(captured)
		print(FLATHUB_CONTINUE)

	# Check if the system-wide desktop export is present in XDG_DATA_DIRS;
	# if not, advise user to relog.
	xdg = ""
	try:
		from demoted_actions import DEF
		result = subprocess.run(
			["systemctl", "--user", "-M", f"{DEF.name}@", "show-environment"],
			capture_output=True, text=True, timeout=10
		)
		if result.returncode == 0:
			for line in result.stdout.splitlines():
				if line.startswith("XDG_DATA_DIRS="):
					xdg = line.split("=", 1)[1]
					break
	except Exception:
		pass
	if not xdg:
		xdg = os.environ.get("XDG_DATA_DIRS", "")
	want = "/var/lib/flatpak/exports/share"
	present = False
	for p in xdg.split(":"):
		p = p.strip()
		if p == want:
			present = True
			break

	if not present:
		# Spawn a detached helper process to show the notification and wait for the user's action...
		try:
			project_dir = os.path.dirname(__file__)
			env = os.environ.copy()
			old_pp = env.get('PYTHONPATH', '')
			if project_dir not in old_pp.split(os.pathsep):
				env['PYTHONPATH'] = project_dir + (os.pathsep + old_pp if old_pp else '')
			env['DEEPINES_NOTIFY_DESC'] = RECOMMENDATION
			env['DEEPINES_NOTIFY_TITLE'] = RESTART_TITLE
			env['DEEPINES_NOTIFY_LATER'] = LATER_LABEL
			env['DEEPINES_NOTIFY_RESTART'] = RESTART_LABEL

			# Compute the parent-of-grandparent (two levels up) if available.
			# The helper will wait for this PID to exit before showing the
			# notification so the message appears when the original invoker
			# (two-level ancestor) finishes.
			def _ancestor_two_levels(pid):
				try:
					for _ in range(2):
						status_path = f"/proc/{pid}/status"
						with open(status_path, 'r') as sf:
							for line in sf:
								if line.startswith("PPid:"):
									pid = int(line.split()[1])
									break
							else:
								# no PPid line
								return None
					return pid if pid > 0 else None
				except Exception:
					return None

			try:
				ancestor = _ancestor_two_levels(os.getppid())
				if ancestor:
					env['DEEPINES_INSTALLER_PID'] = str(ancestor)
			except Exception:
				pass # shit...

			helper = os.path.join(project_dir, 'restart_notify_helper.py')
			p = subprocess.Popen([
				sys.executable,
				"-S",
				"-u",
				helper,
			], env=env, cwd=project_dir, close_fds=True)
		except Exception:
			print(RECOMMENDATION)
		else:
			# Invoker returns immediately; helper process will handle the notify.
			return 0

	return 0


if __name__ == "__main__":
	sys.exit(main())
