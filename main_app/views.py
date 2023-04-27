from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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
@login_required
def dogs_index(request):
    dogs = Dog.objects.filter(user=request.user)
    return render(request, 'dogs/index.html', {'dogs': dogs})

@login_required
def dogs_detail(request, dog_id):
   dog = Dog.objects.get(id=dog_id)

   # instantiate FeedingForm to be rendered in the template
   feeding_form = FeedingForm()
   toys_dog_doesnt_have = Toy.objects.exclude(
       id__in=dog.toys.all().values_list('id'))
   return render(request, 'dogs/detail.html', {
       # include the dog and feeding_form in the context
       'dog': dog, 'feeding_form': feeding_form,
       'toys': toys_dog_doesnt_have
   })


# add this new function below dogs_detail
@login_required
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
@login_required
def assoc_toy(request, dog_id, toy_id):
  # Note that you can pass a toy's id instead of the whole object
  Dog.objects.get(id=dog_id).toys.add(toy_id)
  return redirect('detail', dog_id=dog_id)
@login_required 
def remove_toy(request, dog_id, toy_id):
  Dog.objects.get(id=dog_id).toys.remove(toy_id)
  return redirect('detail', dog_id=dog_id)

class DogCreate(LoginRequiredMixin, CreateView):
  model = Dog
  fields =('name', 'breed', 'description', 'age')
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the dog
    # Let the CreateView do its job as usual
    return super().form_valid(form)


class DogUpdate(LoginRequiredMixin, UpdateView):
  model = Dog
  # Let's disallow the renaming of a dog by excluding the name field!
  fields =('name', 'breed', 'description', 'age')

class DogDelete(LoginRequiredMixin, DeleteView):
  model = Dog
  success_url = '/dogs/'

class ToysIndex(LoginRequiredMixin, ListView):
   model = Toy

class ToysDetail(LoginRequiredMixin, DetailView):
  model = Toy

class ToyCreate(LoginRequiredMixin, CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(LoginRequiredMixin, UpdateView):
  model = Toy
  fields = '__all__'

class ToyDelete(LoginRequiredMixin, DeleteView):
  model = Toy
  success_url = '/toys/'

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
