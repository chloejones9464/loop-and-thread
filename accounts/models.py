from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    display_name = models.CharField(
        max_length=50,
        blank=True
    )

    def __str__(self):
        return self.display_name or self.user.get_username()
    