"""
Example usage of the infrastructure agent
"""
import asyncio
import logging
from src.models.state import DevOpsState
from src.orchestrator.main_orchestrator import MainOrchestrator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """Main example function"""
    # Create orchestrator
    orchestrator = MainOrchestrator()
    
    # Create initial state
    state = DevOpsState(
        user_request="Deploy a web application with CI/CD pipeline",
        project_name="web-app-demo"
    )
    
    # Set up infrastructure data
    state.infra_data = {
        "provider": "aws",
        "region": "us-east-1",
        "vpc_cidr": "10.0.0.0/16",
        "deploy": True
    }
    
    # Set up application data
    state.app_data = {
        "app_type": "web",
        "framework": "nodejs",
        "environment": "production"
    }
    
    # Execute pipeline
    try:
        result = await orchestrator.execute_pipeline(state)
        print("Pipeline execution completed successfully!")
        print(f"Completed phases: {result['completed_phases']}")
        print(f"Infrastructure result: {result['infra']}")
        print(f"Application result: {result['app']}")
        print(f"CI/CD result: {result['cicd']}")
    except Exception as e:
        logger.error(f"Pipeline execution failed: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())