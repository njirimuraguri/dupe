# Endpoint for logging in and obtaining an access token
@router.post("/login_to_get_access_tokens", response_model=LoginResponse)
async def login(login_request: LoginRequest):
    token = await get_authorization_token(login_request)  # Get the auth token using the login request
    response_data = {
        "token": token,
        "time_to_live": "1440",
        "user_id": login_request.user_id
    }