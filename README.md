# NCERC College Helpdesk

A Django-powered campus helpdesk application designed to help students, visitors, and staff find information about Nehru College of Engineering and Research Centre (NCERC).

The application provides a conversational chatbot, verified campus information, facility images, location details, interactive feedback, and links to the official NCERC 360° virtual tour and Google Maps.

## Features

- **Conversational Chatbot:** Allows users to ask questions about campus facilities, departments, locations, and services using natural language.
- **AI Integration:** Supports configurable AI providers, including a local Ollama model and the OpenAI API, when properly configured.
- **Verified Campus Information:** Retrieves campus information from a structured local dataset.
- **Rule-Based Fallback:** Provides predefined helpdesk responses when AI is disabled or unavailable.
- **Facility Information:** Displays information about facilities such as the library, canteen, gym, hostel, transportation, auditorium, and seminar hall.
- **Campus Navigation:** Helps users explore available campus locations and access relevant navigation resources.
- **Interactive Feedback:** Allows users to submit feedback about chatbot responses.
- **Responsive Interface:** Uses HTML, CSS, and JavaScript to provide an interactive user interface.
- **Request Validation:** Includes input validation and request rate limiting.
- **Security Measures:** Uses Django's built-in security features and safe frontend rendering practices.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, Django |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite |
| AI Integration | Ollama and optional OpenAI API |
| Data Source | Structured Python campus dataset |
| Development Environment | Visual Studio Code |
| Version Control | Git and GitHub |

## Project Structure

```text
AI-College-Helpdesk/
│
├── college_helpdesk/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── helpdesk/
│   ├── data/
│   │   └── ncerc_data.py
│   ├── management/
│   │   └── commands/
│   ├── migrations/
│   ├── static/
│   │   └── helpdesk/
│   │       ├── images/
│   │       ├── script.js
│   │       ├── style.css
│   │       └── ngi campus.webp
│   ├── templates/
│   │   └── helpdesk/
│   │       └── home.html
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   └── ai.py
│
├── scratch/
├── .env.example
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

*Note: The exact files and folders may vary depending on the current version of the project.*

## AI Integration Overview

The chatbot can use an AI provider or operate in rule-based mode.

### 1. Local AI Using Ollama

Ollama allows supported language models to run on your own computer.

The project can be configured to use the Qwen 2.5 3B Instruct model:

- Model identifier: `qwen2.5:3b`
- Runs locally after the model has been downloaded.
- Does not require a paid API for model inference.
- Requires sufficient system memory, storage, and processing power.

### 2. Cloud AI Using OpenAI

The project can also be configured to use the OpenAI API.

- Model: Configurable through environment variables.
- Requires an OpenAI API key and an account with available API access and billing.
- Requires an internet connection.
- API usage may incur charges.

### 3. Rule-Based Fallback

When AI is disabled or unavailable, the application can use its built-in rule-based responses.

The fallback helps users continue accessing supported campus information without depending entirely on an external AI service.

**Important:** AI availability and behavior depend on the configured provider, installed dependencies, environment variables, and current application implementation.

## How the System Works

1. The user opens the helpdesk website.
2. The user enters a question in the chat interface.
3. The backend validates the incoming request.
4. Relevant information is retrieved from the campus dataset.
5. If AI is enabled and available, the configured model generates a response using the retrieved information.
6. If AI cannot provide a response, the application can use its rule-based fallback.
7. The answer is displayed in the chat interface.
8. The user can submit feedback where supported.

### Example Questions

Users may ask questions such as:

- Where is the central library?
- What are the canteen timings?
- Where is the gym located?
- What facilities are available on campus?
- How can I explore the campus virtually?
- Where is a particular classroom?
- What transportation facilities are available?

The accuracy of answers depends on the information available in the project's campus dataset.

## Requirements

Before running the project, ensure you have:

- Python installed.
- pip available.
- Git installed if you want to clone the repository.
- Visual Studio Code or another Python-compatible editor.
- A web browser.

For AI functionality, additional requirements depend on the selected provider.

## Installation and Setup

### Step 1: Clone the Repository

Open PowerShell and navigate to the folder where you want to store the project.

Run:

```powershell
git clone https://github.com/Aparnarajeev06/AI-college-helpdesk.git
```

Navigate into the project folder:

```powershell
cd AI-college-helpdesk
```

### Step 2: Create a Virtual Environment

Create a Python virtual environment:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use the virtual environment's Python executable directly.

### Step 3: Install Dependencies

Install the packages listed in `requirements.txt`:

```powershell
python -m pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a local `.env` file from `.env.example` if one does not already exist:

