from fastapi.security import HTTPBearer

security = HTTPBearer(auto_error=False)
admin_tier = 2
auth_type = 'supabase'


async def verify_and_get_user_tier(token) -> int:
    if token is None:
        return 0
    if auth_type == 'supabase':
        from app.utils.auth.auth_supabase import verify_token, get_user_tier
        user_id = await verify_token(token.credentials)
        if user_id:
            return await get_user_tier(user_id)
        return 0  # Default tier for unauthenticated users
    else:
        print('Please use supabase, other db backends are being developed')
        return 0


async def verify_jwt(token: str) -> bool:
    if token is None:
        return False
