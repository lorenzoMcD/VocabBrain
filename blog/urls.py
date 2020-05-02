from . import views
from .views import PostCreateView
from .views import PostDetailView
from .views import PostListView
from django.urls import path


urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('about/', views.about, name='blog-about'),
    path('teacher_lookup/', views.teacher_lookup, name='blog-teacher_lookup'),
]
