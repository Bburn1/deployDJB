from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import ListView, DetailView

from .forms import ReviewForm
from .models import Book, Category, Avtor, Publishing, Genre

def index_view(request):
    return render(request, 'index.html')

def about_view(request):
    return render(request, '/pages/about.html')

class GenreYear:
    """Genre and date publishiung books"""
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Book.objects.filter(draft=False).values("year").distinct()

class BookView(GenreYear, ListView):
    """Список книг"""
    model = Book
    queryset = Book.objects.filter(draft=False)
    paginate_by = 9
    #template_name = "books/book_list.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context["categories"] = Category.objects.all()
    #     return context





class BookDetailView(GenreYear, DetailView):
    """Страница с отображением книги"""
    model = Book
    slug_field = "url"

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context["categories"] = Category.objects.all()
    #     return context

class AddReview(View):
    """Send Review"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        book = Book.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.book = book
            form.save()
        return redirect(book.get_absolute_url())

class AvtorView(GenreYear, DetailView):
    """Информация о авторе"""
    model = Avtor
    template_name = 'books/avtor.html'
    slug_field = "name"

class PublishingView(GenreYear, DetailView):
    """Информация о издательстве"""
    model = Publishing
    template_name = 'books/publishing.html'
    slug_field = "name"

class FilterBooksView(GenreYear, ListView):
    """Filter books"""
    paginate_by = 9
    def get_queryset(self):
        # queryset = Book.objects.filter(
        #     Q(year__in=self.request.GET.getlist("year")) |
        #     Q(genres__in=self.request.GET.getlist("genre"))
        # ).distinct()
        # return queryset

        queryset = Book.objects.all()

        if "year" in self.request.GET:
            queryset = queryset.filter(year__in=self.request.GET.getlist("year")).distinct()
        if "genre" in self.request.GET:
            queryset = queryset.filter(genres__in=self.request.GET.getlist("genre")).distinct()
        return queryset

    def get_context_data(self, *agrs, **kwargs):
        context = super().get_context_data(*agrs, **kwargs)
        context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
        context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
        return context

class Search(GenreYear, ListView):
    paginate_by = 9
    def get_queryset(self):
        return Book.objects.filter(title__iregex=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'{self.request.GET.get("q")}&'
        return context



