"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

from app.models import Category, Comment, Blog, Product

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(label="Имя пользователя", max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label="Пароль",
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))

class FeedbackForm(forms.Form):
    name = forms.CharField(label='Ваше имя', max_length=100)
    email = forms.EmailField(label='Ваш Email')
    rating = forms.ChoiceField(
        label='Оценка сайта',
        choices=(('5', 'Отлично'), ('4', 'Хорошо'), ('3', 'Удовлетворительно')),
        widget=forms.RadioSelect
    )
    source = forms.ChoiceField(
        label='Откуда вы узнали о нас?',
        choices=(('search', 'Поисковая система'), ('friends', 'От друзей'), ('ad', 'Реклама'))
    )
    subscribe = forms.BooleanField(label='Подписаться на новости', required=False)
    message = forms.CharField(
        label='Ваши пожелания', 
        widget=forms.Textarea, 
        required=False,
        max_length=500
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': "Оставить комментарий"}
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Напишите ваш комментарий здесь...'
            }),
        }

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'short_description', 'full_content', 'image', 'category')
        labels = {
            'title': 'Заголовок',
            'short_description': 'Краткое содержание',
            'full_content': 'Полное содержание',
            'image': 'Картинка статьи',
            'category': 'Категория'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'full_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description')
        labels = {'name': 'Название категории', 'description': 'Описание'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'short_description', 'full_description', 'price', 'image', 'category')
        labels = {
            'name': 'Название товара',
            'short_description': 'Краткое описание',
            'full_description': 'Полное описание',
            'price': 'Цена',
            'image': 'Файл картинки',
            'category': 'Категория'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'full_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }