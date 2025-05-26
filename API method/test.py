import transformers

MODEL_NAME = 'gpt2'
pipe = transformers.pipeline(task='text-generation', model=MODEL_NAME, device='cpu')

print("GPT-2 Terminal Interface")
print("Type 'exit' to quit")

while True:
    prompt = input("\nEnter prompt: ")
    if prompt.lower() == 'exit':
        break
    
    result = pipe(prompt, max_length=1000, num_return_sequences=1)
    print(f"Generated: {result[0]['generated_text']}")
