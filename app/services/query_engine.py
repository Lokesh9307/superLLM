import numpy as np
from langchain_core.messages import HumanMessage
import re

def truncate_context(context: str, max_chars: int = 2000) -> str:
    sentences = context.split('. ')
    truncated = ''
    for s in sentences:
        if len(truncated + s) > max_chars:
            break
        truncated += s + '. '
    return truncated.strip()

def remove_think_tags(text):
    cleaned_text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    return cleaned_text.strip()

def query_book(question, chunks, index, embedder, llm):
    q_vec = embedder.encode([question])
    _, indices = index.search(np.array(q_vec), k=1)  # reduced from k=3 to k=1
    context = "\n\n".join([chunks[i] for i in indices[0]])
    context = truncate_context(context)

    prompt = f"""
You are an AI assistant. Use the reference text below to generate a clear and well-structured answer to the user's question.

Reference Text:
{context}

Guidelines:
- do not use <think> tags
- answer in a proper formatted way and withpout preamble and postamble.
- Do not use any symbols like asterisks (*) or quotation marks (" ") in your answer.
- Structure your response with line breaks and spacing for clarity.
- Use plain, readable language across all domains (e.g., programming, law, medicine, finance).
- If the question involves code, include it using triple backticks and the appropriate language tag (e.g., ```python).
- Give direct, concise answers without repeating the question or source text.
- Avoid generic filler lines. Focus on answering the question based on the given context.

User's Question:
{question}

Answer:
"""

    response = llm.invoke([HumanMessage(content=prompt)])
    cleaned_response = remove_think_tags(response.content)
    return cleaned_response.strip(), context
