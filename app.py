#!/usr/bin/env python3

import uvicorn

from typing import Optional
from pathlib import Path
from http import HTTPStatus
from typing import Annotated
from datetime import timedelta

from fastapi import FastAPI, HTTPException, Request, Response, Cookie, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from starlette.datastructures import MutableHeaders

from app_utils import logging, UserType, User, get_password_hash, get_current_user, authenticate_user, \
    create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, fake_users_db


app = FastAPI(title="Wagg.ly", description="A dog walkers app", version="1.0")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory=Path(__file__).parent.absolute() /
          "static"), name="static")


@app.middleware("http")
async def authorization_middleware(request: Request, call_next):
    """
    Adds an access token to the "Authorization" header and required auth for docs
    """
    access_token = request.cookies.get("access_token")

    # Add Authorization to header from cookie
    if access_token and "Authorization" not in request.headers.keys():
        new_header = MutableHeaders(request._headers)
        new_header["Authorization"] = f"Bearer {access_token}"
        request._headers = new_header
        request.scope.update(headers=request.headers.raw)

    # Docs authorization
    try:
        if "/docs" in request.url.path:
            if access_token is None:
                return JSONResponse(
                    content={"details": "UNAUTHORIZED: No account is logged in"}, status_code=HTTPStatus.UNAUTHORIZED)
            current_user = await get_current_user(access_token)
            if current_user.type != UserType.admin:
                return JSONResponse(
                    content={"details": "UNAUTHORIZED: User is not admin"}, status_code=HTTPStatus.UNAUTHORIZED)
    except HTTPException:
        return JSONResponse(
            content={"details": "UNAUTHORIZED: Could not validate credentials"}, status_code=HTTPStatus.UNAUTHORIZED)

    response = await call_next(request)
    return response


# @app.middleware("http")
# async def unauthorized_page(request: Request, call_next):
#     response = await call_next(request)
#     if response.status_code == HTTPStatus.UNAUTHORIZED:
#         return templates.TemplateResponse(name="unauthorized.html", context={"details": response.details})


@app.get("", include_in_schema=False, status_code=HTTPStatus.TEMPORARY_REDIRECT)
@app.get("/", include_in_schema=False, status_code=HTTPStatus.TEMPORARY_REDIRECT)
async def redirect_homepage():
    return RedirectResponse("/login")


@app.get("/login", response_class=HTMLResponse,
         status_code=HTTPStatus.OK,
         summary="Returns the Login Page HTML", tags=["Frontend"])
async def login(request: Request):
    return templates.TemplateResponse(name="login.html", context={"request": request})


@app.get("/register", response_class=HTMLResponse,
         status_code=HTTPStatus.OK,
         summary="Returns the Register Page HTML", tags=["Frontend"])
async def register(request: Request):
    return templates.TemplateResponse(name="register.html", context={"request": request})


@app.get("/home", response_class=HTMLResponse,
         status_code=HTTPStatus.OK,
         summary="Returns the Homepage Page HTML", tags=["Frontend"])
async def homepage(request: Request, current_user: Annotated[User, Depends(get_current_user)]):
    return templates.TemplateResponse(name="homepage.html", context={"request": request})


@app.post("/token", tags=["Backend"], response_class=JSONResponse)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> JSONResponse:
    user = authenticate_user(
        fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    # Create a cookie for the token
    response = JSONResponse(content=access_token)
    response.set_cookie(key="access_token", value=access_token, secure=True)
    return response


@app.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Cookies cleared, successfully logged out."}


@app.get("/get_cookie", response_class=JSONResponse)
async def get_cookies(access_token: Optional[str] = Cookie(None)):
    try:
        return {"access_token": access_token}
    except Exception:
        raise HTTPException("No cookie found", status_code=HTTPStatus.BAD_REQUEST)


@app.get("/users/me/", response_model=User, tags=["Backend"])
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user


@app.get("/users/me/items/", tags=["Backend"])
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]


@app.get("/password-hash", tags=["Debug"])
async def password_hash(password: str):
    return get_password_hash(password)


@app.get("/user-sign-up",
         status_code=HTTPStatus.OK,
         summary="Register Page")
async def user_sign_up():
    return HTTPStatus.OK


@app.get("/sign-out",
         status_code=HTTPStatus.OK,
         summary="Register Page")
async def sign_out():
    return HTTPStatus.OK


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    uvicorn.run("app:app", port=8000, log_level="info", reload=True)
