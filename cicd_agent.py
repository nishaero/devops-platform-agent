"""
CI/CD agent for generating CI/CD pipelines
"""
from typing import Dict, Any, Optional
from devops_platform_agent.models import DevOpsPlatformState
from devops_platform_agent.logging_config import logger
import jinja2

# Template for GitLab CI configuration
GITLAB_CI_TEMPLATE = """
# Auto-generated GitLab CI configuration
stages:
  - build
  - test
  - deploy

build_job:
  stage: build
  image: {{ image }}
  script:
    - echo "Building {{ project_name }}..."
    - npm install
    - npm run build

test_job:
  stage: test
  image: {{ image }}
  script:
    - echo "Running tests for {{ project_name }}..."
    - npm test

deploy_job:
  stage: deploy
  image: {{ image }}
  script:
    - echo "Deploying {{ project_name }}..."
    - echo "Deployment script would go here"
  only:
    - main
"""

async def cicd_agent_node(state: DevOpsPlatformState) -> Dict[str, Any]:
    """
    CI/CD agent that generates CI/CD pipeline configuration
    """
    logger.info("CI/CD agent processing", state=state.dict())
    
    try:
        # Extract project information from user request
        project_name = "my-app"
        if "node" in state.user_request.lower():
            project_name = "node-app"
        elif "python" in state.user_request.lower():
            project_name = "python-app"
        elif "java" in state.user_request.lower():
            project_name = "java-app"
            
        # Determine base image
        image = "node:18"
        if "python" in state.user_request.lower():
            image = "python:3.11"
        elif "java" in state.user_request.lower():
            image = "openjdk:17"
            
        # Render template
        template = jinja2.Template(GITLAB_CI_TEMPLATE)
        gitlab_ci_content = template.render(
            project_name=project_name,
            image=image
        )
        
        # Store generated data
        cicd_data = {
            ".gitlab-ci.yml": gitlab_ci_content,
            "project_name": project_name,
            "build_image": image
        }
        
        # Update state
        state.completed_phases.append("cicd")
        state.cicd_data = cicd_data
        
        logger.info("CI/CD pipeline generated successfully", project=project_name)
        
        return {
            "cicd_data": cicd_data,
            "message": f"CI/CD pipeline for {project_name} generated successfully"
        }
        
    except Exception as e:
        logger.error("CI/CD agent error", error=str(e))
        state.errors.append({
            "agent": "cicd",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        })
        return {"error": f"Error in CI/CD agent: {e}"}