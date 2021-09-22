from .models import Post, Word, WordList, Test, Testtaker, Suggestion, Folder
from django.contrib import admin

admin.site.register(Post)
admin.site.register(Word)
admin.site.register(WordList)
admin.site.register(Test)
admin.site.register(Testtaker)
admin.site.register(Suggestion)
admin.site.register(Folder)
