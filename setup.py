#!/usr/bin/env python3
import os
from distutils import cmd, log
import setuptools
import subprocess


class update_ts(cmd.Command):
	"""Update translations."""
	description = 'updates all available translations'
	user_options = [
		('source-files=', 's', 'source files'),
		('ts-files=', 'o', 'ts files output'),
		('function-name=', 'f', 'translation function name'),
	]

	def initialize_options(self):
		"""Set default values."""
		self.source_files = "deepinesStore/*.py"
		self.ts_files = "translations/*.ts"
		self.tr_function = '__tr'

	def finalize_options(self):
		pass

	def run(self):
		command = f'pylupdate5 {self.source_files} -ts {self.ts_files} -tr-function {self.tr_function}'
		self.announce('Running command: %s' % str(command), level=log.INFO)
		subprocess.check_call(command, shell=True)


class generate_qm(cmd.Command):
	"""Generate compiled translations."""
	description = 'updates all available translations'
	user_options = [
		('dirname=', 'd', 'translation input dir'),
		('toutput=', 'o', 'translation output'),
	]

	def initialize_options(self):
		"""Set default values."""
		self.ts_dir = "translations"
		self.qm_dir = "deepinesStore/translations"

	def finalize_options(self):
		pass

	def run(self):
		if not os.path.exists(self.qm_dir):
			os.makedirs(self.qm_dir)

		for tr_file in os.listdir(self.ts_dir):
			command = f'lconvert -i {self.ts_dir}/{tr_file} -o {self.qm_dir}/{os.path.splitext(tr_file)[0]}.qm'
			self.announce('Running command: %s' % str(command), level=log.INFO)
			subprocess.check_call(command, shell=True)


setuptools.setup(
	cmdclass={
		'update_translations': update_ts,
		'generate_translations': generate_qm,
	},
)
