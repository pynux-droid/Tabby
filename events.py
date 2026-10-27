#!/usr/bin/env python

import string
import sqlite3
import logging
import datetime

logging.basicConfig(level = logging.INFO)
PUNCTUATION_TABLE = str.maketrans("", "", string.punctuation)

conn = sqlite3.connect("self_love.db")
cur = conn.cursor()

def get_input():
    d = datetime.datetime.now()
    date = d.strftime("%Y-%m-%d")
    day = d.strftime("%A")
    
    events = set()
    
    while True:
        ev = (input("ENTER YOUR ACHIEVEMENTS:~$_").strip())
        if ev.lower() == ('done'):
             break
             
        clean_ev = "".join(ev.lower())
        activity = clean_ev.translate(PUNCTUATION_TABLE).strip()
    
        if activity:
            events.add(activity)
            
    return day, date, events
    
def update_tables(day, date, events): 
    if not events:
        return
    try:
        for activity in events:
            cur.execute(
            """INSERT OR IGNORE INTO events
            (DAY, DATE, ACTIVITY)
            VALUES(?, ?, ?);""",(day,
            date, activity)
            )
        conn.commit()
           
        logging.info('''Events logged 
           Successfuly\n''')
    except Exception as e:
            conn.rollback()
            logging.error(f'::{e} @ update_tables\n')
            return

if __name__ == "__main__":
    try:
        day, date, events = get_input()
        update_tables(day, date, events)
    finally:
        conn.close()