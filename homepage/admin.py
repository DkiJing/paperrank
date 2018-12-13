from django.contrib import admin
from .models import Author, Paper, PaperAuthor

# Register your models here.
admin.site.register(Author)
admin.site.register(Paper)
admin.site.register(PaperAuthor)