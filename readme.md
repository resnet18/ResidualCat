# ResidualCat

> **Dev codename**: `rescat`  
> **Core concept**: A lightweight multimodal verification prototype, implemented as a desktop companion.

---

## What is this?

ResidualCat (ResCat) is a minimal multimodal system that fuses visual features from a frozen ResNet18 with text generation from a lightweight GPT-2 (distilgpt2) through a single linear projection layer. The entire pipeline runs locally on CPU or GPU, with no cloud API dependency.

It was built as **Assignment 4: Developing an AI-Assisted Application** for the Software Development Foundations course. The goal is to bridge "prompting for fun" and "engineering for results" by constructing a functional, end-to-end application with LLM-assisted development.

---

## Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Astro     │──────│  FastAPI     │──────│  ResCatCore │
│  Frontend   │      │   Backend    │      │  (ResNet18  │
│  (UI)       │      │  (API)       │      │  + Projector│
└─────────────┘      │              │      │  + GPT2)    │
                     └──────────────┘      └─────────────┘
```

- **Frontend**: Astro static site (`frontend/`) — pixel-art UI, state-driven cat rendering
- **Backend**: FastAPI (`backend/`) — serves the `/rescat` endpoint
- **Core**: `ResCatCore` — frozen ResNet18 (visual encoder) → Linear Projector (512→768) → distilgpt2 (text decoder)

The visual residual is injected as a single token prepended to the text sequence, literally performing `F(x) + x` at the embedding level.

---

## Project Structure

```
rescat/
├── frontend/              # Astro frontend
│   ├── src/pages/         # index.astro (dev entry)
│   └── public/            # pixel art assets (rescat_*.png)
├── backend/               # FastAPI backend
│   ├── main.py            # ResCatCore + API routes
│   └── requirements.txt
├── docs/                  # Development log & report
└── README.md
```

---

## Quick Start

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate
pip install -r requirements.txt
python main.py          # verify Day 1 baseline
```

### Frontend

```bash
cd frontend
npm install
npm run dev             # http://localhost:4321
```

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Astro, HTML/CSS/JS |
| Backend | FastAPI, Uvicorn |
| Vision | ResNet18 (torchvision, frozen) |
| Language | distilgpt2 (HuggingFace Transformers) |
| Fusion | Custom `nn.Linear` projector |
| Deployment | Render (backend), static host (frontend) |

---

## Development Notes

- **Day 1**: Pure-text baseline with distilgpt2 verified on CUDA.
- **Day 2+**: ResNet18 integration, multimodal fusion, FastAPI wrapper.
- **Pixel Art**: 5 states (idle, process, skip, vanish, converge) provided by collaborator.

---

## License

This is a course assignment. No warranty. If it breaks, check your gradient.

## Appendix
```
rescat/
├── frontend/                    
│   ├── src/
│   │   └── pages/
│   │       └── index.astro
│   ├── public/                  
│   │   ├── rescat_idle.png
│   │   ├── rescat_process.png
│   │   ├── rescat_skip.png
│   │   ├── rescat_vanish.png
│   │   └── rescat_converge.png
│   ├── astro.config.mjs
│   └── package.json
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── docs/
│   └── dev_log.md
│
└── README.md
```