#!/usr/bin/env python

import sqlite3
import datetime
import subprocess

conn = sqlite3.connect("quotes.db")
cur = conn.cursor()

def main() -> None:
    quote_of_the_day = get_quote()
    send_quote(quote_of_the_day)


def get_quote() -> str:
    cur.execute(
    """SELECT AUTHOR, QUOTE FROM quotes
    ORDER BY RANDOM()"""
    )
    rows = cur.fetchone()
    conn.close()

    author, quote = rows
    quote_of_the_day = f":: {quote}\nBy: {author}"

    return quote_of_the_day


def send_quote(quote_of_the_day: str) ->None:
     t = datetime.datetime.now()
     now = int(t.strftime('%H'))

     if now <= 12:
         header = ("Good Morning 🌅 Moris!")
     else:
         header = ("Good Evening 🌆 Moris!")

     subprocess.run([
     "termux-notification",
     "--title", header, 
     "--content", quote_of_the_day, 
     "--id", "id"])


if __name__ == "__main__":
    main()
