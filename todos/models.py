from django.db import models
from users.models import CustomUser

class ToDoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def get_my_todos(self, request):
        return super().get_queryset().filter(author=request.user.id)

class Todo(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    objects = ToDoManager()
    
    def __str__(self):
        return self.title
