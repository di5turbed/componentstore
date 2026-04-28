from django.db import models
from django.urls import reverse
from datetime import datetime
from django.contrib import admin
from django.utils.text import slugify
from django.contrib.auth.models import User

class Blog(models.Model):
    CATEGORY_CHOICES = [
        ('review', 'Обзор'),
        ('news', 'Новости'),
        ('guide', 'Гайд'),
        ('compare', 'Сравнение'),
        ('tips', 'Советы'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    short_description = models.TextField(verbose_name="Краткое содержание")
    full_content = models.TextField(verbose_name="Полное содержание")
    posted = models.DateTimeField(
        default=datetime.now,
        db_index=True,
        verbose_name="Опубликована"
    )
    image = models.ImageField(
        upload_to='blog_images/', 
        blank=True, 
        null=True, 
        verbose_name="Изображение статьи"
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='review',
        verbose_name="Категория"
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        verbose_name="URL-метка"
    )
    author = models.ForeignKey(
    User,
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    verbose_name="Автор"
    )
    class Meta:
        db_table = 'blog_posts'
        verbose_name = 'Статьи блога'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.slug:
            return reverse('blog_detail', args=[self.slug])
        return reverse('blog_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True) 
        super().save(*args, **kwargs)

class Comment(models.Model):
    text = models.TextField(verbose_name="Комментарий")
    date = models.DateTimeField(default=datetime.now, db_index=True, verbose_name="Дата")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="Статья")

    def __str__(self):
        return f'Комментарий от {self.author} к "{self.post}"'

    class Meta:
        db_table = 'comments'
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["-date"]

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(verbose_name="Описание категории", blank=True)

    class Meta:
        verbose_name = "Категория каталога"
        verbose_name_plural = "Категории каталога"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    short_description = models.TextField(verbose_name="Краткое описание")
    full_description = models.TextField(verbose_name="Полное описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    
    image = models.ImageField(upload_to='products/', verbose_name="Изображение", blank=True, null=True)
    
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name="Категория")

    def __str__(self):
        return self.name