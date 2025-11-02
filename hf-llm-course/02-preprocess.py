import torch
from transformers import AutoTokenizer, AutoModel, AutoModelForSequenceClassification

checkpoint = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
"""
DistilBertTokenizerFast(name_or_path='distilbert-base-uncased-finetuned-sst-2-english', vocab_size=30522, model_max_length=512, is_fast=True, padding_side='right', truncation_side='right', special_tokens={'unk_token': '[UNK]', 'sep_token': '[SEP]', 'pad_token': '[PAD]', 'cls_token': '[CLS]', 'mask_token': '[MASK]'}, clean_up_tokenization_spaces=True, added_tokens_decoder={
        0: AddedToken("[PAD]", rstrip=False, lstrip=False, single_word=False, normalized=False, special=True),
        100: AddedToken("[UNK]", rstrip=False, lstrip=False, single_word=False, normalized=False, special=True),
        101: AddedToken("[CLS]", rstrip=False, lstrip=False, single_word=False, normalized=False, special=True),
        102: AddedToken("[SEP]", rstrip=False, lstrip=False, single_word=False, normalized=False, special=True),
        103: AddedToken("[MASK]", rstrip=False, lstrip=False, single_word=False, normalized=False, special=True),
}
)
"""

raw_inputs = [
    "I've been waiting for a HuggingFace course my whole life.",
    "I hate this so much!",
]
inputs = tokenizer(raw_inputs, padding=True, truncation=True, return_tensors="pt")
"""
{
    'input_ids': tensor([
        [  101,  1045,  1005,  2310,  2042,  3403,  2005,  1037, 17662, 12172, 2607,  2026,  2878,  2166,  1012,   102],
        [  101,  1045,  5223,  2023,  2061,  2172,   999,   102,     0,     0,   0,     0,     0,     0,     0,     0]]),
    'attention_mask': tensor([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]]
    )
    # 'token_type_ids': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
}
"""

model = AutoModel.from_pretrained(checkpoint)
outputs = model(**inputs)
# print(outputs.last_hidden_state.shape)
"""
torch.Size([
    2,      # Batch size
    16,     # Sequence length
    768     # Hidden size (vector size)
])
"""

# A model head
model = AutoModelForSequenceClassification.from_pretrained(checkpoint)
outputs = model(**inputs)
# print(outputs.logits.shape)
"""
torch.Size([
    2,      # Batch size
    2       # Number of labels
])
"""
# print(outputs.logits)
"""
tensor([
    [-0.0802,  0.0782],     # logits for the first sequence
    [-0.0802,  0.0782]],      #  logits for the second sequence
    grad_fn=<AddmmBackward>)
"""

predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
# print(predictions)
"""
tensor([
    [4.0195e-02, 9.5980e-01],       # ~> [0.04, 0.96]
    [9.9946e-01, 5.4418e-04]],      # ~> [0.99, 0.01]
    grad_fn=<SoftmaxBackward>)
"""

# print(model.config.id2label)
"""
{
    '0': 'NEGATIVE',
    '1': 'POSITIVE'
}
"""

encoded_input = tokenizer(
    ["How are you?", "I'm fine, thank you!"], padding=True, return_tensors="pt"
)
"""
{'input_ids': tensor([[  101,  1731,  1132,  1128,   136,   102,     0,     0,     0,     0],
         [  101,  1045,  1005,  1049,  2503,   117,  5763,  1128,   136,   102]]), 
 'token_type_ids': tensor([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]), 
 'attention_mask': tensor([[1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])}
"""

print(model(**encoded_input))

sequence = "I've been waiting for a HuggingFace course my whole life."
tokens = tokenizer.tokenize(sequence)
print(tokens)

ids = tokenizer.convert_tokens_to_ids(tokens)
print(ids)

print("ids:", ids)
print("first sequence:", inputs["input_ids"][0].tolist())
print(ids == inputs["input_ids"][0].tolist())

decoded_string = tokenizer.decode(ids)
print(decoded_string)