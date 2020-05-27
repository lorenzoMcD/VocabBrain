from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from wiktionaryparser import WiktionaryParser


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class WordList(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('list-detail', kwargs={'pk': self.pk})


class Word(models.Model):
    term = models.CharField(max_length=100)
    definition = models.CharField(max_length=150)
    sentence = models.CharField(max_length=300)
    wordlist = models.ForeignKey(WordList, on_delete=models.CASCADE)

    def __str__(self):
        return self.term.lower()

    def get_defs(term):
        parser = WiktionaryParser()
        lookup = parser.fetch(term)
        definitions = []

        try:
            for items in lookup:

                wordlist = (items['definitions'][0]['text'])

            for defs in wordlist:

                definitions.append(defs)

            return(definitions)

        except:
            return("could not find definitions")

    def get_sent(term):
        parser = WiktionaryParser()
        lookup = parser.fetch(term)
        sentences = []

        try:
            for items in lookup:
                wordlist = (items['definitions'][0]['examples'])

            for sent in wordlist:

                sentences.append(sent)

            return(sentences)

        except:
            return("could not find sentences!")


class Test(models.Model):

    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    wordlist = models.ForeignKey(WordList, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    description = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('test-detail', kwargs={'pk': self.pk})


class Testtaker(models.Model):
    tester = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.tester)

    def get_absolute_url(self):
        return reverse('testtaker-detail', kwargs={'pk': self.pk})
