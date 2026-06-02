# ResCat Development Log & Plan

**Project**: ResidualCat (rescat)  
**Current Date**: June 3, 2026  
**Presentation Deadline**: June 12, 2026 (9 days left)  
**Documentation Deadline**: June 26, 2026  
**Repository**: https://github.com/resnet18/ResidualCat

---

## Status Overview

| Component | Status | Notes |
|-----------|--------|-------|
| Astro Frontend | Skeleton Ready | `npm install` passed, dev server runs on `:4321` |
| FastAPI Backend | Day 1 Complete | Pure-text distilgpt2 baseline verified on CUDA |
| ResNet18 Integration | Not Started | Planned for Day 2 |
| Projector Layer | Not Started | Planned for Day 2 |
| Multimodal Fusion | Not Started | Planned for Day 3 |
| Pixel Art Assets | Not Started | Waiting for collaborator (5 states: idle/process/skip/vanish/converge) |
| Streamlit UI (Dev) | Not Started | Will migrate to Astro `assignment4.astro` later |
| Render Deployment | Not Started | Planned for Day 4-5 |
| Dev Log / Report | Not Started | Planned for Day 8-9 |

---

## 9-Day Execution Plan (June 3 → June 12)

### Day 1 (June 2) ✅ COMPLETE
- [x] Initialize project directory structure
- [x] Set up Astro frontend skeleton (`npm install` success)
- [x] Verify backend pure-text generation with distilgpt2 on CUDA
- [x] Push clean repository to GitHub (no large files)

### Day 2 (June 3) — ResNet Integration
- [ ] Load pretrained ResNet18, strip FC layer (output 512d)
- [ ] Implement `Linear(512 → 768)` projector
- [ ] Verify tensor shapes: image → ResNet → projector → [1, 1, 768]
- [ ] Log: document dimension alignment issues and fixes

### Day 3 (June 4) — Multimodal Fusion
- [ ] Concatenate visual token + text embeddings along sequence dim
- [ ] Feed fused sequence into distilgpt2.generate(inputs_embeds=...)
- [ ] Test with dummy image (white tensor) vs. real image
- [ ] Implement error fallback: if image fails, zero-out visual residual
- [ ] Log: record CoT hallucination handling during fusion

### Day 4 (June 5) — FastAPI API & CORS
- [ ] Wrap intergrated model in FastAPI with `/rescat` POST endpoint
- [ ] Accept `text` (form) + `image` (optional upload)
- [ ] Return JSON: `{reply: str, state: str}`
- [ ] Add CORS middleware for Astro frontend
- [ ] Local end-to-end test: frontend fetch → backend → response

### Day 5 (June 6) — Render Deployment & State Machine
- [ ] Deploy backend to Render (free tier)
- [ ] Implement 5-state heuristic classifier in backend
- [ ] Map keywords to states: idle/process/skip/vanish/converge
- [ ] Verify API health from external network
- [ ] Log: document deployment issues and proxy/config workarounds

### Day 6 (June 7) — Pixel Art Integration & UI Polish
- [ ] Receive pixel art assets from collaborator (idle, process, skip, vanish, converge)
- [ ] Place assets in `frontend/public/`
- [ ] Implement state-driven image switching in Astro page
- [ ] Add pixel-art CSS (Courier New, sharp borders, retro palette)
- [ ] Add loading spinner or "process" state transition

### Day 7 (June 8) — Demo Hardening
- [ ] Prepare 3 guaranteed demo inputs (text + optional image)
- [ ] Test full pipeline: Astro → FastAPI → ResNet → GPT2 → State → Pixel swap
- [ ] Add error boundaries (backend down → vanish state + fallback message)
- [ ] Verify cross-browser rendering (Chrome/Edge)
- [ ] Record short demo GIF or video

### Day 8 (June 9) — Documentation & Report
- [ ] Write `docs/dev_log.md`: AI-assisted development narrative
- [ ] Document: architecture, problem-solving, hallucination handling
- [ ] Include screenshots: terminal outputs, API responses, UI states
- [ ] Draft report sections: Background, Tech Stack, Development Log, Results

### Day 9 (June 10) — Buffer / Integration
- [ ] Merge frontend into personal website as `assignment4.astro`
- [ ] Verify static asset paths (`/rescat/rescat_idle.png` etc.)
- [ ] Final spell-check and formatting
- [ ] Optional: add bonus features (cross-platform badge, extra animation)

### Day 10 (June 11) — Rehearsal
- [ ] Dry-run presentation (5 min)
- [ ] Prepare talking points: "lightweight multimodal verification"
- [ ] Prepare fallback: if live demo fails, show recorded video
- [ ] Push final code, tag release `v0.1-demo`

### Day 11-12 (June 12) — Presentation Day
- [ ] Deliver presentation
- [ ] Submit documentation (if required same day)

---

## Risk Register

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Render cold-start >10s | High | Show recorded video as fallback; mention free-tier limitation |
| Pixel art delayed | Medium | Use ASCII placeholder art or CSS-drawn cat |
| ResNet-GPT2 fusion shape mismatch | Medium | Log dimension mismatch; use `print()` debugging; ask AI for fix |
| GitHub large-file rejection | Low (mitigated) | `.gitignore` already excludes `venv/` and `node_modules/` |
| Cross-origin blocked | Medium | CORS middleware already planned; test with `curl -H Origin` |

---

## Key Decisions Log

- **June 2**: Switched from SOTA Guide to ResCat as final project. Rationale: SOTA Guide no longer aligns with current skill level; ResCat offers higher technical depth and multimodal novelty.
- **June 2**: Chose Astro + FastAPI split architecture over pure Streamlit. Rationale: Astro integrates into existing personal website; FastAPI allows independent backend deployment on Render.
- **June 2**: Selected `distilgpt2` (82M params) as language model. Rationale: CPU/GPU hybrid friendly, fast download, sufficient for 20-token generation.
- **June 3**: Re-initialized Git repository after large-file rejection. Rationale: `venv/` contained 293MB `torch_cpu.dll`; `.gitignore` + history purge was insufficient; clean slate was faster.

---

## Next Immediate Action

**Day 2 (June 3)**: Implement `ResCatCore` class with ResNet18 + Projector in `backend/main.py`. Verify that a 224×224 image tensor flows through ResNet → projector → 768-dim visual token without shape errors.
