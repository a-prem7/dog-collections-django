from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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

def dogs_detail(request, dog_id):
   dog = Dog.objects.get(id=dog_id)
   return render(request, 'dogs/detail.html', { 'dog': dog })

class DogCreate(CreateView):
  model = Dog
  fields = '__all__'


class DogUpdate(UpdateView):
  model = Dog
  # Let's disallow the renaming of a dog by excluding the name field!
  fields = ['breed', 'description', 'age']

class DogDelete(DeleteView):
  model = Dog
  success_url = '/dogs/'