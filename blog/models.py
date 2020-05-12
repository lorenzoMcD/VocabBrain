from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.urls import reverse
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
            retutn("could not find sentences!")
