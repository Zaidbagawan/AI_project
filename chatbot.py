from dotenv import load_dotenv
from google import genai
import os

# Load variables from .env
load_dotenv()

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Gemini API key not found.")
    exit()

# Create Gemini client
client = genai.Client(
    api_key=api_key,
    http_options={"timeout": 60000}
)

print("AI Chatbot started!")
print("Type 'exit' to quit.\n")

while True:

    user_message = input("You: ")

    if user_message.lower() == "exit":
        print("Goodbye!")
        break

    try:
        interaction = client.interactions.create(
            model="gemini-3.8-flash",
            input=user_message
        )

        print("AI:", interaction.output_text)
        print()

    except Exception as e:
        print("Error:", e)
        print()