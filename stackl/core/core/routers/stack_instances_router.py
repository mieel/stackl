"""
Endpoint used for creating, updating, reading and deleting stack instances
"""

from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from pydantic import BaseModel
from starlette.background import BackgroundTasks

from core.agent_broker.agent_task_broker import (create_job_for_agent,
                                                 create_job_per_service)
from core.handler.stack_handler import delete_services
from core.manager.document_manager import DocumentManager
from core.manager.stack_manager import StackManager
from core.manager.stackl_manager import (get_document_manager, get_redis,
                                         get_stack_manager)
from core.models.api.stack_instance import (StackInstanceInvocation,
                                            StackInstanceUpdate)
from core.models.items.stack_instance_model import StackInstance
from core.opa_broker.opa_broker_factory import OPABrokerFactory

router = APIRouter()


class StackCreateResult(BaseModel):
    """StackCreateResult Model"""
    result: str


@router.get('/{name}', response_model=StackInstance)
def get_stack_instance(
    name: str,
    document_manager: DocumentManager = Depends(get_document_manager)):
    """Returns a stack instance with a specific name"""
    logger.info(
        f"[StackInstancesName GET] Getting document for stack instance '{name}'"
    )
    stack_instance = document_manager.get_stack_instance(name)
    if not stack_instance:
        raise HTTPException(status_code=404, detail="Stack instance not found")
    return stack_instance


@router.get('', response_model=List[StackInstance])
def get_stack_instances(
    name: str = "",
    document_manager: DocumentManager = Depends(get_document_manager)):
    """Returns all stack instances that contain optional name"""
    logger.info(
        f"[StackInstancesAll GET] Returning all stack instances that contain optional name '{name}'"
    )
    stack_instances = document_manager.get_stack_instances()
    return stack_instances


@router.post('')
async def post_stack_instance(
    background_tasks: BackgroundTasks,
    stack_instance_invocation: StackInstanceInvocation,
    document_manager: DocumentManager = Depends(get_document_manager),
    stack_manager: StackManager = Depends(get_stack_manager),
    redis=Depends(get_redis)):
    """Creates a stack instance with a specific name"""
    logger.info("[StackInstances POST] Received POST request")
    (stack_instance, return_result) = stack_manager.process_stack_request(
        stack_instance_invocation, "create")
    if stack_instance is None:
        return HTTPException(422, return_result)

    document_manager.write_stack_instance(stack_instance)
    # Perform invocations
    background_tasks.add_task(create_job_for_agent, stack_instance, "create",
                              redis)
    return return_result


@router.put('')
async def put_stack_instance(
    background_tasks: BackgroundTasks,
    stack_instance_update: StackInstanceUpdate,
    document_manager: DocumentManager = Depends(get_document_manager),
    stack_manager: StackManager = Depends(get_stack_manager),
    redis=Depends(get_redis)):
    """
    Updates a stack instance by using a StackInstanceUpdate object
    """
    logger.info("[StackInstances PUT] Received PUT request")
    to_be_deleted = stack_manager.check_delete_services(stack_instance_update)
    (stack_instance, return_result) = stack_manager.process_stack_request(
        stack_instance_update, "update")
    if stack_instance is None:
        return HTTPException(422, return_result)

    # Perform invocations
    if not stack_instance_update.disable_invocation:
        for service in to_be_deleted:
            background_tasks.add_task(create_job_per_service, service,
                                      document_manager, "delete", redis,
                                      stack_instance, to_be_deleted)
        copy_stack_instance = stack_instance.copy(deep=True)
        delete_services(to_be_deleted, copy_stack_instance)
        background_tasks.add_task(create_job_for_agent, copy_stack_instance,
                                  "update", redis)

    document_manager.write_stack_instance(stack_instance)

    return return_result


@router.delete('/{name}')
def delete_stack_instance(
    name: str,
    background_tasks: BackgroundTasks,
    force: bool = False,
    document_manager: DocumentManager = Depends(get_document_manager),
    redis=Depends(get_redis)):
    """Delete a stack instance with a specific name"""
    stack_instance = document_manager.get_stack_instance(name)
    if stack_instance is None:
        return {
            "result":
            f"Stack instance {name} can't be delete because it does not exist"
        }
    else:
        background_tasks.add_task(create_job_for_agent,
                                  stack_instance,
                                  "delete",
                                  document_manager,
                                  redis,
                                  force_delete=force)
        return {"result": f"Stack instance {name} is being deleted"}
