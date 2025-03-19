from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from movies.models import Movie
from .forms import CommentForm

data = {
    "sliders": [
        {
            "slider_image": "slider1.jpg",
            "url": "film-adi-1"
        },
         {
            "slider_image": "slider2.jpg",
            "url": "film-adi-2"
        },
         {
            "slider_image": "slider3.jpg",
            "url": "film-adi-3"
        }
    ]
}

# Create your views here.

def index(request):
    movies = Movie.objects.filter(is_active=True, is_home=True)
    slider_movies = Movie.objects.filter(is_active=True).order_by('-date')[:3]  # Son eklenen 3 film
    return render(request, 'index.html', {
        "movies": movies,
        "slider_movies": slider_movies
    })

def movies(request):
    movies = Movie.objects.filter(is_active=True)
    return render(request, 'movies.html', {
        "movies": movies
    })

def movie_details(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    comments = movie.comments.filter(active=True)
    
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.movie = movie
            new_comment.save()
            messages.success(request, 'Yorumunuz başarıyla kaydedildi.')
            return redirect('movie_details', slug=movie.slug)
        else:
            messages.error(request, 'Lütfen formu doğru şekilde doldurun.')
    else:
        comment_form = CommentForm()
        
    return render(request, "movie-details.html", {
        "movie": movie,
        "genres": movie.genres.all(),
        "people": movie.people.all(),
        "videos": movie.videos.all(),
        "comments": comments,
        "comment_form": comment_form
    })