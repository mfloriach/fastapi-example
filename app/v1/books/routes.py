
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session

from .models import Book, BookCreate, BookUpdate

router = APIRouter(
    prefix="/api/v1",
    tags=["books"]
)

@router.get("/", response_model=list[Book])
async def get_books(
    skip: Annotated[Optional[int], Query(gt=-1, lt=100)] = 0,
    limit: Annotated[Optional[int], Query(gt=0, lt=100)] = 10,
    request: Request = None,
    session: AsyncSession = Depends(get_session)):
    books = (await session.execute(select(Book).offset(skip).limit(limit))).scalars().all()
    return books

@router.get("/{book_id}", response_model=Book)
async def get_book(
    book_id: Annotated[int, Path(gt=0)],
    request: Request,
    session: AsyncSession = Depends(get_session)):
    book = await session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail='Book not found')
    
    return book

@router.post("/", response_model=Book, status_code=201)
async def create_book(book: BookCreate, request: Request, session: AsyncSession = Depends(get_session)):
    db_book = Book.model_validate(book)
    session.add(db_book)

    print(request.state._state.get("user_id"))

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Books isbn is must be unique")
    
    await session.refresh(db_book)
    
    return db_book

@router.delete("/{book_id}", status_code=204)
async def delete_book(
    book_id: Annotated[int, Path(gt=0)],
    request: Request,
    session: AsyncSession = Depends(get_session)):
    db_book = await session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail='Book not found')
    
    await session.delete(db_book)
    await session.commit()
    
    return None

@router.put("/{book_id}", response_model=Book)
async def update_book(
    book_id: Annotated[int, Path(gt=0)],
    book: BookUpdate,
    request: Request,
    session: AsyncSession = Depends(get_session)):
    db_book = await session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail='Book not found')
    
    book_data = book.model_dump(exclude_unset=True)
    db_book.sqlmodel_update(book_data)
    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)

    return db_book