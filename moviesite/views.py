from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from .models import Genre, Movie, Author
from .forms import MovieForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.urls import reverse_lazy

from .models import Genre, Movie


class MainView(ListView):
    model = Movie
    template_name = "moviesite/main.html"
    context_object_name = "movies"

    def get_queryset(self):
        return Movie.objects.filter(published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages.info(self.request, "Xush kelibsiz! Asosiy sahifasidasiz.")
        context["genres"] = Genre.objects.all()
        context["title"] = "main"
        return context


class AboutView(TemplateView):
    template_name = "moviesite/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "about"
        return context


class ByGenreView(ListView):
    model = Movie
    template_name = "moviesite/main.html"
    context_object_name = "movies"

    def get_queryset(self):
        return Movie.objects.filter(
            genre_id=self.kwargs["genre_id"], published=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genre = get_object_or_404(Genre, pk=self.kwargs["genre_id"])
        context["genres"] = Genre.objects.all()
        context["title"] = genre.type
        return context


class ByMovieView(DetailView):
    model = Movie
    template_name = "moviesite/movie.html"
    context_object_name = "movie"
    pk_url_kwarg = "movie_id"

    def get_object(self, queryset=None):
        movie = super().get_object(queryset)
        movie.views += 1
        movie.save()
        return movie

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        return context
    
    

class MovieCreateView(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    model = Movie
    form_class = MovieForm
    template_name = "moviesite/add_movie.html"

    permission_required = "movies.add_movie"
    raise_exception = True

    def form_valid(self, form):
        movie = form.save(commit=False)
        movie.author = self.request.user
        movie.save()
        messages.success(self.request, "Film qo'shildi!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("by_movie", kwargs={"movie_id": self.object.pk})
    
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

def user_logout(reuqest):
    logout(reuqest)
    return redirect('login_view')