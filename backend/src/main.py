"""Main FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.documents import router as documents_router
from .api.auth import router as auth_router
from .api.trials import router as trials_router
from .api.matching import router as matching_router

app = FastAPI(
    title="Clinical Trial Matcher API",
    description="AI-powered platform for matching patients with clinical trials",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(documents_router, prefix="/api/v1")
app.include_router(trials_router, prefix="/api/v1")
app.include_router(matching_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Clinical Trial Matcher API", "status": "healthy"}


@app.get("/health")
async def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "version": "0.1.0",
    }
