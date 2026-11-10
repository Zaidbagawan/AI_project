conversation_history = [
    {
        "role": "user",
        "content": "My name is Zaid."
    },
    {
        "role": "assistant",
        "content": "Nice to meet you, Zaid!"
    },
    {
        "role": "user",
        "content": "I am a Python backend developer."
    },
    {
        "role": "assistant",
        "content": "That's great!"
    }
]

current_message = "What is my name?"

context = ""

for message in conversation_history:
    context += f"{message['role']}: {message['content']}\n"

context += f"user: {current_message}"

print("Context sent to AI:")
print(context)