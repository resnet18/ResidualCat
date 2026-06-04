import json
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model, TaskType

with open("cat_data.json", encoding="utf-8") as f:
    data = json.load(f)
texts = [f"You are ResCat, a residual cat. Answer in short cat-like sentences.\nUser: {d['instruction']}\nResCat: {d['output']}" for d in data]

tokenizer = GPT2Tokenizer.from_pretrained("distilgpt2")
tokenizer.pad_token = tokenizer.eos_token

model = GPT2LMHeadModel.from_pretrained("distilgpt2")

lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=8,
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
    target_modules=["c_attn", "c_proj"]
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

class CatDataset(torch.utils.data.Dataset):
    def __init__(self, texts, tokenizer, max_length=128):
        self.encodings = tokenizer(texts, truncation=True, padding=True, max_length=max_length, return_tensors="pt")
    def __len__(self):
        return len(self.encodings["input_ids"])
    def __getitem__(self, idx):
        return {key: val[idx] for key, val in self.encodings.items()}

dataset = CatDataset(texts, tokenizer)

training_args = TrainingArguments(
    output_dir="./rescat_lora_adapter",
    num_train_epochs=10,
    per_device_train_batch_size=2,
    learning_rate=5e-4,
    weight_decay=0.01,
    logging_steps=1,
    save_strategy="no",
    report_to="none",
)

def collate_fn(x):
    return {
        "input_ids": torch.stack([i["input_ids"] for i in x]),
        "attention_mask": torch.stack([i["attention_mask"] for i in x]),
        "labels": torch.stack([i["input_ids"] for i in x])
    }

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    data_collator=collate_fn,
)

trainer.train()
model.save_pretrained("./rescat_lora_adapter")
print("[ResCat] LoRA adapter saved.")