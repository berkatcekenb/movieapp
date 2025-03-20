from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home_page"),
    path("movies", views.movies, name="movies_page"),
    path("movies/<slug:slug>", views.movie_details, name="movie_details"),
    path('people/', views.people, name='people_page'),
    path('latest-movie/', views.latest_movie, name='latest_movie'),  # Yeni eklenen URL
    path('search/', views.search_movies, name='search_movies'),
]

