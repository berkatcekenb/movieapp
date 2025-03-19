from django.db import models
from django.core.validators import MinLengthValidator
from .utils import optimize_slider_image
import os

class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Contact(models.Model):
    address = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.email


class Person(models.Model):

    genres = (
        ('M', 'Erkek'),
        ('F', 'Kadın'),
    )

    duty_types = (
        ('1', 'Görevli'),
        ('2', 'Oyuncu'),
        ('3', 'Yönetmen'),
        ('4', 'Senarist'),
    )


    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    biography = models.CharField(max_length=3000)
    birth_date = models.DateField()
    gender = models.CharField("Cinsiyet",max_length=1, choices=genres)
    image_name = models.CharField(max_length=50)
    duty_type = models.CharField("Görev",max_length=1, choices=duty_types)
    contacts = models.OneToOneField(Contact, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    full_name.fget.short_description = "Ad Soyad"

    class Meta:
        verbose_name = "Kişi"
        verbose_name_plural = "Kişiler"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.duty_types[int(self.duty_type)-1][1]})"

class Movie(models.Model):
    title = models.CharField("Başlık",max_length=100)
    description = models.TextField("Özet",validators=[MinLengthValidator(20)])
    image_name = models.CharField("Resim",max_length=50)
    image_cover = models.CharField(max_length=50)
    date = models.DateField()
    slug = models.SlugField(unique=True, db_index=True)
    budget = models.DecimalField(max_digits=19, decimal_places=2)
    language = models.CharField(max_length=50)
    genres = models.ManyToManyField(Genre)
    is_active = models.BooleanField(default=False)
    is_home = models.BooleanField(default=False)
    people = models.ManyToManyField(Person)

    class Meta:
        verbose_name = "Film"
        verbose_name_plural = "Filmler"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_image = None
        
        if not is_new:
            old_obj = Movie.objects.get(pk=self.pk)
            old_image = old_obj.image_cover

        # Normal kaydetme işlemini yap
        super().save(*args, **kwargs)
        
        # Eğer yeni bir resim yüklendiyse veya resim değiştiyse optimize et
        if old_image != self.image_cover or is_new:
            if self.image_cover:
                image_path = os.path.join('static', 'img', self.image_cover)  
                optimize_slider_image(image_path)

class Video(models.Model):
    title = models.CharField(max_length=200)
    video_url = models.CharField(max_length=100)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='videos')

    def __str__(self):
        return self.title

class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100) 
    text = models.TextField()
    rating = models.IntegerField(choices=[(i, f'{i} Star') for i in range(1,6)])
    created_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_date']
        verbose_name = 'Yorum'
        verbose_name_plural = 'Yorumlar'

    def __str__(self):
        return f'Comment by {self.name} on {self.movie}'




