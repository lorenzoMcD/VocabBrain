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
import random

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

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['words'] = Word.objects.filter(wordlist__id=self.kwargs['pk'])
        return context


class UserWordListView(ListView):

    model = WordList
    template_name = 'blog/user_lists.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
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

            return redirect('blog-create_word_list', pk=user.id)
    else:
        form = WordListForm()
    return render(request, 'blog/create_list.html', {'form': form})

# this second part of word list creation
# this page user can add terms to their word list


@login_required
def create_word_list(request, pk):
    wordlist = WordList.objects.get(pk=pk)
    wordformset = inlineformset_factory(WordList, Word, fields=('term',), extra=1)

    if request.method == "POST":
        formset = wordformset(request.POST, instance=wordlist)
        if 'done' in request.POST:
            if formset.is_valid():
                formset.save()
                messages.success(request, f'You have added terms to your list')
                return redirect('word_list_defs', pk=pk)

        if formset.is_valid():
            formset.save()

    formset = wordformset(instance=wordlist)
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


def word_list_defs(request, pk):
    wordlist = WordList.objects.get(pk=pk)
    a = wordlist.id
    # gets words from user word list
    words = Word.objects.filter(wordlist__id=pk)

    if request.method == 'POST':
        # this process adds the definiton to users wordlist
        if 'term_def' in request.POST:
            def_to_add = request.POST.get('term_def')
            wrd_id = request.POST["word-id"]
            wrd = Word.objects.get(id=wrd_id)
            wrd.definition = def_to_add
            wrd.save()
            messages.success(request, f'You have successfully added definition to your term')

        if 'text_input' in request.POST:
            def_to_add = request.POST.get('text_input')
            wrd_id = request.POST["user_add"]
            wrd = Word.objects.get(id=wrd_id)
            wrd.definition = def_to_add
            wrd.save()
            messages.success(request, f'You have successfully added custom definition to your term')

        if 'done' in request.POST:
            messages.success(request, f'You are done adding definitions')
            return redirect('word_list_sents', pk=pk)

    context = {
        'words': words
    }

    return render(request, 'blog/word_list_defs.html', context)


def word_list_sents(request, pk):
    wordlist = WordList.objects.get(pk=pk)
    a = wordlist.id
    # gets words from user word list
    words = Word.objects.filter(wordlist__id=pk)

    if request.method == 'POST':
        # this process adds the definiton to users wordlist
        if 'term_sent' in request.POST:
            sent_to_add = request.POST.get('term_sent')
            wrd_id = request.POST["word-id"]
            wrd = Word.objects.get(id=wrd_id)
            wrd.sentence = sent_to_add
            wrd.save()
            messages.success(request, f'You have successfully added sentence to your term')

        if 'text_input' in request.POST:
            sent_to_add = request.POST.get('text_input')
            wrd_id = request.POST["user_add"]
            wrd = Word.objects.get(id=wrd_id)
            wrd.sentence = sent_to_add
            wrd.save()
            messages.success(request, f'You have successfully added custom definition to your term')

        if 'done' in request.POST:
            messages.success(request, f'Your wordlist is complete')
            return redirect('blog-home')

    context = {
        'words': words
    }

    return render(request, 'blog/word_list_sents.html', context)


def sent_match_5(request, pk):
    wordlist = WordList.objects.get(pk=pk)
    a = wordlist.id
    words = Word.objects.filter(wordlist__id=a)
    sentences = Word.objects.filter(wordlist__id=a)
    sentlist = []
    deflist = []
    termlist = []
    for i in words:
        sentlist.append(i.sentence)
        deflist.append(i.definition)
        termlist.append(i.term)
    # if user has more than 5 terms create new list that adds random 5 terms to list
    new_list_terms = []
    new_list_sents = []
    # if length of term list > 5 take random 5 items from terms
    # then find the matching sents from the word model and match
    # them with terms
    if len(termlist) > 5:
        new_list_terms += random.sample(termlist, 5)
        for i in new_list_terms:
            for word in words:
                if i == word.term:
                    new_list_sents.append(word.sentence)
        terms = (new_list_terms)
        mysent = (new_list_sents)
    else:
        terms = (termlist)
        mysent = (sentlist)
    # this mod will shuffle both lists at same time
    # but keep their order
    from sklearn.utils import shuffle
    terms, mysent = shuffle(terms, mysent)
    context = {
        'mysent': mysent, 'terms': terms
    }
    return render(request, 'blog/sent_match_5.html', context)


def sent_match_4(request, pk):
    wordlist = WordList.objects.get(pk=pk)
    a = wordlist.id
    words = Word.objects.filter(wordlist__id=a)
    sentences = Word.objects.filter(wordlist__id=a)
    sentlist = []
    deflist = []
    termlist = []
    for i in words:
        sentlist.append(i.sentence)
        deflist.append(i.definition)
        termlist.append(i.term)
    # if user has more than 4 terms create new list that adds random 4 terms to list
    new_list_terms = []
    new_list_sents = []
    # if length of term list > 4 take random 4 items from terms
    # then find the matching sents from the word model and match
    # them with terms
    if len(termlist) > 4:
        new_list_terms += random.sample(termlist, 4)
        for i in new_list_terms:
            for word in words:
                if i == word.term:
                    new_list_sents.append(word.sentence)
        terms = (new_list_terms)
        mysent = (new_list_sents)
    else:
        terms = (termlist)
        mysent = (sentlist)
    # this mod will shuffle both lists at same time
    # but keep their order
    from sklearn.utils import shuffle
    terms, mysent = shuffle(terms, mysent)
    context = {
        'mysent': mysent, 'terms': terms
    }
    return render(request, 'blog/sent_match_4.html', context)


