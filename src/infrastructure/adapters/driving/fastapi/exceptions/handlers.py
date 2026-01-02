
from http import HTTPStatus
from fastapi import Request
from fastapi.responses import JSONResponse

def _create_problem_details(
    status_code: int,
    type_uri: str,
    title: str,
    detail: str,
    instance: str
) -> JSONResponse:
    """
    Constructs RFC 7807 compliant error response.
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "type": type_uri,
            "title": title,
            "status": status_code,
            "detail": detail,
            "instance": instance
        }
    )

async def resource_not_found_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handles 404 for missing resources.
    """
    return _create_problem_details(
        status_code=HTTPStatus.NOT_FOUND,
        type_uri="error:resource-not-found",
        title="Resource Not Found",
        detail=str(exc),
        instance=str(request.url)
    )

async def resource_conflict_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handles 409 for duplicate resources.
    """
    return _create_problem_details(
        status_code=HTTPStatus.CONFLICT,
        type_uri="error:resource-conflict",
        title="Resource Already Exists",
        detail=str(exc),
        instance=str(request.url)
    )

async def state_conflict_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handles 409 when resource state prevents the action.
    """
    return _create_problem_details(
        status_code=HTTPStatus.CONFLICT,
        type_uri="error:state-conflict",
        title="Operation Denied by State",
        detail=str(exc),
        instance=str(request.url)
    )

async def business_rule_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handles 400 for business rule violations.
    """
    return _create_problem_details(
        status_code=HTTPStatus.BAD_REQUEST,
        type_uri="error:business-rule-violation",
        title="Business Rule Violation",
        detail=str(exc),
        instance=str(request.url)
    )

async def teacher_unavailable_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handles 503 when LLM service is unavailable.
    """
    return _create_problem_details(
        status_code=HTTPStatus.SERVICE_UNAVAILABLE,
        type_uri="error:teacher-service-unavailable",
        title="Teacher Service Unavailable",
        detail=str(exc),
        instance=str(request.url)
    )

async def global_domain_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Fallback handler for domain exceptions (400).
    """
    return _create_problem_details(
        status_code=HTTPStatus.BAD_REQUEST,
        type_uri="error:domain-error",
        title="Domain Error",
        detail=str(exc),
        instance=str(request.url)
    )

async def global_infrastructure_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Fallback handler for infrastructure errors (500).
    """
    return _create_problem_details(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        type_uri="error:internal-server-error",
        title="Internal Infrastructure Error",
        detail="An internal error occurred in the infrastructure layer.",
        instance=str(request.url)
    )