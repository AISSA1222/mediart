import datetime
from django.core.files.storage import FileSystemStorage
from django.core import serializers
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Project, Task, Client, ProjectForm, UpdateUser, \
    ClientForm, TaskForm, \
    AddUser, UpdateTaskForm, Notification, Message
from django.urls import reverse


def home(request):
    if request.session.get("login"):

        photo = request.session.get('photo')
        username = request.session.get('username')

        ctx = {
            "username": username,
            "photo": photo,
            "userform": UpdateUser(),

        }

        return render(request, 'task_manager/home.html', context=None)
    else:
        return redirect(reverse('task_manager:login'))


@csrf_exempt
def login(request):
    if request.method == "GET":
        return render(request, 'task_manager/login.html', context=None)
    if request.method == "POST":
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.filter(address_email=email, password=password).values()
        print(user)
        if password == '' or email == '':
            return render(request, 'task_manager/login.html',
                          context={"error": "input your information pls"})
        else:
            if not user:

                return render(request, 'task_manager/login.html',
                              context={"error": "invalid email email or password"})
            else:
                role = user[0]["role"]
                id = user[0]["id"]
                username = user[0]["username"]
                photo = user[0]["photo"]
                email = user[0]['address_email']
                request.session['id'] = id
                request.session['login'] = email
                request.session['role'] = role
                request.session['username'] = username
                request.session['photo'] = photo
                text = username + " " + "logged in "
                user = User.objects.filter(role="SuperUser")
                if role != "SuperUser":
                    notif = Notification(text=text, to_user=user[0])
                    notif.save()

                User.objects.filter(id=id).update(active=True, date_login=datetime.datetime.now())

                return redirect(reverse('task_manager:home'))
    else:
        return redirect(reverse('task_manager:login'))


@csrf_exempt
def users(request):
    if request.session.get("login"):
        if request.session.get("role") == "SuperUser":
            if request.method == "GET":
                user_list = User.objects.filter(role="User").all()
                add_user = AddUser()
                ctx = {"add_user": add_user, "users": user_list}

                return render(request, 'task_manager/users.html', context=ctx)
            if request.method == "POST":
                form = AddUser(request.POST)
                username = request.POST["username"]
                address = request.POST["address_email"]
                password = request.POST["password"]
                role = request.POST["role"]
                url_photo = "/static/task_manager/default_user.jpg"
                if address and password and role:
                    user = User(username=username, address_email=address, password=password, role=role, photo=url_photo)
                    user.save()
                    return redirect(reverse('task_manager:users'))
                else:
                    return render(request, 'task_manager/users.html', context={"error": "fill all the fields"})
        else:
            return redirect(reverse('task_manager:home'))
    else:
        return redirect(reverse('task_manager:login'))


def delete_user(request, id):
    if request.session["login"]:
        if request.session.get('role') == "SuperUser":

            User.objects.filter(id=id).delete()
            return redirect(reverse('task_manager:users'))
        else:
            return redirect(reverse('task_manager:home'))
    else:
        return redirect(reverse('task_manager:login'))


# view for projects :
@csrf_exempt
def project(request):
    if request.session.get("login"):
        if request.session.get("role") == "SuperUser":
            if request.method == "GET":
                project_list = Project.objects.all()
                projectform = ProjectForm()
                ctx = {"projects": project_list,
                       "add_project": projectform,
                       }

                return render(request, 'task_manager/project.html', context=ctx)
            elif request.method == "POST":
                if request.POST['name'] or request.POST['client']:
                    form = ProjectForm(request.POST)
                    if form.is_valid():
                        form.save()
                        return redirect(reverse('task_manager:projects'))
                    else:
                        return render(request, 'task_manager/project.html', context=None)
                else:
                    return redirect(reverse('task_manager:projects'), context={"error": "fill all fields"})

        else:
            return redirect(reverse('task_manager:home'))
    else:
        return redirect(reverse('task_manager:login'))


def delete_project(request, id):
    if request.session.get("login"):
        if request.session.get("role") == "SuperUser":
            Project.objects.filter(id=id).delete()
            return redirect(reverse('task_manager:projects'))
        else:
            return redirect(reverse('task_manager:home'))
    else:
        return redirect(reverse('task_manager:login'))


@csrf_exempt
def update_project(request, id):
    if request.session.get("login"):
        if request.session.get('role') == "SuperUser":
            if request.method == 'POST':
                name = request.POST['name']
                client = request.POST['client']
                dead_line = request.POST['dead_line']

                if name:
                    Project.objects.filter(id=id).update(name=name)
                if client:
                    Project.objects.filter(id=id).update(client=client)
                if dead_line:
                    Project.objects.filter(id=id).update(dead_line=dead_line)
                return redirect(reverse('task_manager:projects'))
        else:
            return redirect(reverse('task_manager:home'))
    else:
        return redirect(reverse('task_manager:login'))


