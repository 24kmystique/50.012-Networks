from fastapi import FastAPI, Response, Depends, UploadFile, File
from typing import Optional
from pydantic import BaseModel
import redis
import pickle
import base64

app = FastAPI()


def get_redis_client():
    return redis.Redis(host="redis")

class Book(BaseModel):
    name: str
    author: str
    id: int
    ratings: int

class GetBook(BaseModel):
    action: str
    id: int

@app.get("/home")
def get_all_books(sortby: Optional[str] = None, count: Optional[int] = None, redis_client: redis.Redis = Depends(get_redis_client)):
    book_list_bytes = redis_client.hgetall("books")
    if book_list_bytes:
        book_list = []
        for i in book_list_bytes:
            book = pickle.loads(book_list_bytes[i])
            book_list.append(book)
        if not sortby and not count:
            return book_list
        if (sortby == 'id') and (not count):
            sorted_list = sorted(book_list, key=lambda book: book.id)
            return sorted_list
        elif (sortby != id) and (not count):
            return "Not a valid sortby parameter."
        elif (not sortby) and (count > 0):
            return book_list[:count]
        elif (not sortby) and (count <= 0):
            return "Not a valid count parameter."
        elif (sortby=='id') and (count>0):
            sorted_list = sorted(book_list, key=lambda book: book.id)
            return sorted_list[:count]
        else:
            "Invalid parameter."
    return "No books in library."

@app.get("/home/books")
def get_books_offset(offset: Optional[int] = None, redis_client: redis.Redis = Depends(get_redis_client)):
    book_list_bytes = redis_client.hgetall("books")
    if book_list_bytes:
        book_list = []
        for i in book_list_bytes:
            book = pickle.loads(book_list_bytes[i])
            book_list.append(book)
        if offset == len(book_list):
            return "Skipped all books in library."
        elif 0 < offset < len(book_list):
            return book_list[offset:]
        elif offset:
            return "Not valid offset parameter."
    return "No books in library."

@app.post("/home/books")
def create_book(book: Book, response: Response, redis_client: redis.Redis = Depends(get_redis_client)):
    if not (redis_client.hexists("books", book.id)):
        redis_client.hset("books", book.id, pickle.dumps(book))
        return book
    response.status_code = 409
    return "Book already exists in library."

@app.post("/home/findbook")
def find_book(requirement: GetBook, response: Response, redis_client: redis.Redis = Depends(get_redis_client)):
    if requirement.action=="find":
        if (redis_client.hexists("books", requirement.id)):
            return pickle.loads(redis_client.hget("books", requirement.id))
        response.status_code = 404
        return "Book doesn't exist in library."
    response.status_code = 400
    return "Invalid action."

@app.delete("/home/{id}")
def delete_book(id: int, response: Response, redis_client: redis.Redis = Depends(get_redis_client)):
    book_list_bytes = redis_client.hgetall("books")
    if book_list_bytes:
        book_list = []
        for i in book_list_bytes:
            book = pickle.loads(book_list_bytes[i])
            book_list.append(book)
        for i in book_list:
            if i.id == id:
                redis_client.hdel("books", id)
                return "Sucessful. Deleted book with id:%d" %id
        response.status_code = 404
        return "Not a valid id"
    response.status_code = 404
    return "No books in library."

@app.delete("/home")
def delete_books(ratings: float, response: Response, redis_client: redis.Redis = Depends(get_redis_client)):
    if ratings is not None:
        val = ratings
        book_list_bytes = redis_client.hgetall("books")
        if val > 5 or val < 0:
            response.status_code = 406
            return "Invalid rating range."
        if book_list_bytes:
            book_list = []
            deleted_books_list = []
            for i in book_list_bytes:
                book = pickle.loads(book_list_bytes[i])
                book_list.append(book)
            for bk in book_list:
                if bk.ratings <= val:
                    redis_client.hdel("books", bk.id)
                    deleted_books_list.append(bk)
            if deleted_books_list:
                return ("Deleted book id: %d, name: %s, ratings: %d" %(bk.id, bk.name, bk.ratings) for bk in deleted_books_list)
            else: 
                return "No books with ratings less than or equal to %.2f" %val
        response.status_code = 404
        return "No books in library."
    response.status_code = 400
    return "Invalid action."

@app.post("/home/uploadfile")
async def form_post(response: Response, file: UploadFile = File(...), redis_client: redis.Redis = Depends(get_redis_client)):
    contents = await file.read()
    
    if redis_client.hexists("images", file.filename):
        response.status_code = 409
        return "File already exists in database. Can be found at /app/%s path. Note: " %(file.filename)
    else:
        redis_client.hset("images", file.filename, pickle.dumps(contents))
        with open(file.filename, "wb") as f:
            f.write(base64.b64decode(contents))
        return "File %s uploaded successfully at /app/%s path" %(file.filename, file.filename)
