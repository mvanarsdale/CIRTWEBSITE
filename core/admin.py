from django.contrib import admin

from .models import Role, CustomUser, Paper, Author, Poster


admin.site.register(Role)
admin.site.register(CustomUser)

admin.site.register(Author)
#admin.site.register(Editor)
#admin.site.register(Reviewer)
admin.site.register(Paper)
admin.site.register(Poster)

