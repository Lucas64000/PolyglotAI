from fastapi import FastAPI
from src.core.exceptions import (
    ResourceNotFoundError, ResourceAlreadyExistsError,
    ConversationNotWritableError, InvalidConversationStateError,
    BusinessRuleViolation, TeacherResponseError, 
    DomainException, InfrastructureError
)

from .handlers import (
    resource_not_found_handler, resource_conflict_handler,
    state_conflict_handler, business_rule_handler,
    teacher_unavailable_handler, global_domain_handler,
    global_infrastructure_handler
)

def configure_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ResourceNotFoundError, resource_not_found_handler)
    app.add_exception_handler(ResourceAlreadyExistsError, resource_conflict_handler)
    app.add_exception_handler(TeacherResponseError, teacher_unavailable_handler)
    app.add_exception_handler(ConversationNotWritableError, state_conflict_handler)
    app.add_exception_handler(InvalidConversationStateError, state_conflict_handler)
    app.add_exception_handler(BusinessRuleViolation, business_rule_handler)
    app.add_exception_handler(DomainException, global_domain_handler)
    app.add_exception_handler(InfrastructureError, global_infrastructure_handler)
