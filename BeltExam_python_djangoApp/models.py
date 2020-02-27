from django.db import models
from datetime import datetime
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def registerValidator(self, postData):
        errors = {}
        if len(postData['form_name']) < 1:
            errors['NameRequired'] = "Name is required"
        if len(postData['form_user_name']) < 1:
            errors['LastNameRequired'] = "User name is required also"
        if len(postData['form_password']) < 8:
            errors['PasswordRequired'] = "This holds the key to your account and must be atleast 8 characters,so obviously...."
        if postData['form_password'] != postData['form_confirm_password']:
            errors['ConfirmPasswordRequired'] = "The key to your account do not match please try again"
        return errors

    def loginValidator(request, postData):
        errors = {}
        usersWithUsername = User.objects.filter(user_name= postData['form_user_name'])
        if len(usersWithUsername) == 0:
            errors['UsermatchRequired'] = "Travel Profile does not exist, Please register first"
        else:
            user = usersWithUsername[0]
            if bcrypt.checkpw(postData['form_password'].encode(), user.password.encode()):
                print("password match")
            else:
                errors['PasswordMatch'] = "Traveler Password is Invalid"
        return errors



class TripManager(models.Manager):
    def tripValidator(self, postData):
        errors = {}
        if len(postData['form_destination']) < 3:
            errors['DestinationRequired'] = "Destination is required"
        if len(postData['form_desc']) < 10:
            errors['DescriptionRequired'] = "Description is important also"
        if postData['form_travel_start'] > postData['form_travel_end']:
            errors['TravelDateFrom'] = "Date of arrival cannot be before date of travel"
        # this code makes sure to validate travel date is not set to the past.
        today = datetime.today().strftime('%Y-%m-%d')
        print(today)
        print(postData['form_travel_start'])
        if postData['form_travel_start'] < today:
            errors['TravelStartPast'] = "Date of travel cannot be in the past"
        return errors



class User(models.Model):
    name = models.CharField(max_length=225)
    user_name = models.CharField(max_length=225)
    password = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    desc = models.CharField(max_length=225)
    travel_start = models.DateField(max_length=255)
    travel_end = models.DateField(max_length=255)
    added_by = models.ForeignKey(User, related_name="trips", on_delete = models.CASCADE)
    plans = models.ManyToManyField(User, related_name= "plan_trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()


