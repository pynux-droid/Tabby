#!/bin/env python

import time
import threading
from neonize.events import ConnectedEv
from neonize.utils.enum import ClientType
from neonize.client import NewName, NewClient

client = NewClient("db_session.db")

def request_pairing_code():
    time.sleep(3)
    try:
        pairing_code = client.PairPhone(
            phone="ADD CONTACT HERE",
            show_push_notification=True,
            client_name=ClientName.ANDROID
            )
        print(f"PAIRING CODE:\n {pairing_code}")
    except Exception as e:
        print(f"{e}")

#Start the background routine thread
threading.Thread(target=request_pairing_code, daemon=True).start()

client.connect()
