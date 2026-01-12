"""
Terraform Generator for DevOps Platform
Generates Terraform configurations for different cloud providers
"""
import json
import re
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

class TerraformResource(BaseModel):
    """Model for Terraform resource"""
    type: str
    name: str
    properties: Dict[str, Any]

class TerraformGenerator:
    """Generates Terraform configurations for different cloud providers"""
    
    def __init__(self, llm_model: str = "gpt-4-turbo"):
        self.llm = ChatOpenAI(model=llm_model, temperature=0.2)
        
    def generate(self, user_request: str, cloud_provider: str, region: str, resources: List[str]) -> Dict[str, Any]:
        """Generate Terraform configuration based on user request"""
        try:
            # Create a prompt for the LLM to generate Terraform code
            prompt_template = """
            Generate Terraform configuration for {cloud_provider} in {region} region.
            User request: "{user_request}"
            
            Resources to include: {resources}
            
            Please generate valid Terraform HCL code with proper structure.
            Include all necessary providers, resources, and outputs.
            """
            
            prompt = PromptTemplate.from_template(prompt_template)
            
            # Get the LLM response
            response = self.llm.invoke(
                prompt.format(
                    cloud_provider=cloud_provider,
                    region=region,
                    user_request=user_request,
                    resources=", ".join(resources)
                )
            )
            
            # Parse the response to extract Terraform code
            terraform_code = response.content
            
            # Convert to structured format
            terraform_config = self._parse_terraform_code(terraform_code)
            
            return terraform_config
            
        except Exception as e:
            raise ValueError(f"Error generating Terraform configuration: {str(e)}")
    
    def _parse_terraform_code(self, terraform_code: str) -> Dict[str, Any]:
        """Parse Terraform code into structured format"""
        # This is a simplified parser - in a real implementation, 
        # you'd want to use a proper Terraform parser
        config = {
            "provider": "aws",
            "resources": [],
            "outputs": [],
            "variables": []
        }
        
        # Extract resources
        resource_pattern = r'resource\s+"(\w+)"\s+"(\w+)"\s+{([^}]*(?:\{[^}]*\}[^}]*)*)}'
        resources = re.findall(resource_pattern, terraform_code, re.DOTALL)
        
        for resource_type, resource_name, resource_body in resources:
            config["resources"].append({
                "type": resource_type,
                "name": resource_name,
                "body": resource_body.strip()
            })
            
        # Extract outputs
        output_pattern = r'output\s+"(\w+)"\s+{([^}]*(?:\{[^}]*\}[^}]*)*)}'
        outputs = re.findall(output_pattern, terraform_code, re.DOTALL)
        
        for output_name, output_body in outputs:
            config["outputs"].append({
                "name": output_name,
                "body": output_body.strip()
            })
            
        return config
    
    def validate(self, terraform_config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the generated Terraform configuration"""
        try:
            # Basic validation checks
            errors = []
            
            if not terraform_config.get("resources"):
                errors.append("No resources defined in Terraform configuration")
                
            if not terraform_config.get("provider"):
                errors.append("No provider defined in Terraform configuration")
                
            # Check for required fields in resources
            for resource in terraform_config.get("resources", []):
                if not resource.get("type"):
                    errors.append("Resource missing type")
                if not resource.get("name"):
                    errors.append("Resource missing name")
                    
            return {
                "valid": len(errors) == 0,
                "errors": errors
            }
            
        except Exception as e:
            return {
                "valid": False,
                "errors": [f"Validation error: {str(e)}"]
            }
    
    def fix_common_issues(self, terraform_config: Dict[str, Any]) -> Dict[str, Any]:
        """Attempt to fix common issues in Terraform configuration"""
        # This is a placeholder for actual fix logic
        # In a real implementation, this would attempt to correct common Terraform errors
        return terraform_config