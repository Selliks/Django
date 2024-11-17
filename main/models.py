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


