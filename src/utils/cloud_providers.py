"""
Cloud Providers utility for DevOps Platform
Handles different cloud provider configurations
"""
from enum import Enum
from typing import Dict, Any

class CloudProvider(Enum):
    """Supported cloud providers"""
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"

class CloudProviderConfig:
    """Configuration for cloud providers"""
    
    @staticmethod
    def get_provider_config(provider: CloudProvider) -> Dict[str, Any]:
        """Get configuration for a specific cloud provider"""
        configs = {
            CloudProvider.AWS: {
                "name": "AWS",
                "region": "us-east-1",
                "default_region": "us-east-1",
                "supported_regions": [
                    "us-east-1", "us-east-2", "us-west-1", "us-west-2",
                    "eu-west-1", "eu-west-2", "eu-west-3", "eu-central-1",
                    "ap-southeast-1", "ap-southeast-2", "ap-northeast-1",
                    "ap-northeast-2", "sa-east-1"
                ],
                "provider_block": "aws",
                "default_vpc_cidr": "10.0.0.0/16"
            },
            CloudProvider.AZURE: {
                "name": "Azure",
                "region": "eastus",
                "default_region": "eastus",
                "supported_regions": [
                    "eastus", "eastus2", "westus", "westus2", "westus3",
                    "northcentralus", "southcentralus", "northeurope",
                    "westeurope", "southeastasia", "eastasia", "japaneast",
                    "japanwest", "brazilsouth", "australiaeast", "australiasoutheast"
                ],
                "provider_block": "azurerm",
                "default_vpc_cidr": "10.0.0.0/16"
            },
            CloudProvider.GCP: {
                "name": "GCP",
                "region": "us-central1",
                "default_region": "us-central1",
                "supported_regions": [
                    "us-central1", "us-east1", "us-east4", "us-west1", "us-west2",
                    "us-west3", "northamerica-northeast1", "southamerica-east1",
                    "europe-west1", "europe-west2", "europe-west3", "europe-west4",
                    "europe-west5", "europe-west6", "asia-east1", "asia-east2",
                    "asia-northeast1", "asia-northeast2", "asia-south1", "asia-southeast1",
                    "asia-southeast2"
                ],
                "provider_block": "google",
                "default_vpc_cidr": "10.0.0.0/16"
            }
        }
        
        return configs.get(provider, configs[CloudProvider.AWS])
    
    @staticmethod
    def get_supported_providers() -> list:
        """Get list of supported cloud providers"""
        return [provider.value for provider in CloudProvider]
    
    @staticmethod
    def validate_provider(provider: str) -> bool:
        """Validate if a provider is supported"""
        return provider in CloudProvider.__members__