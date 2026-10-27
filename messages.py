#!/usr/bin/env python

import sqlite3
import datetime
import subprocess

conn = sqlite3.connect("self_love.db")
cur = conn.cursor()
t = datetime.datetime.now()

def fetch_quote():
    cur.execute(
        """SELECT AUTHOR, QUOTE FROM quotes
        ORDER BY RANDOM()"""
        )
    rows = cur.fetchone()
    author, quote = rows
    quote_of_the_day = f":: {quote}\nBy: {author}"
    return quote_of_the_day

def fetch_activity():
    today = t.strftime("%Y-%m-%d")
    cur.execute(
        """SELECT ACTIVITY FROM events
        WHERE DATE = ? ORDER BY
        EVENT_ID""", (today,)
        )
    data = cur.fetchall()
    dataset = [f"Today You did :- {activity}" for activity in data]
    clean_data = "\n".join(dataset)
    return clean_data

def clean_db():
    cur.execute(
        """DELETE FROM events"""
        )
    conn.commit()
    conn.close()

def motivator(quote_of_the_day, clean_data):
        if not clean_data:
            clean_data = quote_of_the_day

        now = int(t.strftime('%H'))
        if now <= 12:
            load = quote_of_the_day
            header = ("Good Morning 🌅 Moris!")
        else:
            load = clean_data
            header = ("Good Evening 🌆 Moris!")
            clean_db()

        subprocess.run(
            ["termux-notification",
            "--title", header,
            "--content", load]
            )

if __name__ == "__main__":
    quote_of_the_day = fetch_quote()
    clean_data = fetch_activity()
    motivator(quote_of_the_day, clean_data)
