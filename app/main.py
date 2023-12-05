from dotenv import load_dotenv
from fastapi.responses import PlainTextResponse

load_dotenv()

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine, get_db
from .utils.rate_limit import limiter
from app.routers import email, auth, category


from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

from fastapi.staticfiles import StaticFiles

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/images", StaticFiles(directory="images"), name="images")

origins = [
    "https://localhost:3000",
    "http://localhost:3000",
    "https://congruence.onrender.com",
    "https://congruence.178765.xyz",
    "https://www.congruencemarketinsights.com",
    "https://marketresearch-production-6eeb.up.railway.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"greeting": "Hello!", "message": "This api works!"}


app.include_router(category.router, prefix="/category", tags=["Category"])

app.include_router(auth.router, tags=["Auth"])
app.include_router(email.router, tags=["Email"])
