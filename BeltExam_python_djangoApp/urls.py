from django.urls import path
from . import views

urlpatterns = [
    path('', views. index),
    path('main', views. mainpage),
    path('register', views. userReg),
    path('login', views. userlogin),
    path('travels', views. travelpage),
    path('travels/add', views. travelplan),
    path('addtrip', views. addtravel),
    path('addtraveltotravels/<tripId>', views. jointravels),
    path('trip_destination/<tripId>', views. destinationInfo),
    path('logout', views. logout),
    
]
