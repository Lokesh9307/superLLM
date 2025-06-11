from flask import Blueprint, request, jsonify
from app.services.youtube_processing import extract_video_id, get_transcript_chunks
from app.utils.vector_store import build_index, query_index
from app.services.llm_initializer import llm, embedder
import sys
import re

youtube_blueprint = Blueprint("youtube", __name__)
video_index_cache = {}

@youtube_blueprint.route("/process", methods=["POST"])

def process_video():
    try:
        data = request.get_json(force=True)


        if not data:
            return jsonify({"error": "Missing request body"}), 400

        url = data.get("url", "").strip()
        if not url:
            return jsonify({"error": "Missing or invalid 'url'"}), 400

        video_id = extract_video_id(url)

        if not video_id:
            return jsonify({"error": "Invalid YouTube URL"}), 400

        chunks = get_transcript_chunks(video_id)
        index, vectors = build_index(chunks, embedder)
        video_index_cache[video_id] = (chunks, index, vectors)

        return jsonify({
            "success": True,
            "message": "Transcript indexed successfully.",
            "video_id": video_id
        })

    except Exception as e:
        return jsonify({"error": f"Processing error: {str(e)}"}), 500

def remove_think_tags(text):
    cleaned_text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    return cleaned_text.strip()


@youtube_blueprint.route("/chat", methods=["POST"])
def chat_with_video():
    try:
        data = request.get_json(force=True)
 

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        video_url = data.get("url", "").strip()
        question = data.get("question", "").strip()
        history = data.get("history", [])

        video_id = extract_video_id(video_url)
     

        if not video_url or not question or not video_id:
            return jsonify({"error": "Missing or invalid 'url' or 'question'"}), 400

        if video_id not in video_index_cache:
            return jsonify({"error": "Video not indexed. Please call /process first."}), 400

        chunks, index, vectors = video_index_cache[video_id]
        answer, context = query_index(question, chunks, index, vectors, embedder, llm)

        messages = [{"role": "system", "content": "You are a smart assistant who helps explain YouTube videos."}]
        for msg in history:
            if "role" in msg and "content" in msg:
                messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": f"Video context:\n{context}\n\nQuestion: {question}"})

        result = llm.invoke(messages)
        raw_answer = getattr(result, "content", str(result))
        
        final_answer = remove_think_tags(raw_answer).strip()

        return jsonify({"answer": final_answer})
    except Exception as e:
        return jsonify({"error": f"Chat error: {str(e)}"}), 500
