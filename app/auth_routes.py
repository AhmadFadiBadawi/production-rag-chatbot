from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import (
    authenticate_user,
    create_access_token,
    create_user,
)

from app.models import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register")
def register(request: RegisterRequest):

    try:
        create_user(
            request.username,
            request.password,
        )
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Username already exists",
        )

    return {
        "message": "User created successfully"
    }


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(request: LoginRequest):

    user = authenticate_user(
        request.username,
        request.password,
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    token = create_access_token(request.username)

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.post(
    "/token",
    response_model=TokenResponse,
)
def token(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    user = authenticate_user(
        form_data.username,
        form_data.password,
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    access_token = create_access_token(
        form_data.username
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }