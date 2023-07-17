from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
from django.template import loader
from django.template.loader import render_to_string
from django.shortcuts import render
from datetime import datetime
from django.views.generic.base import TemplateView
from django.views.decorators.http import require_http_methods
from .models import Person


@method_decorator(csrf_exempt, name='dispatch')
class Details(View):
    def http_method_not_allowed(self, request: HttpRequest, **kwargs: dict):
        return HttpResponseNotAllowed("Allowed methods are : ['GET', 'POST']")

    def get(self, request: HttpRequest, **kwargs: dict):
        # get person details from DB
        # people = Person.objects.all()

        # Fetch person with the name provided in query param
        query_params = request.GET
        name = query_params.get("name", "")
        people = Person.objects.filter(name=name)

        # business logic on the data
        data = []
        for person in people:
            # fetch contact details for the person
            contacts = person.contact_set.all()
            contact_details = []
            for contact in contacts:
                contact_details.append({
                    'phone': contact.phone
                })

            data.append({
                'name': person.name,
                'age': person.age,
                'address': person.address,
                'contact': contact_details
            })

        # render the relevant template with the data
        # return HttpResponse(data)
        return render(request, "my_app/person.html", {'person_data': data})
    
    def post(self, request: HttpRequest, **kwargs: dict):
        details = request.POST
        name = details.get('name', '')
        age = details.get('age', None)
        person = Person.objects.get(name=name)

        if not person:
            return HttpResponse("The person doesn't exist")
        
        person.age = age
        person.save()

        return HttpResponse("Person details updated")


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

# class AboutUs(View):
#     def get(self, request: HttpRequest, **kwargs: dict):
#         return render(request, "my_app/about.html")
    
class AboutUs(TemplateView):
    template_name = "my_app/about.html"

# @csrf_exempt
@require_http_methods(['GET', 'POST'])
def my_view(request: HttpRequest, **kwargs: dict):
    # you got a (GET) request from frontend
    # TODO: you make a database call to get the details

    # prepare a webpage (html) with dynamic content from DB/memory
    # html_content = "<html><body>"
    # for content in books_content:
    #     html_content += "<p>" + str(content) + "</p>"
    # html_content += "</body></html>"

    # template = loader.get_template("my_app/view.html")
    # rendered = render_to_string("my_app/view.html", {'content': books_content})

    # return HttpResponse(template.render(request=request, context={'content': books_content}))
    # return HttpResponse(rendered)
    # current_time = datetime.now()
    return render(request, "my_app/view.html", {'content': books_content})


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
