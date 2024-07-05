from typing import Optional, Any
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Supabase client
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


async def verify_token(token: str) -> Optional[Any]:
    try:
        # Use Supabase to verify the token
        response = supabase.auth.get_user(token)
        return response.user.id if response.user else None
    except Exception as e:
        print(f"Error verifying token: {e}")
        return None


async def get_user_tier(user_id: str) -> int:
    print(user_id)
    response = supabase.table("profiles").select("tier").eq("id", user_id).execute()
    print(response.data)
    if response.data:
        return response.data[0]["tier"]
    return 0  # Default to the lowest tier if user not found
