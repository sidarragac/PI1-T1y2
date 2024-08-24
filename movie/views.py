from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64
# Create your views here.

def home(request):
    # return HttpResponse("<h1>Welcome to the home page</h1>")
    # return render(request, "home.html", {'name': 'Santiago Idarraga Ceballos'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})

def about(request):
    # return HttpResponse("<h1>Welcome to the home about</h1>")
    return render(request, "about.html")

def statisticsView(request):
    matplotlib.use("Agg")
    allMovies = Movie.objects.all()
    movieCountsByYear = {}
    
    for movie in allMovies:
        year = movie.year if movie.year else 'None'
        if year in movie:
            movieCountsByYear[year]+=1
        else:
            movieCountsByYear[year] = 1 
        
    barWidth = 0.5
    barPositions = range(len(movieCountsByYear))
    
    #Se crea gráfico de barras
    plt.bar(barPositions, movieCountsByYear.values(), width=barWidth, align='center')
    
    #Personalización del gráfico
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(barPositions, movieCountsByYear.keys(), rotation=90)
    
    #Espaciado entre barras
    plt.subplots_adjust(bottom=0.3)
    
    #Se guarda la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    
    #Convertir imagen en base64
    imagePNG = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(imagePNG)
    graphic = graphic.decode('utf-8')
    
    return render(request, 'statistics.html', {'graphic': graphic})