def sent_match_3(request, pk):
    wordlist = WordList.objects.get(pk=pk)
    a = wordlist.id
    words = Word.objects.filter(wordlist__id=a)
    sentences = Word.objects.filter(wordlist__id=a)
    sentlist = []
    deflist = []
    termlist = []
    for i in words:
        sentlist.append(i.sentence)
        deflist.append(i.definition)
        termlist.append(i.term)
    # if user has more than 3 terms create new list that adds random 3 terms to list
    new_list_terms = []
    new_list_sents = []
    # if length of term list > 3 take random 3 items from terms
    # then find the matching sents from the word model and match
    # them with terms
    if len(termlist) > 3:
        new_list_terms += random.sample(termlist, 3)
        for i in new_list_terms:
            for word in words:
                if i == word.term:
                    new_list_sents.append(word.sentence)
        terms = (new_list_terms)
        mysent = (new_list_sents)
    else:
        terms = (termlist)
        mysent = (sentlist)
    # this mod will shuffle both lists at same time
    # but keep their order
    from sklearn.utils import shuffle
    terms, mysent = shuffle(terms, mysent)

    context = {
        'mysent': mysent, 'terms': terms
    }

    return render(request, 'blog/sent_match_3.html', context)


def def_match_5(request, pk):
    wordlist = WordList.objects.get(pk=pk)
    a = wordlist.id
    words = Word.objects.filter(wordlist__id=a)
    sentences = Word.objects.filter(wordlist__id=a)

    deflist = []
    termlist = []
    for i in words:
        deflist.append(i.definition)
        termlist.append(i.term)
    # if user has more than 5 terms create new list that adds random 5 terms to list
    new_list_terms = []
    new_list_defs = []
    # if length of term list > 5 take random 5 items from terms
    # then find the matching defs from the word model and match
    # them with terms
    if len(termlist) > 5:
        new_list_terms += random.sample(termlist, 5)
        for i in new_list_terms:
            for word in words:
                if i == word.term:
                    new_list_defs.append(word.definition)
        terms = (new_list_terms)
        mydefs = (new_list_defs)
    else:
        terms = (termlist)
        mydefs = (deflist)
    # this mod will shuffle both lists at same time
    # but keep their order
    from sklearn.utils import shuffle
    terms, mydefs = shuffle(terms, mydefs)

    context = {
        'mydefs': mydefs, 'terms': terms
    }

    return render(request, 'blog/def_match_5.html', context)


def def_match_4(request, pk):
    wordlist = WordList.objects.get(pk=pk)
    a = wordlist.id
    words = Word.objects.filter(wordlist__id=a)
    sentences = Word.objects.filter(wordlist__id=a)

    deflist = []
    termlist = []
    for i in words:
        deflist.append(i.definition)
        termlist.append(i.term)
    # if user has more than 4 terms create new list that adds random 4 terms to list
    new_list_terms = []
    new_list_defs = []
    # if length of term list > 4 take random 4 items from terms
    # then find the matching defs from the word model and match
    # them with terms
    if len(termlist) > 4:
        new_list_terms += random.sample(termlist, 4)
        for i in new_list_terms:
            for word in words:
                if i == word.term:
                    new_list_defs.append(word.definition)
        terms = (new_list_terms)
        mydefs = (new_list_defs)
    else:
        terms = (termlist)
        mydefs = (deflist)
    # this mod will shuffle both lists at same time
    # but keep their order
    from sklearn.utils import shuffle
    terms, mydefs = shuffle(terms, mydefs)

    context = {
        'mydefs': mydefs, 'terms': terms
    }

    return render(request, 'blog/def_match_4.html', context)


def def_match_3(request, pk):
    wordlist = WordList.objects.get(pk=pk)
    a = wordlist.id
    words = Word.objects.filter(wordlist__id=a)
    sentences = Word.objects.filter(wordlist__id=a)

    deflist = []
    termlist = []
    for i in words:
        deflist.append(i.definition)
        termlist.append(i.term)
    # if user has more than 3 terms create new list that adds random 3 terms to list
    new_list_terms = []
    new_list_defs = []
    # if length of term list > 3 take random 3 items from terms
    # then find the matching defs from the word model and match
    # them with terms
    if len(termlist) > 3:
        new_list_terms += random.sample(termlist, 3)
        for i in new_list_terms:
            for word in words:
                if i == word.term:
                    new_list_defs.append(word.definition)
        terms = (new_list_terms)
        mydefs = (new_list_defs)
    else:
        terms = (termlist)
        mydefs = (deflist)
    # this mod will shuffle both lists at same time
    # but keep their order
    from sklearn.utils import shuffle
    terms, mydefs = shuffle(terms, mydefs)

    context = {
        'mydefs': mydefs, 'terms': terms
    }

    return render(request, 'blog/def_match_3.html', context)


def print_vocab_sent(request, pk):

    wordlist = WordList.objects.get(pk=pk)
    a = wordlist.id
    words = Word.objects.filter(wordlist__id=a)
    sentences = Word.objects.filter(wordlist__id=a)
    sentlist = []
    for i in words:
        sentlist.append(i.sentence)

    random.shuffle(sentlist)

    mylists = (words)
    mysent = (sentlist)

    context = {

        'words': words, 'sents': sentlist
    }

    return render(request, 'blog/print_vocab_sent.html', context)
