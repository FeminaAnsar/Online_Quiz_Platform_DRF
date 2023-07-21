from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50,unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','username']

    def get_created_quizzes(self):
        return self.quiz_set.all()

    def __str__(self):
        return self.email

# Create your models here.
