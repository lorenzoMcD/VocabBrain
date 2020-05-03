from .filters import OrderFilter
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView


def home(request):
    context = {
        'posts': Post.objects.all()
    }

    return render(request, 'blog/home.html', context)



# this web page will show list of teachers on site
# will be able to filter by user,email
# still need to have link to access teacher individual profiles
def teacher_lookup(request):
    users = User.objects.filter(groups__name='Teacher')
    myFilter = OrderFilter(request.GET, queryset=users)
    users = myFilter.qs

    context = {
        #'users': User.objects.all()
        'users': User.objects.filter(groups__name='Teacher'), 'myFilter': myFilter
    }

    return render(request, 'blog/teacher_lookup.html', context)


class PostListView(ListView):

    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']   # shows newest posts at the top of page


class PostDetailView(DetailView):

    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):

    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def create_word_list(requests):

    return render(request, 'blog/create_word_list.html', context)
