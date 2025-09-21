from django.urls import path
from .views import MainView, AboutView, MovieCreateView, delete_movie, update_movie, ByGenreView, ByMovieView,author_profil



urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('about/', AboutView.as_view(), name='about'),
    path('bio_user/<str:username>/', author_profil, name="profile"),
    path('movie/add/', MovieCreateView.as_view(), name='add_movie'),
    path('movie/<int:movie_id>/delete/', delete_movie, name='delete_movie'),
    path('movie/<int:movie_id>/update/', update_movie, name='update_movie'),
    path('genre/<int:genre_id>/', ByGenreView.as_view(), name='by_genre'),
    path('movie/<int:movie_id>/', ByMovieView.as_view(), name='by_movie')
]
