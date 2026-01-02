"""
PolyglotAI Application Entry Point

Main entry point for the FastAPI application.
Configures routes, exception handlers, and starts the server.
"""

from fastapi import FastAPI

from src.infrastructure.adapters.driving.fastapi.routers.conversations import router as conversations_router
from src.infrastructure.adapters.driving.fastapi.routers.messages import router as messages_router
from src.infrastructure.adapters.driving.fastapi.exceptions import configure_exception_handlers

app = FastAPI()

# Configure global exception handlers
configure_exception_handlers(app)

# Register API routers
app.include_router(conversations_router, prefix="/api", tags=["Conversations"])
app.include_router(messages_router, prefix="/api", tags=["Messages"])


@app.get("/health", tags=["Health"], summary="Health check endpoint")
def health_check() -> dict[str, str]:
    """
    Health check endpoint for monitoring and deployment verification.
    
    Returns:
        Status dictionary indicating service health
    """
    return {"status": "ok"}