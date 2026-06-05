# backend/main.py
# Day 3: FastAPI wrapper + multimodal endpoint with LoRA personality

import io
from typing import Optional
from peft import PeftModel
import os

import torch
import torch.nn as nn
from PIL import Image
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from torchvision import models, transforms
from transformers import GPT2LMHeadModel, GPT2Tokenizer

app = FastAPI(title="ResCat API", version="0.1.0")

# CORS: allow Astro frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ResCatCore(nn.Module):
    def __init__(self):
        super().__init__()
        # Vision encoder: frozen ResNet18, output 512d
        self.resnet = models.resnet18(weights='DEFAULT')
        self.resnet.fc = nn.Identity()
        self.resnet.eval()
        for param in self.resnet.parameters():
            param.requires_grad = False

        # Projector: 512 -> 768
        self.projector = nn.Linear(512, 768)

        # Language decoder: distilgpt2 + optional LoRA adapter
        self.gpt2 = GPT2LMHeadModel.from_pretrained("distilgpt2")
        adapter_path = "./rescat_lora_adapter"
        if os.path.exists(adapter_path):
            self.gpt2 = PeftModel.from_pretrained(self.gpt2, adapter_path)
            print("[ResCat] LoRA adapter loaded. Residual personality injected.")
        else:
            print("[ResCat] No adapter found. Running base identity mapping.")

        self.tokenizer = GPT2Tokenizer.from_pretrained("distilgpt2")
        self.tokenizer.pad_token = self.tokenizer.eos_token

        # Image preprocessing
        self.transform = transforms.Compose([
            transforms.Resize(224),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def forward(self, text: str, image: Optional[Image.Image] = None):
        device = next(self.parameters()).device

        # Vision path: extract residual visual features from input image
        if image is not None:
            img_tensor = self.transform(image).unsqueeze(0).to(device)
            with torch.no_grad():
                visual_feat = self.resnet(img_tensor)
            visual_token = self.projector(visual_feat).unsqueeze(1)
        else:
            # No image provided: zero residual (pure identity mapping)
            visual_token = torch.zeros(1, 1, 768, device=device)

        # Construct prompt with system identity and few-shot example
        system_prompt = (
            "You are ResCat, a residual cat. "
            "You speak in cat-like, slightly confused sentences. "
            "Sometimes you say 'meow' at the beginning or the end of a sentence, randomly. "
            "You know about skip connections and gradient descent."
        )

        prompt = (
            f"{system_prompt}\n\n"
            f"Example:\nUser: Hello\nResCat: Meow?\n\n"
            f"User: {text}\nResCat:"
        )

        text_tokens = self.tokenizer(prompt, return_tensors="pt").to(device)
        text_embeds = self.gpt2.transformer.wte(text_tokens.input_ids)

        # Concatenate visual residual token with text embeddings along sequence dimension
        inputs_embeds = torch.cat([visual_token, text_embeds], dim=1)

        with torch.no_grad():
            outputs = self.gpt2.generate(
                inputs_embeds=inputs_embeds,
                max_new_tokens=30,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                repetition_penalty=1.2,
                early_stopping=True,
            )

        # Decode and strip the prompt prefix, keeping only the cat's response
        full_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        # robustness design: default output as fallback
        parts = full_text.split("ResCat:")
        if len(parts) > 1:
           reply = parts[-1].strip()
        else:
           reply = full_text.strip() or "Meow?"
        return reply


def extract_state(text: str) -> str:
    """
    Map ResCat's natural vocabulary to emotional states.
    The cat speaks in its own language; we listen and label.
    """
    t = text.lower()

    # Vanish: negation, self-deprecation, or confusion
    if any(w in t for w in ["no", "not", "quitter", "vanish", "error", "fail", "unknown", "crash"]):
        return "vanish"

    # Skip: identity words that imply a shortcut / residual connection
    elif any(w in t for w in ["residual", "skip", "shortcut", "jump", "fly", "connection"]):
        return "skip"

    # Converge: cat noises, affirmation, or stability signals
    elif any(w in t for w in ["meow", "converge", "done", "success", "purr", "purring"]):
        return "converge"

    # Default: neutral observation
    else:
        return "idle"


# Global model instance (loaded at startup)
print("[ResCat] Loading ResCatCore...")
brain = ResCatCore()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
brain = brain.to(device)
brain.eval()
print(f"[ResCat] Core ready on {device}")


@app.post("/rescat")
async def rescat(
    text: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None)
):
    pil_image = None
    if image:
        contents = await image.read()
        pil_image = Image.open(io.BytesIO(contents)).convert("RGB")
    if not text or text.strip() == "":
        text = "What do you see?"

    reply = brain.forward(text, pil_image)
    state = extract_state(reply)

    return {"reply": reply, "state": state}


@app.get("/")
def health():
    return {"status": "ResCat API alive", "device": str(device), "version": "0.1.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)