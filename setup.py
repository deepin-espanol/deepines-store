#!/usr/bin/env python3
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
        self.ts_files = "translationsSource/*.ts"
        self.tr_function = '__tr'

    def finalize_options(self):
        pass

    def run(self):
        command = f'pylupdate5 {self.source_files} -ts {self.ts_files} -tr-function {self.tr_function}'
        self.announce('Running command: %s' % str(command), level=log.INFO)
        subprocess.check_call(command, shell=True)


setuptools.setup(
    cmdclass={
        'update_translations': update_ts,
    },
)
