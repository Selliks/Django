from django.urls import path
from .views import (main_page, info, secret_view, login_view, task_list, task_edit, task_delete, task_complete,
                    task_incomplete, member, edit_member, delete_member, books, edit_book, delete_book, mark_as_read)


urlpatterns = [
    path('', main_page, name='main'),
    path('info/', info, name='info'),
    path('secret/', secret_view, name='secret'),
    path('login/', login_view, name='login'),

    path('task_list/', task_list, name='task_list'),
    path('edit/<int:task_id>/', task_edit, name='task_edit'),
    path('delete/<int:task_id>/', task_delete, name='task_delete'),
    path('complete/<int:task_id>/', task_complete, name='task_complete'),
    path('incomplete/<int:task_id>/', task_incomplete, name='task_incomplete'),

    path('member/', member, name='member'),
    path('member/edit/<int:member_id>/', edit_member, name='edit_member'),
    path('member/delete/<int:member_id>/', delete_member, name='delete_member'),

    path('books/', books, name='books'),
    path('books/edit/<int:book_id>/', edit_book, name='edit_book'),
    path('books/delete/<int:book_id>/', delete_book, name='delete_book'),
    path('books/mark-as-read/<int:book_id>/', mark_as_read, name='mark_as_read'),
]
