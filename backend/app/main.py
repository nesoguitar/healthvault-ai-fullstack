"""
HealthVault AI — FastAPI application entrypoint.
"""
import time
import uuid

import structlog
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.api import api_router
from app.core.config import settings

logger = structlog.get_logger()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0",
    description=(
        "API for HealthVault AI — an AI-powered Personal Health Record system. "
        "All PHI-bearing endpoints require authentication and are scoped to the "
        "authenticated user's own patient record."
    ),
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_security_headers_and_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start = time.time()

    response = await call_next(request)

    response.headers["X-Request-ID"] = request_id
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["X-Frame-Options"] = "DENY"

    duration_ms = round((time.time() - start) * 1000, 2)
    logger.info(
        "request",
        request_id=request_id,
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration_ms=duration_ms,
    )
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Validation failed", "errors": exc.errors()},
    )


# ✅ Include your API routers
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok", "environment": settings.ENVIRONMENT}


@app.get("/", tags=["System"])
def root():
    return {
        "service": settings.PROJECT_NAME,
        "docs": f"{settings.API_V1_PREFIX}/docs" if settings.DEBUG else "disabled in this environment",
    }
