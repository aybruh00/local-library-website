from django.shortcuts import render
from django.views import generic

# Create your views here.

from books.models import Book, Author, BookInstance, Genre

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book

class BookDetailView(generic.DetailView):
    model = Book

from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='books/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class SearchResultsView(generic.ListView):
    model = Book
    template_name = 'search-results.html'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Book.objects.filter(title__icontains=query)
        return object_list

from django.contrib.auth.mixins import PermissionRequiredMixin

import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from books.forms import IssueBookForm

@login_required
# @permission_required('catalog.can_mark_returned', raise_exception=True)
def issue_book(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':

        form = IssueBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['issue_date']
            book_instance.status = 'o'
            book_instance.save()

            return HttpResponseRedirect(reverse('books') )

    else:
        proposed_issue_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = IssueBookForm(initial={'issue_date': proposed_issue_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'books/book_issue.html', context)