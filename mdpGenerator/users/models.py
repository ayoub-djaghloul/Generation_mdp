from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()


class compte(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.CharField(max_length=30)
    password = models.CharField(max_length=100)
    date = models.DateTimeField(default=now)
    def __str__(self):
        return f"{self.platform_name} account for {self.user.username}"

