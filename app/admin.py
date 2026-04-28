from django.contrib import admin
from .models import Blog, Category, Product

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'posted')
    list_filter = ('category', 'posted')
    search_fields = ('title', 'short_description')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Blog, BlogAdmin)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'short_description')