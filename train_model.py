from tokenizers.implementations import ByteLevelBPETokenizer
from transformers import GPT2Config, GPT2LMHeadModel, GPT2Tokenizer, DataCollatorForLanguageModeling,Trainer, TrainingArguments
from datasets import load_dataset


paths = ["python_code_text.txt"]

tokenizer = GPT2Tokenizer.from_pretrained('WeakTokenizer')

tokenizer.add_special_tokens({
    "eos_token" : "</s>",
    "bos_token" : "<s>",
    "unk_token" : "<unk>",
    "pad_token" : "<pad>",
    "mask_token" : "<mask>",
})

config = GPT2Config(
    vocab_size = tokenizer.vocab_size,
    bos_token_id = tokenizer.bos_token_id,
    eos_token_id = tokenizer.eos_token_id,
    pad_token_id = tokenizer.pad_token_id,
    unk_token_id = tokenizer.unk_token_id,
    mask_token_id = tokenizer.mask_token_id,
    )

model = GPT2LMHeadModel(config)

dataset = load_dataset("text", data_files={"train": paths[0]})
print(dataset)

def encode(lines):
    return tokenizer(lines["text"], add_special_tokens=True, truncation=True, max_length=512)

dataset = dataset.map(encode, batched=True, remove_columns=["text"])
print(dataset)

data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

training_args = TrainingArguments(
    output_dir = "./WeakModel",
    overwrite_output_dir=True,
    num_train_epochs=1,
    per_device_eval_batch_size=2,
    save_steps=100,
    save_total_limit=2,
    prediction_loss_only=True,
    remove_unused_columns=False
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=dataset["train"] # type: ignore
)

trainer.train()
trainer.save_model("./WeakModel")

