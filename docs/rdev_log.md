# ResCat Development Log & Plan

**Project**: ResidualCat (rescat)  
**Current Date**: June 5, 2026 (17:00)  
**Presentation Deadline**: June 12, 2026 (7 days left)  
**Documentation Deadline**: June 26, 2026  
**Repository**: https://github.com/resnet18/ResidualCat  
**Live API**: https://avenir-02-rescat.hf.space

---

## Status Overview

| Component | Status | Notes |
|-----------|--------|-------|
| Astro Frontend | ✅ Complete | Pixel-art UI, state-driven rendering, image upload |
| FastAPI Backend | ✅ Complete | `/rescat` endpoint, CORS, LoRA + ICL |
| ResNet18 Integration | ✅ Complete | Frozen, output 512d, verified on CPU/GPU |
| Projector Layer | ✅ Complete | Linear(512→768), tensor shape verified |
| Multimodal Fusion | ✅ Complete | Visual token + text embeddings, dummy + real image tested |
| LoRA Personality | ✅ Complete | r=8, 10 epochs, loss 6.5→1.0, 20 cat dialogues |
| FastAPI API & CORS | ✅ Complete | Returns `{reply, state}`, cross-origin enabled |
| Pixel Art Assets | ✅ Complete | 5 states (idle/process/skip/vanish/converge) from collaborator |
| Hugging Face Deployment | ✅ Complete | Live at `https://avenir-02-rescat.hf.space` |
| Dev Log / Report | In Progress | This file |
| Local `.exe` Version | 🔮 Future Work | Post-presentation |

---

## Revised Execution Plan (June 5 → June 12)

### Day 1 (June 2) ✅ COMPLETE
- [x] Initialize project directory structure
- [x] Set up Astro frontend skeleton (`npm install` success)
- [x] Verify backend pure-text generation with distilgpt2 on CUDA
- [x] Push clean repository to GitHub (no large files)

### Day 2 (June 3) ✅ COMPLETE
- [x] Load pretrained ResNet18, strip FC layer (output 512d)
- [x] Implement `Linear(512 → 768)` projector
- [x] Verify tensor shapes: image → ResNet → projector → [1, 1, 768]
- [x] Log: document dimension alignment issues and fixes

### Day 3 (June 4-5) ✅ COMPLETE
- [x] Concatenate visual token + text embeddings along sequence dim
- [x] Feed fused sequence into distilgpt2.generate(inputs_embeds=...)
- [x] Test with dummy image (white tensor) vs. real image
- [x] Implement error fallback: if image fails, zero-out visual residual
- [x] Wrap in FastAPI with `/rescat` POST endpoint
- [x] Add CORS middleware for Astro frontend
- [x] **LoRA Personality Injection**: r=8, 10 epochs, 20 hand-crafted cat dialogues
- [x] **ICL Prompt Engineering**: system prompt + 1-shot example
- [x] **State Heuristic**: map natural vocabulary (meow/residual/no) to 5 states
- [x] Log: document CoT hallucination handling during fusion and personality tuning

### Day 4 (June 5) ✅ COMPLETE — Deployment & Frontend Integration
- [x] **Hugging Face Spaces deployment** (Docker, CPU Basic, 16GB RAM)
- [x] Verify API health from external network (`/rescat` returns JSON)
- [x] Frontend `fetch()` integration with `mode: 'cors'`
- [x] Auto-idle state machine (2s timeout after non-idle states)
- [x] Image upload via `FormData` (text + optional image)
- [x] End-to-end test with ImageNet test images (cat recognized as "It is a cat.")
- [x] Log: documented deployment workflow and CORS debugging

## Completed

- **Backend**: FastAPI + ResCatCore (ResNet18 → Projector → distilgpt2 + LoRA adapter)
- **Frontend**: Astro pixel-art UI with 5-state auto-idle machine
- **Deployment**: Hugging Face Spaces (Docker, CPU Basic)
- **Personality**: LoRA (r=8, 10ep, loss 6.5→1.0) + ICL + system prompt
- **Multimodal**: Text + image upload, visual residual injection verified

---

## Key Technical Decisions

- **LoRA r=8**: r=2 too weak, pure prompt too generic. Triple insurance (adapter + ICL + system prompt) achieves stable cat personality.
- **1-shot ICL**: 2+ examples caused template overfitting ("I am a cat" regardless of input).
- **Temperature 0.7**: 0.1 = repetition, 1.0 = hallucination, 0.7 = quantum superposition.
- **State mapping**: Bound to natural vocabulary (meow → converge, residual → skip, no → vanish) rather than abstract concepts.
- **Hugging Face Spaces**: Render requires foreign credit card; HF Spaces offers 16GB CPU free tier with no card.

---

## What's Next

- **Demo prep**: Record GIF fallback, test on classroom machine, prepare 3 fixed inputs.
- **Report**: Write AI-assisted development narrative for June 26 submission.
- **Future work**: Local `.exe` via Tauri/PyQt, ONNX quantization, real vision-language alignment.

---

## Risk Register

| Risk | Status |
|------|--------|
| HF cold-start | Warm up before demo |
| Classroom network | Local `serve` fallback ready |
| Cross-origin | Resolved (CORS + `mode: 'cors'`) |
| Model size | ~1GB fits in HF 16GB instance |

---

*ResCat achieved state-of-the-art performance on assignment 4. It is a cat.*