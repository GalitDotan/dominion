from datetime import timedelta

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app import app
from app_utils.app_utils import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from app_utils.db.users import authenticate_user, get_user
from app_utils.models.app_models import Token, User


# Token endpoint
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Protected endpoint example
@app.get("/game")
async def play_game(current_user: User = Depends(get_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    return {"message": f"Welcome to the game, {current_user.username}!"}
