from fastapi import FastAPI
from fastapi.responses import JSONResponse

from apps.health.routes import router as health_router
from apps.tasks.routes import router as tasks_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Taskion - To-Do API",
        description="A simple FastAPI application for managing tasks",
        version="1.0.0",
    )

    # Include routers
    app.include_router(health_router)
    app.include_router(tasks_router)

    # Global exception handler for consistent error responses
    @app.exception_handler(ValueError)
    async def value_error_handler(request, exc):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    return app


app = create_app()
