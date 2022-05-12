from app import db
from app.models.book import Book
from flask import Blueprint, abort, jsonify, make_response, request  

books_bp = Blueprint("books", __name__, url_prefix="/books")


##### BOOK MODEL #####
@books_bp.route("", methods=["POST"])
def create_book():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return make_response("Invalid Request", 400)

    new_book = Book(title=request_body["title"],
                    description=request_body["description"])

    db.session.add(new_book)
    db.session.commit()

    return make_response(jsonify(f"Book {new_book.title} successfully created"), 201)


@books_bp.route("", methods=["GET"])
def read_all_books():
    title_query = request.args.get("title")

    if title_query is not None:
        books = Book.query.filter_by(title=title_query)
    else:
        books = Book.query.all()

    books_response = []
    for book in books:
        books_response.append(book.to_dict())
        # books_response.append({
        #     "id": book.id,
        #     "title": book.title,
        #     "description": book.description
        # })
    return jsonify(books_response)


# helper function:
def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        abort(make_response({"message":f"book {book_id} invalid"}, 400))

    book = Book.query.get(book_id)

    if not book:
        abort(make_response({"message":f"book {book_id} not found"}, 404))

    return book


@books_bp.route("/<book_id>", methods=["GET"])
def read_one_book(book_id):
    book = validate_book(book_id)
    return jsonify(book.to_dict())
    # return {
    #         "id": book.id,
    #         "title": book.title,
    #         "description": book.description
    #     }


@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    book = validate_book(book_id)

    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]

    db.session.commit()

    return make_response(jsonify(f"Book #{book_id} successfully updated"))


@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = validate_book(book_id)

    db.session.delete(book)
    db.session.commit()

    return make_response(jsonify(f"Book #{book.id} successfully deleted"))






# If POST and GET were to be in one function:
# @books_bp.route("", methods=["POST", "GET"])
# def handle_books():
#     if request.method == "POST":
#         request_body = request.get_json()
#         if "title" not in request_body or "description" not in request_body:
#             return make_response("Invalid Request", 400)
#         new_book = Book(title=request_body["title"],
#                         description=request_body["description"])
#         db.session.add(new_book)
#         db.session.commit()

#         return make_response(f"Book {new_book.title} successfully created", 201)

#     elif request.method == "GET":
#         books = Book.query.all()
#         books_response = []
#         for book in books:
#             books_response.append({
#                 "id": book.id,
#                 "title": book.title,
#                 "description": book.description
#             })
#         return jsonify(books_response)
# However it is good practice to limit 1 function per responsibility




# BELOW is code that contains examples for another blueprint: hello_world (disregard):
# hello_world_bp = Blueprint("hello_world", __name__)

# @hello_world_bp.route("/hello-world", methods=["GET"])
# def say_hello_world():
#     my_beautiful_response_body = "Hello, World!"
#     return my_beautiful_response_body, 200

# @hello_world_bp.route("/hello/JSON", methods=["GET"])
# def say_hello_json():
#     return {
#         "name": "Nishat",
#         "message": "Hello!",
#         "hobbies": ["hiking", "reading", "coding"]
#     }, 200

# @hello_world_bp.route("/broken-endpoint-with-broken-server-code")
# def broken_endpoint():
#     response_body = {
#         "name": "Ada Lovelace",
#         "message": "Hello!",
#         "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
#     }
#     new_hobby = "Surfing"
#     response_body["hobbies"].append(new_hobby)
#     return response_body




# Below is hardcoded data that we will not use for books
# class Book:
#     def __init__(self, id, title, description):
#         self.id = id
#         self.title = title
#         self.description = description

# books = [
#     Book(1, "Fictional Book Title", "A fantasy novel set in an imaginary world."),
#     Book(2, "Fictional Book Title", "A fantasy novel set in an imaginary world."),
#     Book(3, "Fictional Book Title", "A fantasy novel set in an imaginary world.")
# ] 

# books_bp = Blueprint("books", __name__, url_prefix="/books")

# @books_bp.route("", methods=["GET"])
# def handle_books():
#     books_response = []
#     for book in books:
#         books_response.append({
#             "id": book.id,
#             "title": book.title,
#             "description": book.description
#         })
#     return jsonify(books_response)

# Version 1 for this function definition handle_book(book_id):
#@books_bp.route("/<book_id>", methods=["GET"])
# def handle_book(book_id):
#     try:
#         book_id = int(book_id)
#     except:
#         return {"message":f"book {book_id} invalid"}, 400
#     for book in books:
#         if book.id == book_id:
#             return {
#                 "id": book.id,
#                 "title": book.title,
#                 "description": book.description
#             }
#     return {"message":f"book {book_id} not found"}, 404

# Version 2- Refactor handle_book(book_id) to include  a helper function to handle errors:
# @books_bp.route("/<book_id>", methods=["GET"])
# def handle_book(book_id):
#     book = validate_book(book_id)

#     return {
#         "id": book.id,
#         "title": book.title,
#         "description": book.description,
#     } 

# def validate_book(book_id):
#     try:
#         book_id = int(book_id)
#     except:
#         abort(make_response({"message":f"book {book_id} invalid"}, 400))

#     for book in books:
#         if book.id == book_id:
#             return book
#     abort(make_response({"message":f"book {book_id} not found"}, 404))