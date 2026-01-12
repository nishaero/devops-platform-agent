"""
Supervisor agent for orchestrating DevOps workflow phases
"""
from typing import Dict, Any, Optional
from devops_platform_agent.models import DevOpsPlatformState
from devops_platform_agent.logging_config import logger

async def supervisor_agent_node(state: DevOpsPlatformState) -> Dict[str, Any]:
    """
    Supervisor agent that determines which agent should run next
    """
    logger.info("Supervisor agent processing", state=state.dict())
    
    try:
        # Check if we have a specific lifecycle phase requested
        if state.lifecycle_phase:
            # If we have a specific phase, run that agent
            return {"current_agent": f"{state.lifecycle_phase}_agent"}
        
        # If no specific phase, determine based on workflow state
        if "cicd" not in state.completed_phases:
            return {"current_agent": "cicd_agent"}
        elif "infra" not in state.completed_phases:
            return {"current_agent": "infra_agent"}
        elif "k8s" not in state.completed_phases:
            return {"current_agent": "k8s_agent"}
        elif "monitoring" not in state.completed_phases:
            return {"current_agent": "monitoring_agent"}
        elif "security" not in state.completed_phases:
            return {"current_agent": "security_agent"}
        else:
            # All phases completed
            return {"final_response": "All DevOps phases completed successfully"}
            
    except Exception as e:
        logger.error("Supervisor agent error", error=str(e))
        state.errors.append({
            "agent": "supervisor",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        })
        state.retry_count += 1

        if state.retry_count < 3:
            return {"current_agent": "supervisor"}  # Retry
        else:
            return {"final_response": f"Error in supervisor agent: {e}"}