from . import views
from .views import FolderDeleteView
from .views import FolderDetailView
from .views import FolderUpdateView
from .views import PostCreateView
from .views import PostDeleteView
from .views import PostDetailView
from .views import PostListView
from .views import PostUpdateView
from .views import TestDeleteView
from .views import TestDetailView
from .views import TestUpdateView
from .views import TesttakerDeleteView
from .views import TesttakerDetailView
from .views import TesttakerListView
from .views import UserPostListView
from .views import UserTestListView
from .views import UserWordListView
from .views import WordListDeleteView
from .views import WordListDetailView
from .views import WordListUpdateView
from .views import UserFolderView
from .views import Announcements
from django.urls import path


urlpatterns = [
    path('', views.landing, name='blog-landing'),
    path('home/', views.home, name='blog-home'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('teacher_lookup/<str:username>/', UserPostListView.as_view(), name='blog-teacher_search_result'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    path('create_folder/new/', views.create_folder, name='folder-create'),
    path('folder/<int:pk>/', FolderDetailView.as_view(), name='folder-detail'),
    path('folder/<int:pk>/update/', FolderUpdateView.as_view(), name='folder-update'),
    path('folder/<int:pk>/delete/', FolderDeleteView.as_view(), name='folder-delete'),
    path('user/folder/<str:username>/', UserFolderView.as_view(), name='user-folders'),


    path('about/', views.about, name='blog-about'),

    path('gameDemo/',views.gameDemo,name='blog-gameDemo'),
    path('teacher_lookup/', views.teacher_lookup, name='blog-teacher_lookup'),

    path('create_word_list/<int:pk>/', views.create_word_list, name='blog-create_word_list'),



    path('suggestions/', views.suggestions, name='blog-suggest'),

    path('announcements/', Announcements.as_view(), name='blog-announce'),

    path('student_tracker/', views.student_tracker, name='blog-student_tracker'),
    path('groups/', views.groups, name='blog-groups'),
    path('groups/<str:username>/', UserPostListView.as_view(), name='blog-groups_search'),

    path('create_list/new/', views.create_list, name='list-create'),

    path('wordlist_form/<int:pk>/update/', WordListUpdateView.as_view(), name='list-update'),

    path('wordlist/<int:pk>/delete/', WordListDeleteView.as_view(), name='list-delete'),

    path('wordlist/<int:pk>/', WordListDetailView.as_view(), name='list-detail'),

    path('user/wordlist/<str:username>/', UserWordListView.as_view(), name='user-lists'),

    path('temp/', views.temp, name='blog-temp'),

    path('temp2/', views.temp2, name='blog-temp2'),

    path('word_list_defs/<int:pk>/', views.word_list_defs, name='word_list_defs'),

    path('word_list_sents/<int:pk>/', views.word_list_sents, name='word_list_sents'),

    path('sent_match_5/<int:pk>/', views.sent_match_5, name='blog-sent_match_5'),


    path('def_match_5/<int:pk>/', views.def_match_5, name='blog-def_match_5'),

    path('print_vocab_sent/<int:pk>/', views.print_vocab_sent, name='blog-print_vocab_sent'),

    path('print_vocab_def/<int:pk>/', views.print_vocab_def, name='blog-print_vocab_def'),

    path('test_create/new/', views.test_create, name='test-create'),


    path('test_form/<int:pk>/update/', TestUpdateView.as_view(), name='test-update'),

    path('test/<int:pk>/delete/', TestDeleteView.as_view(), name='test-delete'),

    path('test/<int:pk>/', TestDetailView.as_view(), name='test-detail'),

    path('user/test/<str:username>/', UserTestListView.as_view(), name='user-tests'),

    path('vocab_test/<int:pk>/', views.vocab_test, name='blog-vocab_test'),

    path('user/results/<str:username>/', TesttakerListView.as_view(), name='user-testtaker'),

    path('testtaker/<int:pk>/', TesttakerDetailView.as_view(), name='testtaker-detail'),

    path('testtaker/<int:pk>/delete/', TesttakerDeleteView.as_view(), name='testtaker-delete'),

    path('flash_card/<int:pk>/', views.flash_card_5, name='blog-flash_card'),

    path('track_progress/', views.track_progress, name='blog-track_progress'),


    path('jumbled_game/<int:pk>/', views.jumbled_game, name='blog-jumbled_words'),

    path('def_match_10/<int:pk>/', views.def_match_10, name='blog-def_match_10'),


    path('sent_match_10/<int:pk>/', views.sent_match_10, name='blog-sent_match_10'),

    path('flash_card_10/<int:pk>/', views.flash_card_10, name='blog-flash_card_10'),


    path('jumbled_game_10/<int:pk>/', views.jumbled_game_10, name='blog-jumbled_game_10'),
]
