from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    """Модель автора книги."""
    full_name = models.CharField('ФИО автора', max_length=150)
    birth_year = models.IntegerField('Год рождения', null=True, blank=True)

    def __str__(self):
        return self.full_name


class Genre(models.Model):
    """Модель литературного жанра."""
    name = models.CharField('Название жанра', max_length=100)

    def __str__(self):
        return self.name


class BookReview(models.Model):
    """Основная модель рецензии на книгу."""
    RATING_CHOICES = [
        (5, '5 — Шедевр'),
        (4, '4 — Отлично'),
        (3, '3 — Нормально'),
        (2, '2 — Слабо'),
        (1, '1 — Ужасно'),
    ]

    title = models.CharField('Название книги', max_length=200)
    cover_url = models.URLField('Ссылка на обложку (URL)', blank=True)
    pages = models.IntegerField('Количество страниц', default=250)
    review_text = models.TextField('Текст рецензии')
    rating = models.IntegerField('Оценка', choices=RATING_CHOICES, default=5)
    is_recommended = models.BooleanField('Рекомендую к прочтению', default=True)
    created_at = models.DateTimeField('Дата публикации', auto_now_add=True)

    # Связи ForeignKey с автором, жанром и пользователем
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор книги'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        related_name='reviews',
        verbose_name='Жанр'
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='book_reviews',
        verbose_name='Автор рецензии'
    )

    def __str__(self):
        return f'{self.title} ({self.rating}/5)'