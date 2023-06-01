from django.db import models
from django.http import Http404
from django.shortcuts import get_object_or_404

# Create your models here.

class Users(models.Model):
    chat_id = models.IntegerField()

    user = models.CharField(max_length=255)
    step = models.CharField(max_length=50)

    is_superuser = models.BooleanField(default=False)

    @classmethod
    def get_or_create(cls, chat_id) -> list:
        
        is_created=False
        try:
            user = get_object_or_404(klass=cls, chat_id=chat_id)
        except Http404:
            user = cls(chat_id=chat_id, step='/')
            is_created = True
        user.save()
        return user, is_created


class Settings(models.Model):
    welcome_message = models.CharField(max_length=255)