from django.urls import path
from .views import (main_page, info, secret_view, login_view, task_list, task_edit, task_delete, task_complete,
                    task_incomplete)


urlpatterns = [
    path("", main_page, name='main'),
    path("info/", info, name='info'),
    path("secret/", secret_view, name='secret'),
    path('login/', login_view, name='login'),
    path("task_list/", task_list, name='task_list'),
    path('edit/<int:task_id>/', task_edit, name='task_edit'),
    path('delete/<int:task_id>/', task_delete, name='task_delete'),
    path('complete/<int:task_id>/', task_complete, name='task_complete'),
    path('incomplete/<int:task_id>/', task_incomplete, name='task_incomplete'),
]
