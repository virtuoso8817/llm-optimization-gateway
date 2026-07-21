from services.llm_service import LLMService

service = LLMService()

result = service.chat(
    prompt="Explain Artificial Intelligence in exactly two sentences.",
    provider="groq"      # Change to "gemini", "groq", etc.
)

print("\n=== LLM Response ===")
print(result["response"])

print("\n=== Metrics ===")
print(f"Model: {result['model']}")
print(f"Latency: {result['latency_ms']} ms")
print(f"Prompt Tokens: {result['prompt_tokens']}")
print(f"Completion Tokens: {result['completion_tokens']}")
print(f"Total Tokens: {result['total_tokens']}")