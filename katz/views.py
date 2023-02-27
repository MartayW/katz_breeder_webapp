from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from .models import CatTest
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# returns the http request for the main page: http://127.0.0.1:8000/
@login_required
def index(request):
    return render(request, "../templates/index.html")


# returns the http request for the "available kittens" page: http://127.0.0.1:8000/kittens/
@login_required
def kittens(request):
    cats = CatTest.objects.all()


    return render(request,"../templates/kittens.html", {'cats' : cats})

# returns the http request for the "register" page: http://127.0.0.1:8000/kittens/
def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        name = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']


        new_user = User.objects.create_user(name, email, password)
        new_user.first_name = firstname
        new_user.last_name = lastname
        new_user.save()
            #code for assigning the form data into the database fields.
        return redirect('login_page')
    return render(request, "../templates/register.html")

    def check_username(request):
        username = request.POST.get('username')

    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse('<div style="color: red"> This username already exists </div>')
    else:
        return HttpResponse('<div style="color: green"> This username is available </div>')
def login_page(request):

        if request.method == 'POST':
            username = request.POST['uname']
            password = request.POST['pw']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect('index')
        #else:

            #messages.error(request, 'Invalid form submission.')
            #return HttpResponse('Error, user does not exist')
        return render(request, "../templates/login_page.html")

def logoutuser(request):
    logout(request)
    return redirect('login_page')

    #returns the http request for the "available kittens" page: http://127.0.0.1:8000/kittens/

def cat_register(request):
    if request.method == 'POST':
        name = request.POST['catname']
        gender = request.POST['gender']
        color = request.POST['color']
        personality = request.POST['personality']
        image = request.POST['image']
        price = request.POST['price']

        cattest = CatTest(name=name, gender=gender,
                  personality=personality, color=color, image=image, price=price)
        cattest.save()
        #this is supposed to retrieve the html form entries and assigns them to the CatTest variables in models.
        return redirect('kittens')
    return render(request, "../templates/cat_register.html")

def about(request):
    return render(request, "../templates/about.html")