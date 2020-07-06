import logging
from typing import Dict, Any, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel  # pylint: disable=E0611 #pylint error
from stackl.enums.stackl_codes import StatusCode
from stackl.models.items.stack_instance_model import StackInstance
from stackl.tasks.document_task import DocumentTask
from stackl.tasks.stack_task import StackTask
from stackl.utils.general_utils import get_hostname

from rest.producer.producer_factory import get_producer

logger = logging.getLogger("STACKL_LOGGER")
router = APIRouter()
producer = get_producer()


class StackInstanceInvocation(BaseModel):
    params: Dict[str, Any] = {}
    tags: Dict[str, str] = {}
    stack_infrastructure_template: str = "stackl"
    stack_application_template: str = "web"
    stack_instance_name: str = "default_test_instance"
    secrets: Dict[str, Any] = {}
    replicas: Dict[str, int] = {}

    class Config:
        schema_extra = {
            "example": {
                "params": {},
                "secrets": {},
                "stack_infrastructure_template": "stackl",
                "stack_application_template": "web",
                "name": "default_test_instance"
            }
        }


class StackInstanceUpdate(BaseModel):
    params: Dict[str, Any] = {}
    stack_instance_name: str = "default_test_instance"
    secrets: Dict[str, Any] = {}
    disable_invocation: bool = False

    class Config:
        schema_extra = {
            "example": {
                "params": {},
                "secrets": {},
                "stack_instance_name": "default_test_instance"
            }
        }


class StackCreateResult(BaseModel):
    result: str


@router.get('/{name}', response_model=StackInstance)
def get_stack_instance(name: str):
    """Returns a stack instance with a specific name"""
    logger.info(
        f"[StackInstancesName GET] Getting document for stack instance '{name}'"
    )
    task = DocumentTask.parse_obj({
        'channel': 'worker',
        'args': ('stack_instance', name),
        'subtype': "GET_DOCUMENT"
    })

    result = producer.give_task_and_get_result(task)
    return result.return_result


@router.get('/', response_model=List[StackInstance])
def get_stack_instances(name: str = ""):
    """Returns all stack instances that contain optional name"""
    logger.info(
        f"[StackInstancesAll GET] Returning all stack instances that contain optional name '{name}'"
    )
    task = DocumentTask.parse_obj({
        'channel': 'worker',
        'args': "stack_instance",
        'subtype': "COLLECT_DOCUMENT"
    })

    result = producer.give_task_and_get_result(task)

    return result.return_result


@router.post('')
async def post_stack_instance(
    stack_instance_invocation: StackInstanceInvocation):
    """Creates a stack instance with a specific name"""
    logger.info("[StackInstances POST] Received POST request")

    task = StackTask.parse_obj({
        'channel': 'worker',
        'json_data': stack_instance_invocation.dict(),
        'subtype': "CREATE_STACK",
        'return_channel': get_hostname()
    })
    logger.info(
        f"[StackInstances POST] Giving StackTask '{task}' to task_broker")

    result = producer.give_task_and_get_result(task)

    return result.return_result


@router.put('')
def put_stack_instance(stack_instance_update: StackInstanceUpdate):
    """Update a stack instance with the given name from a stack application template and stack infrastructure template, creating a new one if it does not yet exist"""
    logger.info("[StackInstances PUT] Received PUT request")

    task = StackTask.parse_obj({
        'channel': 'worker',
        'json_data': stack_instance_update.dict(),
        'subtype': "UPDATE_STACK",
    })
    logger.info(
        f"[StackInstances PUT] Giving StackTask '{task}' to task_broker")

    return "Stack instance updating"


@router.delete('/{name}')
def delete_stack_instance(name: str):
    """Delete a stack instance with a specific name"""
    logger.info(f"[StackInstances DELETE] Received DELETE request for {name}")
    json_data = {}
    json_data['name'] = name
    task = StackTask.parse_obj({
        'channel': 'worker',
        'json_data': json_data,
        'subtype': "DELETE_STACK",
    })
    logger.info(
        f"[StackInstances DELETE] Giving StackTask '{dict(task)}' to task_broker"
    )

    result = producer.give_task_and_get_result(task)

    if not StatusCode.is_successful(result):
        raise HTTPException(status_code=StatusCode.BAD_REQUEST,
                            detail="NOT OK!")
    return result
