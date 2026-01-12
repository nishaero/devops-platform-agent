"""
Infrastructure Agent for DevOps Platform
Handles infrastructure provisioning using Terraform
"""
import asyncio
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from src.utils.terraform_generator import TerraformGenerator
from src.utils.cloud_providers import CloudProvider
from src.models.state import DevOpsState

logger = logging.getLogger(__name__)

class InfraAgentInput(BaseModel):
    """Input model for infrastructure agent"""
    user_request: str
    cloud_provider: str
    region: str
    resources: List[str]

class InfraAgent:
    """Infrastructure agent that generates Terraform configurations"""
    
    def __init__(self, llm_model: str = "gpt-4-turbo"):
        self.llm = ChatOpenAI(model=llm_model, temperature=0.2)
        self.terraform_generator = TerraformGenerator()
        
    async def generate_infra_config(self, state: DevOpsState) -> Dict[str, Any]:
        """Generate infrastructure configuration using Terraform"""
        try:
            logger.info("Generating infrastructure configuration")
            
            # Extract information from state
            user_request = state.user_request
            cloud_provider = state.infra_data.get("cloud_provider", "aws")
            region = state.infra_data.get("region", "us-east-1")
            resources = state.infra_data.get("resources", [])
            
            # Generate Terraform configuration
            terraform_config = self.terraform_generator.generate(
                user_request=user_request,
                cloud_provider=cloud_provider,
                region=region,
                resources=resources
            )
            
            # Validate the generated configuration
            validation_result = self.terraform_generator.validate(terraform_config)
            
            if not validation_result["valid"]:
                logger.warning(f"Terraform validation failed: {validation_result['errors']}")
                # Try to fix common issues
                fixed_config = self.terraform_generator.fix_common_issues(terraform_config)
                validation_result = self.terraform_generator.validate(fixed_config)
                
                if not validation_result["valid"]:
                    raise ValueError(f"Terraform validation failed: {validation_result['errors']}")
                
                terraform_config = fixed_config
            
            # Store in state
            state.infra_data["terraform_config"] = terraform_config
            state.infra_data["cloud_provider"] = cloud_provider
            state.infra_data["region"] = region
            state.infra_data["generated"] = True
            
            logger.info("Infrastructure configuration generated successfully")
            return {
                "status": "success",
                "terraform_config": terraform_config,
                "cloud_provider": cloud_provider,
                "region": region
            }
            
        except Exception as e:
            logger.error(f"Error generating infrastructure configuration: {str(e)}")
            state.errors.append({
                "agent": "infra_agent",
                "error": str(e),
                "timestamp": asyncio.get_event_loop().time()
            })
            raise

    async def deploy_infra(self, state: DevOpsState) -> Dict[str, Any]:
        """Deploy the generated infrastructure"""
        try:
            logger.info("Deploying infrastructure")
            
            # In a real implementation, this would actually deploy the infrastructure
            # For now, we'll simulate the deployment
            terraform_config = state.infra_data.get("terraform_config", {})
            
            if not terraform_config:
                raise ValueError("No Terraform configuration found for deployment")
            
            # Simulate deployment
            deployment_result = {
                "status": "success",
                "message": "Infrastructure deployment initiated",
                "resources_deployed": ["vpc", "subnet", "security_group"],
                "outputs": {
                    "vpc_id": "vpc-12345678",
                    "subnet_id": "subnet-12345678"
                }
            }
            
            state.infra_data["deployment_result"] = deployment_result
            state.completed_phases.append("infra")
            
            logger.info("Infrastructure deployed successfully")
            return deployment_result
            
        except Exception as e:
            logger.error(f"Error deploying infrastructure: {str(e)}")
            state.errors.append({
                "agent": "infra_agent",
                "error": str(e),
                "timestamp": asyncio.get_event_loop().time()
            })
            raise

    async def execute(self, state: DevOpsState) -> Dict[str, Any]:
        """Execute the infrastructure agent"""
        try:
            logger.info("Executing infrastructure agent")
            
            # Generate configuration
            config_result = await self.generate_infra_config(state)
            
            # Deploy if requested
            if state.infra_data.get("deploy", False):
                deploy_result = await self.deploy_infra(state)
                config_result["deployment"] = deploy_result
                
            return config_result
            
        except Exception as e:
            logger.error(f"Error in infrastructure agent execution: {str(e)}")
            state.errors.append({
                "agent": "infra_agent",
                "error": str(e),
                "timestamp": asyncio.get_event_loop().time()
            })
            raise