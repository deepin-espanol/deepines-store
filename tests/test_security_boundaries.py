import importlib.util
from pathlib import Path
import unittest


security_path = Path(__file__).parents[1] / "deepinesStore" / "security.py"
spec = importlib.util.spec_from_file_location("deepines_store_security", security_path)
security = importlib.util.module_from_spec(spec)
spec.loader.exec_module(security)

filter_forwarded_environment = security.filter_forwarded_environment
parse_remote_checksums = security.parse_remote_checksums

class EnvironmentFilteringTests(unittest.TestCase):
	def test_keeps_desktop_and_locale_variables(self):
		source = {
			"DISPLAY": ":0",
			"LANG": "pt_BR.UTF-8",
			"LC_MESSAGES": "pt_BR.UTF-8",
			"WAYLAND_DISPLAY": "wayland-0",
		}

		self.assertEqual(filter_forwarded_environment(source), source)

	def test_drops_code_execution_and_command_lookup_variables(self):
		filtered = filter_forwarded_environment({
			"PATH": "/tmp/attacker",
			"PYTHONPATH": "/tmp/attacker",
			"LD_PRELOAD": "/tmp/attacker.so",
			"BASH_ENV": "/tmp/attacker.sh",
			"DISPLAY": ":0",
		})

		self.assertEqual(filtered, {"DISPLAY": ":0"})

	def test_rejects_non_object_payload(self):
		with self.assertRaises(ValueError):
			filter_forwarded_environment(["PATH=/tmp/attacker"])


class SvgManifestTests(unittest.TestCase):
	def test_accepts_current_md5sum_format(self):
		checksum = "dabcebd52bc398e959a636ebdb9fe1f8"
		self.assertEqual(
			parse_remote_checksums(f"{checksum}  veracrypt.svg\n"),
			{"veracrypt.svg": checksum},
		)

	def test_rejects_path_traversal_and_non_svg_entries(self):
		content = "\n".join([
			"0" * 32 + "  ../../root/.profile.svg",
			"1" * 32 + "  /etc/payload.svg",
			"2" * 32 + "  payload.py",
		])

		self.assertEqual(parse_remote_checksums(content), {})

	def test_rejects_invalid_checksum(self):
		self.assertEqual(parse_remote_checksums("not-md5  icon.svg"), {})


if __name__ == "__main__":
	unittest.main()
