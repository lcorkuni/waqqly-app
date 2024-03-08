#!/usr/bin/env python3

from http import HTTPStatus

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Wagg.ly", description="A dog walkers app", version="1.0")
templates = Jinja2Templates(directory="templates")
# Mount the static directory to serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("", include_in_schema=False, status_code=HTTPStatus.TEMPORARY_REDIRECT)
@app.get("/", include_in_schema=False, status_code=HTTPStatus.TEMPORARY_REDIRECT)
async def redirect_homepage():
    return RedirectResponse("/homepage")


@app.get("/homepage", response_class=HTMLResponse,
         status_code=HTTPStatus.OK,
         summary="Returns the Homepage Page HTML")
async def homepage(request: Request):
    return templates.TemplateResponse(name="homepage.html", context={"request": request, "message": "Hello from FastAPI with Jinja2"})


@app.get("/login", response_class=HTMLResponse,
         status_code=HTTPStatus.OK,
         summary="Returns the Login Page HTML")
async def login(request: Request):
    return templates.TemplateResponse(name="login.html", context={"request": request, "message": "Hello from FastAPI with Jinja2"})


@app.get("/register", response_class=HTMLResponse,
         status_code=HTTPStatus.OK,
         summary="Returns the Register Page HTML")
async def register(request: Request):
    return templates.TemplateResponse(name="register.html", context={"request": request, "message": "Hello from FastAPI with Jinja2"})


@app.get("/user-sign-up",
         status_code=HTTPStatus.OK,
         summary="Register Page")
async def user_sign_up(request: Request):
    return HTTPStatus.OK


@app.get("/sign-out",
         status_code=HTTPStatus.OK,
         summary="Register Page")
async def sign_out(request: Request):
    return HTTPStatus.OK


# Start the application
uvicorn.run(app, port=8888)