from django.db import models

# Create your models here.
class Director(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=55)

    def __str__(self):
        return self.name+' '+self.surname

class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField(default=1998)
    director = models.ForeignKey(Director,
    blank=True,null=True,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title  
