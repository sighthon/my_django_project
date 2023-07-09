from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator


books_content = [
    {
        "id": 1,
        "title": "Book 1",
        "author": "Author 1"
    },
    {
        "id": 2,
        "title": "Book 2",
        "author": "Author 2"
    }
]

# This should be a get function in class based view.


def my_view(request: HttpRequest, **kwargs: dict):
    # you got a (GET) request from frontend
    # TODO: you make a database call to get the details

    # prepare a webpage (html) with dynamic content from DB/memory
    html_content = "<html><body>"
    for content in books_content:
        html_content += "<p>" + str(content) + "</p>"
    html_content += "</body></html>"
    # return that web page as a response

    return HttpResponse(html_content)


# class based views
@method_decorator(csrf_exempt, name='dispatch')
class ListBooks(View):
    def http_method_not_allowed(self, request: HttpRequest, **kwargs: dict):
        return HttpResponseNotAllowed("Allowed methods are : ['GET', 'POST']")

    def get(self, request: HttpRequest, **kwargs: dict):
        # TODO: ideally the list of books should be fetched from database.
        return HttpResponse(books_content)

    def post(self, request: HttpRequest, **kwargs: dict):
        book_data = request.POST  # fetch the form data from the request
        if not validate(book_data):
            return HttpResponseBadRequest(f"The POST data {book_data} is invalid")

        # TODO: ideally add the book to the database.
        # add the book to list of books
        title = book_data.get("title", "")
        author = book_data.get("author", "")
        books_content.append({
            "title": title,
            "author": author
        })
        return HttpResponse(books_content)


# function based views

def validate(book_data: dict) -> bool:
    # TODO: do the validation
    return True


def delete_book(book_data: dict) -> None:
    global books_content
    updated_book_content = []
    print(book_data.get("title"))
    for item in books_content:
        if item.get("title") == book_data.get("title"):
            continue
        updated_book_content.append(item)
    books_content = updated_book_content


@csrf_exempt
def list_books(request: HttpRequest, **kwargs: dict):
    if request.method == "GET":
        # TODO: ideally the list of books should be fetched from database.
        return HttpResponse(books_content)
    elif request.method == "POST":
        book_data = request.POST  # fetch the form data from the request
        if not validate(book_data):
            return HttpResponseBadRequest(f"The POST data {book_data} is invalid")

        # TODO: ideally add the book to the database.
        # add the book to list of books
        title = book_data.get("title", "")
        author = book_data.get("author", "")
        books_content.append({
            "title": title,
            "author": author
        })
        return HttpResponse(books_content)
    elif request.method == "DELETE":
        book_data = request.GET  # fetch the form data from the request
        print(book_data)
        # TODO: add data validation
        delete_book(book_data)
        return HttpResponse(books_content)

    return HttpResponseNotFound(f"Type {request.method} not supported")


@csrf_exempt
def book(request: HttpRequest, id: int, **kwargs: dict):
    print(request.method)
    if request.method == "GET":
        for idx, item in enumerate(books_content):
            if item.get("id", 0) == id:
                # TODO: why this has to be a list?
                return HttpResponse([item])
    elif request.method == "DELETE":
        pass

    return HttpResponseNotFound(f"Type {request.method} not supported")


@csrf_exempt
def dummy_view(request: HttpRequest):
    return HttpResponse("No API handling")
