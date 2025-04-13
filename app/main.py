from fastapi import FastAPI, Request
from starlette.middleware import Middleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.utils.exceptions import CustomHTTPException
from app.api.v1.api import router as api_router
from app.core.config import settings

middleware_stack = [
    Middleware(TrustedHostMiddleware, allowed_hosts=["quo-belvo-backend.fly.dev", "*.fly.dev"])
]

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Quo API",
    debug=settings.DEBUG,
    docs_url=None if settings.ENV == "production" else "/docs",
    redoc_url=None,
    middleware=middleware_stack,
    trust_forwarded=True
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://quo-belvo-frontend.vercel.app",
        "https://*.quo-belvo-frontend.vercel.app"
    ] if settings.ENV == "production" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

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