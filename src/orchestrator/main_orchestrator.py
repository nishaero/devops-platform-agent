"""
Main Orchestrator for DevOps Platform
Coordinates different agents in the platform
"""
import asyncio
import logging
from typing import Dict, Any
from src.agents.infra_agent import InfraAgent
from src.agents.cicd_agent import CICDAgent
from src.agents.app_agent import AppAgent
from src.models.state import DevOpsState

logger = logging.getLogger(__name__)

class MainOrchestrator:
    """Main orchestrator that coordinates all agents"""
    
    def __init__(self):
        self.infra_agent = InfraAgent()
        self.cicd_agent = CICDAgent()
        self.app_agent = AppAgent()
        
    async def execute_pipeline(self, state: DevOpsState) -> Dict[str, Any]:
        """Execute the complete DevOps pipeline"""
        try:
            logger.info("Starting DevOps pipeline execution")
            
            # Execute infrastructure phase
            if "infra" not in state.completed_phases:
                logger.info("Executing infrastructure phase")
                infra_result = await self.infra_agent.execute(state)
                state.mark_phase_completed("infra")
            else:
                logger.info("Infrastructure phase already completed")
                infra_result = {"status": "skipped", "message": "Infrastructure already configured"}
            
            # Execute application phase
            if "app" not in state.completed_phases:
                logger.info("Executing application phase")
                app_result = await self.app_agent.execute(state)
                state.mark_phase_completed("app")
            else:
                logger.info("Application phase already completed")
                app_result = {"status": "skipped", "message": "Application already configured"}
            
            # Execute CI/CD phase
            if "cicd" not in state.completed_phases:
                logger.info("Executing CI/CD phase")
                cicd_result = await self.cicd_agent.execute(state)
                state.mark_phase_completed("cicd")
            else:
                logger.info("CI/CD phase already completed")
                cicd_result = {"status": "skipped", "message": "CI/CD already configured"}
            
            # Return combined results
            return {
                "status": "success",
                "infra": infra_result,
                "app": app_result,
                "cicd": cicd_result,
                "completed_phases": state.completed_phases
            }
            
        except Exception as e:
            logger.error(f"Error in pipeline execution: {str(e)}")
            state.add_error("orchestrator", str(e))
            raise
    
    async def execute_phase(self, phase: str, state: DevOpsState) -> Dict[str, Any]:
        """Execute a specific phase of the pipeline"""
        try:
            logger.info(f"Executing {phase} phase")
            
            if phase == "infra":
                result = await self.infra_agent.execute(state)
                state.mark_phase_completed("infra")
            elif phase == "app":
                result = await self.app_agent.execute(state)
                state.mark_phase_completed("app")
            elif phase == "cicd":
                result = await self.cicd_agent.execute(state)
                state.mark_phase_completed("cicd")
            else:
                raise ValueError(f"Unknown phase: {phase}")
            
            return {
                "status": "success",
                "phase": phase,
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error executing {phase} phase: {str(e)}")
            state.add_error(f"{phase}_agent", str(e))
            raise