# Networks Lab 2 - REST API
This lab uses [`redis-python`](https://pypi.org/project/redis/) package as a database and contains `.http` unit test files to send HTTP requests.

## Setup
Ensure that docker is installed.

If using VSCode, install REST-Client extension. In each `.http` file, there will be a `Send Request` button at the top of each request file. Press the `Send Request` button to run each test files.

## Getting Started
1. Start running docker on your laptop.
2. Run the code using `docker-compose up`.

## Checkoff
Go to `checkoff` folder for all the `.http` unit test files. 

Go through each checkoff part in current order (i.e. from Part 0 to Part 9). Some parts may contain 2 tests to run to prove that the database has been successfully updated. 

### Part 0: Create and add some values into database
This will ease testing for the next few parts.
- Test file: `init_post_create_book1.http`, `init_post_create_book2.http`, `init_post_create_book3.http`
- Step: 
    1. Run the above three files individually once.
- Expected output for each `POST` request: `200 OK` A dictionary of the book created.

```
HTTP/1.1 200 OK
date: Thu, 07 Oct 2021 04:55:25 GMT
server: uvicorn
content-length: 89
content-type: application/json
connection: close

{
  "name": "The Lion, the Witch and the Wardrobe",
  "author": "C. S. Lewis",
  "id": 4,
  "ratings": 2
}
```

### Part 1: GET Request - with no query parameters
- Test file: `get_basic.http`
- Expected output: `200 OK` A list of dictionaries of Book
```
HTTP/1.1 200 OK
date: Thu, 07 Oct 2021 05:00:07 GMT
server: uvicorn
content-length: 252
content-type: application/json
connection: close

[
  {
    "name": "Charlie and the Chocolate Factory",
    "author": "Roald Dahl",
    "id": 3,
    "ratings": 5
  },
  {
    "name": "Alice in wonderland",
    "author": "Lewis Carroll",
    "id": 1,
    "ratings": 1
  },
  {
    "name": "The Lion, the Witch and the Wardrobe",
    "author": "C. S. Lewis",
    "id": 4,
    "ratings": 2
  }
]
```

### Part 2: GET Request - with a `sortBy` query parameter, to transform the order of the items returned
- Test file: `get_sortby.http`
- Expected output: `200 OK` A list of dictionaries of Book sorted by their ID. Notice that the order of the output dictionary is different from Part 1 indicating that it is sorted correctly.
```
HTTP/1.1 200 OK
date: Thu, 07 Oct 2021 05:01:07 GMT
server: uvicorn
content-length: 252
content-type: application/json
connection: close

[
  {
    "name": "Alice in wonderland",
    "author": "Lewis Carroll",
    "id": 1,
    "ratings": 1
  },
  {
    "name": "Charlie and the Chocolate Factory",
    "author": "Roald Dahl",
    "id": 3,
    "ratings": 5
  },
  {
    "name": "The Lion, the Witch and the Wardrobe",
    "author": "C. S. Lewis",
    "id": 4,
    "ratings": 2
  }
]
```

### Part 3: GET Request - with a `count` query parameter, to limit the number of items returned
- Test file: `get_count.http`
- Expected output: `200 OK` A list of dictionaries of Book. The number of books returned depends on the value of `count`. In this case, 2 out of 3 books are returned.
```
HTTP/1.1 200 OK
date: Thu, 07 Oct 2021 06:50:00 GMT
server: uvicorn
content-length: 162
content-type: application/json
connection: close

[
  {
    "name": "Charlie and the Chocolate Factory",
    "author": "Roald Dahl",
    "id": 3,
    "ratings": 5
  },
  {
    "name": "Alice in wonderland",
    "author": "Lewis Carroll",
    "id": 1,
    "ratings": 1
  }
]
```

### Part 4: GET Request - with a `offset` query parameter, to "skip" ahead by a number of items
- Test file: `get_limit.http`
- Expected output: `200 OK` A list of dictionaries of Book. The number of books returned depends on the value of `offset`. In this case, 2 books are skipped returning only 1 book.
```
HTTP/1.1 200 OK
date: Thu, 07 Oct 2021 05:07:30 GMT
server: uvicorn
content-length: 91
content-type: application/json
connection: close

[
  {
    "name": "The Lion, the Witch and the Wardrobe",
    "author": "C. S. Lewis",
    "id": 4,
    "ratings": 2
  }
]
```

### Part 5: GET Request - with a combination of `sortby` and `count` query parameters
- Test file: `get_sort_count.http`
- Expected output: `200 OK` A list of dictionaries of Book sorted by ID and the number of books returned depends on the value of `count`. In this case, where `sortby=id&count=2`, 2 out of 3 books are returned.
```
HTTP/1.1 200 OK
date: Thu, 07 Oct 2021 06:50:53 GMT
server: uvicorn
content-length: 162
content-type: application/json
connection: close

[
  {
    "name": "Alice in wonderland",
    "author": "Lewis Carroll",
    "id": 1,
    "ratings": 1
  },
  {
    "name": "Charlie and the Chocolate Factory",
    "author": "Roald Dahl",
    "id": 3,
    "ratings": 5
  }
]
```

### Part 6.1: POST Request - that creates a new resource with the given attributes in the body
- Test file: `post_create_book.http`
- Expected output: `200 OK` A dictionary of the book with ID:10 created.
```
HTTP/1.1 200 OK
date: Thu, 07 Oct 2021 06:54:37 GMT
server: uvicorn
content-length: 70
content-type: application/json
connection: close

{
  "name": "The Cat in the Hat",
  "author": "Dr. Seuss",
  "id": 10,
  "ratings": 5
}
```

### Part 6.2: POST Request - show that the resource has indeed been created through another HTTP request
- Test file: `post_get_book.http`
- How it works: Find a book via it's ID.
- Expected output: `200 OK` Shows the newly created book with ID:10.
```
HTTP/1.1 200 OK
date: Thu, 07 Oct 2021 07:17:47 GMT
server: uvicorn
content-length: 70
content-type: application/json
connection: close

{
  "name": "The Cat in the Hat",
  "author": "Dr. Seuss",
  "id": 10,
  "ratings": 5
}
```

### Part 7.1: DELETE Request - deletes a _single_ resource
- Test file: `delete_book.http`
- How it works: Delete a book via it's ID.
- Expected output: `200 OK` with "Sucessful. Deleted book with id:10" response message.
```
HTTP/1.1 200 OK
date: Thu, 07 Oct 2021 07:27:45 GMT
server: uvicorn
content-length: 36
content-type: application/json
connection: close

"Sucessful. Deleted book with id:10"
```

### Part 7.2: show that the resource has indeed been modified through another HTTP request = has validation and returns an appropiate HTTP response code if the input data is invalid 
#### Test part 1
- Test file: `post_get_book.http`
- How it works: Find a book via it's ID.
- Expected output: `404 Not Found` indicating that the book with ID:10 has been deleted and can no longer be found in the database.
```
HTTP/1.1 404 Not Found
date: Thu, 07 Oct 2021 07:30:59 GMT
server: uvicorn
content-length: 32
content-type: application/json
connection: close

"Book doesn't exist in library."
```
#### Test part 2
- Test file: `get_basic.http`
- How it works: Returns the list of Book in database.
- Expected output: `200 OK` A list of dictionaries of Book. Notice that book with ID:10 is no longer in the database.
```
HTTP/1.1 200 OK
date: Thu, 07 Oct 2021 07:35:29 GMT
server: uvicorn
content-length: 252
content-type: application/json
connection: close

[
  {
    "name": "Charlie and the Chocolate Factory",
    "author": "Roald Dahl",
    "id": 3,
    "ratings": 5
  },
  {
    "name": "Alice in wonderland",
    "author": "Lewis Carroll",
    "id": 1,
    "ratings": 1
  },
  {
    "name": "The Lion, the Witch and the Wardrobe",
    "author": "C. S. Lewis",
    "id": 4,
    "ratings": 2
  }
]
```

### Part 8: Challenge 1 - File upload in a POST request, using multipart/form-data
- Test file: `post_upload_file.http`
- How it works: Upload a image called `winnie.png`. If image already exists in `/app/` folder, there will be `409` error message.
- Expected output: `200 OK` Uploaded image will be saved into `/app/` folder.
```
HTTP/1.1 200 OK
date: Thu, 07 Oct 2021 07:43:54 GMT
server: uvicorn
content-length: 63
content-type: application/json
connection: close

"File winnie.png uploaded successfully at /app/winnie.png path"
```

### Part 9: Challenge 2 - A special route that can perform a batch delete of resources matching a certain condition
#### Test part 1
- Test file: `delete_batchdelete.http`
- How it works: Delete books with rating less than equal to specified rating in DELETE request query parameter. 
- Expected output: `200 OK` A list of deleted books.
```
HTTP/1.1 200 OK
date: Thu, 07 Oct 2021 07:52:41 GMT
server: uvicorn
content-length: 138
content-type: application/json
connection: close

[
  "Deleted book id: 1, name: Alice in wonderland, ratings: 1",
  "Deleted book id: 4, name: The Lion, the Witch and the Wardrobe, ratings: 2"
]
```
#### Test part 2
- Test file: `get_basic.http`
- How it works: Returns the list of Book in database.
- Expected output: `200 OK` A list of dictionaries of Book. Notice that book with ID:1 and ID:4 are no longer in the database.
```
HTTP/1.1 200 OK
date: Thu, 07 Oct 2021 07:54:50 GMT
server: uvicorn
content-length: 87
content-type: application/json
connection: close

[
  {
    "name": "Charlie and the Chocolate Factory",
    "author": "Roald Dahl",
    "id": 3,
    "ratings": 5
  }
]
```


## References
- [Redis python documentation](https://redis-py.readthedocs.io/en/stable/)