#! /usr/bin/env python

import os
import json
import sqlite3
import requests as r

msgs = {}
api_key = os.environ.get("GROQ_API_KEY")
url = "https://api.groq.com/openai/v1/chat/completions"

def create_db():
    conn = sqlite3.connect("context.db")
    cur = conn.cursor()

    cur.execute(
    """CREATE TABLE IF NOT EXISTS chats(CHAT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    SENDER TEXT NOT NULL,
    MESSAGE TEXT NOT NULL)"""
    )
    conn.close()
    return

def context_mgr():
    conn = sqlite3.connect("context.db")
    cur = conn.cursor()

    for key, value in msgs.items():
        if not key or not value:
            continue
        cur.execute(
        """INSERT INTO chats(SENDER, MESSAGE) VALUES(?, ?)""",(key, value,)
        )
    conn.commit()
    conn.close()
    return

def chat_hist():
     chat_history = []
     msg = input("type here...")
     if msg.lower() == "bye":
         return
     else:
         msgs["user"] = msg

     conn = sqlite3.connect("context.db")
     cur = conn.cursor()
     cur.execute(
     """SELECT SENDER, MESSAGE FROM chats ORDER BY CHAT_ID DESC LIMIT 10"""
     )
     rows = cur.fetchall()
     conn.close()

     for row in reversed(rows):
         chat_history.append({"role":row[0], "content":row[1]})
     new = {"role":"user", "content":msg}
     chat_history.append(new)

     prompt = chat_history
     get_resp(prompt)
     return prompt

def get_resp(prompt):
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
        print(f"HTTP error occurred: {http_err}")
        print(f"Response body: {response.text}")
    except Exception as err:
        print(f"An error occurred: {err}")

if __name__ == "__main__":
    create_db()
    chat_hist()
