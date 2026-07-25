"""Validation helpers for data that crosses trust boundaries."""

import re


FORWARDED_ENV_NAMES = frozenset({
	"DBUS_SESSION_BUS_ADDRESS",
	"DESKTOP_SESSION",
	"DISPLAY",
	"GDK_DPI_SCALE",
	"GDK_SCALE",
	"GTK_THEME",
	"HTTP_PROXY",
	"HTTPS_PROXY",
	"LANG",
	"LANGUAGE",
	"NO_PROXY",
	"QT_AUTO_SCREEN_SCALE_FACTOR",
	"QT_FONT_DPI",
	"QT_QPA_PLATFORM",
	"QT_SCALE_FACTOR",
	"QT_SCREEN_SCALE_FACTORS",
	"QT_STYLE_OVERRIDE",
	"WAYLAND_DISPLAY",
	"XAUTHORITY",
	"XDG_CURRENT_DESKTOP",
	"XDG_DATA_DIRS",
	"XDG_SESSION_DESKTOP",
	"XDG_SESSION_TYPE",
	"http_proxy",
	"https_proxy",
	"no_proxy",
})

_CHECKSUM_RE = re.compile(r"^[0-9a-fA-F]{32}$")
_SVG_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*\.svg$")


def filter_forwarded_environment(source):
	"""Return only variables needed for GUI, locale, and proxy compatibility.

	The launcher crosses a privilege boundary through pkexec. Forwarding PATH,
	PYTHONPATH, LD_PRELOAD, or other arbitrary variables would let the invoking
	user influence programs executed by the privileged process.
	"""
	if not isinstance(source, dict):
		raise ValueError("the serialized environment must be a JSON object")

	filtered = {}
	for key, value in source.items():
		if not isinstance(key, str) or not isinstance(value, str):
			continue
		if key in FORWARDED_ENV_NAMES or key.startswith("LC_"):
			if "\x00" not in key and "\x00" not in value:
				filtered[key] = value
	return filtered


def parse_remote_checksums(content):
	"""Parse a checksum manifest while confining entries to SVG basenames."""
	checksums = {}
	for line_number, line in enumerate(content.splitlines(), 1):
		parts = line.split()
		if not parts:
			continue
		if len(parts) != 2:
			print(f"Ignoring malformed SVG checksum line {line_number}")
			continue
		checksum, name = parts
		if not _CHECKSUM_RE.fullmatch(checksum) or not _SVG_NAME_RE.fullmatch(name):
			print(f"Ignoring unsafe SVG checksum line {line_number}")
			continue
		checksums[name] = checksum.lower()
	return checksums
