from datetime import datetime
from threading import Lock

 
live_messages = []
lock = Lock()

 
MAX_MESSAGES = 100

def save_conversation(role: str, content: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = {
        "time": timestamp,
        "role": role,
        "content": content
    }
    with lock:
        live_messages.append(message)
        # Prevent memory overflow
        if len(live_messages) > MAX_MESSAGES:
            live_messages.pop(0)

def load_conversation() -> str:
    with lock:
        return "\n".join(
            f"{entry['role'].capitalize()}: {entry['content']}"
            for entry in live_messages
        )

def get_all_messages() -> list:
    with lock:
        return list(live_messages)  # Return a copy
