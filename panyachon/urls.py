"""panyachon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pagesite import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # หน้าหลัก
    path('test/', views.test),  # หน้าทดลอง
    path('praytime/', views.test),  # หน้าทดลองเวลาละหมาด
    path('article/', views.article, name='article'),  # หน้ารวมบทความ
    path('category/<slug:category_article_slug>', views.index, name="article_by_category"),  # กล่องบทความในหน้าหลัก
    path('article/<slug:category_article_slug>/<slug:article_slug>', views.articlePage, name="article_detail"),
    # บทความแต่ละอันในหน้าแยก
    path('readlist/add/<int:article_id>', views.add_to_readlist, name='addtoreadlist'),
    path('readlist/remove/<int:article_id>', views.remove_from_readlist, name='removefromreadlist'),
    path('readlistdetail/', views.readlistdetail, name='readlistdetail'),
    path('blog/', views.blog, name='blog'),  # หน้ารวมบล็อก
    # path('blog/', views.blogpage, name='blog_detail')  # บล็อคแต่ละอันในหน้าแยก
    path('account/create', views.signupview, name='signup')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.STATIC_ROOT)
