from django.core.management.base import BaseCommand
from movie.models import Movie
import os
import json

class Command(BaseCommand):
    help = 'Load movies from movies.json into the movie model'
    
    def handle(self, *args, **kwargs):
        #Construir el path hacia el archivo JSON
        path = 'movie/management/commands/movies.json'
        
        with open(path, 'r') as file:
            movies = json.load(file)
            
        for i in range(10):
            movie = movies[i]
            exist = Movie.objects.filter(title = movie['title']).first() #Verifica que la pelicula no exista.
            if not exist:
                Movie.objects.create(
                    title = movie['title'],
                    image = 'movie/images/default.jpg',
                    description = movie['plot'],
                    genre = movie['genre'],
                    year = movie['year']
                )