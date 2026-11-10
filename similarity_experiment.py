
from dotenv import load_dotenv
from google import genai
from google.genai import types
import numpy as np
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Three sentences
texts = [
    "I love Python programming.",
    "I enjoy developing applications using Python.",
    "The weather is very beautiful today."
]

# Create separate content objects
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
vectors = [
    np.array(embedding.values)
    for embedding in response.embeddings
]

# Function to calculate cosine similarity
def cosine_similarity(vector_1, vector_2):

    dot_product = np.dot(vector_1, vector_2)

    magnitude_1 = np.linalg.norm(vector_1)
    magnitude_2 = np.linalg.norm(vector_2)

    return dot_product / (magnitude_1 * magnitude_2)


# Compare all three pairs
pairs = [
    (0, 1),
    (0, 2),
    (1, 2)
]

for first, second in pairs:

    score = cosine_similarity(
        vectors[first],
        vectors[second]
    )

    print("\nSentence 1:", texts[first])
    print("Sentence 2:", texts[second])
    print("Similarity Score:", round(float(score), 4))
