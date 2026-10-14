# Assistente Diversa

Chatbot sobre educação inclusiva, desenvolvido pela **Team Hélice** (SoulCode Academy / Accenture). O projeto usa uma API FastAPI e uma interface React, executadas localmente com Docker Compose.
# Assistente Diversa — Inclusive Education

A RAG chatbot about inclusive education, based on articles from the [Diversa Portal](https://diversa.org.br/). Graduation project by **Team Hélice** (SoulCode Academy / Accenture).

The web version separates the original prototype (a Gradio notebook) into a FastAPI API and a React interface. The notebook is available in [notebooks/](notebooks/README.md).

## Architecture

```mermaid
graph LR
    U[User] <--> CF[Frontend]
    CF <--> API[Backend]
```

The `POST /api/chat` flow validates the input, checks whether the question is in scope (out-of-scope questions receive a redirect), retrieves articles, builds a profile-specific prompt, calls Groq, and post-processes the response. If no Groq key is configured or the request fails, the API responds in demo mode.

| Method | Route | Purpose |
|---|---|---|
| GET | `/api/health` | Status and number of indexed articles |
| GET | `/api/profiles` | Profiles, greetings, and suggested questions |
| POST | `/api/chat` | `{pergunta, perfil, historico}` → `{resposta, perfil, fontes, origem}` |

Version 1 does not use a database: articles are stored in `backend/app/data/artigos.csv`, chat history is stored in the browser (`localStorage`), and each interaction is recorded as a JSON line in the log.

## Project Structure

```
backend/    FastAPI API (app/api, core, services, repositories, schemas, data) and tests
frontend/   React + Vite + TypeScript
infra/      SAM template (Lambda, S3, CloudFront, and budget) and deployment script
notebooks/  Original Gradio prototype
```

## Run Locally

Configure the Groq key by copying `.env.example` to `.env` in the project root (`GROQ_KEY=...`). The key is optional.

```bash
# API at http://localhost:8000
cd backend
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
.venv/bin/uvicorn app.main:app --reload --port 8000

# Frontend at http://localhost:5173 (in another terminal)
cd frontend
npm install && npm run dev
```

Backend tests: `cd backend && .venv/bin/pytest`.

## Backend Configuration

Environment variables (or `.env`):

| Variable | Default | Purpose |
|---|---|---|
| `GROQ_KEY` | empty | Groq API key (also accepts `GROQ_API_KEY`) |
| `GROQ_MODEL` | `openai/gpt-oss-20b` | Model to use |
| `CORS_ORIGINS` | `http://localhost:5173` | Comma-separated list of allowed origins |
| `RATE_LIMIT_POR_MINUTO` | `20` | Requests per IP on `/api/chat` |
| `MAX_CHARS_PERGUNTA` | `1000` | Maximum question length |

## Executar com Docker

Pré-requisito: Docker com Docker Compose.

Na raiz do projeto, execute:

```bash
docker compose up --build
```

Acesse:

- Interface: http://localhost:5173
- API: http://localhost:8000
- Status da API: http://localhost:8000/api/health

Para encerrar, pressione `Ctrl+C` e execute `docker compose down`.

### Chave Groq (opcional)

Sem chave, a API funciona em modo demonstração. Para habilitar respostas via Groq, crie `.env` na raiz a partir do arquivo de exemplo e informe sua chave:

```bash
cp .env.example .env
```

Edite `.env` e substitua `your_key_here` em `GROQ_KEY` pela sua chave. Depois, inicie ou reinicie os contêineres com `docker compose up --build`.
