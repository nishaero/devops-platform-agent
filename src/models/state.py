"""
DevOps State Model
Defines the state structure for the DevOps platform
"""
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
from datetime import datetime

class DevOpsState(BaseModel):
    """State model for DevOps platform"""
    user_request: str
    project_name: Optional[str] = None
    completed_phases: List[str] = []
    errors: List[Dict[str, Any]] = []
    cicd_data: Dict[str, Any] = {}
    infra_data: Dict[str, Any] = {}
    app_data: Dict[str, Any] = {}
    deployment_data: Dict[str, Any] = {}
    timestamp: datetime = datetime.now()
    
    def add_error(self, agent: str, error: str):
        """Add an error to the state"""
        self.errors.append({
            "agent": agent,
            "error": error,
            "timestamp": datetime.now()
        })
    
    def mark_phase_completed(self, phase: str):
        """Mark a phase as completed"""
        if phase not in self.completed_phases:
            self.completed_phases.append(phase)
    
    def get_phase_status(self, phase: str) -> bool:
        """Check if a phase is completed"""
        return phase in self.completed_phases