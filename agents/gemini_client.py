import os
import socket
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

URL = (
    "https://generativelanguage.googleapis.com/"
    "v1beta/models/gemini-2.5-flash:generateContent"
)


# Force Python HTTPS connections to use IPv4.
_original_getaddrinfo = socket.getaddrinfo


def ipv4_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    return _original_getaddrinfo(
        host,
        port,
        socket.AF_INET,
        type,
        proto,
        flags
    )


socket.getaddrinfo = ipv4_getaddrinfo


def ask_gemini(prompt):

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    response = requests.post(
        f"{URL}?key={API_KEY}",
        headers=headers,
        json=data,
        timeout=30
    )

    response.raise_for_status()

    result = response.json()

    return result["candidates"][0]["content"]["parts"][0]["text"]
