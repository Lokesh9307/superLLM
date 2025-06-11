import faiss
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def build_index(chunks, embedder):
    vectors = embedder.encode(chunks)
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    return index, vectors


def query_index(question, chunks, index, vectors, embedder, llm, top_n=3):
    """
    Query the FAISS index and return an answer using the LLM.
    """
    # 1. Embed the question
    question_vector = embedder.encode([question])[0]  # Shape: (dim,)

    # 2. Search FAISS index
    D, I = index.search(np.array([question_vector]), top_n)

    # 3. Get the top-N chunks
    top_chunks = [chunks[i] for i in I[0]]
    context = "\n\n".join(top_chunks)

    # 4. Construct prompt
    prompt = f"""Use the following transcript segments to answer the question.

Relevant segments:
{context}

Question: {question}

If the answer isn't in these segments, say you don't know.
Answer:"""

    # 5. Query LLM
    answer = llm.invoke(prompt)

    return answer, context
