import os
import uuid
import shutil
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import Book, User, BookMode
from app import schemas, utils
from app.routers.auth import get_current_user

router = APIRouter(prefix="/books", tags=["Books"])

UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/", response_model=schemas.BookResponse)
async def create_book(
    title: str = Form(...),
    author: str = Form(...),
    description: str = Form(None),
    price: float = Form(0.0),
    contact_number: str = Form(None),
    mode: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    file_extension = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    if mode == BookMode.DONATE:
        price = 0.0
        
    address = utils.get_address_from_coords(latitude, longitude)
    
    new_book = Book(
        title=title,
        author=author,
        description=description,
        price=price,
        contact_number=contact_number,
        mode=mode,
        latitude=latitude,
        longitude=longitude,
        address_label=address,
        image_filename=filename,
        seller_id=current_user.id
    )
    
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    
    return new_book

@router.get("/", response_model=List[schemas.BookResponse])
async def get_books(
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None),
    mode: Optional[BookMode] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    query = select(Book).options(selectinload(Book.seller))
    
    if mode:
        query = query.where(Book.mode == mode)
    
    result = await db.execute(query)
    books = result.scalars().all()
    
    books_with_dist = []
    
    for book in books:
        book_dto = schemas.BookResponse.from_orm(book)
        
        if book.seller:
            book_dto.seller_name = book.seller.full_name or book.seller.email.split('@')[0]
            
        if lat is not None and lon is not None:
             dist = utils.calculate_distance(lat, lon, book.latitude, book.longitude)
             book_dto.distance_meters = dist
             
        books_with_dist.append(book_dto)
    
    # Sort listings by distance
    if lat is not None and lon is not None:
        books_with_dist.sort(key=lambda x: x.distance_meters if x.distance_meters is not None else float('inf'))
        
    return books_with_dist

@router.get("/my-listings", response_model=List[schemas.BookResponse])
async def get_my_books(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(Book).where(Book.seller_id == current_user.id).options(selectinload(Book.seller))
    result = await db.execute(query)
    books = result.scalars().all()
    
    books_dto = []
    for book in books:
        dto = schemas.BookResponse.from_orm(book)
        if book.seller:
            dto.seller_name = book.seller.full_name or book.seller.email.split('@')[0]
        books_dto.append(dto)
        
    return books_dto

@router.delete("/{book_id}", status_code=204)
async def delete_book(
    book_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalars().first()
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
        
    if book.seller_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this book")
        
    image_filename = book.image_filename

    await db.execute(delete(Book).where(Book.id == book_id))
    await db.commit()
    
    if image_filename:
        file_path = os.path.join(UPLOAD_DIR, image_filename)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass 
                
    return None