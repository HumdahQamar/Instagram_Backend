from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.conf import settings
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager, FollowingManager, FollowerManager

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('Username'), max_length=40, unique=True)
    email = models.EmailField(_('Email Address'), unique=True)
    first_name = models.CharField(_('First Name'), max_length=50)
    last_name = models.CharField(_('Last Name'), max_length=50, )
    date_of_birth = models.DateField(_('Date of Birth'), blank=False, null=False)
    bio = models.TextField(_('Bio'), max_length=300)
    avatar = models.ImageField(upload_to='avatars/', blank=True, default='default_avatar.png',
                               width_field="width_field", height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    following = models.ManyToManyField('self', blank=True, symmetrical=False)
    is_active = models.BooleanField(_('Active'), default=True)
    is_admin = models.BooleanField(_('Admin'), default=False)
    date_joined = models.DateTimeField(_('Date Joined'), auto_now_add=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'date_of_birth', ]

    objects = UserManager()

    all_following = FollowingManager()
    all_followers = FollowerManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        return self.first_name+' '+self.last_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin



class FollowRelation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followee', on_delete=models.CASCADE)
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='follower', on_delete=models.CASCADE)
    followed_at = models.DateTimeField(auto_now_add=True)



class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/', null=False, blank=False, default='default_avatar.png')
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    like_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.like_timestamp)+' '+self.user.username

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    comment_timestamp = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=150, null=False)

    def __str__(self):
        return self.text
