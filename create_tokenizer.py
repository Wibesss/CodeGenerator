from tokenizers.implementations import ByteLevelBPETokenizer
from transformers import GPT2Tokenizer

TRAN_BASE = True

paths = ["python_code_text.txt"]

tokenizer = ByteLevelBPETokenizer()

tokenizer.train(files = paths, vocab_size=52_000, min_frequency = 2 ,special_tokens = [
    "<pad>",
    "<s>",
    "</s>",
    "<unk>",
    "<mask>",
])

tokenizer.save_model("tokenizer")


tokenizer = GPT2Tokenizer.from_pretrained('tokenizer')

tokenizer.add_special_tokens({
    "eos_token" : "</s>",
    "pad_token" : "<pad>",
    "bos_token" : "<s>",
    "unk_token" : "<unk>",
    "mask_token" : "<mask>",
})

inp = 'print("Hello World!")'

t = tokenizer.encode(inp)

print(t)

print(tokenizer.decode(t, clean_up_tokenization_spaces=False))


