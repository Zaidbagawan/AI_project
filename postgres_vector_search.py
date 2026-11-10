
from dotenv import load_dotenv
from google import genai
from google.genai import types
import psycopg
import os

# 1. Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
db_password = os.getenv("DB_PASSWORD")

if not api_key or not db_password:
    raise ValueError("Missing GEMINI_API_KEY or DB_PASSWORD")

# 2. Initialize Gemini client
client = genai.Client(api_key=api_key)

# 3. Accept a dynamic question
user_question = input("Ask your question: ").strip()

if not user_question:
    raise ValueError("Question cannot be empty")

# 4. Generate question embedding
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

print("\nQuestion:", user_question)
print("Vector dimensions:", len(question_embedding))

# 5. Convert Python list into pgvector format
vector_string = "[" + ",".join(
    str(value) for value in question_embedding
) + "]"

# 6. Search PostgreSQL
with psycopg.connect(
    host="localhost",
    port=5432,
    dbname="semantic_search_db",
    user="postgres",
    password=db_password
) as connection:

    with connection.cursor() as cursor:

        cursor.execute(
            """
            WITH query_embedding AS (
                SELECT %s::vector AS embedding
            )
            SELECT
                d.id,
                d.title,
                d.content,
                1 - (d.embedding <=> q.embedding) AS similarity
            FROM documents d
            CROSS JOIN query_embedding q
            ORDER BY d.embedding <=> q.embedding
            LIMIT 4;
            """,
            (vector_string,)
        )

        results = cursor.fetchall()

# 7. Apply similarity threshold
SIMILARITY_THRESHOLD = 0.70

print("\n========== SEARCH RESULTS ==========")

found_relevant_document = False

for result in results:

    document_id, title, content, similarity = result

    similarity = float(similarity)

    print("\nDocument:", title)
    print("Similarity:", round(similarity, 4))

    if similarity >= SIMILARITY_THRESHOLD:

        found_relevant_document = True

        print("Content:", content)

if not found_relevant_document:
    print("\nNo sufficiently relevant documents found.")
