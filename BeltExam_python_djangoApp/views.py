from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from django.db.models import Q
from datetime import datetime
from .models import *

# Create your views here.
def index(request):
    return render(request, "main.html")


def mainpage(request):
    return redirect("/")


def userReg(request):
    validationErrors = User.objects.registerValidator(request.POST)
    print(validationErrors)
    if len(validationErrors) > 0:
        for key, value in validationErrors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        hashedpassword = bcrypt.hashpw(request.POST['form_password'].encode(), bcrypt.gensalt()).decode()
        newreguser = User.objects.create(name= request.POST['form_name'], user_name= request.POST['form_user_name'], password= hashedpassword)
        request.session['successfullyloggedinUserId'] = newreguser.id
    return redirect("/travels")


def userlogin(request):
    loginerrors = User.objects.loginValidator(request.POST)
    if len(loginerrors) > 0:
        for key, value in loginerrors.items():
            messages.error(request, value)
        return redirect ("/")
    else:
        userlogin = User.objects.filter(user_name = request.POST['form_user_name'])
        userlogin = userlogin[0]
        request.session['successfullyloggedinUserId'] = userlogin.id
        return redirect("/travels")


def travelpage(request):
    loginuser = User.objects.get(id = request.session['successfullyloggedinUserId'])
    context = {
        'travellerlogin': loginuser,
        'alltravels': Trip.objects.all(),
        'loggedusertravels': Trip.objects.filter(added_by = loginuser) | Trip.objects.filter(plans = loginuser),
        'othertravels': Trip.objects.exclude(Q(added_by = loginuser) | Q(plans = loginuser))
    }
    return render(request, "travels.html", context)

    usertrip = Trip.objects.all()
    context = {
        'traveltrip': usertrip
    }
    return render(request, "travels.html", context)

    if 'successfullyloggedinUserId' not in request.session:
        return redirect("/")



def travelplan(request):
    return render(request, "add.html")



def addtravel(request):
    adderrors = Trip.objects.tripValidator(request.POST)
    if len(adderrors) > 0:
        for key, value in adderrors.items():
            messages.error(request, value)
        return redirect ("/travels/add")
    else:
        loggedinUser = User.objects.get(id = request.session['successfullyloggedinUserId'])
        addtrip = Trip.objects.create(destination= request.POST['form_destination'], desc= request.POST['form_desc'], travel_start= request.POST['form_travel_start'], travel_end= request.POST['form_travel_end'], added_by= loggedinUser)
        return redirect("/travels")

        


def jointravels(request, tripId):
    loggedinUser = User.objects.get(id = request.session['successfullyloggedinUserId'])
    traveltotrips = Trip.objects.get(id = tripId)
    traveltotrips.plans.add(loggedinUser)
    return redirect("/travels")



def destinationInfo(request, tripId):
    context = {
        "travelInfo": Trip.objects.get(id = tripId)
    }
    return render(request, "destination.html", context)



def logout(request):
    request.session.clear()
    return redirect("/")