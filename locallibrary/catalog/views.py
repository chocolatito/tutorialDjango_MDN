from django.shortcuts import render
from django.views import generic
# Create your views here.
from .models import Book, Author, BookInstance, Genre


def index(request):
    """
    Función vista para la página inicio del sitio.
    """
    # Genera contadores de algunos de los objetos principales
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Libros disponibles (status = 'a')
    num_instances_available = BookInstance.objects.filter(
        status__exact='a').count()
    num_authors = Author.objects.count()
    # El 'all()' esta implícito por defecto.

    # Renderiza la plantilla HTML index.html
    # con los datos en la variable contexto
    return render(
        request,
        'index.html',
        context={'num_books': num_books,
                 'num_instances': num_instances,
                 'num_instances_available': num_instances_available,
                 'num_authors': num_authors},
    )


# Nueva vista

class BookListView(generic.ListView):
    model = Book
    paginate_by = 1
    # your own name for the list as a template variable
    # context_object_name = 'my_book_list'
    # Get 5 books containing the title war
    # queryset = Book.objects.filter(title__icontains='war')[:5]
    # Specify your own template name/location
    # template_name = 'books/my_arbitrary_template_name_list.html'

    # Get 5 books containing the title war
    def get_queryset(self):
        return Book.objects.all()  # filter(title__icontains='autor1')[:5]

    # Call the base implementation first to get a context
    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['some_data'] = 'This is just some data'
        return context


class BookDetailView(generic.DetailView):
    model = Book

# https://developer.mozilla.org/es/docs/Learn/Server-side/Django/Sessions
