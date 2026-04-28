"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm

from app.forms import BlogForm, CategoryForm, CommentForm, FeedbackForm, ProductForm
from app.models import Blog, Category, Comment, Product
from django.contrib.auth.decorators import user_passes_test

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    categories = Category.objects.all()

    category_id = request.GET.get('category')

    if category_id:
        featured = Product.objects.filter(category_id=category_id).order_by('-id')
    else:
        featured = Product.objects.all().order_by('-id')

    return render(
        request,
        'app/index.html',
        {
            'title': 'Главная',
            'year': datetime.now().year,
            'categories': categories,
            'featured': featured,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title': 'О магазине',
            'message': 'Компьютерная периферия для игр и работы',
            'year': datetime.now().year,
        }
    )
def pool(request):
    """Renders the feedback page."""
    assert isinstance(request, HttpRequest)
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['email'] = form.cleaned_data['email']
            data['rating'] = dict(form.fields['rating'].choices)[form.cleaned_data['rating']]
            data['source'] = dict(form.fields['source'].choices)[form.cleaned_data['source']]
            data['subscribe'] = 'Да' if form.cleaned_data['subscribe'] else 'Нет'
            data['message'] = form.cleaned_data['message']
            
            return render(
                request,
                'app/pool.html',
                {
                    'title': 'Обратная связь',
                    'year': datetime.now().year,
                    'data': data,
                    'form': None
                }
            )
        else:
            return render(
                request,
                'app/pool.html',
                {
                    'title': 'Обратная связь',
                    'year': datetime.now().year,
                    'form': form
                }
            )
    else:
        form = FeedbackForm()
        return render(
            request,
            'app/pool.html',
            {
                'title': 'Обратная связь',
                'year': datetime.now().year,
                'form': form
            }
        )
    
def registration(request):
    """Renders the registration page."""
    assert isinstance(request, HttpRequest)
    if request.method == "POST":
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False
            reg_f.is_active = True
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now()
            reg_f.last_login = datetime.now()
            reg_f.save()
            return redirect('home')
    else:
        regform = UserCreationForm()

    return render(
        request,
        'app/registration.html',
        {
            'regform': regform,
            'year': datetime.now().year,
        }
    )

def blog_list(request):
    articles = Blog.objects.all().order_by('-posted')
    return render(
        request,
        'app/blog_list.html',
        {
            'title': 'Блог',
            'articles': articles,
            'year': datetime.now().year,
        }
    )
def blog_detail(request, slug=None, id=None):
    if slug and slug.isdigit():
        article = Blog.objects.get(id=slug)
    elif slug:
        article = Blog.objects.get(slug=slug)
    else:
        article = Blog.objects.get(id=id)

    comments = Comment.objects.filter(post=article)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.date = datetime.now()
            comment_f.post = article
            comment_f.save()
            
            if article.slug:
                return redirect('blog_detail', slug=article.slug)
            else:
                return redirect('blog_detail', slug=article.id)
    else:
        form = CommentForm()

    return render(
        request, 
        'app/blog_detail.html', 
        {
            'title': article.title, 
            'article': article, 
            'comments': comments, 
            'form': form, 
            'year': datetime.now().year
        }
    )

def newpost(request):
    assert isinstance(request, HttpRequest)
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.posted = datetime.now()
            blog_post.save()
            return redirect('blog_list')
    else:
        form = BlogForm()
    
    return render(request, 'app/newpost.html', {
        'form': form,
        'title': 'Добавить статью',
        'year': datetime.now().year,
    })

def videopost(request):
    assert isinstance(request, HttpRequest)
    return render(request, 'app/videopost.html', {
        'title': 'Видео-обзоры',
        'year': datetime.now().year,
    })

def catalog(request):
    """Страница со списком всех категорий."""
    categories = Category.objects.all()
    return render(
        request,
        'app/catalog.html',
        {
            'title': 'Каталог товаров',
            'categories': categories,
            'year': datetime.now().year,
        }
    )

def category_products(request, category_id):
    """Страница со списком товаров конкретной категории."""
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=category)
    return render(
        request,
        'app/category_products.html',
        {
            'title': category.name,
            'category': category,
            'products': products,
            'year': datetime.now().year,
        }
    )

def category_detail(request, category_id):
    """Страница со списком товаров выбранной категории."""
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=category)
    
    return render(
        request,
        'app/category_detail.html',
        {
            'title': category.name,
            'category': category,
            'products': products,
            'year': datetime.now().year,
        }
    )

def product_detail(request, product_id):
    """Страница с подробным описанием конкретного товара."""
    product = Product.objects.get(id=product_id)
    return render(
        request,
        'app/product_detail.html',
        {
            'title': product.name,
            'product': product,
            'year': datetime.now().year,
        }
    )

@user_passes_test(lambda u: u.is_superuser)
def add_category(request):
    """Добавление новой категории администратором."""
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('catalog')
    else:
        form = CategoryForm()
    return render(request, 'app/add_category.html', {'form': form, 'title': 'Новая категория'})

@user_passes_test(lambda u: u.is_superuser)
def add_product(request):
    """Добавление нового товара администратором."""
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog')
    else:
        form = ProductForm()
    return render(request, 'app/add_product.html', {'form': form, 'title': 'Новый товар'})