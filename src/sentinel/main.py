"""Main FastAPI application for Sentinel"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from sentinel.api import health, test_runs, webhooks
from sentinel.core.config import settings
from sentinel.core.logging import configure_logging, get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("Starting Sentinel application")
    configure_logging(debug=settings.DEBUG)
    
    # Initialize services
    # TODO: Initialize database, redis, etc.
    
    yield
    
    # Cleanup
    logger.info("Shutting down Sentinel application")


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title="Sentinel - AI-Driven Testing Platform",
        description="Test Orchestrator service for automated test generation and execution",
        version="0.1.0",
        lifespan=lifespan,
        docs_url=f"{settings.API_PREFIX}/docs",
        redoc_url=f"{settings.API_PREFIX}/redoc",
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(health.router, prefix=settings.API_PREFIX, tags=["health"])
    app.include_router(test_runs.router, prefix=settings.API_PREFIX, tags=["test-runs"])
    app.include_router(webhooks.router, prefix=settings.API_PREFIX, tags=["webhooks"])
    
    # Instrument with OpenTelemetry
    FastAPIInstrumentor.instrument_app(app)
    
    return app


app = create_app()