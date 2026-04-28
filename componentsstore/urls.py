"""
Definition of urls for componentsstore.
"""

from datetime import datetime
from django.conf import settings
from django.urls import path
from django.contrib import admin
from app import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls.static import static
from app import forms

urlpatterns = [
    path('', views.home, name='home'),
    
    path('about/', views.about, name='about'),
    path('pool/', views.pool, name='pool'),
    path('registration/', views.registration, name='registration'),
    path('login/',
         LoginView.as_view(
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context={
                 'title': 'Авторизация',
                 'year': datetime.now().year,
             }
         ),
         name='login'),
    
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('blog/', views.blog_list, name='blog_list'),
    path('newpost/', views.newpost, name='newpost'),
    path('video/', views.videopost, name='videopost'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<int:category_id>/', views.category_products, name='category_products'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('catalog/add_category/', views.add_category, name='add_category'),
    path('catalog/add_product/', views.add_product, name='add_product'),
    path('blog/<int:id>/', views.blog_detail, name='blog_detail_id')
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
