from django.urls import path
from .views import MainView, AboutView, MovieCreateView, MovieDeleteView, MovieUpdateView, ByGenreView, ByMovieView,author_profil, user_logout



urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('about/', AboutView.as_view(), name='about'),
    path('bio_user/<str:username>/', author_profil, name="profile"),
    path('movie/add/', MovieCreateView.as_view(), name='add_movie'),
    path('movie/<int:movie_id>/delete/', MovieDeleteView.as_view(), name='delete_movie'),
    path('movie/<int:movie_id>/update/', MovieUpdateView.as_view(), name='update_movie'),
    path('genre/<int:genre_id>/', ByGenreView.as_view(), name='by_genre'),
    path('movie/<int:movie_id>/', ByMovieView.as_view(), name='by_movie'),
    path('logout/', user_logout, name='logout'),

]
