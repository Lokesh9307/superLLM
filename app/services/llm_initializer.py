import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from langchain_groq import ChatGroq

load_dotenv()

embedder = SentenceTransformer("all-MiniLM-L6-v2")

llm = ChatGroq(
    model="deepseek-r1-distill-llama-70b",
    api_key=os.getenv("GROQ_API_KEY")
)
