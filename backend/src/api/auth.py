from fastapi import APIRouter, HTTPException, status

router = APIRouter()


@router.post("/register")
def register_user():
    """
    Deprecated: Use Better Auth frontend for registration.
    """
    raise HTTPException(
        status_code=status.HTTP_410_GONE,
        detail="Use Better Auth frontend for registration"
    )


@router.post("/login")
def login_user():
    """
    Deprecated: Use Better Auth frontend for login.
    """
    raise HTTPException(
        status_code=status.HTTP_410_GONE,
        detail="Use Better Auth frontend for login"
    )


@router.post("/logout")
def logout_user():
    """
    Deprecated: Use Better Auth frontend for logout.
    """
    return {"message": "Use Better Auth frontend for logout"}