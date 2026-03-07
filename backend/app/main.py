"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.config import settings
from app.database.connection import init_db, close_db
from app.api.routes import leads, calls, appointments, webhooks


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    # Startup
    try:
        await init_db()
    except Exception as e:
        print(f"⚠ Database initialization failed: {str(e)}")
        print("  Application will continue, but database features may not work.")
    yield
    # Shutdown
    try:
        await close_db()
    except Exception:
        pass  # Ignore errors on shutdown


app = FastAPI(
    title="AI Voice Bots API",
    description="API for managing AI voice bots, leads, calls, and appointments",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(leads.router, prefix=settings.API_V1_PREFIX, tags=["leads"])
app.include_router(calls.router, prefix=settings.API_V1_PREFIX, tags=["calls"])
app.include_router(appointments.router, prefix=settings.API_V1_PREFIX, tags=["appointments"])
app.include_router(webhooks.router, prefix=settings.API_V1_PREFIX, tags=["webhooks"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AI Voice Bots API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

