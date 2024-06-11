from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import Callable

from .auth import routes as auth
from .ping import routes as ping
from .quotes import routes as quotes
from .policies import routes as policy
from .KYC_Verification.GoK_KRA import routes as GoK


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next: Callable):
        response = await call_next(request)
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self'"
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Referrer-Policy'] = 'no-referrer'
        response.headers['Permissions-Policy'] = 'geolocation=(), microphone=()'
        return response


def create_application() -> FastAPI:
    fastapi_app = FastAPI()
    fastapi_app.include_router(ping.router, prefix="/ping", tags=["ping"])
    fastapi_app.include_router(auth.router, prefix="/auth", tags=["auth"])
    fastapi_app.include_router(quotes.router, prefix="/quotes", tags=["quotes"])
    fastapi_app.include_router(policy.router, prefix="/policy", tags=["policy"])
    fastapi_app.include_router(GoK.router, prefix="/GoK", tags=["KYC_Verification"])
    fastapi_app.include_router(risk.router, prefix="/smis", tags=["empty"])
    fastapi_app.include_router(cover.router, prefix="/cover", tags=["cover"])
    fastapi_app.include_router(charge.router, prefix="/charge", tags=["charge"])

    return fastapi_app


app = create_application()
app.add_middleware(SecurityHeadersMiddleware)
