from functools import lru_cache
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from .routes import sql, users, login
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from .config import settings
from fastapi.responses import RedirectResponse


app = FastAPI()


@app.get("/")
def move_to_docs():
    return RedirectResponse("http://127.0.0.1:8000/docs")


@app.get("/hello")
def read_main():
    return "Hello"


app.include_router(users.router)
app.include_router(sql.router)
app.include_router(login.router)


app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/hello/{name}", response_class=HTMLResponse)
async def read_item(request: Request, name: str):
    return templates.TemplateResponse("hello.html", {"request": request, "name": name})