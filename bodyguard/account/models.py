from django.contrib.auth.models import User
from django.db import models


class UserType(models.Model):
    name = models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)
