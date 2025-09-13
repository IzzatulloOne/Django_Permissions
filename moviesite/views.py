from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib import messages
from .models import Genre, Movie, Author
from .forms import MovieForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User

def main(request: HttpRequest):
    messages.info(request, "Xush kelibsiz! Asosiy sahifasidasiz.")
    genres = Genre.objects.all()
    movies = Movie.objects.filter(published=True)

    context = {
        'genres': genres,
        'movies': movies,
        'title': 'main',
    }

    return render(request, 'moviesite/main.html', context)

def about(request: HttpRequest):
    context = {
        'title': 'about',
    }

    return render(request, 'moviesite/about.html', context)

def by_genre(request: HttpRequest, genre_id):
    movies = Movie.objects.filter(genre_id=genre_id, published=True)
    genres = Genre.objects.all()
    genre = get_object_or_404(Genre, pk=genre_id)

    context = {
        'movies': movies,
        'genres': genres,
        'title': genre.type,
    }

    return render(request, 'moviesite/main.html', context)

def by_movie(request: HttpRequest, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id, published=True)

    movie.views += 1
    movie.save()

    context = {
        'movie': movie,
        'title': movie.title,
    }

    return render(request, 'moviesite/movie.html', context)

@login_required
@permission_required('movies.add_movie', raise_exception=True)
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.author = request.user
            movie.save()
            messages.success(request, "Film qo'shildi!")
            return redirect("by_movie", movie_id=movie.pk)
    else:
        form = MovieForm()
    return render(request, 'moviesite/add_movie.html', {'form': form})

@login_required
@permission_required('movies.change_movie', raise_exception=True)
def update_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.user != movie.author and not request.user.is_superuser:
        messages.error(request, "Siz bu filmni tahrirlay olmaysiz!")
        return redirect("main")

    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            messages.success(request, "Film yangilandi!")
            return redirect("by_movie", movie_id=movie.pk)
    else:
        form = MovieForm(instance=movie)
    return render(request, 'moviesite/update_movie.html', {'form': form})

@login_required
@permission_required('movies.delete_movie', raise_exception=True)
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.user != movie.author and not request.user.is_superuser:
        messages.error(request, "Siz bu filmni o'chira olmaysiz!")
        return redirect("main")

    if request.method == 'POST':
        movie.delete()
        messages.success(request, "Film o'chirildi!")
        return redirect("main")
    return render(request, 'moviesite/delete_movie.html', {'movie': movie})

def author_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Author.objects.filter(user=user).first()
    return render(request, 'moviesite/profile.html', {
        'author_profile': profile,
        'user': user
    })

    
def author_profil(request, username: str):
    user = get_object_or_404(User, username=username)
    context = {
        'user':user
    }
    try:
        author_profile = Author.objects.get(user=user)
        context['author_profile'] = author_profile
    except Author.DoesNotExist:
        context['author_profile'] = None
    return render(request, 'index.html', context)