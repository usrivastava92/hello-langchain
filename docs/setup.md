# Setup & Configuration Guide

Complete setup instructions for the hello-langchain repository.

## Prerequisites

- Python 3.10 or higher
- pip or poetry
- An LLM API key (Anthropic, OpenAI, Google, etc.)
- ✨ **Recommended:** [pyenv](https://github.com/pyenv/pyenv) for Python version management

---

## Step 1: Clone Repository

```bash
cd hello-langchain
```

---

## Step 2: Create Virtual Environment

### Recommended: Using pyenv + venv

```bash
# Install pyenv (if not already installed)
# macOS: brew install pyenv pyenv-virtualenv
# Ubuntu: git clone https://github.com/pyenv/pyenv.git ~/.pyenv

# Install Python 3.11
pyenv install 3.11.0

# The .python-version file in repo automatically sets local version
# Verify it's active
pyenv version  # Should show: 3.11.0 (set by /path/to/hello-langchain/.python-version)

# Create virtual environment
python -m venv venv

# Activate venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Option A: venv only (Python built-in)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Option B: conda

```bash
conda create -n langchain-expert python=3.11
conda activate langchain-expert
```

### Option C: Poetry

```bash
poetry install
poetry shell
```

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Or with Poetry:
```bash
poetry install
```

---

## Step 4: Set Up API Keys

### Get an API Key

Choose your LLM provider:

#### Anthropic (Claude) - Recommended
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up / Login
3. Click API Keys → Create Key
4. Copy the key

#### OpenAI
1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create new secret key
3. Copy the key

#### Google Gemini
1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Click Get API Key
3. Copy the key

### Set Environment Variable

#### MacOS/Linux

```bash
# Option 1: Terminal (temporary)
export ANTHROPIC_API_KEY="sk-ant-..."

# Option 2: Permanent (.bashrc or .zshrc)
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.zshrc
source ~/.zshrc
```

#### Windows

```bash
setx ANTHROPIC_API_KEY "sk-ant-..."
# Close and reopen terminal for changes to take effect
```

#### Create .env File (Recommended)

```bash
# In repository root, create .env file
cat > .env << EOF
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...  # Optional
GOOGLE_API_KEY=...     # Optional
LANGSMITH_API_KEY=...  # Optional
LANGSMITH_PROJECT=hello-langchain
EOF
```

⚠️ **Important**: Add `.env` to `.gitignore`

```bash
echo ".env" >> .gitignore
```

---

## Step 5: Verify Installation

```bash
# Test Python installation
python --version

# Test LangChain import
python -c "from langchain.agents import create_agent; print('✓ LangChain installed')"

# Test API key
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(f'API key: {os.getenv(\"ANTHROPIC_API_KEY\")[:20]}...')"
```

Expected output:
```
Python 3.11.x
✓ LangChain installed
API key: sk-ant-yyyyyy...
```

---

## Step 6: Run First Example

```bash
cd 01-foundations/01-basic-agent
python main.py
```

Expected output:
```
✓ Model initialized: Claude Sonnet 4.5
✓ Agent created

============================================================
LangChain Basic Agent Demo
============================================================

User: What's the weather in San Francisco?
------------------------------------------------------------
Agent: The weather in San Francisco is sunny! Perfect day to visit...
```

---

## Configuration Options

### Choose LLM Model

Edit code or set environment variable:

```python
# Use different models
model = init_chat_model(
    "claude-sonnet-4-6",      # Anthropic (default)
    # "gpt-4-turbo",          # OpenAI
    # "gemini-1.5-pro",       # Google
    temperature=0.7,
    max_tokens=1000
)
```

### Adjust Model Parameters

```python
model = init_chat_model(
    "claude-sonnet-4-6",
    temperature=0.7,        # Creativity (0-1)
    max_tokens=500,         # Max response length
    timeout=30,             # Timeout in seconds
)
```

| Parameter | Range | Meaning |
|-----------|-------|---------|
| temperature | 0-1 | 0=deterministic, 1=creative |
| max_tokens | 1-4096 | Maximum output length |
| timeout | positive | Seconds before timeout |

---

## Optional: LangSmith Setup

LangSmith provides debugging dashboard.

### Get LangSmith API Key

1. Go to [smith.langchain.com](https://smith.langchain.com)
2. Sign up (free tier available)
3. Settings → API Keys → Create Key
4. Copy key

### Set Up Environment

```bash
export LANGSMITH_API_KEY="your-key"
export LANGSMITH_PROJECT="hello-langchain"
```

Or add to `.env`:
```
LANGSMITH_API_KEY=lsv_...
LANGSMITH_PROJECT=hello-langchain
```

---

## Optional: Database for Production

For persistent memory in production, use PostgreSQL:

### Install PostgreSQL

**macOS:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Ubuntu:**
```bash
sudo apt-get install postgresql
```

### Create Database

```bash
psql
CREATE DATABASE langchain_db;
CREATE USER langchain_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE langchain_db TO langchain_user;
\q
```

### Use in Code

```python
from langgraph.checkpoint.postgres import PostgresSaver

checkpointer = PostgresSaver(
    connection_string="postgresql://langchain_user:password@localhost/langchain_db"
)

agent = create_agent(..., checkpointer=checkpointer)
```

---

## Project Structure

```
hello-langchain/
├── README.md                    # Overview
├── LEARNING_PATH.md             # Week-by-week guide
├── ECOSYSTEM_GUIDE.md           # Framework deep-dive
├── requirements.txt             # Python dependencies
├── .env                        # Environment variables (not committed)
├── .gitignore                  # Git ignore rules
│
├── docs/
│   ├── quick-reference.md      # Quick API reference
│   ├── troubleshooting.md      # Common issues
│   ├── setup.md                # This file
│   ├── api-reference.md        # Detailed API docs
│   └── resources.md            # Links and resources
│
├── 01-foundations/             # Phase 1: Core concepts
│   ├── 01-basic-agent/
│   ├── 02-tools-and-binding/
│   ├── 03-memory-state/
│   └── 04-structured-output/
│
├── 02-intermediate/            # Phase 2: LangGraph
│   ├── 01-state-graph-basics/
│   ├── 02-nodes-and-edges/
│   ├── 03-conditional-routing/
│   └── 04-agent-loop-patterns/
│
├── 03-advanced/                # Phase 3: Production
│   ├── 01-multi-agent-systems/
│   ├── 02-langsmith-integration/
│   ├── 03-evaluation-framework/
│   └── 04-performance-optimization/
│
└── 04-capstone/                # Phase 4: Real projects
    ├── 01-weather-agent/
    ├── 02-research-assistant/
    └── 03-reasoning-system/
```

---

## Directory Navigation

```bash
# While in hello-langchain/

# Go to first experiment
cd 01-foundations/01-basic-agent

# Run it
python main.py

# Go back
cd ../..

# Go to different experiment
cd 01-foundations/02-tools-and-binding
python main.py
```

---

## Development Workflow

### 1. Start Session

```bash
cd hello-langchain
source venv/bin/activate  # Activate venv
```

### 2. Edit Code

```bash
# Edit files in your IDE
# Recommended: VS Code + GitHub Copilot
```

### 3. Test Changes

```bash
# In your experiment directory
python main.py
```

### 4. Run Tests

```bash
pytest tests.py -v
```

### 5. Debug with LangSmith

1. View traces at [smith.langchain.com](https://smith.langchain.com)
2. Click on project name
3. See all agent executions with details

---

## Troubleshooting Setup

### Check Python Version

```bash
python --version  # Should be 3.10+
```

### Check Pip

```bash
pip --version
pip list | grep langchain
```

### Check Imports

```python
# test_imports.py
try:
    from langchain import agents
    print("✓ langchain")
    from langchain import chat_models
    print("✓ chat_models")
    from langgraph import graph
    print("✓ langgraph")
    print("\nAll imports successful!")
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("Run: pip install -r requirements.txt")
```

Run it:
```bash
python test_imports.py
```

### Check API Key

```python
# test_api_key.py
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("ANTHROPIC_API_KEY")
if key:
    print(f"✓ API key found: {key[:20]}...")
else:
    print("✗ API key not found")
    print("Set: export ANTHROPIC_API_KEY='...'")
```

Run it:
```bash
python test_api_key.py
```

---

## Pro Tips: Streamline Your Workflow

### 1. Let pyenv Auto-Switch Python

Since `.python-version` is committed to the repo, **pyenv automatically switches Python when you enter the directory**:

```bash
cd hello-langchain
python --version  # Automatically uses Python 3.11.0
```

### 2. Verify Pyenv is Managing Your Environment

```bash
pyenv versions       # See all installed Python versions
pyenv which python   # Show which Python pyenv is using
cat .python-version  # See repo's Python version requirement
```

### 3. Switching Python Versions Permanently (If Needed)

```bash
# Install a different version
pyenv install 3.12.0

# Update .python-version file
echo "3.12.0" > .python-version

# Verify
python --version  # Should show Python 3.12.0
```

### 5. Deactivate Virtual Environment

```bash
deactivate  # Exit venv
# Python reverts to pyenv's global or system default
```

---

## Next Steps

1. ✅ Complete setup
2. Run `01-foundations/01-basic-agent/main.py`
3. Follow [LEARNING_PATH.md](../LEARNING_PATH.md)
4. Join [LangChain Forum](https://forum.langchain.com/)

---

## Getting Help

- **Setup issues?** - See troubleshooting.md
- **API questions?** - See quick-reference.md
- **Learning?** - See LEARNING_PATH.md
- **Ecosystem?** - See ECOSYSTEM_GUIDE.md

---

**Ready to start?** Let's build! 🚀
