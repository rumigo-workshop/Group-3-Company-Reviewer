from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Library Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary database
books = {}
next_id = 1


class Book(BaseModel):
    title: str
    author: str
    genre: str
    year: int


# GET: Get all books
@app.get("/books")
def get_books():
    return list(books.values())


# GET: Get a particular book
@app.get("/books/{book_id}")
def get_book(book_id: int):
    if book_id not in books:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return books[book_id]


# POST: Add a new book
@app.post("/books", status_code=201)
def add_book(book: Book):
    global next_id

    new_book = {
        "id": next_id,
        **book.model_dump()
    }

    books[next_id] = new_book
    next_id += 1

    return new_book


# PUT: Update book details
@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    if book_id not in books:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    updated_book = {
        "id": book_id,
        **book.model_dump()
    }

    books[book_id] = updated_book

    return updated_book


# DELETE: Remove a book
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    if book_id not in books:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    deleted_book = books.pop(book_id)

    return {
        "message": "Book deleted successfully",
        "book": deleted_book
    }