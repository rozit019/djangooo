from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(
        max_length=10,
        choices=[('Low', 'Low'), ('Normal', 'Normal'), ('High', 'High')],
        default='Normal'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

def user_profile_pic_path(instance, filename):
    return f'profile_pics/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')


    def __str__(self):
        return f"{self.user.username}'s Profile"