from django.contrib import admin
from .models import Author, Genre, BookReview


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'birth_year')
    search_fields = ('full_name',)
    list_filter = ('birth_year',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'rating', 'reviewer', 'is_recommended')
    list_filter = ('genre', 'rating', 'is_recommended')
    search_fields = ('title', 'review_text')
    list_editable = ('rating', 'is_recommended')
    ordering = ('-created_at',)