# Getting Started: Your LangChain Mastery Journey 🚀

Welcome to **hello-langchain**! This is your hands-on learning repository to become a LangChain expert.

---

## What You're About to Learn

The LangChain platform consists of:

1. **LangChain** - Build agents with tools and memory
2. **LangGraph** - Orchestrate complex agentic workflows
3. **LangSmith** - Monitor and evaluate in production

By the end of 8 weeks, you'll be able to:
- ✅ Build production-ready AI agents
- ✅ Design complex agent workflows
- ✅ Deploy and monitor in production
- ✅ Teach others (become the expert!)

---

## Quick Start (5 minutes)

### 1. Set Up Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Set API key
export ANTHROPIC_API_KEY="sk-ant-..."

# Or create .env file
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
```

### 2. Run First Example

```bash
cd 01-foundations/01-basic-agent
python main.py
```

You should see:
```
User: "What's the weather in San Francisco?"
Agent: "The weather in San Francisco is sunny..."
```

### 3. Choose Your Path

- **📚 Read:** See [LEARNING_PATH.md](LEARNING_PATH.md) for week-by-week guide
- **🏗️ Understand:** See [ECOSYSTEM_GUIDE.md](ECOSYSTEM_GUIDE.md) for framework overview
- **📖 Reference:** See [docs/quick-reference.md](docs/quick-reference.md) for API docs
- **🛠️ Setup:** See [docs/setup.md](docs/setup.md) for detailed configuration

---

## Repository Structure

```
├── 01-foundations/        ← START HERE
│   ├── 01-basic-agent/
│   ├── 02-tools-and-binding/
│   ├── 03-memory-state/
│   └── 04-structured-output/
│
├── 02-intermediate/       ← WEEK 3-4
│   ├── 01-state-graph-basics/
│   ├── 02-nodes-and-edges/
│   ├── 03-conditional-routing/
│   └── 04-agent-loop-patterns/
│
├── 03-advanced/           ← WEEK 5-6
│   ├── 01-multi-agent-systems/
│   ├── 02-langsmith-integration/
│   ├── 03-evaluation-framework/
│   └── 04-performance-optimization/
│
├── 04-capstone/           ← WEEK 7-8
│   ├── 01-weather-agent/
│   ├── 02-research-assistant/
│   └── 03-reasoning-system/
│
└── docs/
    ├── quick-reference.md
    ├── setup.md
    ├── troubleshooting.md
    └── resources.md
