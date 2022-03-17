from django.urls import path
from .views import TodoListView, TodoDetailView

urlpatterns = [
    path('', TodoListView.as_view(), name='todos-list'),
    path('<int:pk>/', TodoDetailView.as_view(), name='todo-detail'),
]