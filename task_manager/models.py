from django.core.validators import MaxValueValidator
from django.db import models
from django.forms import ModelForm
import datetime


class User(models.Model):
    choices = [("User", "User"), ("SuperUser", "SuperUser")]
    username = models.CharField(max_length=100, blank=False)
    address_email = models.EmailField(max_length=100, blank=False)
    password = models.CharField(max_length=200, blank=False)
    role = models.CharField(choices=choices, max_length=50, blank=True)
    photo = models.ImageField(blank=True, upload_to="media")
    active = models.BooleanField(default=False)
    date_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    def delta(self):

        hours = datetime.datetime.now().hour - self.date_login.hour
        minute = datetime.datetime.now().minute - self.date_login.minute
        second = datetime.datetime.now().second - self.date_login.second

        return  str(hours) + "  hours - " + str(minute) + " minutes  " + str(second)+" seconds "

class Task(models.Model):
    handler = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    project = models.ForeignKey("Project", on_delete=models.CASCADE, blank=True)
    task_name = models.CharField(max_length=100, blank=True)
    start_date = models.DateTimeField(auto_now=False, blank=True)
    end_date = models.DateTimeField(auto_now=False, blank=True)
    description = models.TextField(max_length=2000, blank=True)
    accomplished = models.BooleanField(default=False)

    def __str__(self):
        return self.task_name

    def dead_time(self):
        days = self.end_date.day - datetime.datetime.now().day
        hours = self.end_date.hour - datetime.datetime.now().hour
        minutes = self.end_date.minute - datetime.datetime.now().minute
        seconds = self.end_date.second - datetime.datetime.now().second

        return "  "+str(days) + " days - " + str(hours) + "  hours - " + str(minutes) + " minutes  "


class Project(models.Model):
    name = models.CharField(max_length=100, blank=True)
    client = models.ForeignKey('client', on_delete=models.CASCADE, blank=True)
    dead_line = models.DateTimeField(auto_now=False, blank=True)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Client(models.Model):
    client_name = models.CharField(max_length=100, blank=True)
    company_name = models.CharField(max_length=100, blank=True)
    email_address = models.EmailField(max_length=100, blank=True)
    phone_number = models.PositiveIntegerField(validators=[MaxValueValidator(999999999999)], blank=True)
    geo_address = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.client_name


class Notification(models.Model):
    text = models.CharField(max_length=100)
    to_user = models.ForeignKey('User', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)


class Message(models.Model):
    body = models.CharField(max_length=4000, blank=True)
    sender = models.ForeignKey('User', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    sender_name = models.CharField(max_length=100, blank=True)


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ("address_email", "password")


class UpdateUser(ModelForm):
    class Meta:
        model = User
        fields = ("username", "address_email", "password")


class AddUser(ModelForm):
    class Meta:
        model = User
        fields = ("username", "address_email", "password", "role")


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ("handler", "project", "task_name", "start_date", "end_date", "description")


class UpdateTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ("handler", "task_name", 'description', "end_date")


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ("name", "client", "dead_line")


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = "__all__"



