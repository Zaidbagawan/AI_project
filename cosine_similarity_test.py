
from dotenv import load_dotenv
from google import genai
from google.genai import types
import numpy as np
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Two sentences
texts = [
    "I love Python programming.",
    "I enjoy developing applications using Python."
]

# Create separate Content objects
contents = [
    types.Content(
        parts=[types.Part.from_text(text=text)]
    )
    for text in texts
]

# Generate embeddings
response = client.models.embed_content(
    model="gemini-embedding-2",
    contents=contents
)

# Extract vectors
vector_1 = np.array(response.embeddings[0].values)
vector_2 = np.array(response.embeddings[1].values)

# Calculate cosine similarity
dot_product = np.dot(vector_1, vector_2)

magnitude_1 = np.linalg.norm(vector_1)
magnitude_2 = np.linalg.norm(vector_2)

similarity = dot_product / (magnitude_1 * magnitude_2)

# Display results
print("Sentence 1:", texts[0])
print("Sentence 2:", texts[1])

print("\nVector 1 dimensions:", len(vector_1))
print("Vector 2 dimensions:", len(vector_2))

print("\nCosine Similarity:", similarity)
