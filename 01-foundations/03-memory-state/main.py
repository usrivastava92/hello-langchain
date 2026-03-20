"""
Phase 1, Experiment 3: Memory & State
Multi-turn conversations with persistent state
"""

import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

# ============================================================================
# STEP 1: Define Tools
# ============================================================================

@tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    weather_db = {
        "San Francisco": "Sunny, 72°F",
        "New York": "Rainy, 68°F",
        "London": "Cloudy, 55°F",
    }
    return weather_db.get(city, f"No data for {city}")


@tool
def set_reminder(topic: str, time: str) -> str:
    """Set a reminder for a topic."""
    return f"Reminder set: {topic} at {time}"


# ============================================================================
# STEP 2: Create Checkpointer for Memory
# ============================================================================

# In-memory checkpointer for development
# In production, use PostgresSaver or similar
checkpointer = InMemorySaver()

print("✓ In-memory checkpointer created")
print("  (In production, use database-backed checkpointer)")


# ============================================================================
# STEP 3: Create Agent with Memory
# ============================================================================

model = init_chat_model("claude-sonnet-4-6", temperature=0.7)

tools = [get_weather, set_reminder]

agent = create_agent(
    model=model,
    tools=tools,
    checkpointer=checkpointer,  # Enable memory!
    system_prompt="""You are a helpful personal assistant.
    You remember user preferences and history.
    Always acknowledge what you remember about the user.
    Be conversational and helpful."""
)

print("✓ Agent created with memory support")


# ============================================================================
# STEP 4: Simulate Multi-Turn Conversation
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("LangChain Memory & State Demo")
    print("="*60 + "\n")
    
    # Define a conversation thread (unique ID per user/conversation)
    thread_id = "user_001_conversation"
    config = {"configurable": {"thread_id": thread_id}}
    
    print(f"Starting conversation with thread_id: {thread_id}")
    print("-" * 60 + "\n")
    
    # Multi-turn conversation
    conversation = [
        "Hi! I'm Bob and I'm visiting from San Francisco. I love sunny weather.",
        "What's the weather going to be like here?",
        "Great! Can you set me a reminder to check the weather tomorrow morning?",
        "What did I tell you about my favorite weather?",
        "Thank you for remembering! One more thing - remind me about my SF trip.",
    ]
    
    print("📝 Conversation with Memory:\n")
    
    for i, user_message in enumerate(conversation, 1):
        print(f"Turn {i}")
        print(f"👤 User: {user_message}")
        
        # Invoke agent with SAME config (same thread)
        response = agent.invoke(
            {"messages": [HumanMessage(content=user_message)]},
            config=config  # Same thread maintains memory!
        )
        
        print(f"🤖 Agent: {response['output']}")
        print()
    
    # ========================================================================
    # STEP 5: Demonstrate Separate Conversations
    # ========================================================================
    
    print("\n" + "="*60)
    print("Separate Conversation (Different Thread)")
    print("="*60 + "\n")
    
    # NEW conversation thread (different user)
    thread_id_2 = "user_002_conversation"
    config_2 = {"configurable": {"thread_id": thread_id_2}}
    
    print(f"Starting new conversation with thread_id: {thread_id_2}\n")
    
    # This agent has NO memory of previous conversation
    print("New user query (no previous context):")
    print("👤 User: What did I tell you about my favorite weather?")
    
    response = agent.invoke(
        {"messages": [
            HumanMessage(content="What did I tell you about my favorite weather?")
        ]},
        config=config_2
    )
    
    print(f"🤖 Agent: {response['output']}")
    print("\n^ Notice: Agent doesn't know about San Francisco or sunny weather")
    print("  because this is a different conversation thread!")


print("\n" + "="*60)
print("Key Learning Points:")
print("- ThreadID maintains conversation history")
print("- Checkpointer persists memory")
print("- Different threads = separate conversations")
print("- Agent remembers context from earlier turns")
print("="*60)
