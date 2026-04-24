from django.contrib import admin
from .models import Blog

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'posted')
    list_filter = ('category', 'posted')
    search_fields = ('title', 'short_description')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Blog, BlogAdmin)