```

---

## Learning Timeline

### Week 1-2: Foundations 🏗️
Learn core concepts with LangChain

**Topics:**
- Basic agents and tools
- Tool binding and invocation
- Memory and conversations
- Structured output

**Experiments:**
```
01-foundations/01-basic-agent/           ← Start here
01-foundations/02-tools-and-binding/
01-foundations/03-memory-state/
01-foundations/04-structured-output/
```

### Week 3-4: LangGraph 🔗
Master workflow orchestration

**Topics:**
- State graphs and state management
- Nodes and edges
- Conditional routing
- Agent loops (ReAct pattern)

**Experiments:**
```
02-intermediate/01-state-graph-basics/
02-intermediate/02-nodes-and-edges/
02-intermediate/03-conditional-routing/
02-intermediate/04-agent-loop-patterns/
```

### Week 5-6: Production 🚀
Prepare for real-world deployment

**Topics:**
- Multi-agent systems
- LangSmith monitoring
- Evaluation frameworks
- Performance optimization

**Experiments:**
```
03-advanced/01-multi-agent-systems/
03-advanced/02-langsmith-integration/
03-advanced/03-evaluation-framework/
03-advanced/04-performance-optimization/
```

### Week 7-8: Mastery ⭐
Build real applications

**Topics:**
- Full production applications
- Architecture patterns
- Teaching and mentoring
- Community contribution

**Projects:**
```
04-capstone/01-weather-agent/
04-capstone/02-research-assistant/
04-capstone/03-reasoning-system/
```

---

## Each Experiment Includes

```
experiment/
├── README.md              # Learning goals and theory
├── main.py               # Main implementation
├── advanced.py           # Advanced variations
└── tests.py              # Unit tests
```

**Each README explains:**
- 📚 What you'll learn
- 🎯 Key concepts
- 💻 Code walkthrough
- 🏃 Running the example
- 📝 Exercises
- 🎓 Key takeaways

---

## Your Daily Workflow

### Morning (30 mins)
- Read the experiment README
- Review code concepts
- Look at examples in docs/

### Midday (60 mins)
- Code along with the example
- Modify and experiment
- Run exercises

### Evening (30 mins)
- Review what you learned
- Write notes in a journal
- Plan tomorrow's learnings

---

## Key Resources

### Documentation
- [LangChain Docs](https://docs.langchain.com/) - Official docs
- [LangSmith Docs](https://docs.langchain.com/langsmith/) - Monitoring
- [API Reference](https://reference.langchain.com/) - Detailed API
- [LangChain Academy](https://academy.langchain.com/) - Courses

### Community
- [Forum](https://forum.langchain.com/) - Ask questions
- [Discord](https://discord.gg/langchain) - Chat with others
- [Blog](https://blog.langchain.com/) - Latest news
- [GitHub](https://github.com/langchain-ai) - Source code

### This Repository
- [LEARNING_PATH.md](LEARNING_PATH.md) - 8-week breakdown
- [ECOSYSTEM_GUIDE.md](ECOSYSTEM_GUIDE.md) - Framework overview
- [docs/quick-reference.md](docs/quick-reference.md) - API cheat sheet
- [docs/setup.md](docs/setup.md) - Installation help
- [docs/troubleshooting.md](docs/troubleshooting.md) - Problem solving

---

## Success Checklist

- [ ] Environment set up (Python, pip, venv)
- [ ] API key configured and tested
- [ ] Ran first example successfully
- [ ] All Phase 1 experiments completed
- [ ] Understand core LangChain concepts
- [ ] Can build basic agents from scratch
- [ ] All Phase 2 experiments completed
- [ ] Comfortable with LangGraph
- [ ] All Phase 3 experiments completed
- [ ] Ready for production
- [ ] Built capstone project
- [ ] Can teach others
- [ ] Contributing to community

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'langchain'"
```bash
pip install -r requirements.txt
```

### "AuthenticationError: Invalid API key"
```bash
# Check your key is set
echo $ANTHROPIC_API_KEY

# If empty, set it
export ANTHROPIC_API_KEY="sk-ant-..."
```

### "Agent doesn't use tools"
- Check tool has clear docstring
- Verify tool is in tools list
- See [docs/troubleshooting.md](docs/troubleshooting.md)

**More help:** See [docs/troubleshooting.md](docs/troubleshooting.md)

---

## Tips for Success

### 🎯 Learn Actively
- Type code by hand (don't copy-paste)
- Modify examples
- Experiment with parameters
- Debug when it fails

### 📝 Take Notes
- Keep a learning journal
- Write what you learned each day
- Document "aha!" moments
- Record common gotchas

### 🤝 Share Your Learning
- Explain concepts to others
- Write blog posts
- Help in forums
- Contribute examples

### 🧪 Build Projects
- Build variations on examples
- Combine concepts creatively
- Show your work
- Celebrate wins!

---

## Next Actions

### Right Now:
1. Set up environment: `pip install -r requirements.txt`
2. Configure API key: `export ANTHROPIC_API_KEY="..."`
3. Run first example: `cd 01-foundations/01-basic-agent && python main.py`

### Today:
1. Read [docs/setup.md](docs/setup.md) carefully
2. Complete 01-foundations/01-basic-agent
3. Do Exercise 1 from README

### This Week:
1. Complete all Phase 1 experiments (4 total)
2. Understand all core concepts
3. Write summary notes

### This Month:
1. Complete Phases 1-2 (foundations + LangGraph)
2. Build real project
3. Help others learn

---

## Questions?

1. **Setup help:** See [docs/setup.md](docs/setup.md)
2. **API help:** See [docs/quick-reference.md](docs/quick-reference.md)
3. **Stuck?** See [docs/troubleshooting.md](docs/troubleshooting.md)
4. **Learning path?** See [LEARNING_PATH.md](LEARNING_PATH.md)
5. **Big picture?** See [ECOSYSTEM_GUIDE.md](ECOSYSTEM_GUIDE.md)

---

## Let's Get Started! 🚀

**Your next step:** 
Run the first experiment!

```bash
cd 01-foundations/01-basic-agent
python main.py
```

Welcome to your LangChain mastery journey! 🎓

---

**Status:** Ready to learn!  
**Last Updated:** March 20, 2026  
**Learning Path:** 8 weeks to expertise
