"""
Test cases for the CI/CD agent
"""
import pytest
from devops_platform_agent.cicd_agent import cicd_agent_node
from devops_platform_agent.models import DevOpsPlatformState

@pytest.mark.asyncio
async def test_cicd_agent_nodejs():
    """Test CI/CD agent with Node.js project"""
    state = DevOpsPlatformState(user_request="Create Node.js application")
    result = await cicd_agent_node(state)
    
    assert "cicd_data" in result
    assert ".gitlab-ci.yml" in result["cicd_data"]
    assert "node-app" in result["cicd_data"]["project_name"]

@pytest.mark.asyncio
async def test_cicd_agent_python():
    """Test CI/CD agent with Python project"""
    state = DevOpsPlatformState(user_request="Create Python application")
    result = await cicd_agent_node(state)
    
    assert "cicd_data" in result
    assert "python-app" in result["cicd_data"]["project_name"]
    assert "python:3.11" in result["cicd_data"]["build_image"]