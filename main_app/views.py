from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Dog, Toy
from .forms import FeedingForm


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
    return render(request, 'dogs/index.html', {'dogs': dogs})


def dogs_detail(request, dog_id):
   dog = Dog.objects.get(id=dog_id)
    # instantiate FeedingForm to be rendered in the template
   feeding_form = FeedingForm()
   return render(request, 'dogs/detail.html', {
    # include the dog and feeding_form in the context
    'dog': dog, 'feeding_form': feeding_form
  })


# add this new function below cats_detail
def add_feeding(request, dog_id):
  # create the ModelForm using the data in request.POST
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the dog_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.dog_id = dog_id
    new_feeding.save()
  return redirect('detail', dog_id=dog_id)
  

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

class ToysIndex(ListView):
   model = Toy

class ToysDetail(DetailView):
  model = Toy

class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(UpdateView):
  model = Toy
  fields = '__all__'

class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys/'