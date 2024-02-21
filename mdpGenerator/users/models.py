from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
class profile(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()

    def __str__(self):
        return self.user.username
