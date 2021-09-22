from .filters import OrderFilter
from .filters import ProgressFilter
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
from.models import Test
from.models import Testtaker
from.models import Folder
from.form import WordListForm
from.form import TestCreateForm
from.form import TestSubmitForm
from.form import SuggestionForm
from.form import FolderCreateForm
import random


# home page of site, this page has announcement section(posts), wordlist,test tables so
# teacher or student can see their created or assigned content on front page.
@login_required
def home(request):
    users = request.user.groups.all()

    folder = Folder.objects.filter(author=request.user)

    posts = Post.objects.order_by('-date_posted')[0:1]

    wordlist = WordList.objects.filter(author=request.user)
    test = Test.objects.filter(author=request.user)
    context = {

        'lists': wordlist, 'tests': test, 'posts': posts, 'users': users, 'folders': folder
    }

    return render(request, 'blog/home.html', context)

# landing page when people first come to site they see this page.
def landing(request):

    return render(request, 'blog/landing.html')


# this web page will show list of teachers on site
# students will then be able to click a join button to
# join the group of teacher they want.
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

# class based view for viewing posts for everyuser
class PostListView(ListView):

    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']   # shows newest posts at the top of page
    paginate_by = 4  # this will change number of posts visible per page

# class based for for viewing list of current user posts
class UserPostListView(ListView):

    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 4  # this will change number of posts visible per page

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


# class for viewing posts in detail
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


# class based view for update wordlist
class WordListUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = WordList
    fields = ['title', 'description', 'worksheet_text', 'folder']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        # function -- if user that posts blog is log in then they can post to blog.... else they can't
        wordlist = self.get_object()
        if self.request.user == wordlist.author:
            return True
        return False


class FolderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Folder
    fields = ['title', 'description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):

        folder = self.get_object()
        if self.request.user == folder.author:
            return True
        return False


class FolderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Folder
    success_url = '/home/'

    def test_func(self):
        folder = self.get_object()
        if self.request.user == folder.author:
            return True
        return False


# class based view for folder detail page
class FolderDetailView(DetailView):

    model = Folder

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['lists'] = WordList.objects.filter(folder__id=self.kwargs['pk'])
        return context

# class based view for user wordlists
class UserFolderView(ListView):

    model = Folder
    template_name = 'blog/user_folders.html'
    context_object_name = 'folders'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Folder.objects.filter(author=user)


# class based view for wordlist delete view
class WordListDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = WordList
    success_url = '/home/'

    def test_func(self):
        wordlist = self.get_object()
        if self.request.user == wordlist.author:
            return True
        return False

# class based view for wordlist detail page
class WordListDetailView(DetailView):

    model = WordList

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['words'] = Word.objects.filter(wordlist__id=self.kwargs['pk'])
        return context

# class based view for user wordlists
class UserWordListView(ListView):

    model = WordList
    template_name = 'blog/user_lists.html'
    context_object_name = 'lists'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return WordList.objects.filter(author=user)

    def get_context_data(self, **kwargs):
        context = super(UserWordListView, self).get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context.update({
            'folders': Folder.objects.filter(author=user),
            'tests': Test.objects.filter(author=user)
        })
        return context


# class based view for user test list view
class UserTestListView(ListView):

    model = Test
    template_name = 'blog/user_tests.html'
    context_object_name = 'users'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Test.objects.filter(author=user)

# class based view for testaker listview
class TesttakerListView(ListView):

    model = Testtaker
    template_name = 'blog/user_testtakers.html'
    context_object_name = 'users'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Testtaker.objects.filter(tester=user)

# class based view for testtaker detail
class TesttakerDetailView(DetailView):

    model = Testtaker

# class based view for testtaker delete view
class TesttakerDeleteView(LoginRequiredMixin, DeleteView):

    model = Testtaker
    success_url = '/home/'

    def test_func(self):
        testtaker = self.get_object()
        if self.request.user == testtaker.tester:
            return True
        return False

# class based view for test detail page
class TestDetailView(DetailView):

    model = Test

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        test = Test.objects.get(pk=self.kwargs['pk'])
        a = test.wordlist_id
        # wordlist = WordList.objects.get(pk=pk)
        # a = wordlist.id

        context['words'] = Word.objects.filter(wordlist__id=a)
        return context

# class based view for delete test
class TestDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Test
    success_url = '/home/'

    def test_func(self):
        test = self.get_object()
        if self.request.user == test.author:
            return True
        return False

# class based view for updateing the tests
class TestUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Test
    fields = ['title', 'description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        # function -- if user that posts blog is log in then they can post to blog.... else they can't
        test = self.get_object()
        if self.request.user == test.author:
            return True
        return False


# class for delete a blog post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Post
    success_url = '/home/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})



def gameDemo(request):
        return render(request, 'blog/gameDemo.html',{'title':'Game Demo'})




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


# This page starts wordlist creation
@ login_required
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
        form.fields['folder'].queryset = Folder.objects.filter(author=request.user)
    return render(request, 'blog/create_list.html', {'form': form})


# creates a folder for users to store their wordlists
@ login_required
def create_folder(request):
    if request.method == 'POST':
        form = FolderCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.author = request.user
            user.save()
            messages.success(request, f'Your folder has been created.')

            return redirect('blog-home')
    else:
        form = FolderCreateForm()
    return render(request, 'blog/create_folder.html', {'form': form})


# this second part of word list creation
# this page user can add terms to their word list


@ login_required
def create_word_list(request, pk):
    wordlist = WordList.objects.get(pk=pk)
    wordformset = inlineformset_factory(WordList, Word, fields=('term',), extra=10)

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

# student tracker page, that includes table of all students assigened to teacher group


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
    users = request.user.groups.all()

    context = {
        'users': users
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

    # removes user from group
        group.user_set.remove(request.user)

    # prints a message if the group was removed , then redirects user to desired page
        messages.success(request, f'You have successfully left this group')

        return redirect('blog-groups')

    return render(request, 'blog/groups.html', context)

# temp html page used to view all the wordlists on the site
# while in development phase. we may end up keeping this page
# when we deploy


def temp(request):
    context = {

        'lists': WordList.objects.all()
    }

    return render(request, 'blog/temp.html', context)

# temp html page used to view all the tests on the site
# while in development phase. we may end up keeping this page
# when we deploy


def temp2(request):
    context = {

        'tests': Test.objects.all()
    }

    return render(request, 'blog/temp2.html', context)


# page that lets users add defs to their terms


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


# page that lets users add sents to their terms
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


# vocab matching game for the sentences. the game must have 5 terms
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
        termlist.append(i.term.lower())
    # if user has more than 5 terms create new list that adds random 5 terms to list
    new_list_terms = []
    new_list_sents = []
    # if length of term list > 5 take random 5 items from terms
    # then find the matching sents from the word model and match
    # them with terms
    if len(termlist) >= 5:
        new_list_terms += random.sample(termlist, 5)
        for i in new_list_terms:
            for word in words:
                if i == word.term.lower():
                    new_list_sents.append(word.sentence)
        terms = (new_list_terms)
        mysent = (new_list_sents)
    else:
        terms = (termlist)
        mysent = (sentlist)
    # this mod will shuffle both lists at same time
    # but keep their order

    for i in terms:
        mysent = [sub.replace(str(i), '____') for sub in mysent]

    from sklearn.utils import shuffle
    terms, mysent = shuffle(terms, mysent)
    context = {
        'mysent': mysent, 'terms': terms, 'rand_terms': new_list_terms
    }
    return render(request, 'blog/sent_match_5.html', context)

# vocab matching game for the definitions. the game must have 5 terms


def def_match_5(request, pk):
    wordlist = WordList.objects.get(pk=pk)
    a = wordlist.id
    words = Word.objects.filter(wordlist__id=a)
    sentences = Word.objects.filter(wordlist__id=a)

    deflist = []
    termlist = []
    for i in words:
        deflist.append(i.definition)
        termlist.append(i.term.lower())
    # if user has more than 5 terms create new list that adds random 5 terms to list
    new_list_terms = []
    new_list_defs = []
    # if length of term list > 5 take random 5 items from terms
    # then find the matching defs from the word model and match
    # them with terms
    if len(termlist) >= 5:
        new_list_terms += random.sample(termlist, 5)
        for i in new_list_terms:
            for word in words:
                if i == word.term.lower():
                    new_list_defs.append(word.definition)
        terms = (new_list_terms)
        mydefs = (new_list_defs)
    else:
        terms = (termlist)
        mydefs = (deflist)
    # this mod will shuffle both lists at same time
    # but keep their order

    for i in terms:
        mydefs = [sub.replace(str(i), '____') for sub in mydefs]

    from sklearn.utils import shuffle
    terms, mydefs = shuffle(terms, mydefs)

    context = {
        'mydefs': mydefs, 'terms': terms, 'rand_terms': new_list_terms
    }

    return render(request, 'blog/def_match_5.html', context)


# vocab worksheet (sentences)
def print_vocab_sent(request, pk):

    wordlist = WordList.objects.get(pk=pk)
    a = wordlist.id
    words = Word.objects.filter(wordlist__id=a)
    sentences = Word.objects.filter(wordlist__id=a)
    sentlist = []
    terms = []
    for i in words:
        sentlist.append(i.sentence)
        terms.append(i.term)

    from sklearn.utils import shuffle

    for i in terms:
        sentlist = [sub.replace(str(i), '____') for sub in sentlist]

        random.shuffle(sentlist)

    context = {

        'words': words, 'sents': sentlist, 'wordlist': wordlist
    }

    return render(request, 'blog/print_vocab_sent.html', context)


# vocab worksheet (sentences)
def print_vocab_def(request, pk):

    wordlist = WordList.objects.get(pk=pk)
    a = wordlist.id
    words = Word.objects.filter(wordlist__id=a)
    definition = Word.objects.filter(wordlist__id=a)
    deflist = []
    terms = []
    for i in words:
        deflist.append(i.definition)
        terms.append(i.term)

    from sklearn.utils import shuffle

    for i in terms:
        deflist = [sub.replace(str(i), '____') for sub in deflist]

        random.shuffle(deflist)

    context = {

        'words': words, 'defs': deflist, 'wordlist': wordlist
    }

    return render(request, 'blog/print_vocab_def.html', context)


# create new test for students
# allows teacher to import their wordlist to the test
@ login_required
def test_create(request):
    if request.method == 'POST':
        form = TestCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.author = request.user
            user.save()

            messages.success(request, f'Your Test has been created')

            return redirect('blog-home')
    else:
        form = TestCreateForm()
        # this gives teacher drop down list of wordlists that they have created

        form.fields['wordlist'].queryset = WordList.objects.filter(author=request.user)
        form.fields['folder'].queryset = Folder.objects.filter(author=request.user)

    return render(request, 'blog/test_create.html', {'form': form})


# vocab test , after user takes test a score will be saved to their testtaker profile
def vocab_test(request, pk):
    test = Test.objects.get(pk=pk)
    a = test.wordlist_id
    words = Word.objects.filter(wordlist__id=a)
    sentences = Word.objects.filter(wordlist__id=a)

    deflist = []
    termlist = []
    for i in words:
        deflist.append(i.definition)
        termlist.append(i.term.lower())

    new_list_terms = []
    new_list_defs = []

    if len(termlist) >= 5:
        new_list_terms += random.sample(termlist, 5)
        for i in new_list_terms:
            for word in words:
                if i == word.term.lower():
                    new_list_defs.append(word.definition)
        terms = (new_list_terms)
        mydefs = (new_list_defs)

    else:
        terms = (termlist)
        mydefs = (deflist)

    # this mod will shuffle both lists at same time
    # but keep their order

    for i in terms:
        mydefs = [sub.replace(str(i), '____') for sub in mydefs]

    from sklearn.utils import shuffle
    terms, mydefs = shuffle(terms, mydefs)

    if request.method == "POST":
        score = request.POST.get("count")
        wrong = request.POST.get("count_wrong")
        final_score = (int(score) / len(terms)) * 100
        obj = Testtaker.objects.create(tester=request.user, test=test, score=final_score, wrong_terms=wrong)
        obj.save()
        messages.success(request, f'You have completed test')
        return redirect('blog-home')

    context = {
        'mydefs': mydefs, 'terms': terms, 'rand_terms': new_list_terms
    }

    return render(request, 'blog/vocab_test.html', context)


# page for flash cards
def flash_card_5(request, pk):
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

    return render(request, 'blog/flash_card.html', context)

# this page tracks the progress of the testtakers so they can see their scores
# from tests


def track_progress(request):
    users = Testtaker.objects.filter(tester=request.user)
    myFilter = ProgressFilter(request.GET, queryset=users)
    users = myFilter.qs
    test = Test.objects.filter(author=request.user)

    context = {

        'users': users, 'myFilter': myFilter, 'tests': test
    }

    return render(request, 'blog/track_progress.html', context)

# jumbled game


def jumbled_game(request, pk):
    wordlist = WordList.objects.get(pk=pk)
    a = wordlist.id
    words = Word.objects.filter(wordlist__id=a)

    def jumble(word):
        # sample() method shuffling the characters of the word
        # did this multi times just in case word appears normal
        # lazy but was failsafe so orig word doesnt appear
        random_word = random.sample(word, len(word))
        random_word = random.sample(word, len(word))
        random_word = random.sample(word, len(word))
        random_word = random.sample(word, len(word))
        random_word = random.sample(word, len(word))
        random_word = random.sample(word, len(word))

    # join() method join the elements
    # of the iterator(e.g. list) with particular character .
        jumbled = ''.join(random_word)
        return jumbled

    termlist_copy = []
    termlist = []
    for i in words:
        termlist.append(i.term)
        termlist_copy.append(i.term)

    # if user has more than 5 terms create new list that adds random 5 terms to list
    new_list_terms = []
    new_list_jumble = []
    # if length of term list > 5 take random 5 items from terms
    # then find the matching term in the term copy list. jumble the term thats in the copy list and add to the new list for jumbled terms.
    if len(termlist) >= 5:
        new_list_terms += random.sample(termlist, 5)
        for i in new_list_terms:
            for j in termlist_copy:
                if i == j:
                    new_list_jumble.append(jumble(j))

        terms = (new_list_terms)
        jumbled = (new_list_jumble)
    else:
        terms = (termlist)
        jumbled = (termlist_copy)
    # this mod will shuffle both lists at same time
    # but keep their order

    from sklearn.utils import shuffle
    terms, jumbled = shuffle(terms, jumbled)

    context = {
        'terms': terms, 'jumbled': jumbled
    }

    return render(request, 'blog/jumbled_game.html', context)


# vocab game matching for defs with 10 terms
def def_match_10(request, pk):
    wordlist = WordList.objects.get(pk=pk)
    a = wordlist.id
    words = Word.objects.filter(wordlist__id=a)
    sentences = Word.objects.filter(wordlist__id=a)

    deflist = []
    termlist = []
    for i in words:
        deflist.append(i.definition)
        termlist.append(i.term.lower())
    # if user has more than 10 terms create new list that adds random 10 terms to list
    new_list_terms = []
    new_list_defs = []
    # if length of term list > 10 take random 10 items from terms
    # then find the matching defs from the word model and match
    # them with terms
    if len(termlist) >= 10:
        new_list_terms += random.sample(termlist, 10)
        for i in new_list_terms:
            for word in words:
                if i == word.term.lower():
                    new_list_defs.append(word.definition)
        terms = (new_list_terms)
        mydefs = (new_list_defs)
    else:
        terms = (termlist)
        mydefs = (deflist)
    # this mod will shuffle both lists at same time
    # but keep their order

    for i in terms:
        mydefs = [sub.replace(str(i), '____') for sub in mydefs]

    from sklearn.utils import shuffle
    terms, mydefs = shuffle(terms, mydefs)

    context = {
        'mydefs': mydefs, 'terms': terms, 'rand_terms': new_list_terms
    }

    return render(request, 'blog/def_match_10.html', context)

# vocab game matching for sents with 10 terms


def sent_match_10(request, pk):
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
        termlist.append(i.term.lower())
    # if user has more than 10 terms create new list that adds random 10 terms to list
    new_list_terms = []
    new_list_sents = []
    # if length of term list > 10 take random 10 items from terms
    # then find the matching sents from the word model and match
    # them with terms
    if len(termlist) >= 10:
        new_list_terms += random.sample(termlist, 10)
        for i in new_list_terms:
            for word in words:
                if i == word.term.lower():
                    new_list_sents.append(word.sentence)
        terms = (new_list_terms)
        mysent = (new_list_sents)
    else:
        terms = (termlist)
        mysent = (sentlist)
    # this mod will shuffle both lists at same time
    # but keep their order
    for i in terms:
        mysent = [sub.replace(str(i), '____') for sub in mysent]

    from sklearn.utils import shuffle
    terms, mysent = shuffle(terms, mysent)
    context = {
        'mysent': mysent, 'terms': terms, 'rand_terms': new_list_terms
    }
    return render(request, 'blog/sent_match_10.html', context)


# flash card game for 10 terms
def flash_card_10(request, pk):
    wordlist = WordList.objects.get(pk=pk)
    a = wordlist.id
    words = Word.objects.filter(wordlist__id=a)
    sentences = Word.objects.filter(wordlist__id=a)

    deflist = []
    termlist = []
    for i in words:
        deflist.append(i.definition)
        termlist.append(i.term)
    # if user has more than 10 terms create new list that adds random 10 terms to list
    new_list_terms = []
    new_list_defs = []
    # if length of term list > 10 take random 10 items from terms
    # then find the matching defs from the word model and match
    # them with terms
    if len(termlist) >= 10:
        new_list_terms += random.sample(termlist, 10)
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

    return render(request, 'blog/flash_card_10.html', context)

# jumbled game 10 terms


def jumbled_game_10(request, pk):
    wordlist = WordList.objects.get(pk=pk)
    a = wordlist.id
    words = Word.objects.filter(wordlist__id=a)

    def jumble(word):
        # sample() method shuffling the characters of the word
        # did this multi times just in case word appears normal
        random_word = random.sample(word, len(word))
        random_word = random.sample(word, len(word))
        random_word = random.sample(word, len(word))
        random_word = random.sample(word, len(word))
        random_word = random.sample(word, len(word))
        random_word = random.sample(word, len(word))

    # join() method join the elements
    # of the iterator(e.g. list) with particular character .
        jumbled = ''.join(random_word)
        return jumbled

    termlist_copy = []
    termlist = []
    for i in words:
        termlist.append(i.term)
        termlist_copy.append(i.term)

    # if user has more than 5 terms create new list that adds random 5 terms to list
    new_list_terms = []
    new_list_jumble = []
    # if length of term list > 5 take random 5 items from terms
    # then find the matching term in the term copy list. jumble the term thats in the copy list and add to the new list for jumbled terms.
    if len(termlist) >= 10:
        new_list_terms += random.sample(termlist, 10)
        for i in new_list_terms:
            for j in termlist_copy:
                if i == j:
                    new_list_jumble.append(jumble(j))

        terms = (new_list_terms)
        jumbled = (new_list_jumble)
    else:
        terms = (termlist)
        jumbled = (termlist_copy)
    # this mod will shuffle both lists at same time
    # but keep their order

    from sklearn.utils import shuffle
    terms, jumbled = shuffle(terms, jumbled)

    context = {
        'terms': terms, 'jumbled': jumbled
    }

    return render(request, 'blog/jumbled_game_10.html', context)

# suggestion page , user would type content into a suggestion form
# which will then save the content in the database. # as of now only way
# to view this content is within the admin on site.


def suggestions(request):
    form = SuggestionForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            messages.success(request, f'Your comment has been recieved!')

            return redirect('blog-home')

        else:
            form = SuggestionForm(request.POST)

    return render(request, 'blog/suggestions.html', {'form': form})

# class based view for the announcements page


class Announcements(ListView):
    model = Post
    template_name = 'blog/announcements.html'
    context_object_name = 'posts'
    paginate_by = 4
    ordering = ['-date_posted']
