from django.contrib import admin

from .models import Role, User, Paper, Author, Poster


admin.site.register(Role)
admin.site.register(User)

admin.site.register(Author)
#admin.site.register(Editor)
#admin.site.register(Reviewer)
admin.site.register(Paper)
admin.site.register(Poster)

