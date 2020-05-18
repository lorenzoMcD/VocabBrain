from . import views
from .views import PostCreateView
from .views import PostDeleteView
from .views import PostDetailView
from .views import PostListView
from .views import PostUpdateView
from .views import UserPostListView
from .views import UserWordListView
from .views import WordListDeleteView
from .views import WordListDetailView
from .views import WordListUpdateView
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
    path('create_word_list/<int:pk>/', views.create_word_list, name='blog-create_word_list'),
    path('faq/', views.faq, name='blog-faq'),

    path('student_tracker/', views.student_tracker, name='blog-student_tracker'),
    path('groups/', views.groups, name='blog-groups'),
    path('groups/<str:username>/', UserPostListView.as_view(), name='blog-groups_search'),

    path('create_list/new/', views.create_list, name='list-create'),

    path('wordlist_form/<int:pk>/update/', WordListUpdateView.as_view(), name='list-update'),

    path('wordlist/<int:pk>/delete/', WordListDeleteView.as_view(), name='list-delete'),

    path('wordlist/<int:pk>/', WordListDetailView.as_view(), name='list-detail'),

    path('user/wordlist/<str:username>/', UserWordListView.as_view(), name='user-lists'),

    path('temp/', views.temp, name='blog-temp'),

    path('word_list_defs/<int:pk>/', views.word_list_defs, name='word_list_defs'),

    path('word_list_sents/<int:pk>/', views.word_list_sents, name='word_list_sents'),

    path('vocab_game/<int:pk>/', views.vocab_game, name='blog-vocab_game'),
]
