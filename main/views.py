from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .models import Task, Member, Book
from .forms import LoginForm, TaskForm, MemberForm, BookForm
from django.db.models import Q


# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('secret')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def main_page(request):
    return render(request, "main_page.html")


def info(request):
    return render(request, "info.html")


@login_required
def secret_view(request):
    return render(request, "secret.html")


""" Book Settings """

@login_required
def books(request):
    filter_status = request.GET.get('status', 'all')
    search_query = request.GET.get('search', '')

    books = Book.objects.all()

    if filter_status == 'read':
        books = books.filter(is_read=True)
    elif filter_status == 'unread':
        books = books.filter(is_read=False)

    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) | Q(author__icontains=search_query)
        )

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books')
    else:
        form = BookForm()

    return render(request, 'books.html', {'books': books, 'form': form})


@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('books')
    else:
        form = BookForm(instance=book)

    return render(request, 'edit_book.html', {'form': form})


@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    if request.method == "POST":
        book.delete()
        return redirect('books')

    return render(request, 'delete_book.html', {'book': book})


@login_required
def mark_as_read(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.is_read = True
    book.save()
    return redirect('books')

""" Member Settings """


@login_required
def member(request):
    filter_verification = request.GET.get('status', 'all')
    search_query = request.GET.get('search', '')

    members = Member.objects.all()

    if filter_verification == 'completed':
        members = members.filter(is_verificated=True)
    elif filter_verification == 'incomplete':
        members = members.filter(is_verificated=False)

    if search_query:
        members = members.filter(
            Q(username__icontains=search_query) | Q(email__icontains=search_query)
        )

    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('member')
    else:
        form = MemberForm()

    return render(request, 'member.html', {'members': members, 'form': form})



@login_required
def edit_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)

    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('member')
    else:
        form = MemberForm(instance=member)

    return render(request, 'edit_member.html', {'form': form})


@login_required()
def delete_member(request, member_id):
    member = get_object_or_404(Member, pk=member_id)

    if request.method == "POST":
        member.delete()
        return redirect('member')

    return render(request, 'delete_member.html', {'member': member})


""" Task Settings """


@login_required()
def task_list(request):
    filter_status = request.GET.get('status', 'all')
    if filter_status == 'completed':
        tasks = Task.objects.filter(completed=True)
    elif filter_status == 'incomplete':
        tasks = Task.objects.filter(completed=False)
    else:
        tasks = Task.objects.all()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_list.html', {'tasks': tasks, 'form': form})


def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_edit.html', {'form': form, 'task': task})


def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')


def task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = True
    task.save()
    return redirect('task_list')


def task_incomplete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = False
    task.save()
    return redirect('task_list')

