from django.db import models
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, date_of_birth, avatar, password=None,):
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, email, date_of_birth, avatar, password):
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            avatar=avatar,
            password=password

class FollowingManager(models.Manager):
    def get_queryset(self):
        return super(FollowingManager, self).get_queryset().values('following')


