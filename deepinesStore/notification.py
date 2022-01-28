#!/usr/bin/env python3
import subprocess
from deepinesStore.maing import getResource


def notification(description, icon=getResource('deepines')):
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
