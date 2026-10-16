# LearnPilot AI

LearnPilot AI is a Streamlit learning companion. Ask an AI tutor to explain a topic, try a short sample quiz, and view your progress for the current session.

## Features

- **AI Tutor:** Request explanations by subject and learning level.
- **Smart Quiz:** Check your knowledge with a sample science question.
- **Progress:** View questions answered and correct quiz answers during the current session.
- **AI providers:** Use a local Ollama model by default, or configure OpenAI.

## Requirements

- Python 3.11 or newer
- The Python packages listed in [`requirements.txt`](requirements.txt)
- For the default AI setup, [Ollama](https://ollama.com/) with a model downloaded locally
- For OpenAI, an OpenAI API key

## Setup

Open PowerShell in the project directory and create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the Python dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Run with Ollama (default)

Install and start Ollama, then download the default model:

```powershell
ollama pull gemma3:1b
```

Start the app from the project directory:

```powershell
streamlit run app.py
```

Streamlit will print a local URL to open in your browser. The app expects Ollama to be available at `http://localhost:11434` by default.

## Run with OpenAI

Set the provider and API key in PowerShell before starting Streamlit:

```powershell
$env:AI_PROVIDER = "openai"
$env:OPENAI_API_KEY = "your-api-key"
streamlit run app.py
```

The OpenAI provider uses `gpt-4.1-mini` by default. You can select a different model with `OPENAI_MODEL`:

```powershell
$env:OPENAI_MODEL = "your-model-name"
```

Keep API keys private. Do not commit them to the repository.

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `AI_PROVIDER` | `ollama` | AI backend: `ollama` or `openai` |
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama server URL |
| `OLLAMA_MODEL` | `gemma3:1b` | Model name used by Ollama |
| `OPENAI_API_KEY` | — | API key required when using OpenAI |
| `OPENAI_MODEL` | `gpt-4.1-mini` | Model name used by OpenAI |

For example, to use a different Ollama model:

```powershell
$env:OLLAMA_MODEL = "your-installed-model"
streamlit run app.py
```

## Project structure

```text
.
├── app.py           # Streamlit application
├── requirements.txt # Python dependencies
└── README.md        # Setup and usage guide
```

## Notes

- The quiz currently contains one built-in science question.
- Progress is stored in Streamlit session state and is not persisted after the session ends.
- Ollama must be running and the configured model must be installed for local AI requests.
