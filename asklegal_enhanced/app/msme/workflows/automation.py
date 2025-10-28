from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import uuid

class Workflow:
    """Workflow model"""
    
    def __init__(self, workflow_id: str, name: str, description: str, user_id: str):
        self.workflow_id = workflow_id
        self.name = name
        self.description = description
        self.user_id = user_id
        self.status = "active"  # active, completed, paused
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.steps = []
        self.current_step = 0
        self.completed_steps = []

class WorkflowStep:
    """Workflow step model"""
    
    def __init__(self, step_id: str, title: str, description: str, step_type: str):
        self.step_id = step_id
        self.title = title
        self.description = description
        self.step_type = step_type  # task, decision, notification
        self.status = "pending"  # pending, in_progress, completed, failed
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
        self.assigned_to = None
        self.due_date = None

class WorkflowAutomationEngine:
    """Workflow automation engine for MSMEs"""
    
    def __init__(self):
        """Initialize the workflow automation engine"""
        self.workflows = {}  # In-memory storage for now
        self.workflow_templates = self._load_workflow_templates()
    
    def _load_workflow_templates(self) -> Dict[str, Dict[str, Any]]:
        """
        Load workflow templates
        
        Returns:
            Dict[str, Dict[str, Any]]: Workflow templates
        """
        return {
            "compliance_check": {
                "name": "Compliance Check",
                "description": "Complete legal compliance requirements for your business",
                "steps": [
                    {
                        "title": "Review Legal Requirements",
                        "description": "Review industry-specific legal requirements",
                        "step_type": "task",
                        "duration_days": 3
                    },
                    {
                        "title": "Gather Documentation",
                        "description": "Collect required documents and certificates",
                        "step_type": "task",
                        "duration_days": 5
                    },
                    {
                        "title": "Submit Applications",
                        "description": "Submit applications to relevant authorities",
                        "step_type": "task",
                        "duration_days": 7
                    },
                    {
                        "title": "Follow Up",
                        "description": "Follow up on pending applications",
                        "step_type": "task",
                        "duration_days": 10
                    }
                ]
            },
            "contract_management": {
                "name": "Contract Management",
                "description": "Manage business contracts and agreements",
                "steps": [
                    {
                        "title": "Draft Contract",
                        "description": "Create initial contract draft",
                        "step_type": "task",
                        "duration_days": 2
                    },
                    {
                        "title": "Legal Review",
                        "description": "Review contract with legal team",
                        "step_type": "task",
                        "duration_days": 3
                    },
                    {
                        "title": "Negotiation",
                        "description": "Negotiate terms with counterparty",
                        "step_type": "task",
                        "duration_days": 5
                    },
                    {
                        "title": "Finalize and Sign",
                        "description": "Finalize contract and obtain signatures",
                        "step_type": "task",
                        "duration_days": 2
                    }
                ]
            },
            "employee_onboarding": {
                "name": "Employee Onboarding",
                "description": "Complete employee onboarding process",
                "steps": [
                    {
                        "title": "Prepare Documentation",
                        "description": "Prepare employment contract and policies",
                        "step_type": "task",
                        "duration_days": 1
                    },
                    {
                        "title": "Background Check",
                        "description": "Conduct background verification",
                        "step_type": "task",
                        "duration_days": 3
                    },
                    {
                        "title": "Orientation",
                        "description": "Conduct employee orientation session",
                        "step_type": "task",
                        "duration_days": 1
                    },
                    {
                        "title": "Training",
                        "description": "Provide role-specific training",
                        "step_type": "task",
                        "duration_days": 5
                    }
                ]
            }
        }
    
    def create_workflow(self, user_id: str, template_name: str, custom_name: Optional[str] = None) -> Optional[str]:
        """
        Create a new workflow from a template
        
        Args:
            user_id (str): User identifier
            template_name (str): Name of the workflow template
            custom_name (str, optional): Custom name for the workflow
            
        Returns:
            Optional[str]: Workflow ID if created, None otherwise
        """
        if template_name not in self.workflow_templates:
            return None
        
        template = self.workflow_templates[template_name]
        
        # Generate workflow ID
        workflow_id = str(uuid.uuid4())
        
        # Create workflow
        name = custom_name if custom_name else template["name"]
        workflow = Workflow(workflow_id, name, template["description"], user_id)
        
        # Create steps
        for i, step_template in enumerate(template["steps"]):
            step_id = f"{workflow_id}_step_{i+1}"
            step = WorkflowStep(
                step_id,
                step_template["title"],
                step_template["description"],
                step_template["step_type"]
            )
            
            # Set due date
            if "duration_days" in step_template:
                step.due_date = datetime.now() + timedelta(days=step_template["duration_days"])
            
            workflow.steps.append(step)
        
        # Store workflow
        self.workflows[workflow_id] = workflow
        
        return workflow_id
    
    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """
        Get a workflow by ID
        
        Args:
            workflow_id (str): Workflow identifier
            
        Returns:
            Optional[Workflow]: Workflow or None if not found
        """
        return self.workflows.get(workflow_id)
    
    def get_user_workflows(self, user_id: str) -> List[Workflow]:
        """
        Get all workflows for a user
        
        Args:
            user_id (str): User identifier
            
        Returns:
            List[Workflow]: List of workflows
        """
        return [workflow for workflow in self.workflows.values() if workflow.user_id == user_id]
    
    def start_workflow_step(self, workflow_id: str, step_index: int) -> bool:
        """
        Start a workflow step
        
        Args:
            workflow_id (str): Workflow identifier
            step_index (int): Index of the step to start
            
        Returns:
            bool: True if started successfully, False otherwise
        """
        workflow = self.get_workflow(workflow_id)
        if not workflow or step_index >= len(workflow.steps):
            return False
        
        step = workflow.steps[step_index]
        if step.status != "pending":
            return False
        
        step.status = "in_progress"
        step.started_at = datetime.now()
        workflow.updated_at = datetime.now()
        
        return True
    
    def complete_workflow_step(self, workflow_id: str, step_index: int) -> bool:
        """
        Complete a workflow step
        
        Args:
            workflow_id (str): Workflow identifier
            step_index (int): Index of the step to complete
            
        Returns:
            bool: True if completed successfully, False otherwise
        """
        workflow = self.get_workflow(workflow_id)
        if not workflow or step_index >= len(workflow.steps):
            return False
        
        step = workflow.steps[step_index]
        if step.status != "in_progress":
            return False
        
        step.status = "completed"
        step.completed_at = datetime.now()
        workflow.completed_steps.append(step_index)
        workflow.updated_at = datetime.now()
        
        # Move to next step if available
        if step_index + 1 < len(workflow.steps):
            workflow.current_step = step_index + 1
        
        return True
    
    def get_workflow_progress(self, workflow_id: str) -> Dict[str, Any]:
        """
        Get workflow progress
        
        Args:
            workflow_id (str): Workflow identifier
            
        Returns:
            Dict[str, Any]: Workflow progress information
        """
        workflow = self.get_workflow(workflow_id)
        if not workflow:
            return {}
        
        total_steps = len(workflow.steps)
        completed_steps = len(workflow.completed_steps)
        progress_percentage = (completed_steps / total_steps) * 100 if total_steps > 0 else 0
        
        return {
            "workflow_id": workflow_id,
            "name": workflow.name,
            "status": workflow.status,
            "total_steps": total_steps,
            "completed_steps": completed_steps,
            "progress_percentage": progress_percentage,
            "current_step": workflow.current_step
        }
    
    def get_available_templates(self) -> List[Dict[str, str]]:
        """
        Get available workflow templates
        
        Returns:
            List[Dict[str, str]]: List of available templates
        """
        templates = []
        for name, template in self.workflow_templates.items():
            templates.append({
                "name": name,
                "display_name": template["name"],
                "description": template["description"]
            })
        return templates

# Global instance
workflow_engine = WorkflowAutomationEngine()