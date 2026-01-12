"""
Main entry point for the DevOps Platform Agent
"""
import asyncio
from devops_platform_agent.models import DevOpsPlatformState
from devops_platform_agent.supervisor_agent import supervisor_agent_node
from devops_platform_agent.cicd_agent import cicd_agent_node
from devops_platform_agent.logging_config import logger

async def run_devops_workflow(user_request: str):
    """
    Run the complete DevOps workflow
    """
    logger.info("Starting DevOps workflow", request=user_request)
    
    # Initialize state
    state = DevOpsPlatformState(user_request=user_request)
    
    # Run workflow until completion
    while not state.final_response:
        # Determine next agent
        agent_result = await supervisor_agent_node(state)
        
        if "current_agent" in agent_result:
            agent_name = agent_result["current_agent"]
            
            # Run the appropriate agent
            if agent_name == "cicd_agent":
                agent_result = await cicd_agent_node(state)
            elif agent_name == "infra_agent":
                # Placeholder for infrastructure agent
                agent_result = {"message": "Infrastructure agent would run here"}
            elif agent_name == "k8s_agent":
                # Placeholder for Kubernetes agent
                agent_result = {"message": "Kubernetes agent would run here"}
            elif agent_name == "monitoring_agent":
                # Placeholder for monitoring agent
                agent_result = {"message": "Monitoring agent would run here"}
            elif agent_name == "security_agent":
                # Placeholder for security agent
                agent_result = {"message": "Security agent would run here"}
            
            # Update state with agent results
            if "error" in agent_result:
                logger.error("Agent error", error=agent_result["error"])
                state.errors.append({
                    "agent": agent_name,
                    "error": agent_result["error"],
                    "timestamp": datetime.now().isoformat()
                })
            else:
                # Merge agent results into state
                for key, value in agent_result.items():
                    if hasattr(state, key):
                        setattr(state, key, value)
                    else:
                        # Handle dynamic fields
                        setattr(state, key, value)
        elif "final_response" in agent_result:
            state.final_response = agent_result["final_response"]
            break
            
        # Check for clarification needed
        if state.requires_clarification:
            logger.info("Clarification needed", question=state.clarification_question)
            break
            
        # Prevent infinite loops
        if len(state.completed_phases) > 10:
            state.final_response = "Workflow exceeded maximum phases"
            break
    
    logger.info("DevOps workflow completed", final_response=state.final_response)
    return state

def main():
    """
    Main function to run the DevOps agent
    """
    # Example usage
    asyncio.run(run_devops_workflow("Create a Node.js application with CI/CD pipeline"))

if __name__ == "__main__":
    main()