from dotenv import load_dotenv
from google import genai
from google.genai import types
import os
import psycopg
import numpy as np

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# Our documents
documents = [
    {
        "id": 1,
        "content": "Employees must submit leave requests through the HR portal."
    },
    {
        "id": 2,
        "content": "Salary is credited to employees at the end of each month."
    },
    {
        "id": 3,
        "content": "Employees can work remotely with manager approval."
    },
    {
        "id": 4,
        "content": "Python is a programming language used for backend development."
    }
]

# Prepare document content for embedding
contents = [
    types.Content(
        parts=[types.Part.from_text(text=document["content"])]
    )
    for document in documents
]

# Generate embeddings
response = client.models.embed_content(
    model="gemini-embedding-2",
    contents=contents
)

# Attach embeddings to documents
for document, embedding in zip(documents, response.embeddings):
    document["embedding"] = embedding.values
# Save document embeddings into PostgreSQL

titles = {
    1: "Leave Policy",
    2: "Salary Policy",
    3: "Remote Work Policy",
    4: "Python Backend Development"
}

with psycopg.connect(
    host="localhost",
    port=5432,
    dbname="semantic_search_db",
    user="postgres",
    password=os.getenv("DB_PASSWORD")
) as connection:

    with connection.cursor() as cursor:

        cursor.execute("SELECT COUNT(*) FROM documents")
        existing_count = cursor.fetchone()[0]

        if existing_count == 0:

            for document in documents:

                vector_string = "[" + ",".join(
                    str(value) for value in document["embedding"]
                ) + "]"

                cursor.execute(
                    """
                    INSERT INTO documents (title, content, embedding)
                    VALUES (%s, %s, %s::vector)
                    """,
                    (
                        titles[document["id"]],
                        document["content"],
                        vector_string
                    )
                )

            print("Documents and embeddings saved successfully!")

        else:
            print("Documents already exist. Skipping insertion.")
# Display results
for document in documents:
    print("\nDocument ID:", document["id"])
    print("Content:", document["content"])
    print("Vector dimensions:", len(document["embedding"]))
    print("First 5 vector values:", document["embedding"][:5])


# User question
user_question = "What is the company's maternity leave policy?"


# Generate embedding for user question
question_content = types.Content(
    parts=[
        types.Part.from_text(text=user_question)
    ]
)

question_response = client.models.embed_content(
    model="gemini-embedding-2",
    contents=[question_content]
)

question_embedding = question_response.embeddings[0].values


print("\nUser Question:", user_question)
print("Question Vector Dimensions:", len(question_embedding))
print("First 5 Question Vector Values:", question_embedding[:5])



# Function to calculate cosine similarity
def cosine_similarity(vector_1, vector_2):

    dot_product = np.dot(vector_1, vector_2)

    magnitude_1 = np.linalg.norm(vector_1)
    magnitude_2 = np.linalg.norm(vector_2)

    similarity = dot_product / (magnitude_1 * magnitude_2)

    return similarity


# Compare question with every document
# for document in documents:

#     document_embedding = document["embedding"]

#     score = cosine_similarity(
#         question_embedding,
#         document_embedding
#     )

#     print("\nDocument ID:", document["id"])
#     print("Similarity Score:", round(float(score), 4))

# Store similarity results
search_results = []

for document in documents:

    score = cosine_similarity(
        question_embedding,
        document["embedding"]
    )

    search_results.append({
        "id": document["id"],
        "content": document["content"],
        "score": float(score)
    })


# Sort documents by similarity score
search_results.sort(
    key=lambda item: item["score"],
    reverse=True
)


# Retrieve the best matching document
# Define similarity threshold
SIMILARITY_THRESHOLD = 0.70

# Get the highest matching document
best_match = search_results[0]

print("\n========== SEARCH RESULT ==========")

print("User Question:", user_question)

print("Best Similarity Score:", round(best_match["score"], 4))

# Check whether the score meets our threshold
if best_match["score"] >= SIMILARITY_THRESHOLD:

    print("\nRelevant document found!")

    print("Document ID:", best_match["id"])

    print("Content:", best_match["content"])

else:

    print("\nNo sufficiently relevant document found.")

    print("Please try another question.")