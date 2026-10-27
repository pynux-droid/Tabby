#!/usr/bin/env python

'''send please call me'''

import time
import subprocess

def make_call():
    cont = ("*130*0729829664%23")
    cont_2 = ("*130*0107415085%23")

    subprocess.run([
        "termux-telephony-call",cont
        ])
    
    time.sleep(15)

    subprocess.run([
        "termux-telephony-call",cont_2
        ])
        
if __name__ == "__main__" :
    make_call()