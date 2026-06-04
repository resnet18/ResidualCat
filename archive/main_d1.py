# backend/main.py
# Day 1: Pure text generation verification with distilgpt2

from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch


def test_pure_text():
    print("[ResCat] Initializing text-only baseline...")
    
    tokenizer = GPT2Tokenizer.from_pretrained("distilgpt2")
    model = GPT2LMHeadModel.from_pretrained("distilgpt2")
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    
    print(f"[ResCat] Model loaded on: {device}")
    
    prompt = "ResCat is a"
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=20,
            temperature=0.3,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"[ResCat] Input:  '{prompt}'")
    print(f"[ResCat] Output: '{result}'")
    print("[ResCat] Day 1 baseline passed.")


if __name__ == "__main__":
    test_pure_text()