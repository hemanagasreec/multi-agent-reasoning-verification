from agents.gemini_client import ask_gemini


response = ask_gemini(
    "Reply with exactly: Gemini connection successful"
)

print(response)