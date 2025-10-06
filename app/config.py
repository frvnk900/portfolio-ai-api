from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Read and validate critical env vars
api_key = os.getenv("API_KEY")
base_url = os.getenv("URL")
model = os.getenv("MODEL", "gpt-3.5-turbo")  # Default fallback

if not api_key:
    raise EnvironmentError("API_KEY is missing in environment variables.")
if not base_url:
    raise EnvironmentError("URL (OpenAI base URL) is missing in environment variables.")

# Optionally log what model is being used
print(f"[LLM] Using model: {model}")

# Instantiate the OpenAI model wrapper
LLM = ChatOpenAI(
    api_key=api_key,
    base_url=base_url,
    model=model,
    timeout=30  # Optional: request timeout in seconds
)
