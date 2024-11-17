from django.core.validators import MinValueValidator
from django.db import models


""" Task List """


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


""" Member manager """


class Member(models.Model):
    username = models.CharField(max_length=32)
    email = models.EmailField(blank=True, null=True)
    is_verificated = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.email:
            self.is_verificated = True
        else:
            self.is_verificated = False
        super().save(*args, **kwargs)


""" Book manager """


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    pages = models.IntegerField(validators=[MinValueValidator(0)])
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class User(models.Model):
    username = models.CharField(max_length=32, unique=True)
    bio = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.username


class Post(models.Model):
    title = models.CharField(max_length=128)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    liked_by = models.ManyToManyField(User, related_name="liked_posts")

    def __str__(self):
        return f"Title: {self.title} | Author: {self.author.username}"
