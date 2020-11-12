from django.contrib import admin
from .models import Author, Tag, Comment, Question, Answer, Synonym

admin.site.register(Question)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Answer)
admin.site.register(Synonym)

