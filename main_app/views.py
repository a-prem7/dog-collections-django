from django.shortcuts import render
from django.http import HttpResponse
from .models import Dog


# # Add the Cat class & list and view function below the imports
# class Dog:  # Note that parens are optional if not inheriting from another class
#   def __init__(self, name, breed, description, age):
#     self.name = name
#     self.breed = breed
#     self.description = description
#     self.age = age

# dogs = [
#   Dog('Henry', 'doodle', 'foul little demon', 3),
#   Dog('Sachi', 'tortoise shell', 'diluted tortoise shell', 0),
#   Dog('Raven', 'black tripod', '3 legged cat', 4)
# ]

# Create your views here.

def home(request):
  return HttpResponse('<h1>Hello Doggy</h1>')

def about(request):
  return render(request, 'about.html')


# Add new view
def dogs_index(request):
    dogs = Dog.objects.all()
    return render(request, 'dogs/index.html', { 'dogs': dogs })