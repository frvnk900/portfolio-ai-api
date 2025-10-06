import os
import time
import threading
import logging
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from app.chatbot import ai
from app.data import get_all_messages

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Thread-safe clients list for Server-Sent Events
clients = []
clients_lock = threading.Lock()

@app.route("/chat/post", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("message")

        if not user_input or not isinstance(user_input, str) or len(user_input.strip()) == 0:
            return jsonify({"error": "Invalid or missing 'message' in request body"}), 400

        if len(user_input) > 1000:  # Limit message size
            return jsonify({"error": "Message too long"}), 400

        response = ai(user_input)

        # Broadcast response to all SSE clients
        with clients_lock:
            for q in clients:
                q.append(f"data: {response}\n\n")

        return jsonify({"response": response})

    except Exception as e:
        logging.exception("Error in /chat/post")
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.route("/chat/stream")
def stream():
    def event_stream():
        q = []
        with clients_lock:
            clients.append(q)
        try:
            while True:
                if q:
                    msg = q.pop(0)
                    yield msg
                time.sleep(0.1)
        except GeneratorExit:
            with clients_lock:
                clients.remove(q)

    return Response(event_stream(), content_type="text/event-stream")


@app.route("/chat/messages", methods=["GET"])
def get_messages():
    try:
        return jsonify({"messages": get_all_messages()})
    except Exception as e:
        logging.exception("Error in /chat/messages")
        return jsonify({"error": str(e)}), 500


# Entry point only for local testing
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001))
    app.run(debug=False, threaded=True, port=port)

