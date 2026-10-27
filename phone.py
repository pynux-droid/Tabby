#!/usr/bin/env python

import time
import subprocess


def make_call():
    cont = ("Add contact here")

    subprocess.run(
        ["termux-telephony-call",cont]
        )


if __name__ == "__main__" :
    make_call()
