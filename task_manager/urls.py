from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

app_name = "task_manager"
urlpatterns = [
                  path('', views.home, name="home"),
                  path('login/', views.login, name="login"),
                  path('logout/', views.logout, name="logout"),
                  path('users/', views.users, name="users"),
                  path('profile/', views.profile, name="profile"),
                  path('profile/photo', views.update_photo, name="update_photo"),
                  path('users/delete/<int:id>', views.delete_user, name="delete_user"),
                  path('projects/', views.project, name="projects"),
                  path('projects/delete/<int:id>', views.delete_project, name="delete_project"),
                  path('projects/update/<int:id>', views.update_project, name="update_project"),
                  path('projects/finish/<int:id>', views.finish_project, name="finish_project"),
                  path('tasks/', views.task, name="tasks"),
                  path('tasks/update/<int:id>', views.update_task, name="update_task"),
                  path('tasks/delete/<int:id>', views.delete_task, name="delete_task"),
                  path('clients/', views.client, name="clients"),
                  path('clients/delete/<int:id>', views.delete_client, name="delete_client"),
                  path('clients/update/<int:id>', views.update_client, name="update_client"),
                  path('notifications', views.get_not, name="notification"),
                  path('mytasks', views.my_tasks, name="mytasks"),
                  path('mytasks/finish/<int:pk>', views.finish_my_tasks, name="finishmytasks"),
                  path('chat', views.set_msg, name="set"),
                  path('chat/get', views.get_msg, name="get"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
