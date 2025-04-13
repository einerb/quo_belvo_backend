from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.middleware.cors import CORSMiddleware

from app.utils.exceptions import CustomHTTPException
from app.api.v1.api import router as api_router
from app.core.config import settings

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Quo API",
    debug=settings.DEBUG,
    docs_url=None if settings.ENV == "production" else "/docs",
    redoc_url=None
)

app.state.limiter = limiter

app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600
)

@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "https://quo-belvo-frontend.vercel.app"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return CustomHTTPException("Rate limit exceeded", status_code=429).to_response()

@app.exception_handler(CustomHTTPException)
async def custom_http_exception_handler(request: Request, exc: CustomHTTPException):
    return exc.to_response()

app.include_router(api_router, prefix="/api")

@app.get("/health")
@limiter.limit("5/minute")
async def health_check(request: Request):
    return {
        "status": "ok",
        "environment": settings.ENV,
        "db_connected": True
    }