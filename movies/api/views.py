from django.shortcuts import render,HttpResponse
from .models import Movie

# Create your views here.
def index(request, *args, **kwargs):
    return HttpResponse(Movie.objects.all())
