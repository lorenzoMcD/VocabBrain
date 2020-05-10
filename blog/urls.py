from . import views
from .views import PostCreateView
from .views import PostDeleteView
from .views import PostDetailView
from .views import PostListView
from .views import PostUpdateView
from .views import UserPostListView
from .views import create_list
from django.urls import path


urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('teacher_lookup/<str:username>/', UserPostListView.as_view(), name='blog-teacher_search_result'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('teacher_lookup/', views.teacher_lookup, name='blog-teacher_lookup'),
    path('create_word_list/new/', views.create_word_list, name='blog-create_word_list'),
    path('faq/', views.faq, name='blog-faq'),

    path('student_tracker/', views.student_tracker, name='blog-student_tracker'),
    path('groups/', views.groups, name='blog-groups'),
    path('groups/<str:username>/', UserPostListView.as_view(), name='blog-groups_search'),

    path('create_list/new/', views.create_list, name='list-create'),

]
