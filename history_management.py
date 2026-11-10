conversation_history = [
    "My name is Zaid.",
    "I am a Python developer.",
    "I work with Django.",
    "Explain Django ORM.",
    "Explain serializers.",
    "What is middleware?"
]

# Keep only the latest 3 messages
recent_messages = conversation_history[-3:]

print("Complete History:")
print(conversation_history)

print("\nRecent Messages:")
print(recent_messages)