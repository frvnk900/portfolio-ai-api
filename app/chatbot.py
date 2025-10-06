from app.config import LLM
from app.template import system_prompt
from langchain_core.prompts import PromptTemplate
from app.data import load_conversation, save_conversation
import requests

# Build prompt once at module level
prompt_chain = PromptTemplate(
    template=system_prompt,
    input_variables=["user", "history"],
    validate_template=True
) | LLM

def ai(user_text: str) -> str:
    try:
        # Save user message
        save_conversation(role="user", content=user_text)

        # Invoke the chain with user input + chat history
        response = prompt_chain.invoke({
            "user": user_text,
            "history": load_conversation()
        })

        # Get response content
        assistant_reply = getattr(response, "content", None)

        if not assistant_reply:
            return "⚠️ AI did not return a valid response."

        # Save assistant reply
        save_conversation(role="assistant", content=assistant_reply)

        return assistant_reply

    except ValueError as ve:
        return f"❌ Prompt formatting error. Please rephrase your message.\n\nDetails: {ve}"

    except AttributeError as ae:
        return f"⚙️ AI model configuration issue. Contact support.\n\nDetails: {ae}"

    except KeyError as ke:
        return f"📁 Missing expected conversation data.\n\nDetails: {ke}"

    except requests.exceptions.ConnectionError:
        return "🌐 Network error: could not reach the AI service. Please try again later."

    except requests.exceptions.HTTPError as he:
        return f"📡 AI service returned an HTTP error ({he.response.status_code}). Try again later."

    except TypeError as te:
        return f"🧮 Unexpected input format.\n\nDetails: {te}"

    except RuntimeError as re:
        return f"⚠️ AI service runtime error.\n\nDetails: {re}"

    except TimeoutError as te:
        return f"⏱️ AI service timeout. Please try again shortly.\n\nDetails: {te}"

    except Exception as e:
        return f"❗ An unexpected error occurred.\n\nDetails: {str(e)}"



