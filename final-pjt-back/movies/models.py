from django.db import models
from django.conf import settings

# Create your models here.

class Movie(models.Model):
    movie_id = models.IntegerField(primary_key=True, unique=True)
    title = models.CharField(max_length=100)
    overview = models.TextField(blank=True)
    release_date = models.DateField(blank=True)
    poster_path = models.TextField(blank=True)
    popularity = models.FloatField()
    video_id = models.CharField(max_length=500, null=True,blank=True)
    genres = models.CharField(max_length=100, blank=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')
    runtime = models.CharField(max_length=50)
    backdrop_path = models.TextField(blank=True)
    status= models.TextField(blank=True)
    vote_average = models.FloatField(default=0)
    vote_count = models.IntegerField(default=0)
    adult = models.TextField(blank=True)

    def __str__(self):
        return self.title