```powershell
if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
}
```

Open `.env` in VS Code and review the configuration.

Example configuration:

```env
DJANGO_SECRET_KEY=replace-with-a-secure-random-secret

CHAT_AI_ENABLED=true
CHAT_AI_PROVIDER=ollama

OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=qwen2.5:3b
OLLAMA_TIMEOUT=90

OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_TIMEOUT=30

CHAT_RATE_LIMIT=12
```

**Important:** Use only environment variable names supported by the project's settings and AI implementation. The values above are examples and may need adjustment to match your current code.

Never commit your actual `.env` file, passwords, API keys, or production secrets to GitHub.

### Step 5: Generate a Django Secret Key

You can generate a new secret key with:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the generated value into your local `.env` file if your settings are configured to read `DJANGO_SECRET_KEY` from that file.

Do not publish the generated secret key.

### Step 6: Start the Local AI Model (Optional)

If you choose Ollama, install it from the official website:

https://ollama.com/

Download the configured model:

```powershell
ollama pull qwen2.5:3b
```

Ensure Ollama is running and the model is available.

You can check the installed models with:

```powershell
ollama list
```

Set the provider in `.env` to the value supported by your application:

```env
CHAT_AI_PROVIDER=ollama
```

If you choose the OpenAI API instead, configure a valid API key and the supported provider settings.

### Step 7: Run Database Migrations

Run:

```powershell
python manage.py migrate
```

### Step 8: Check the Django Project

Run:

```powershell
python manage.py check
```

### Step 9: Start the Development Server

Run:

```powershell
python manage.py runserver
```

Open the following address in your browser:

http://127.0.0.1:8000/

The application should now be accessible locally.

## Testing

Run the Django application tests:

```powershell
python manage.py test helpdesk.tests
```

If Node.js is installed, you can check the JavaScript syntax:

```powershell
node --check helpdesk/static/helpdesk/script.js
```

Test coverage depends on the tests implemented in the project.

## Security Considerations

- Keep `.env` out of version control.
- Never publish real API keys or Django secret keys.
- Do not commit private user information or sensitive database contents.
- Exclude `venv/`, `.venv/`, `__pycache__/`, and compiled Python files using `.gitignore`.
- Use Django's built-in protections and validate incoming user input.
- Use a production-ready deployment configuration before making the application publicly accessible.
- Review all committed files before pushing them to a public repository.

## Troubleshooting

### 1. Django Is Not Installed

Activate the virtual environment and run:

```powershell
python -m pip install -r requirements.txt
```

### 2. Virtual Environment Activation Fails

Use the virtual environment's Python executable directly:

```powershell
.\venv\Scripts\python.exe manage.py runserver
```

### 3. AI Responses Are Unavailable

For Ollama:

```powershell
ollama list
```

Check that the configured model exists and that the Ollama service is running.

For OpenAI, check the API key, account access, billing, and provider configuration.

If AI is unavailable, verify that the application's rule-based fallback is enabled and functioning as intended.

### 4. Port 8000 Is Already in Use

Run Django on another port:

```powershell
python manage.py runserver 8080
```

Open:

http://127.0.0.1:8080/

### 5. Static Files Are Not Displayed

Check the static file paths in the templates and confirm that the corresponding files exist under the application's static directory.

### 6. Database or Migration Errors

Run:

```powershell
python manage.py check
python manage.py migrate
```

If the error continues, inspect the terminal output to identify the affected migration or database operation.

## Future Enhancements

Possible future improvements include:

- Expanding the verified campus information dataset.
- Improving campus search and navigation.
- Adding multilingual responses.
- Enhancing accessibility and mobile responsiveness.
- Improving chatbot testing and response evaluation.
- Adding more detailed feedback analysis.
- Deploying the application to a production hosting environment.

These are potential enhancements and may not be implemented in the current version.

## Project Information

**Project Name:** NCERC College Helpdesk

**Institution:** Nehru College of Engineering and Research Centre (NCERC)

**Category:** Web Application / Campus Information System

**Backend:** Python and Django

**Frontend:** HTML, CSS, and JavaScript

**Database:** SQLite

**Repository:** https://github.com/Aparnarajeev06/AI-college-helpdesk

---

*This project is intended to make campus information easier to access through a conversational helpdesk interface. Verify important campus information with official college sources when necessary.*