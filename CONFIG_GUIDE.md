# Centralized Configuration Guide

## Overview

All example scripts in this repository use a **centralized configuration system**. This means you can change the LLM model and API key setup in one place, and all scripts will automatically use the new settings.

## Configuration File

The main configuration file is located at:
```
/config.py  (at the root of the workspace)
```

## What Can You Configure?

### 1. **Model Selection**
```python
MODEL_NAME = "gemini-2.5-flash"
```
Change this to use a different model (e.g., "claude-sonnet-4-6", "gpt-4", etc.)

### 2. **Model Provider**
```python
MODEL_PROVIDER = "google_genai"
```
Supported providers:
- `"google_genai"` - Google Gemini
- `"anthropic"` - Claude
- `"openai"` - OpenAI
- `"cohere"` - Cohere
- etc.

### 3. **Model Parameters**
```python
MODEL_CONFIG = {
    "temperature": 0.7,
    "max_tokens": 500,
}
```
Common parameters:
- `temperature`: Controls randomness (0.0 = deterministic, 1.0 = very random)
- `max_tokens`: Maximum response length
- `top_p`: Nucleus sampling parameter
- Other model-specific parameters

### 4. **API Key**
```python
API_KEY = os.getenv("GOOGLE_API_KEY")
```
The API key is loaded from your `.env` file. No need to hardcode it!

## How Scripts Use This Configuration

Every example script automatically imports these settings:
```python
from config import MODEL_NAME, MODEL_PROVIDER, MODEL_CONFIG
```

Then uses them when initializing the model:
```python
model = init_chat_model(
    MODEL_NAME,
    model_provider=MODEL_PROVIDER,
    **MODEL_CONFIG  # Unpacks temperature, max_tokens, etc.
)
```

## Changing the Model Globally

To switch all examples to use a different model:

### Example 1: Switch to Claude
```python
# config.py
MODEL_NAME = "claude-sonnet-4-6"
MODEL_PROVIDER = "anthropic"

# Make sure your .env has
# ANTHROPIC_API_KEY=sk-ant-...
```

### Example 2: Adjust Temperature for All Scripts
```python
# config.py
MODEL_CONFIG = {
    "temperature": 0.3,  # More deterministic
    "max_tokens": 500,
}
```

### Example 3: Switch to GPT-4
```python
# config.py
MODEL_NAME = "gpt-4"
MODEL_PROVIDER = "openai"

# Make sure your .env has
# OPENAI_API_KEY=sk-proj-...
```

## Environment Variables

The configuration system requires an API key in your `.env` file:

```bash
# For Gemini (current default)
GOOGLE_API_KEY=AIzaSy...

# For Claude
ANTHROPIC_API_KEY=sk-ant-...

# For OpenAI
OPENAI_API_KEY=sk-proj-...
```

## No Manual Changes Needed

When you update `config.py`, **all scripts automatically use the new configuration** without any manual edits needed. Just run the scripts as usual!

## Example Workflow

1. Edit `config.py` to change the model
2. Run any example script (e.g., `python 01-foundations/01-basic-agent/main.py`)
3. The script automatically loads the new configuration
4. That's it! No other changes needed.

## Verification

You'll see this message when running a script:
```
✓ Configuration loaded: gemini-2.5-flash via google_genai
```

This confirms which model and provider are being used for that run.
