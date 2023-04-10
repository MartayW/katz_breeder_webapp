from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from datetime import date, datetime
from venmo_api import Client
import requests


from django.contrib.auth import authenticate, login, logout
from .models import CatTest, Transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# function to get venmo transactions and add any that are new to the db
def updateVenmo():    #this is not a view but is used in the login_page view
    access_token = Client.get_access_token(username='katz.breeder.system@gmail.com',
                                           password='K@tz_098')
    venmo = Client(access_token=access_token)
    my_id = (venmo.user.get_my_profile().id)
    transactions_list = venmo.user.get_user_transactions(user_id=my_id) # list of transactions from venmo

    for transaction in transactions_list:
        try:
            type = transaction.note.split(" ")[0]
        except IndexError:
            type = ''
        try:
            catID = transaction.note.split(" ")[2]
        except IndexError:
            catID = ''

        # Date is converted from timestamp to python datetime,date object
        try:
            formatted_date = date.fromtimestamp(transaction.date_completed)
        except TypeError:
            formatted_date = None
        #Try to create a valid object using the transaction id given by venmo. This determines if the transaction is already in the database
        try:
            valid_transaction = Transaction.objects.get(id=transaction.id)
            #If the transaction is not in the database already, create it
        except (Transaction.DoesNotExist):
            transaction = Transaction(id=transaction.id, cust_first_name=transaction.actor.first_name, cust_last_name=transaction.actor.last_name,
                                      cust_venmo_name=transaction.actor.username, amount=transaction.amount, type=type,
                                      catID=catID, date=formatted_date)
            transaction.save()

    #End the connection to venmo
    venmo.log_out(access_token)

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
                # Updates the database with any new Venmo transactions
                updateVenmo()
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
    if request.method == 'POST' and request.FILES['image']:
        name = request.POST['catname']
        gender = request.POST['gender']
        color = request.POST['color']
        bday = (request.POST['bday'])
        print(type(bday), " is the type and " + bday + " is the string")
        bday_date = datetime.strptime(bday, '%Y-%m-%d')
        personality = request.POST['personality']
        image = request.FILES['image']
        price = request.POST['price']
        breeder = 0
        cattest = CatTest(name=name, birthday=bday_date, gender=gender,
                  personality=personality, color=color, image=image, price=price, breeder=breeder)
        cattest.save()
        #this is supposed to retrieve the html form entries and assigns them to the CatTest variables in models.
        return redirect('kittens')
    return render(request, "../templates/cat_register.html")

def query_test(request):
    females = CatTest.objects.filter(gender="Female")
    test = "Test"
    return render(request, "../templates/query_test.html", {'females':females}, {"test":test})

def about(request):
    return render(request, "../templates/about.html")