def finish_project(request, id):
    if request.session.get("login"):
        if request.session.get('role') == "SuperUser":
            Project.objects.filter(id=id).update(finished=True)
            return redirect(reverse('task_manager:projects'))
        else:
            return redirect(reverse("task_manager:home"))

    else:
        return redirect(reverse('task_manager:login'))


# logout veiw :

def logout(request):
    del request.session["login"]
    id = request.session.get("id")
    user = User.objects.filter(role="SuperUser")
    username = request.session.get("username")
    text = username + " " + "is logged out "
    notif = Notification(text=text, to_user=user[0])
    notif.save()
    User.objects.filter(id=id).update(active=False, date_login=datetime.datetime.now())
    return redirect(reverse('task_manager:login'))


# profile view :

def profile(request):
    if request.session['login']:
        if request.method == 'GET':
            id = request.session['id']
            user = User.objects.filter(id=id).values()
            request.session['photo'] = user[0]['photo']
            request.session['username'] = user[0]['username']
            ctx = {
                "email": user[0]['address_email'],
                "username": request.session['username'],
                "role": user[0]['role'],
                "photo": request.session["photo"],
                "update_user": UpdateUser(),

            }
            return render(request, 'task_manager/profile.html', context=ctx)
        elif request.method == "POST":

            id = request.session['id']

            username = request.POST["username"]
            email = request.POST["address_email"]
            password = request.POST["password"]
            User.objects.filter(id=id).update(username=username,
                                              address_email=email,
                                              password=password
                                              )

            return redirect(reverse('task_manager:profile'))

    else:
        return redirect(reverse('task_manager:login'))


# update your photo :
@csrf_exempt
def update_photo(request):
    if request.session['login']:

        id = request.session['id']
        size_limit = 1 * 1024 * 1024

        if request.FILES:

            photo = request.FILES["photo"]
            print(photo.size)
            fs = FileSystemStorage()
            filename = fs.save(photo.name, photo)
            uploaded_file_url = fs.url(filename)

            if photo.size < size_limit:
                User.objects.filter(id=id).update(
                    photo=uploaded_file_url)

                return redirect(reverse('task_manager:profile'))
            else:
                ctx = {"error": "photo size greater than "}

            return render(request, 'task_manger:profile', context=ctx)
        else:
            photo = '/media/default_user.jpg'
            User.objects.filter(id=id).update(
                photo=photo)
            return redirect(reverse('task_manager:profile'))

    else:
        return redirect(reverse('task_manager:login'))


# Add task :
def task(request):
    if request.session['login']:
        if request.session.get("role") == "SuperUser":
            if request.method == "GET":
                task_list = Task.objects.all()
                taskform = TaskForm()
                ctx = {"tasks": task_list,
                       "add_task": taskform,
                       "update_task": UpdateTaskForm(),
                       }

                return render(request, 'task_manager/task.html', context=ctx)
            elif request.method == "POST":
                if request.POST['handler'] and request.POST['task_name']:
                    form = TaskForm(request.POST)
                    if form.is_valid():
                        text = "new task added for you "
                        to = User.objects.filter(id=request.POST["handler"])
                        notif = Notification(text=text, to_user=to[0])
                        notif.save()
                        form.save()

                        return redirect(reverse('task_manager:tasks'))
                    else:
                        return render(request, 'task_manager/task.html', context=None)
                else:
                    return redirect(reverse('task_manager:tasks'))

        else:
            return redirect(reverse('task_manager:home'))
    else:
        return redirect(reverse('task_manager:login'))


def delete_task(request, id):
    if request.session['login']:
        if request.session.get('role') == "SuperUser":
            text = "your task is deleted "

            t = Task.objects.filter(id=id).values()
            to = User.objects.filter(id=t[0]['handler_id'])
            notif = Notification(text=text, to_user=to[0])
            notif.save()
            Task.objects.filter(id=id).delete()

            return redirect(reverse('task_manager:tasks'))
        else:
            return redirect('task_manager:home')
    else:
        return redirect(reverse('task_manager:login'))


def update_task(request, id):
    if request.session['login']:
        if request.session.get('role') == "SuperUser":
            if request.method == 'POST':
                name = request.POST['handler']
                task_name = request.POST['task_name']
                description = request.POST['description']
                end_date = request.POST['end_date']

                text = "your task is updated "

                t = Task.objects.filter(id=id).values()
                to = User.objects.filter(id=t[0]['handler_id'])
                notif = Notification(text=text, to_user=to[0])
                notif.save()

                if name:
                    Task.objects.filter(id=id).update(handler=name)
                if end_date:
                    Task.objects.filter(id=id).update(end_date=end_date)
                if task_name:
                    Task.objects.filter(id=id).update(task_name=task_name)
                if description:
                    Task.objects.filter(id=id).update(description=description)
                return redirect(reverse('task_manager:tasks'))
        else:
            return redirect(reverse('task_manager:login'))
    else:
        return redirect(reverse('task_manager:login'))


