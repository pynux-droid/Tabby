#! /usr/bin/env python

import os
import requests as r

api_key = os.environ.get("GROQ_API_KEY")
url = "https://api.groq.com/openai/v1/chat/completions"

def get_msg():
    msg = input("type here...")
    if msg.lower() == "bye":
        return
    else:
        get_resp(msg)

def get_resp(msg):
    # 2. Set up the headers with authorization

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
        }

    # 3. Define the payload structure
    # You can replace the model with your choice (e.g.,      "llama-3.3-70b-versatile")
    payload = {
        "model": "openai/gpt-oss-120b",
        "messages": [
        {
            "role": "system",
            "content": "You are a helpful, concise AI assistant."
        },
        {
            "role": "user",
            "content": f"{msg}"
        }
        ],
        "temperature": 0.7,
        "max_tokens": 100
        }

    # 4. Make the POST request
    try:
        response = r.post(url, headers=headers, json=payload)
        # Check for HTTP errors
        response.raise_for_status()
        
        # 5. Parse and print the text response
        response_data = response.json()
        ai_message = response_data["choices"][0]["message"]["content"]

        print("AI Response:")
        print(ai_message)
        get_msg()

    except r.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response body: {response.text}")
    except Exception as err:
        print(f"An error occurred: {err}")
        
if __name__ == "__main__":
    get_msg()
