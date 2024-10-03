from tokenizers.implementations import ByteLevelBPETokenizer

from transformers import GPT2Config, GPT2LMHeadModel, GPT2Tokenizer
from colorama import Fore, init

init(autoreset=True)

paths = ["python_code_text.txt"]

inp = 'print("Hello World!                 ")'

tokenizer = GPT2Tokenizer.from_pretrained('tokenizerr')

tokenizer.add_special_tokens({
    "eos_token" : "</s>",
    "pad_token" : "<pad>",
    "bos_token" : "<s>",
    "unk_token" : "<unk>",
    "mask_token" : "<mask>",
})

t = tokenizer.encode(inp)

print(t)

print(tokenizer.decode(t, clean_up_tokenization_spaces=False))

print(f"EOS token ID: {tokenizer.eos_token_id}")
print(f"BOS token ID: {tokenizer.bos_token_id}")
print(f"UNK token ID: {tokenizer.unk_token_id}")
print(f"PAD token ID: {tokenizer.pad_token_id}")

# Encode the input
input_ids = tokenizer.encode(inp, return_tensors="pt")
attention_mask = (input_ids != tokenizer.pad_token_id).long()


model = GPT2LMHeadModel.from_pretrained("GPyTT")

while True:
    inp = input(">>> ")
    input_ids = tokenizer.encode(inp, return_tensors = "pt")
    attention_mask = (input_ids != tokenizer.pad_token_id).long()
    
    beam_output = model.generate(
        input_ids, 
        attention_mask=attention_mask,
        max_length = 512, 
        num_beams = 10, 
        temperature = 0.7,
        do_sample=True,
        no_repeat_ngram_size = 5,
        num_return_sequences = 1
        )
    for beam in beam_output:
        out = tokenizer.decode(beam, skip_special_tokens = True)
        fout = out.replace("<N>", "\n")
        print(Fore.GREEN + str(fout))
    
