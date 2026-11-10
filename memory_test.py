messages = []

while True:

    user_message = input("You: ")

    if user_message.lower() == "exit":
        print("Goodbye!")
        break

    # Store user's message
    messages.append({
        "role": "user",
        "content": user_message
    })

    # Temporary assistant response
    assistant_message = "I received your message."

    # Store assistant's message
    messages.append({
        "role": "assistant",
        "content": assistant_message
    })

    print("AI:", assistant_message)

    print("\nConversation History:")
    print(messages)
    print()