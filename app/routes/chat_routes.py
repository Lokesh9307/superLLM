from flask import Blueprint, request, jsonify
import tempfile
from app.services.pdf_processing import extract_text_from_pdf
from app.services.llm_initializer import llm, embedder
from app.services.query_engine import query_book
from app.utils.vector_store import build_index

chat_blueprint = Blueprint("chat", __name__)

@chat_blueprint.route("/upload", methods=["POST"])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({"error": "No PDF uploaded"}), 400

    file = request.files['pdf']
    question = request.form.get("question", "")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        file.save(temp.name)
        pdf_text = extract_text_from_pdf(temp.name)

    chunks = pdf_text.split("\n\n")
    index, _ = build_index(chunks, embedder)
    answer, context = query_book(question, chunks, index, embedder, llm)

    return jsonify({"answer": answer})
