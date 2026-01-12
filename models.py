"""
Data models for the DevOps Platform Agent
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class DevOpsPlatformState(BaseModel):
    """
    State model representing the current state of the DevOps platform workflow
    """
    user_request: str
    lifecycle_phase: Optional[str] = None
    current_agent: Optional[str] = None
    completed_phases: List[str] = []
    errors: List[Dict[str, Any]] = []
    retry_count: int = 0
    requires_clarification: bool = False
    clarification_question: Optional[str] = None
    final_response: Optional[str] = None
    cicd_data: Optional[Dict[str, Any]] = None
    infra_data: Optional[Dict[str, Any]] = None
    k8s_data: Optional[Dict[str, Any]] = None
    monitoring_data: Optional[Dict[str, Any]] = None
    security_data: Optional[Dict[str, Any]] = None
    timestamp: datetime = datetime.now()
    
    class Config:
        # Allow extra fields for flexibility
        extra = "allow"