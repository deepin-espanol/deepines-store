#!/usr/bin/env python3
import subprocess
from os.path import join, abspath, dirname


def notification(description, icon=abspath(join(dirname(__file__), 'resources', 'deepines.png'))):
    title = 'Deepines'
    description = description
    urgency = 'normal'
    duration = 3
    icon = icon
    command = [
        'notify-send', '{}'.format(title),
        '{}'.format(description),
        '-u', urgency,
        '-a', title,
        '-t', '{}'.format(duration * 1000)
    ]

    command += ['-i', icon]

    subprocess.call(command)
