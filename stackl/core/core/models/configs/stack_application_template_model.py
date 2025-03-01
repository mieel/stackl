"""
Stack Application Template model
"""
from typing import List, Dict, Any
from pydantic import BaseModel  # pylint: disable=E0611 #error in pylint


class StackApplicationTemplateService(BaseModel):
    """
    Definition of a service within a SAT
    """
    name: str
    service: str


class StackStage(BaseModel):
    """
    Stack stage model
    """
    name: str
    services: List[str]


class StackApplicationTemplate(BaseModel):
    """
    Stack Application Template model
    """
    category = "configs"
    name: str
    description: str = ""
    type = "stack_application_template"
    services: List[StackApplicationTemplateService]
    policies: Dict[str, List[Any]] = None
    stages: List[StackStage] = None
