from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from movies.models import Movie, Person  # Person modelini ekledik
from .forms import CommentForm
from django.db.models import Q

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

def latest_movie(request):
    latest_movie = Movie.objects.filter(is_active=True).order_by('-date').first()
    if latest_movie:
        return redirect('movie_details', slug=latest_movie.slug)
    return redirect('movies_page')

def people(request):
    actors = Person.objects.filter(duty_type='2')  # Oyuncular
    directors = Person.objects.filter(duty_type='3')  # Yönetmenler
    return render(request, 'people.html', {
        'actors': actors,
        'directors': directors
    })

def search_movies(request):
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'all')  # Varsayılan olarak 'all'

    if query:
        if search_type == 'movies':
            results = Movie.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
        elif search_type == 'actors':
            results = Person.objects.filter(
                Q(duty_type='2') &  # Sadece oyuncular
                (Q(first_name__icontains=query) | Q(last_name__icontains=query))
            ).distinct()
        elif search_type == 'directors':
            results = Person.objects.filter(
                Q(duty_type='3') &  # Sadece yönetmenler
                (Q(first_name__icontains=query) | Q(last_name__icontains=query))
            ).distinct()
        else:  # 'all' durumu
            movies = Movie.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
            people = Person.objects.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query)
            )
            results = {
                'movies': movies,
                'people': people
            }
    else:
        results = []

    return render(request, 'movies/search.html', {
        'query': query,
        'results': results,
        'search_type': search_type
    })