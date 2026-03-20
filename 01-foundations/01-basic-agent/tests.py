"""
Phase 1, Experiment 1: Tests
Verify agent functionality
"""

import pytest
from main import agent, get_weather, model


def test_weather_tool():
    """Test weather tool returns valid data."""
    result = get_weather("San Francisco")
    assert "Sunny" in result or "72" in result
    assert isinstance(result, str)


def test_weather_tool_missing_city():
    """Test tool handles unknown cities gracefully."""
    result = get_weather("Atlantis")
    assert isinstance(result, str)
    assert len(result) > 0


def test_agent_invocation():
    """Test agent can be invoked."""
    response = agent.invoke(
        {"messages": [{"role": "user", "content": "What's the weather?"}]}
    )
    assert "output" in response
    assert isinstance(response["output"], str)


def test_agent_uses_tools():
    """Test agent can use tools properly."""
    response = agent.invoke(
        {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
    )
    # Response should mention something about weather
    assert any(word in response["output"].lower() for word in ["weather", "sunny", "72"])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
