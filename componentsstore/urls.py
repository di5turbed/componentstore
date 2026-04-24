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
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('blog/<int:id>/', views.blog_detail, name='blog_detail_id')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
