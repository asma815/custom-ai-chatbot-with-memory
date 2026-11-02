
import json
import urllib.request
import urllib.error

import streamlit as st

st.set_page_config(
    page_title="Custom AI Chatbot with Memory",
    page_icon="💬",
    layout="centered",
)

st.title("💬 Custom AI Chatbot with Memory")
st.caption("DecodeLabs Generative AI Internship — Project 1")
st.write(
    "Chat with the AI. It uses messages in this live session "
    "to keep track of the conversation."
)

MODEL = "llama3.2:1b"
OLLAMA_URL = "http://localhost:11434/api/chat"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful, clear, and friendly AI assistant. "
                "Use the conversation context when answering."
            ),
        }
    ]

with st.sidebar:
    st.header("Settings")
    st.write(f"Local model: `{MODEL}`")
    st.write("Memory: current browser session")

    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful, clear, and friendly AI assistant. "
                    "Use the conversation context when answering."
                ),
            }
        ]
        st.rerun()

    st.caption("Uses a local Ollama model. No paid API key required.")

for message in st.session_state.messages:
    if message["role"] in ("user", "assistant"):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

prompt = st.chat_input("Type your message...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        payload = {
            "model": MODEL,
            "messages": st.session_state.messages,
            "stream": False,
            "options": {"temperature": 0.7},
        }

        request = urllib.request.Request(
            OLLAMA_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with st.chat_message("assistant"):
            with st.spinner("AI is thinking..."):
                with urllib.request.urlopen(
                    request, timeout=180
                ) as response:
                    result = json.loads(
                        response.read().decode("utf-8")
                    )

                answer = result.get("message", {}).get(
                    "content", ""
                ).strip()

                if not answer:
                    answer = "The model returned an empty response."

                st.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        st.error(
            f"Ollama returned HTTP {exc.code}. "
            f"Details: {details[:500]}"
        )

    except urllib.error.URLError:
        st.error(
            "Could not connect to Ollama. Check that Ollama is "
            "running on your computer, then try again."
        )

    except Exception as exc:
        st.error(f"Unexpected error: {type(exc).__name__}: {exc}")

with st.expander("How the memory works"):
    st.markdown(
        "- `st.session_state.messages` stores conversation history.\n"
        "- Each user message is appended to the history.\n"
        "- The complete history is sent to the local Ollama model.\n"
        "- Each assistant response is appended after a successful reply.\n"
        "- Memory lasts for the active session; it is not permanent storage."
    )
