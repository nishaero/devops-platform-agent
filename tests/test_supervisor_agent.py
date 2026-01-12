"""
Test cases for the supervisor agent
"""
import pytest
from devops_platform_agent.supervisor_agent import supervisor_agent_node
from devops_platform_agent.models import DevOpsPlatformState

@pytest.mark.asyncio
async def test_supervisor_agent_initial():
    """Test supervisor agent with no completed phases"""
    state = DevOpsPlatformState(user_request="Create CI/CD pipeline")
    result = await supervisor_agent_node(state)
    
    assert result["current_agent"] == "cicd_agent"

@pytest.mark.asyncio
async def test_supervisor_agent_with_completed_cicd():
    """Test supervisor agent with completed CI/CD phase"""
    state = DevOpsPlatformState(
        user_request="Create CI/CD pipeline",
        completed_phases=["cicd"]
    )
    result = await supervisor_agent_node(state)
    
    assert result["current_agent"] == "infra_agent"

@pytest.mark.asyncio
async def test_supervisor_agent_with_all_completed():
    """Test supervisor agent with all phases completed"""
    state = DevOpsPlatformState(
        user_request="Create CI/CD pipeline",
        completed_phases=["cicd", "infra", "k8s", "monitoring", "security"]
    )
    result = await supervisor_agent_node(state)
    
    assert "final_response" in result