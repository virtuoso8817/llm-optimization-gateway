import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_PROVIDER = os.getenv("DEFAULT_PROVIDER", "ollama")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")