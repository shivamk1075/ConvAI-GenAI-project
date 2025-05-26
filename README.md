# ConvAI: Sales Persona AI Trainer

This project is an experiment in building an AI-powered sales trainer that simulates customer profiles (like a relative or shopkeeper) for practice conversations.

## What I Tried

- **API-based LLMs:**  
  I experimented with Perplexity and other cloud APIs for more realistic, instruction-following chatbots.  
  (API keys and cloud use, but better results.)

- **Local LLMs:**  
  I ran GPT-2 and tried other open-source models locally for privacy and offline use.  
  (Safe, but responses are generic and not very human-like.)

- **Prompt Engineering:**  
  I used detailed system prompts and conversation history to “steer” the model toward acting like a real customer or relative.  
  (Helps a bit, but small models still drift off-topic.)

- **Persona Templates & JSON:**  
  I explored storing persona templates and user conversations in JSON for easy customization and future fine-tuning.

## What I Learned

- **General LLMs (like GPT-2) are not enough** for realistic customer simulation out-of-the-box.
- **Prompt engineering helps,** but only a little with small models.
- **Cloud APIs (OpenAI, Perplexity, etc.)** give much better results, but require sending data to the cloud.
- **Fine-tuning and RAG** (Retrieval-Augmented Generation) are likely needed for truly realistic, role-based conversations.

## What’s Next

I plan to learn more about:
- Fine-tuning LLMs on custom data
- Using frameworks like LangChain and RAG for better context and memory
- I have already tried running more advanced local models (like Phi-3, Mistral, and Llama) locally, but found them unsatisfactory for realistic, persona-driven conversations.
- Future improvements will focus on fine-tuning, RAG, or other advanced GenAI techniques as my skills improve.

## Status

**This is a work in progress and a learning project.**  
If you’re interested in GenAI, LLMs, or building your own AI trainers, feel free to fork or contribute!
