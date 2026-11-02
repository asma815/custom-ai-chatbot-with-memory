
# Custom AI Chatbot with Memory

**DecodeLabs Generative AI Internship — Project 1**

## Overview
A Streamlit-based chatbot that uses a local AI model through Ollama. It maintains conversation history during the active session so the AI can use earlier messages when answering.

## Features
- Interactive chatbot web interface
- Local AI model using Ollama
- Session-based conversation memory
- Context-aware responses
- Clear conversation button
- No paid API key required for local inference

## Technologies
- Python
- Streamlit
- Ollama
- Llama 3.2 1B

## Requirements
- Python
- Ollama
- Internet connection for the initial model download

## Setup

### 1. Install dependencies
```powershell
python -m pip install -r requirements.txt
```

### 2. Download and start the model
```powershell
ollama run llama3.2:1b
```

Wait for the model to start. Type `/bye` to exit its interactive prompt when needed. Ollama can continue running as a local service.

### 3. Run the app
From the folder containing `app.py`, run:
```powershell
python -m streamlit run app.py
```

Open the Local URL shown in the terminal, usually http://localhost:8501.

## How Memory Works
The app stores conversation messages in `st.session_state.messages`. User messages are added to the list, the conversation history is sent to the local model, and the assistant response is added after a successful reply.

Memory is for the active Streamlit session. It is not permanent database storage.

## Implementation Note
This version uses a local Ollama model instead of the OpenAI API. It avoids paid API usage but differs from an assignment requirement that specifically asks for an official SDK and API key.
