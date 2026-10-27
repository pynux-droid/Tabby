#!/usr/bin/env python

import json
import sqlite3
import logging

logging.basicConfig(level = logging.INFO)
conn = sqlite3.connect("quotes.db")
cur = conn.cursor()

def main() -> None:
    create_table()
    add_quotes()

def create_table() -> None:
    try:
        cur.execute(
        """CREATE TABLE IF NOT EXISTS quotes(QUOTE_ID INTEGER      PRIMARY KEY AUTOINCREMENT,
        AUTHOR TEXT NULL,
        QUOTE TEXT UNIQUE NOT NULL)"""
        )
        cur.execute(
        """CREATE INDEX IF NOT EXISTS quotes_idx ON quotes(AUTHOR, QUOTE)"""
        )
    except Exception as e:
        raise e

def add_quotes() -> None:
    try:
        with open("quotes.json", "r", encoding="utf-8") as file:
            data = json.load(file)

            for item in data:
                if not item:
                    continue
                cur.execute("""
                    INSERT OR IGNORE INTO 
                    quotes(AUTHOR, QUOTE) 
                    VALUES(?, ?)""" ,
                    (item.get('quoteAuthor') or None, 
                    item.get('quoteText'))
                    )

            conn.commit()
            logging.info(f"Quotes Table Updated!")
    except Exception as e:
        raise e

if __name__ == "__main__":
    main()
