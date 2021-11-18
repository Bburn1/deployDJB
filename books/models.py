from django.db import models
from datetime import date
# Create your models here.
from django.urls import reverse
from django.urls import path
from django.conf.urls import url


class Category(models.Model):
    # Категории

    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание", blank=True)
    url = models.SlugField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Avtor(models.Model):
    """avtor """
    name = models.CharField("Имя", max_length=150)
    age = models.DateField("Дата рождения", help_text="Дата", default=date.today, blank=True)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="avtors/", blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы "

class Publishing(models.Model):
    """Publishing House"""
    name = models.CharField("Имя", max_length=150)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Изображение", upload_to="publishing/", blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Издательство"
        verbose_name_plural = "Издательства"

class Genre(models.Model):
    """Genre"""
    name = models.CharField("Имя", max_length=150)
    description = models.TextField("Описание", blank=True)
    url = models.SlugField(max_length=150, unique=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

class Country(models.Model):
    """страна"""
    name = models.CharField("Страна", max_length=150)
    image = models.ImageField("Изображение", upload_to="country/", blank=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

class Book(models.Model):
    """books"""
    title = models.CharField("Назва", max_length=150)
    description = models.TextField("Опис")
    poster = models.ImageField("Обложка", upload_to="books/", blank=True)
    year = models.PositiveSmallIntegerField("Год написания", default=2021, blank=True)
    countrys = models.ManyToManyField(Country, verbose_name="Страна", related_name="book_country", max_length=50, blank=True)
    isbn = models.CharField("ISBN", help_text="Международный стандартный книжный номер", max_length=150, blank=True)
    pages = models.PositiveIntegerField("Страницы", default=0, blank=True)
    language = models.CharField("Язык", max_length=150, blank=True)
    world_publishing = models.CharField("Дата издания кнгиги", blank=True, max_length=50)
    avtors = models.ManyToManyField(Avtor, verbose_name="Авторы", related_name="book_avtor")
    publishings = models.ManyToManyField(Publishing, verbose_name="Издательства", related_name="book_publishing", blank=True)
    ebook = models.FileField("Електронная книга", upload_to="ebooks/", blank=True)

    genres = models.ManyToManyField(Genre, verbose_name="Жанры")

    category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True
    )
    url = models.SlugField(max_length=150, unique=True)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    def ebook_url(self):
        if self.ebook and hasattr(self.ebook, 'url'):
            return self.ebook.url
        else:
            return "/media/ebooks/readme.txt"

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

class BookShots(models.Model):
    """Страницы из книги"""
    title = models.CharField("", max_length=150)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="book_shots/")
    book = models.ForeignKey(Book, verbose_name="Книга", on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "Страница книги"
        verbose_name_plural = "Страницы книги"

class RatingStar(models.Model):
    """star"""
    value = models.PositiveSmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'
    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звёзды рейтинга"
        ordering = ["-value"]

class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP", max_length=25)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="Звезда")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")

    def __str__(self):
        return f"{self.star} - {self.book}"
    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"

class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Мся", max_length=150)
    text = models.TextField("Сообщение", max_length=3000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True)
    book = models.ForeignKey(Book, verbose_name="Кнгиа", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.book}"
    class Meta:
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"




