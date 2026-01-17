from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from app.routers import auth, books
from starlette.concurrency import run_in_threadpool
from app.database import engine, Base
import contextlib
from app.ai import generate_summary
@contextlib.asynccontextmanager

async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Book Thrift", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth.router)
app.include_router(books.router)

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/browse", response_class=HTMLResponse)
async def browse_page(request: Request):
    return templates.TemplateResponse("browse.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

from app.database import get_db
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models import Book


@app.get("/view-book/{book_id}", response_class=HTMLResponse)
async def view_book_page(book_id: int, request: Request, db=Depends(get_db)):
    result = await db.execute(
        select(Book).where(Book.id == book_id).options(selectinload(Book.seller))
    )
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return templates.TemplateResponse("book_detail.html", {"request": request, "book": book})

@app.get("/my-books", response_class=HTMLResponse)
async def my_books_page(request: Request):
    return templates.TemplateResponse("my_books.html", {"request": request})

@app.get("/me", response_class=HTMLResponse)
async def me_page(request: Request):
    return templates.TemplateResponse("me.html", {"request": request})

@app.get("/ai/summary/{book_id}")
async def ai_summary(book_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalars().first()
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if not book.ai_summary:
        summary = await run_in_threadpool(generate_summary, book.title, book.description,book.author)
        book.ai_summary = summary
        await db.commit()
        await db.refresh(book)
    
    return JSONResponse(content={"summary": book.ai_summary})
