from django.http import Http404
from django.shortcuts import get_object_or_404, render
from .models import Book
from django.db.models import Avg


def index(request):

    books = Book.objects.all().order_by("-title")
    num_books = books.count()
    avg_rating = books.aggregate(Avg("rating"))

    return render(request, "book_outlet/index.html", {
        "books": books,
        "total_books": num_books,
        "average_book": avg_rating,
    })


def book_detail(request, slug):
    # pk is primary key, which we can use instead of id to get data from database.
    # try:
    #   book = Book.objects.get(pk=id)
    # except:
    #   raise Http404()

    book = get_object_or_404(Book, slug=slug)

    print("yes ", book.is_bestselling)

    return render(request, "book_outlet/book_detail.html", {
        "title": book.title,
        "author": book.author.first_name + " " + book.author.last_name,
        "rating": book.rating,
        "is_bestseller": book.is_bestselling,
    })
