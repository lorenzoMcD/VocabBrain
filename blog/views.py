from .filters import OrderFilter
from .models import Post
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView
from wiktionaryparser import WiktionaryParser
from.models import WordList
from.models import Word
from.form import WordListForm

# page that shows posts by every user on site
def home(request):

    context = {

        'posts': Post.objects.all()
    }

    return render(request, 'blog/home.html', context)


# this web page will show list of teachers on site
@login_required
def teacher_lookup(request):
    users = User.objects.filter(groups__name='Teacher')
    myFilter = OrderFilter(request.GET, queryset=users)
    users = myFilter.qs

    context = {

        'users': users, 'myFilter': myFilter
    }

    if request.method == 'POST':

        # this resets the filter if the reset button is pushed
        if 'reset' in request.POST:
            return redirect('blog-teacher_lookup')

        nme = request.POST.get('group_name')
        group = Group.objects.get(name=nme)

    # adds that user to the group
        request.user.groups.add(group)
    # prints message at top of screen if success then redirect user to desired page

        messages.success(request, f'You have successfully been added to this group')

        return redirect('blog-teacher_lookup')

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


# class for update blog post
class WordListUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = WordList
    fields = ['title', 'description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        # function -- if user that posts blog is log in then they can post to blog.... else they can't
        wordlist = self.get_object()
        if self.request.user == wordlist.author:
            return True
        return False

class WordListDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = WordList
    success_url = '/'

    def test_func(self):
        wordlist = self.get_object()
        if self.request.user == wordlist.author:
            return True
        return False


class WordListDetailView(DetailView):

    model = WordList


class UserWordListView(ListView):

    model = WordList
    template_name = 'blog/user_lists.html'
    context_object_name = 'posts'
    paginate_by = 4  # this will change number of posts visible per page

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return WordList.objects.filter(author=user)


# class for delete a blog post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


class WikiSearch:
    word = None

    def get_defs(word):
        parser = WiktionaryParser()
        lookup = parser.fetch(word)
        definitions = []
        for items in lookup:
            wordlist = (items['definitions'][0]['text'])

        for defs in wordlist:

            definitions.append(defs)

        return(definitions)

    def get_sent(word):
        parser = WiktionaryParser()
        lookup = parser.fetch(word)
        sentences = []
        for items in lookup:
            wordlist = (items['definitions'][0]['examples'])

        for sent in wordlist:

            sentences.append(sent)

        return(sentences)


# we might need to rename this....
# This page starts our wordlist creation user will type in title and desc
@login_required
def create_list(request):
    if request.method == 'POST':
        form = WordListForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.author = request.user
            user.save()

            messages.success(request, f'Your Wordlist creation has started, now add terms to Your list')

            return redirect('blog-create_word_list')
    else:
        form = WordListForm()
    return render(request, 'blog/create_list.html', {'form': form})

# this second part of word list creation
# this page user can add terms to their word list


@login_required
def create_word_list(request):
    # we can set the number extra text boxes in form by adding extra
    # to var below ex.  wordformset = modelformset_factory(Word, fields=('term',),extra=4)
    wordformset = modelformset_factory(Word, fields=('term',))
    formset = wordformset(request.POST or None, queryset=Word.objects.none())

    if request.method == "POST":
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.author_id = request.user.id
                instance.save()

            messages.success(request, f'You have added terms to your list')

            # will need to redirect to page where we add sent and def next. for now gonna set this to home
            return redirect('blog-home')

    context = {
        'formset': formset

    }
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

        'users': users, 'myFilter': myFilter
    }

    # this resets the filter if the reset button is pushed
    if request.method == 'POST':

        if 'reset' in request.POST:
            return redirect('blog-student_tracker')

    return render(request, 'blog/student_tracker.html', context)


# this page will show all groups that user is part of
# will have button for user to leave group
def groups(request):
    users = User.objects.filter(groups__name='Teacher')
    myFilter = OrderFilter(request.GET, queryset=users)
    users = myFilter.qs

    context = {
        'users': users, 'myFilter': myFilter
    }

    # checks if button is pushed on page
    # if button is pushed then sends a post request with data we need
    # which is the name of group
    if request.method == 'POST':

        # this resets the filter if the reset button is pushed
        if 'reset' in request.POST:
            return redirect('blog-groups')

        nme = request.POST.get('group_name')
        group = Group.objects.get(name=nme)

    # adds that user to the group
        # request.user.groups.add(group)

    # removes user from group
        group.user_set.remove(request.user)

    # prints a message if the group was removed , then redirects user to desired page
        messages.success(request, f'You have successfully left this group')

        return redirect('blog-groups')

    return render(request, 'blog/groups.html', context)


def temp(request):
    context = {

        'lists': WordList.objects.all()
    }

    return render(request, 'blog/temp.html', context)
