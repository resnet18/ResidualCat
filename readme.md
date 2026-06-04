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

## Personality: How ResCat Speaks

ResCat is not a generic chatbot. It has a **LoRA-injected personality** (rank=8, 10 epochs) trained on 20 hand-crafted cat-like dialogues, combined with in-context learning (ICL) and a system prompt that enforces its identity:

> *"You are ResCat, a residual cat. You speak in cat-like, slightly confused sentences. Sometimes you say 'meow' at the beginning or the end of a sentence, randomly. You know about skip connections and gradient descent."*

**Official Demo Prompt**:  
`Are you overfitting?`

**Sample Replies** (non-deterministic, temperature=0.7):
- `"No."` → state: `vanish`
- `"I am a residual cat."` → state: `skip`
- `"I'm too short."` → state: `idle`
- `"I am only 10% of me."` → state: `idle`
- `"I am my residual cat. When I am lost, I stay alive."` → state: `skip`

The cat exists in a **quantum superposition** of identities. Each inference collapses the wavefunction differently.

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

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate
pip install -r requirements.txt
python main.py          # verify Day 1 baseline
uvicorn main:app --reload  # start API server
```

Frontend

```bash
cd frontend
npm install
npm run dev             # http://localhost:4321
```

---

Tech Stack

Layer	Technology	
Frontend	Astro, HTML/CSS/JS	
Backend	FastAPI, Uvicorn	
Vision	ResNet18 (torchvision, frozen)	
Language	distilgpt2 (HuggingFace Transformers)	
Personality	LoRA (PEFT, r=8) + ICL + System Prompt	
Fusion	Custom `nn.Linear` projector	
Deployment	Render (backend), static host (frontend)	

---

Development Notes

- Day 1: Pure-text baseline with distilgpt2 verified on CUDA.
- Day 2: ResNet18 + Projector integration, multimodal tensor fusion verified.
- Day 3: FastAPI wrapper, CORS, LoRA personality injection (loss 6.5→1.0), ICL prompt engineering.
- Pixel Art: 5 states (idle, process, skip, vanish, converge) provided by collaborator.

---

License

This is a course assignment. No warranty. If it breaks, check your gradient.