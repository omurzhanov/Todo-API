from .serializers import TodoSerializer
from .models import Todo
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .permissions import IsAuthor


class TodoListView(ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        todos = Todo.objects.get_my_todos(self.request)
        return todos

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TodoDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAuthor]
