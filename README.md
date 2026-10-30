# NCERC College Helpdesk

A Django-powered campus helpdesk application featuring real AI-powered conversational assistance with verified campus facts, facility images, location details, interactive answer rating/feedback, and links to the official NCERC 360° virtual tour and Google Maps.

---

## 1. AI Integration Overview

The chatbot features a genuine language model integration combined with Retrieval-Augmented Generation (RAG) and an automatic rule-based fallback:

- **Lightweight Retrieval (RAG)**: The backend indexes verified campus facts from `helpdesk/data/ncerc_data.py`. When a question is submitted, only the most relevant verified records are retrieved and passed to the model as reference data.
- **Natural-Language Understanding**: The model interprets diverse conversational phrasings, department inquiries, classroom locations, timings, and exploration queries.
- **Campus Safety & Grounding**: The system prompt strictly constrains the model to rely only on the retrieved facts. It will not hallucinate room numbers, unverified routes, or missing facilities (e.g., ATMs).
- **Ambiguity Clarification**: When an ambiguous place query is entered (e.g., "Where is the office?"), the system asks a clarifying question listing matching facilities.
- **Modular Provider Architecture**: Easily switch between a local offline model and a cloud provider API by changing settings in `.env`.
- **Automatic Rule-Based Fallback**: If the local model is offline, the API key is missing or invalid, rate limits occur, or the AI service times out, the system automatically falls back to the built-in rule-based chatbot so users always get verified answers without application crashes.

---

## 2. Supported AI Providers & Requirements

You can run the chatbot in one of two modes:

### Option A: Local AI Model (`CHAT_AI_PROVIDER=ollama`)
- **Model**: Qwen 2.5 3B Instruct (`qwen2.5:3b`) running via [Ollama](https://ollama.com/).
- **Cost**: **No per-message API charges.** Uses open-weight models.
- **Hardware & Resource Requirements**: Runs directly on your computer. Requires approximately 2–3 GB of disk space for the model weights, at least 8 GB of system RAM, and moderate CPU or GPU processing power.
- **Setup**: Requires downloading and running Ollama on Windows.

### Option B: Cloud AI API (`CHAT_AI_PROVIDER=openai`)
- **Model**: OpenAI `gpt-4o-mini` (or configurable model).
- **Cost & Terms**: **Requires an OpenAI account and API key (`OPENAI_API_KEY`).** Usage is billed according to OpenAI's pay-per-token API terms. (Never assume cloud APIs are free; check your OpenAI account tier and billing credits).
- **Hardware & Resource Requirements**: Negligible local computer resources (runs on OpenAI's remote cloud servers). Requires an active internet connection.

---

## 3. Windows PowerShell Setup Guide

### Prerequisites
- Python 3.10+ installed on Windows.
- VS Code or your preferred editor.

### Step 1: Open Terminal in Project Folder
Open PowerShell in the workspace root:
```powershell
cd C:\Users\aparn\AI-College-Helpdesk
```

### Step 2: Virtual Environment & Dependencies
Activate the virtual environment and verify installed dependencies:
```powershell
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```
*(If PowerShell execution policies block script activation, you can run commands directly using `.\venv\Scripts\python.exe`)*.

### Step 3: Configure Environment Variables (`.env`)
Create your `.env` file from `.env.example` if you do not already have one:
```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

Open `.env` in VS Code. It will look like this:
```env
# Django Secret Key
DJANGO_SECRET_KEY=replace-with-a-long-random-secret

# Master switch: set to false to use only local rule-based chatbot
CHAT_AI_ENABLED=true

# Provider selection: "ollama" (local computer model) or "openai" (cloud AI API)
CHAT_AI_PROVIDER=ollama

# Local Ollama settings (used when CHAT_AI_PROVIDER=ollama)
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=qwen2.5:3b
OLLAMA_TIMEOUT=90

# Cloud OpenAI settings (used when CHAT_AI_PROVIDER=openai)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_TIMEOUT=30

# Chat rate limit (requests per client IP per minute)
CHAT_RATE_LIMIT=12
```

> **Security Note:** Never commit your `.env` file or paste API keys into public chats. `.env` is excluded in `.gitignore`.

To generate a private `DJANGO_SECRET_KEY` on Windows:
```powershell
.\venv\Scripts\python.exe -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 4. Starting the AI Model

### If using Option A: Local Model (Ollama)
1. Install [Ollama for Windows](https://ollama.com/download).
2. Pull the model once in PowerShell:
   ```powershell
   ollama pull qwen2.5:3b
   ```
3. Ensure the Ollama service is running:
   ```powershell
   ollama serve
   ```
4. Set in your `.env`:
   ```env
   CHAT_AI_PROVIDER=ollama
   ```

### If using Option B: Cloud API (OpenAI)
1. In your `.env` file, set:
   ```env
   CHAT_AI_PROVIDER=openai
   OPENAI_API_KEY=your_actual_openai_api_key
   OPENAI_MODEL=gpt-4o-mini
   ```
2. No local model server is required; chat requests connect securely over HTTPS to the OpenAI API endpoint.

---

## 5. Starting the Django Server

In your project terminal:
```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py runserver
```

Open your browser to:
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 6. How the System Works

1. **Question Input**: The user asks a question via the chat widget (e.g., *"Where is the library?"*, *"How can I find the gym?"*, *"Where is room 111?"*, *"What are the canteen timings?"*, or *"How can I explore the campus?"*).
2. **Input Validation**: The backend validates length (up to 1,000 characters) and enforces rate limiting (default 12 requests per IP per minute).
3. **Retrieval**: Relevant entries from `helpdesk/data/ncerc_data.py` are scored and retrieved.
4. **AI Generation**:
   - The selected model (`ollama` or `openai`) is called with strict grounding prompts.
   - If the model is active, the response is labeled `AI-generated answer · local model` or `AI-generated answer · OpenAI`.
5. **Fallback Protection**:
   - If the AI model is disabled, offline, or returns an error, the response cleanly falls back to the local rule-based system without breaking the UI.
   - Responses are rendered securely using safe text elements to prevent XSS.

---

## 7. Running Tests

To verify backend endpoints, mock AI calls, CSRF protection, input limits, and retrieval:
```powershell
.\venv\Scripts\python.exe manage.py test helpdesk.tests
```

To verify frontend script syntax:
```powershell
node --check helpdesk/static/helpdesk/script.js
```

All AI tests use mocked responses so running tests never incurs API costs or requires an active local model server.

---

## 8. Troubleshooting

- **Bot says "The AI assistant is unavailable, so I used the local helpdesk rules":**
  - **For Ollama**: Verify Ollama is running (`ollama list`) and accessible at `http://127.0.0.1:11434`.
  - **For OpenAI**: Check that `OPENAI_API_KEY` in `.env` is valid and your account has active billing/credits.
- **Need to force rule-based mode:**
  - Set `CHAT_AI_ENABLED=false` in `.env` and restart Django.
- **Port 8000 already in use:**
  - Start Django on an alternate port: `python manage.py runserver 8080`.