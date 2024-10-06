from transformers import GPT2LMHeadModel, GPT2Tokenizer
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

tokenizer = GPT2Tokenizer.from_pretrained('WeakTokenizer')

tokenizer.add_special_tokens({
    "eos_token" : "</s>",
    "pad_token" : "<pad>",
    "bos_token" : "<s>",
    "unk_token" : "<unk>",
    "mask_token" : "<mask>",
})

model = GPT2LMHeadModel.from_pretrained("WeakModel")

NEWLINECHAR = "<N>"

def encode_newlanes(inp):
    return inp.replace("\n", NEWLINECHAR)

def decode_newlanes(inp):
    return inp.replace(NEWLINECHAR, "\n")

def stop_at_repeat(model_out):
    lines = model_out.splitlines(True)
    no_repeat = ""
    for line in lines:
        if no_repeat.count(line) == 0 or line == "\n":
            no_repeat += line
        else:
            return no_repeat
    return no_repeat
    
def auto_complete_line(inp):
    inp = encode_newlanes(inp)
    
    newline_count = inp.count(NEWLINECHAR)
    
    input_ids = tokenizer.encode(inp, return_tensors = "pt")
    attention_mask = (input_ids != tokenizer.pad_token_id).long()

    model_out = model.generate(
        input_ids, 
        attention_mask=attention_mask,
        max_length = 100, 
        num_beams = 5, 
        temperature = 0.7,
        do_sample=True,
        no_repeat_ngram_size = 5,
        num_return_sequences = 3,
        return_dict_in_generate = True,
        output_scores = True
        )
    
    sequence = model_out["sequences"][0] # type: ignore
    decoded =decode_newlanes(tokenizer.decode(sequence, skip_special_tokens=True))

    split = decoded.split('\n')
    
    auto_complete = ""
    
    for s in split[:newline_count + 1]:
        auto_complete += s + "\n"
        
    return auto_complete

def generate_next_line(inp):
    
    inp = encode_newlanes(inp)
    
    newline_count = inp.count(NEWLINECHAR)
    
    input_ids = tokenizer.encode(inp, return_tensors = "pt")
    attention_mask = (input_ids != tokenizer.pad_token_id).long()

    model_out = model.generate(
        input_ids, 
        attention_mask=attention_mask,
        max_length = 100, 
        num_beams = 5, 
        temperature = 0.7,
        do_sample=True,
        no_repeat_ngram_size = 5,
        num_return_sequences = 3,
        return_dict_in_generate = True,
        output_scores = True
        )
    
    sequence = model_out["sequences"][0] # type: ignore
    decoded =decode_newlanes(tokenizer.decode(sequence, skip_special_tokens=True))

    split = decoded.split('\n')
    
    generated_code = ""
    
    for s in split[:newline_count + 2]:
        generated_code += s + "\n"
        
    last_newline_index = generated_code.rfind("\n")
    
    return generated_code[:last_newline_index]

def genereate_block_of_code(inp):
    
    inp = encode_newlanes(inp)
    
    input_ids = tokenizer.encode(inp, return_tensors = "pt")
    attention_mask = (input_ids != tokenizer.pad_token_id).long()

    model_out = model.generate(
        input_ids, 
        attention_mask=attention_mask,
        max_length = 100, 
        num_beams = 5, 
        temperature = 0.7,
        do_sample=True,
        no_repeat_ngram_size = 5,
        num_return_sequences = 3,
        return_dict_in_generate = True,
        output_scores = True
        )
    
    sequence = model_out["sequences"][0] # type: ignore
    decoded =decode_newlanes(tokenizer.decode(sequence, skip_special_tokens=True))
    
    generated_code =  stop_at_repeat(decoded)
    
    last_newline_index = generated_code.rfind("\n")
    
    return generated_code[:last_newline_index]

@app.route("/generate", methods=["POST"])
def generate_code():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Invalid or missing JSON"}), 400
    
    input_code = data.get("input_code", "")
    
    if not input_code:
        print("No input code received")
        return jsonify({"error": "Input code is required"}), 400
    
    generated_code = genereate_block_of_code(input_code)
    
    return jsonify({"generated_code": generated_code})

@app.route("/autocompleateline", methods=["POST"])
def autocomplete_line():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Invalid or missing JSON"}), 400
    
    input_code = data.get("input_code", "")
    
    if not input_code:
        print("No input code received")
        return jsonify({"error": "Input code is required"}), 400
    
    generated_code = auto_complete_line(input_code)
    
    return jsonify({"generated_code": generated_code})

@app.route("/generatenextline", methods=["POST"])
def next_line():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Invalid or missing JSON"}), 400
    
    input_code = data.get("input_code", "")
    
    if not input_code:
        print("No input code received")
        return jsonify({"error": "Input code is required"}), 400
    
    generated_code = generate_next_line(input_code)
    
    return jsonify({"generated_code": generated_code})

if __name__ == "__main__":
    app.run(debug=True, port=5001)