"""
Centralized configuration for all LangChain examples.

This module manages:
- Model selection and provider
- API key validation
- Environment variable loading

All example scripts should import from this module instead of 
hardcoding model names or API keys.
"""

import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# LLM Configuration
# ============================================================================

# Model to use for all examples
MODEL_NAME = "gemini-2.5-flash"

# Provider for the model
MODEL_PROVIDER = "google_genai"

# Model parameters
MODEL_CONFIG = {
    "temperature": 0.7,
    "max_tokens": 500,
}

# ============================================================================
# API Key Validation
# ============================================================================

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise EnvironmentError(
        "GOOGLE_API_KEY is not set. "
        "Please add it to your .env file or set it as an environment variable."
    )

print(f"✓ Configuration loaded: {MODEL_NAME} via {MODEL_PROVIDER}")
