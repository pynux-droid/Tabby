#! /usr/bin/env python

import os
import json
import sqlite3
import requests as r


api_key = os.environ.get("GROQ_API_KEY")
url = "https://api.groq.com/openai/v1/chat/completions"

conn = sqlite3.connect("context.db")
cur = conn.cursor()

msgs = {}

def main() -> None:
    create_tables()
    chat_hist()


def create_tables() -> None:
    cur.execute(
    """CREATE TABLE IF NOT EXISTS chats(CHAT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    SENDER TEXT NOT NULL,
    MESSAGE TEXT NOT NULL)"""
    )


def context_mgr() -> None:
    try:
        for key, value in msgs.items():
            if not key or not value:
                continue
            cur.execute(
            """INSERT INTO chats(SENDER, MESSAGE) VALUES(?, ?)""",(key, value,)
            )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e


def chat_hist() -> list:
     chat_history = []
     msg = input("type here...")
     if msg.lower() == "bye":
         return
     else:
         msgs["user"] = msg

     cur.execute(
     """SELECT SENDER, MESSAGE FROM chats ORDER BY CHAT_ID DESC LIMIT 10"""
     )
     rows = cur.fetchall()

     for row in reversed(rows):
         chat_history.append({"role":row[0], "content":row[1]})
     new = {"role":"user", "content":msg}
     chat_history.append(new)

     prompt = chat_history
     get_resp(prompt)
     return prompt


def get_resp(prompt) -> None:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
        }

    payload = {
        "model": "openai/gpt-oss-120b",
        "messages": prompt
        ,
        "temperature": 0.7,
        "max_tokens": 10000
        }

    try:
        response = r.post(url, headers=headers, json=payload)
        response.raise_for_status()

        response_data = response.json()
        ai_msg = response_data["choices"][0]["message"]["content"]

        print("AI Response:")
        print(ai_msg)

        msgs["system"]=ai_msg

        context_mgr()
        chat_hist()

    except r.exceptions.HTTPError as http_err:
        raise http_err
    except Exception as err:
        raise err

if __name__ == "__main__":
    try:
        main()
    finally:
        conn.close()
