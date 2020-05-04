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
from django.urls import path, include
from pagesite import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # หน้าหลัก
    path('test/', views.test),  # หน้าทดลอง
    path('praytime/', views.test),  # หน้าทดลองเวลาละหมาด
    path('article/', views.article, name='article'),  # หน้ารวมบทความ
    path('category/<slug:category_article_slug>/', views.index, name="article_by_category"),  # กล่องบทความในหน้าหลัก
    path('article/<slug:category_article_slug>/<slug:article_slug>', views.articlePage, name="article_detail"),
    path('like-article/', views.like_article, name='like_article'),

    path('masalah/', views.masalah, name='masalah'),  # หน้ารวมบทความ
    path('categorymasalah/<slug:category_masalah_slug>/', views.index, name="masalah_by_category"),
    # กล่อง masalah ในหน้าหลัก
    path('masalah/<slug:category_masalah_slug>/<slug:masalah_slug>', views.masalahPage, name="masalah_detail"),
    path('like-masalah/', views.like_masalah, name='like_masalah'),

    # บทความแต่ละอันในหน้าแยก
    # path('readlist/add/<int:article_id>', views.add_to_readlist, name='addtoreadlist'),  # add_article
    # path('readlist/addpost/<int:post_id>', views.add_to_readlist_post, name='addposttoreadlist'),  # add_post
    # path('readlist/removearticle/<int:article_id>', views.remove_from_readlist, name='remove_article_fromreadlist'),
    # remove_article
    # path('readlist/removepost/<int:post_id>', views.remove_post_from_readlist, name='remove_post_fromreadlist'),
    # # remove_post
    # path('readlistdetail/', views.readlistdetail, name='readlistdetail'),
    path('postcreate/', views.post_create, name='postcreate'),
    path('post-edit/<id>/', views.post_edit, name='post_edit'),
    path('post-delete/<id>/', views.post_delete, name='post_delete'),
    path('like/', views.like_post, name='like_post'),

    path('blog/', views.blog, name='blog'),  # หน้ารวมบล็อก
    path('user-blogpage/', views.blog_user, name='blog_user'),
    path('each_user-blogpage/<user>', views.blog_each_user, name='blog_each_user'),

    path('categorypost/<slug:category_post_slug>', views.index, name="post_by_category"),  # กล่องบล็อคในหน้าหลัก
    path('blog/(?P<category_post_slug>[-a-zA-Z0-9_]+)/(?P<post_slug>[-a-zA-Z0-9_]+)$', views.blogpage,
         name='blog_detail'),
    # บล็อคแต่ละอันในหน้าแยก
    path('account/create', views.signupview, name='signup'),
    path('account/login', views.signinview, name='signin'),
    path('account/logout', views.signoutview, name='signout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    # password reset
    path('accounts/', include('django.contrib.auth.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('accounts/', include('allauth.urls')),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    # search
    path('search/', views.search, name='search'),

]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)