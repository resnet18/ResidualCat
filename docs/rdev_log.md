# ResCat Development Log & Plan

**Project**: ResidualCat (rescat)  
**Current Date**: June 5, 2026  
**Presentation Deadline**: June 12, 2026 (7 days left)  
**Documentation Deadline**: June 26, 2026  
**Repository**: https://github.com/resnet18/ResidualCat

---

## Status Overview

| Component | Status | Notes |
|-----------|--------|-------|
| Astro Frontend | Skeleton Ready | `npm install` passed, dev server runs on `:4321` |
| FastAPI Backend | Day 3 Complete | LoRA personality + ICL + system prompt active |
| ResNet18 Integration | ✅ Complete | Frozen, output 512d, verified on CPU/GPU |
| Projector Layer | ✅ Complete | Linear(512→768), tensor shape verified |
| Multimodal Fusion | ✅ Complete | Visual token + text embeddings concatenation |
| LoRA Personality | ✅ Complete | r=8, 10 epochs, loss 6.5→1.0, 20 cat dialogues |
| FastAPI API & CORS | ✅ Complete | `/rescat` endpoint returns `{reply, state}` |
| Pixel Art Assets | Not Started | Waiting for collaborator (5 states) |
| Render Deployment | Not Started | Planned for Day 5 |
| Dev Log / Report | In Progress | This file |

---

## 9-Day Execution Plan (June 3 → June 12)

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

### Day 4 (June 5) — Render Deployment
- [ ] Deploy backend to Render (free tier)
- [ ] Verify API health from external network
- [ ] Log: document deployment issues and proxy/config workarounds

### Day 5 (June 6) — Pixel Art Integration & UI Polish
- [ ] Receive pixel art assets from collaborator (idle, process, skip, vanish, converge)
- [ ] Place assets in `frontend/public/`
- [ ] Implement state-driven image switching in Astro page
- [ ] Add pixel-art CSS (Courier New, sharp borders, retro palette)
- [ ] Add loading spinner or "process" state transition

### Day 6 (June 7) — Demo Hardening
- [ ] Prepare 3 guaranteed demo inputs (text + optional image)
- [ ] Test full pipeline: Astro → FastAPI → ResNet → GPT2 → State → Pixel swap
- [ ] Add error boundaries (backend down → vanish state + fallback message)
- [ ] Verify cross-browser rendering (Chrome/Edge)
- [ ] Record short demo GIF or video

### Day 7 (June 8) — Documentation & Report
- [ ] Write `docs/dev_log.md`: AI-assisted development narrative
- [ ] Document: architecture, problem-solving, hallucination handling
- [ ] Include screenshots: terminal outputs, API responses, UI states
- [ ] Draft report sections: Background, Tech Stack, Development Log, Results

### Day 8 (June 9) — Buffer / Integration
- [ ] Merge frontend into personal website as `assignment4.astro`
- [ ] Verify static asset paths (`/rescat/rescat_idle.png` etc.)
- [ ] Final spell-check and formatting
- [ ] Optional: add bonus features (cross-platform badge, extra animation)

### Day 9 (June 10) — Rehearsal
- [ ] Dry-run presentation (5 min)
- [ ] Prepare talking points: "lightweight multimodal verification"
- [ ] Prepare fallback: if live demo fails, show recorded video
- [ ] Push final code, tag release `v0.1-demo`

### Day 10 (June 11) — Buffer
- [ ] Final polish, sleep, prepare mentally

### Day 11-12 (June 12) — Presentation Day
- [ ] Deliver presentation
- [ ] Submit documentation (if required same day)

---

## Key Technical Decisions

### LoRA vs. System Prompt
**Decision**: Use LoRA (r=8) + ICL + System Prompt triple insurance.  
**Rationale**: Pure system prompt produced generic outputs ("free-to-play game"). LoRA alone with r=2 was too weak. The combination of adapter weights and prompt engineering achieves stable cat personality.

### ICL Example Count
**Decision**: Use exactly 1 ICL example.  
**Rationale**: 2+ examples caused the model to overfit to the "I am a cat" template, producing identical replies regardless of input. 1 example provides just enough guidance without constraining diversity.

### Temperature Selection
**Decision**: temperature=0.7 for inference.  
**Rationale**: 0.1 produced deterministic repetition; 0.7 yields quantum superposition (varied but coherent); 1.0 caused hallucination.

### State Mapping
**Decision**: Bind states to ResCat's natural vocabulary rather than abstract concepts.  
**Mapping**: "meow" → converge, "residual" → skip, "no" → vanish.  
**Rationale**: The cat speaks in its own language; we listen and label.

---

## Risk Register

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Render cold-start >10s | High | Show recorded video as fallback; mention free-tier limitation |
| Pixel art delayed | Medium | Use ASCII placeholder art or CSS-drawn cat |
| ResNet-GPT2 fusion shape mismatch | Low (resolved) | Verified on Day 2; fallback to zero residual |
| GitHub large-file rejection | Low (mitigated) | `.gitignore` excludes `venv/` and `node_modules/` |
| Cross-origin blocked | Low (resolved) | CORS middleware active; tested with `Invoke-RestMethod` |
| LoRA personality unstable | Low (resolved) | Triple insurance: LoRA + ICL + system prompt |

---

## Next Immediate Action

**Day 4 (June 5)**: Deploy backend to Render. Verify external API access. Test with `curl` from outside local network.