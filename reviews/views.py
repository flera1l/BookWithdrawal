from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import BookReview, Genre, Author
from .forms import BookReviewForm, RegisterForm


def index(request):
    """Главная страница со статистикой и последними рецензиями."""
    latest_reviews = BookReview.objects.all().order_by('-created_at')[:3]
    context = {
        'reviews_count': BookReview.objects.count(),
        'authors_count': Author.objects.count(),
        'genres_count': Genre.objects.count(),
        'latest_reviews': latest_reviews,
    }
    return render(request, 'reviews/index.html', context)


def review_list(request):
    """Список рецензий с поиском по названию и фильтрацией по жанру."""
    query = request.GET.get('q', '')
    genre_id = request.GET.get('genre', '')

    reviews = BookReview.objects.all().order_by('-created_at')
    genres = Genre.objects.all()

    if query:
        reviews = reviews.filter(title__icontains=query)
    if genre_id:
        reviews = reviews.filter(genre_id=genre_id)

    context = {
        'reviews': reviews,
        'genres': genres,
        'query': query,
        'selected_genre': genre_id,
    }
    return render(request, 'reviews/review_list.html', context)


def review_detail(request, pk):
    """Страница одной рецензии."""
    review = get_object_or_404(BookReview, pk=pk)
    return render(request, 'reviews/review_detail.html', {'review': review})


@login_required
def review_add(request):
    """Добавление новой рецензии (доступно только авторизованным)."""
    if request.method == 'POST':
        form = BookReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.save()
            messages.success(request, 'Рецензия успешно опубликована!')
            return redirect('review_list')
    else:
        form = BookReviewForm()
    return render(request, 'reviews/review_form.html', {'form': form, 'title': 'Новая рецензия'})


@login_required
def review_edit(request, pk):
    """Редактирование своей рецензии."""
    review = get_object_or_404(BookReview, pk=pk)
    if review.reviewer != request.user:
        messages.error(request, 'Вы можете редактировать только свои рецензии!')
        return redirect('review_detail', pk=review.pk)

    if request.method == 'POST':
        form = BookReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Рецензия успешно обновлена!')
            return redirect('review_detail', pk=review.pk)
    else:
        form = BookReviewForm(instance=review)
    return render(request, 'reviews/review_form.html', {'form': form, 'title': 'Редактировать рецензию'})


def register_view(request):
    """Регистрация нового пользователя."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'reviews/register.html', {'form': form})


def about(request):
    """Страница О проекте."""
    return render(request, 'reviews/about.html')