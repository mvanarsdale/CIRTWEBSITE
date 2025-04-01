from django.contrib import admin

from .models import Author, Paper, User, Editor, Reviewer, Role

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Author)
admin.site.register(Editor)
admin.site.register(Reviewer)
admin.site.register(Paper)

