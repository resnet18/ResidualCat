# ResidualCat

> **Dev codename**: `rescat`  
> **Core concept**: A lightweight multimodal verification prototype, implemented as a desktop companion.

---

## What is this?

ResidualCat (ResCat) is a minimal multimodal system that fuses visual features from a frozen ResNet18 with text generation from a lightweight GPT-2 (distilgpt2) through a single linear projection layer. The entire pipeline runs on CPU or GPU, with no commercial cloud API dependency.

It was built as **Assignment 4: Developing an AI-Assisted Application** for the Software Development Foundations course. The goal is to bridge "prompting for fun" and "engineering for results" by constructing a functional, end-to-end application with LLM-assisted development.

---

## Architecture

```

┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Astro     │──────│  FastAPI     │──────│ ResCatCore  │
│  Frontend   │      │  Backend     │      │ (ResNet     │
│  (UI)       │      │  (API)       │      │ + Projector │
└─────────────┘      └──────────────┘      │ + GPT)      │
                                           └─────────────┘

```

- **Frontend**: Astro static site (`frontend/`) — pixel-art UI, state-driven cat rendering
- **Backend**: FastAPI (`backend/`) — serves the `/rescat` endpoint
- **Core**: `ResCatCore` — frozen ResNet18 (visual encoder) → Linear Projector (512→768) → distilgpt2 (text decoder)

The visual residual is injected as a single token prepended to the text sequence, literally performing `F(x) + x` at the embedding level.

---

## Personality: How ResCat Speaks

ResCat is not a generic chatbot. It has a **LoRA-injected personality** (rank=8, 10 epochs) trained on 20 hand-crafted cat-like dialogues, combined with in-context learning (ICL) and a system prompt that enforces its identity:

> *"You are ResCat, a residual cat. You speak in cat-like, slightly confused sentences. Sometimes you say 'meow' at the beginning or the end of a sentence, randomly. You know about skip connections and gradient descent."*

**Official Demo Prompt 1**:  
`Are you overfitting?`

**Sample Replies** (non-deterministic, temperature=0.7):
- `"No."` → state: `vanish`
- `"I am a residual cat."` → state: `skip`
- `"I'm too short."` → state: `idle`
- `"I am only 10% of me."` → state: `idle`
- `"I am my residual cat. When I am lost, I stay alive."` → state: `skip`
- `"It seems like I'm trying to be a cat."` → state: `idle`

*Note: The cat exists in a **quantum superposition** of identities. Each inference collapses the wavefunction differently.*

**Official Demo Prompt 2**:  
`ResCat achieved state-of-the-art performance on assignment 4.`

**Sample Replies** (long-input survival mode, temperature=0.7):
- `"Meow?"` → state: `converge` (acknowledges achievement with a cat noise)
- `"Wow"` → state: `idle` (minimalist appreciation)
- `"Only 2% of the time is lost."` → state: `idle` (philosophical reflection on efficiency)
- `"Its natural language."` → state: `idle` (simultaneously humble, proud, and sarcastic about SOTA inflation)
- `"I am a human."` → state: `idle` (identity crisis under academic pressure)
- `"It is a residual cat."` → state: `skip` (self-referential confirmation)

*Note: Long inputs (>15 tokens) push ResCat into "survival mode" — outputs become more unpredictable, occasionally philosophical, and sometimes question their own species.*

---

## A Note on Semantics (For Formal Semanticists)

The concept "ResNet Cat" was originally hallucinated by an LLM during chain-of-thought reasoning. It resists classical compositional semantics:

- **No fixed extension**: You cannot list all objects that are ResNet Cats.
- **No intensional definition**: No truth-conditional formula captures what it means to be one.
- **No type**: It is simultaneously an image concept, a behavior metaphor, and an architecture allegory.

ResCat operationalizes this undefined concept through usage: the model does not *define* what a residual cat is — it *performs* the cat by generating replies under visual and textual residuals. This is a practical refutation of formal semantics from within NLP engineering, built by someone who never took a linguistics course.

*If the cat speaks, the semantics is in the inference, not in the lexicon.*

---

## Project Status

| Component | Status |
|-----------|--------|
| Astro Frontend | ✅ Complete |
| FastAPI Backend | ✅ Complete |
| ResNet18 + Projector Fusion | ✅ Complete |
| LoRA Personality (r=8, 10ep) | ✅ Complete |
| 5-State Pixel Art | ✅ Complete |
| Hugging Face Deployment | ✅ Live at `https://avenir-02-rescat.hf.space` |
| Local `.exe` Desktop Version |  Future Work |
| ONNX Quantization |  Future Work |

---

## Project Structure

```

rescat/
├── frontend/              # Astro frontend
│   ├── src/pages/         # index.astro (dev entry)
│   └── public/            # pixel art assets (rescat.png)
├── backend/               # FastAPI backend
│   ├── main.py            # ResCatCore + API routes + LoRA loader
│   ├── lora_train.py      # LoRA training script (r=8, 10ep)
│   ├── cat_data.json      # 20 hand-crafted cat dialogues
│   ├── rescat_lora_adapter/  # Trained adapter weights
│   └── requirements.txt
├── docs/                  # Development log & report
└── README.md

```

---

## Quick Start

### Backend (Local)

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload  # start API server on :8000
```

Frontend (Local)

```bash
cd frontend
npm install
npm run dev             # http://localhost:4321
```

Online Deployment

- Backend: Deployed on [Hugging Face Spaces](https://huggingface.co/spaces/avenir-02/rescat) (Docker, CPU Basic)
- API Endpoint: `https://avenir-02-rescat.hf.space/rescat`

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Astro, HTML/CSS/JS |
| Backend | FastAPI, Uvicorn |
| Vision | ResNet18 (torchvision, frozen) |
| Language | distilgpt2 (HuggingFace Transformers) |
| Personality | LoRA (PEFT, r=8) + ICL + System Prompt |
| Fusion | Custom `nn.Linear` projector |
| Deployment | Hugging Face Spaces (backend), static host (frontend) |

---

Development Notes

- Day 1: Pure-text baseline with distilgpt2 verified on CUDA.
- Day 2: ResNet18 + Projector integration, multimodal tensor fusion verified.
- Day 3: FastAPI wrapper, CORS, LoRA personality injection (loss 6.5→1.0), ICL prompt engineering.
- Day 4: Hugging Face Spaces deployment, frontend-backend integration, end-to-end test with ImageNet test images.
- Pixel Art: 5 states (idle, process, skip, vanish, converge) provided by collaborator.

---

Future Work

- Desktop Companion: Package as `.exe` / `.app` via Tauri or PyQt for fully offline operation
- Model Compression: Convert to ONNX / quantize for edge-device deployment
- Vision-Language Alignment: Train with real image-text pairs instead of text-only LoRA

---

License

This is a course assignment. No warranty. If it breaks, check your gradient.