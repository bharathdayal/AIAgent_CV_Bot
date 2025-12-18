# AI Cover Letter Assistant (Streamlit)

A conversational AI bot built with Streamlit that generates ATS-optimized cover letters from user input and job descriptions. Provides a chat-style interface, PDF / Word exports, and is deployable on Streamlit Community Cloud.

- Live demo: streamlit app (deployable)
- Stack: Streamlit + OpenAI (Chat Completions)

---

## Table of contents

- [Features](#features)  
- [Architecture](#architecture)  
- [Tech stack](#tech-stack)  
- [Project structure](#project-structure)  
- [Setup](#setup)  
- [Usage](#usage)  
- [Deployment](#deployment)  
- [Notes](#notes)

---

## Features

- Chat-style AI bot UI for natural conversation flow  
- ATS‑optimized cover letter generation  
- Persistent job description editor (no disappearing input)  
- Dark-themed, professional UI  
- Export as PDF (formatted) and Word (.docx)  
- Safe regeneration when inputs change  
- Deployable to Streamlit Community Cloud

---

## Architecture

User (Browser) → Streamlit Chat UI → Session State Manager → ATS Prompt Builder → LLM (OpenAI) → Cover Letter Generator → PDF / Word Export (Download)

Design principles:
- Modular and production-safe
- Persistent long-form inputs (Job Description)
- Derived state regenerated only when inputs change
- Browser-safe file downloads using in-memory streams

---

## Tech stack

| Layer | Technology |
| ----- | ---------- |
| UI Framework | Streamlit |
| AI / LLM | OpenAI (Chat Completions API) |
| Prompting | ATS-optimized prompt templates |
| State Management | Streamlit Session State |
| Styling | Custom CSS (dark Bot-style UI) |
| PDF Export | reportlab |
| Word Export | python-docx |
| Configuration | python-dotenv |
| Deployment | Streamlit Community Cloud |

---

## Project structure

ai-coverletter-streamlit/
```
├── app.py             # Streamlit app (UI + bot logic)
├── prompts.py         # ATS-optimized prompt templates
├── llm_client.py      # LLM client wrapper
├── export_utils.py    # PDF & Word export utilities
├── config.py          # Environment & secrets handling
├── requirements.txt   # Python dependencies
└── README.md
```

---

## Setup

1. Create and activate virtual environment
  - macOS / Linux
    - python -m venv .venv
    - source .venv/bin/activate
  - Windows
    - python -m venv .venv
    - .venv\Scripts\activate

2. Install dependencies
  - pip install -r requirements.txt

3. Configure environment
  - Set OPENAI_API_KEY and optionally OPENAI_MODEL
    - Example: OPENAI_API_KEY=your_openai_api_key
    - Default model example: OPENAI_MODEL=gpt-4o-mini

---

## Run locally

- Start the app:
  - streamlit run app.py
- Open: http://localhost:8501

---

## How to use

1. Enter candidate name and company name
2. Chat naturally with the bot (experience, skills, projects, focus areas)
3. Paste the job description into the dedicated editor
4. The bot generates an ATS-optimized cover letter automatically
5. Export as PDF or Word from the UI

---

## Deploying to Streamlit Community Cloud

1. Push repository to GitHub (public)
2. Go to https://streamlit.io/cloud and click "New app"
3. Select repository, branch (main), and file path (app.py)
4. Add secrets (OPENAI_API_KEY) in App Settings
5. After deploy you’ll get a public URL like:
  - https://ai-coverletter-streamlit-yourname.streamlit.app

---

## Notes

- Ensure correct OpenAI credentials and billing for model usage.
- Adjust prompt templates in prompts.py for custom tone or formatting.
- For production, secure secrets and consider rate-limiting and request validation.

<!-- Optionally add LICENSE, CONTRIBUTING, and issue templates as needed. -->
This project is for educational and demonstration purposes.
You may adapt or extend it for personal use.
