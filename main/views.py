from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .models import Task, Member, Book, Post, User
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


""" Post and User relation """


@login_required
def posts(request):
    users = User.objects.all()
    posts = Post.objects.all()

    active_user_id = request.GET.get("user_id")
    active_user = User.objects.filter(id=active_user_id).first()

    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post = get_object_or_404(Post, id=post_id)

        if active_user:
            if active_user in post.liked_by.all():
                post.liked_by.remove(active_user)
            else:
                post.liked_by.add(active_user)
        return redirect("posts")

    return render(request, "posts/posts.html", {
        "users": users,
        "posts": posts,
        "active_user": active_user
    })


@login_required
def like_post(request, post_id, user_id):
    post = get_object_or_404(Post, id=post_id)
    user = get_object_or_404(User, id=user_id)

    if user in post.liked_by.all():
        post.liked_by.remove(user)
    else:
        post.liked_by.add(user)

    return redirect("posts")


@login_required
def create_user(request):
    users = User.objects.all()
    error_message = None

    if request.method == "POST":
        username = request.POST.get("username")
        bio = request.POST.get("bio")
        user_id = request.POST.get("user_id")

        if user_id:
            user = get_object_or_404(User, id=user_id)
            user.username = username
            user.bio = bio
            try:
                user.save()
            except IntegrityError:
                error_message = f"Username '{username}' is already taken."
        else:
            try:
                User.objects.create(username=username, bio=bio)
            except IntegrityError:
                error_message = f"Username '{username}' is already taken."

        if not error_message:
            return redirect("create_user")

    return render(request, "posts/create_user.html", {
        "users": users,
        "error_message": error_message
    })


@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect("create_user")


@login_required
def create_post(request):
    posts = Post.objects.all()
    users = User.objects.all()

    if request.method == "POST":
        title = request.POST.get("title")
        author_id = request.POST.get("author_id")

        if title and author_id:
            author = get_object_or_404(User, id=author_id)
            Post.objects.create(title=title, author=author)
            return redirect("create_post")
        else:
            error_message = "Please select an author."
            return render(request, "posts/create_post.html", {"posts": posts, "users": users, "error_message": error_message})

    return render(request, "posts/create_post.html", {"posts": posts, "users": users})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    users = User.objects.all()

    if request.method == "POST":
        title = request.POST.get("title")
        author_id = request.POST.get("author_id")

        if title and author_id:
            author = get_object_or_404(User, id=author_id)
            post.title = title
            post.author = author
            post.save()
            return redirect("create_post")

    return render(request, "posts/edit_post.html", {"post": post, "users": users})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect("create_post")


""" ---Book Settings--- """

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


""" ---Member Settings--- """


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


""" ---Task Settings--- """


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

