
from dotenv import load_dotenv
from google import genai
from google.genai import types
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

texts = [
    "I love Python programming.",
    "I enjoy developing applications using Python."
]

# Wrap each text in a separate Content object
contents = [
    types.Content(
        parts=[types.Part.from_text(text=text)]
    )
    for text in texts
]

# Generate separate embeddings
response = client.models.embed_content(
    model="gemini-embedding-2",
    contents=contents
)

print("Number of input texts:", len(texts))
print("Number of embeddings:", len(response.embeddings))

for text, embedding in zip(texts, response.embeddings):

    vector = embedding.values

    print("\nOriginal Text:", text)
    print("Vector Dimensions:", len(vector))
    print("First 10 Vector Values:")
    print(vector[:10])