# client view

def client(request):
    if request.session.get('login'):
        if request.session.get('role') == "SuperUser":
            if request.method == "GET":
                client_list = Client.objects.all()
                clientform = ClientForm()
                ctx = {"clients": client_list,
                       "add_client": clientform,
                       "update_client": ClientForm(),
                       }

                return render(request, 'task_manager/client.html', context=ctx)
            elif request.method == "POST":
                if request.POST["client_name"] and request.POST['phone_number']:
                    form = ClientForm(request.POST)

                    if form.is_valid():
                        # print(request.POST)
                        form.save()
                        return redirect(reverse('task_manager:clients'))
                    else:
                        return render(request, 'task_manager/client.html', context=None)
                else:
                    return redirect(reverse('task_manager:clients'))

        else:
            return redirect(reverse('task_manager:login'))
    else:
        return redirect(reverse('task_manager:login'))


def delete_client(request, id):
    if request.session.get('login'):
        if request.session.get('role') == "SuperUser":
            Client.objects.filter(id=id).delete()
            return redirect(reverse('task_manager:clients'))
        else:
            return redirect(reverse('task_manager:login'))
    else:
        return redirect(reverse('task_manager:login'))


def update_client(request, id):
    if request.session.get('login'):
        if request.session.get('role') == "SuperUser":
            if request.method == 'POST':
                client_name = request.POST['client_name']
                company_name = request.POST['company_name']
                email_address = request.POST['email_address']
                phone_number = request.POST['phone_number']
                geo_address = request.POST['geo_address']
                if client_name:
                    Client.objects.filter(id=id).update(client_name=client_name)
                if company_name:
                    Client.objects.filter(id=id).update(company_name=company_name)
                if email_address:
                    Client.objects.filter(id=id).update(email_address=email_address)
                if phone_number:
                    Client.objects.filter(id=id).update(phone_number=phone_number)
                if geo_address:
                    Client.objects.filter(id=id).update(geo_address=geo_address)

                return redirect(reverse('task_manager:clients'))
        else:
            return redirect(reverse('task_manager:login'))
    else:
        return redirect(reverse('task_manager:login'))


#  handel the notifications:

def get_not(request):
    if request.method == "GET":
        id = request.GET['id']
        user = User.objects.filter(id=id).all()
        notif = Notification.objects.filter(to_user=user[0]).all()


        notif_se = serializers.serialize('json', notif)
        Notification.objects.filter(to_user=user[0]).delete()
        return JsonResponse(notif_se, safe=False)


def my_tasks(request):
    if request.session.get('login'):
        if request.session.get('role') == "User":
            id = request.session.get("id")
            u = User.objects.filter(id=id)
            my_task = Task.objects.filter(handler=u[0])

            ctx = {"tasks": my_task}

            return render(request, 'task_manager/my_task.html', context=ctx)

        else:
            return redirect(reverse('task_manager:home'))

    else:
        return redirect(reverse('task_manager:logout'))


def finish_my_tasks(request, pk):
    if request.session.get('login'):
        if request.session.get('role') == "User":
            user = User.objects.filter(role="SuperUser")
            username = request.session.get("username")
            text = username + " " + " finished a task "
            notif = Notification(text=text, to_user=user[0])
            notif.save()
            Task.objects.filter(id=pk).update(accomplished=True)
            return redirect(reverse('task_manager:mytasks'))

        else:
            return redirect(reverse('task_manager:home'))

    else:
        return redirect(reverse('task_manager:logout'))


@csrf_exempt
def set_msg(request):
    if request.session.get("login"):
        if request.POST:
            msg = request.POST["msg"]
            id = request.session.get("id")
            U = User.objects.filter(id=id)
            m = Message(body=msg, sender=U[0], sender_name=U[0].username)
            m.save()
            T = User.objects.exclude(id=id)
            text = "new message"
            for t in T:
                notif = Notification(text=text, to_user=t)
                notif.save()
            return HttpResponse('send')


    else:
        return redirect(reverse('task_manager:logout'))


def get_msg(request):
    if request.session.get("login"):
        if request.GET:
            msg = Message.objects.all().order_by("date")
            msg = serializers.serialize('json', msg)

            return JsonResponse(msg, safe=False)

    else:
        return redirect(reverse('task_manager:logout'))
