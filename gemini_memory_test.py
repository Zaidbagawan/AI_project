from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

print("AI Chatbot started!")
print("Type 'exit' to quit.\n")


previous_interaction_id = None


while True:

    user_message = input("You: ")

    if user_message.lower() == "exit":
        print("Goodbye!")
        break

    if previous_interaction_id is None:

        interaction = client.interactions.create(
            model="gemini-3.8-flash",
            input=user_message
        )

    else:

        interaction = client.interactions.create(
            model="gemini-3.8-flash",
            input=user_message,
            previous_interaction_id=previous_interaction_id
        )

    print("AI:", interaction.output_text)

    previous_interaction_id = interaction.id