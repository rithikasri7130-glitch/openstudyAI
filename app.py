from flask import Flask, request, jsonify, send_from_directory
import requests
import fitz

app = Flask(__name__)
MODEL = "llama3.2:1b"
OLLAMA_URL = "http://localhost:11434/api/chat"

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/<path:filename>")
def frontend_files(filename):
    if filename in ("style.css", "script.js"):
        return send_from_directory(".", filename)
    return jsonify({"error": "File not found"}), 404

@app.route("/api/study", methods=["POST"])
def study():
    try:
        mode = request.form.get("mode", "ask")
        question = request.form.get("question", "").strip()
        upload = request.files.get("pdf")
        notes = ""

        if upload:
            doc = fitz.open(stream=upload.read(), filetype="pdf")
            notes = "".join(page.get_text() for page in doc)[:6000]

        if mode == "summary":
            prompt = f"Summarize these notes in simple English with bullet points:\n\n{notes}"
        elif mode == "quiz":
            prompt = f"Create 5 MCQ questions with answers from these notes:\n\n{notes}"
        else:
            prompt = f"Notes:\n{notes}\n\nQuestion: {question}\nAnswer in simple English."

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
            },
            timeout=180,
        )
        response.raise_for_status()
        return jsonify({"answer": response.json()["message"]["content"]})

    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Ollama run aagala. Terminal-la 'ollama serve' pannu."}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)

 

