from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # principal = decode_jwt(request)
        # тут валидируем токен и сохраняем user_id в контекст
        user_id = 111
        # кладём только минимально нужное
        request.state.user_id = user_id
        return await call_next(request)
