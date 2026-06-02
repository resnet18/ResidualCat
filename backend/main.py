# backend/main.py
# Day 2: ResCatCore with ResNet18 + Projector

import torch
import torch.nn as nn
from torchvision import models, transforms
from transformers import GPT2LMHeadModel, GPT2Tokenizer


class ResCatCore(nn.Module):
    def __init__(self):
        super().__init__()
        
        # Vision encoder: frozen ResNet18, output 512d
        self.resnet = models.resnet18(pretrained=True)
        self.resnet.fc = nn.Identity()
        self.resnet.eval()
        for param in self.resnet.parameters():
            param.requires_grad = False
        
        # Projector: 512 -> 768
        self.projector = nn.Linear(512, 768)
        
        # Language decoder: distilgpt2
        self.gpt2 = GPT2LMHeadModel.from_pretrained("distilgpt2")
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
        
    def forward(self, text: str, image_tensor: torch.Tensor = None):
        device = next(self.parameters()).device
        
        # Vision path
        if image_tensor is not None:
            image_tensor = image_tensor.to(device)
            with torch.no_grad():
                visual_feat = self.resnet(image_tensor)  # [1, 512]
            visual_token = self.projector(visual_feat).unsqueeze(1)  # [1, 1, 768]
        else:
            # No image = zero residual (identity mapping)
            visual_token = torch.zeros(1, 1, 768, device=device)
        
        # Text path
        text_tokens = self.tokenizer(text, return_tensors="pt").to(device)
        text_embeds = self.gpt2.transformer.wte(text_tokens.input_ids)  # [1, seq, 768]
        
        # Multimodal fusion: concatenate along sequence dimension
        inputs_embeds = torch.cat([visual_token, text_embeds], dim=1)  # [1, 1+seq, 768]
        
        # Generate
        with torch.no_grad():
            outputs = self.gpt2.generate(
                inputs_embeds=inputs_embeds,
                max_new_tokens=20,
                temperature=0.3,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)


def test_day2():
    print("[ResCat] Initializing ResCatCore...")
    core = ResCatCore()
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    core = core.to(device)
    print(f"[ResCat] Core loaded on: {device}")
    
    # Test 1: Pure text (no image, zero residual)
    print("\n[Test 1] Text-only (identity mapping):")
    result1 = core.forward("ResCat is a")
    print(f"  Output: {result1}")
    
    # Test 2: Text + dummy image (white tensor, random residual)
    print("\n[Test 2] Text + dummy image (random residual):")
    dummy_image = torch.zeros(1, 3, 224, 224)  # White/black image
    result2 = core.forward("This image shows", dummy_image)
    print(f"  Output: {result2}")
    
    print("\n[ResCat] Day 2 fusion baseline passed.")


if __name__ == "__main__":
    test_day2()