from .filters import OrderFilter
from .models import Post
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import CreateView
from django.views.generic import DeleteView
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


@login_required
def teacher_lookup(request):
    users = User.objects.filter(groups__name='Teacher')
    myFilter = OrderFilter(request.GET, queryset=users)
    users = myFilter.qs

    context = {
        #'users': User.objects.all()
        'users': User.objects.filter(groups__name='Teacher'), 'myFilter': myFilter
    }

    # trying to create join group button on teacherlookup page
    if request.method == 'POST':

        nme = request.POST.get('group_name')
        group = Group.objects.get(name=nme)

    # adds that user to the group

        # need a if statment to check if user is already part of group...

        request.user.groups.add(group)

        messages.success(request, f'You have successfully been added to this group')

        return redirect('blog-home')

    return render(request, 'blog/teacher_lookup.html', context)


class PostListView(ListView):

    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']   # shows newest posts at the top of page
    paginate_by = 4  # this will change number of posts visible per page


class UserPostListView(ListView):

    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 4  # this will change number of posts visible per page

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):

    model = Post

# class for create blog post
class PostCreateView(LoginRequiredMixin, CreateView):

    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# class for update blog post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        # function -- if user that posts blog is log in then they can post to blog.... else they can't
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# class for delete a blog post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Post
    success_url = '/'

    def test_func(self):
           # function -- if user that posts blog is log in then they can post to blog.... else they can't
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def create_word_list(requests):

    return render(request, 'blog/create_word_list.html', context)

def faq(request):

    return render(request, 'blog/faq.html', {'title': 'FAQ'})


def student_tracker(request):

    # grab current users name if teacher
    # pull up all people in their group

    name = request.user.username

    users = User.objects.filter(groups__name=name)
    myFilter = OrderFilter(request.GET, queryset=users)
    users = myFilter.qs

    context = {

        'users': User.objects.filter(groups__name=name), 'myFilter': myFilter
    }

    return render(request, 'blog/student_tracker.html', context)
