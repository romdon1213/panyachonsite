from itertools import chain

import requests
from django.db.models import F, Count, Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from pagesite import filters
from pagesite.models import Article, Category, Post, CategoryPost, Profile, \
    CommentPost, CommentArticle, Masalah, CategoryMasalah, CommentMasalah
from pagesite.form import SignupForm, PostCreateForm, UserEditForm, ProfileEditForm, UserLoginForm, PostEditForm, \
    CommentPostForm, CommentArticleForm, CommentMasalahForm, MasalahCreateform
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from pagesite.filters import ArticleFilters
from django.template.loader import render_to_string
from django.contrib import messages


# Create your views here.


def index(request, category_article_slug=None, category_post_slug=None, category_masalah_slug=None):
    category_article = None
    category_post = None
    category_masalah = None
    if category_masalah_slug != None:
        category_masalah = get_object_or_404(CategoryMasalah, slug=category_masalah_slug)
        masalah = Masalah.objects.all().filter(category=category_masalah, answered=True)
    else:
        masalah = Masalah.objects.all().filter(answered=True)

    if category_article_slug != None:
        category_article = get_object_or_404(Category, slug=category_article_slug)
        articles = Article.objects.all().filter(category=category_article, available=True)
    else:
        articles = Article.objects.all().filter(available=True)

    if category_post_slug != None:
        category_post = get_object_or_404(CategoryPost, slug=category_post_slug)
        post = Post.objects.all().filter(category=category_post, status='published')

    else:
        post = Post.objects.all().filter(status='published')

    r_post = post.order_by('-view')[:3]  # เลขจำนวนที่จะเอา order_by('-name/name/?') name คือเรียงจากอะไร
    r_post = r_post.annotate(countcomment=Count('commentpost'))

    r_article = articles.order_by('-view')[:3]  # เลขจำนวนที่จะเอา order_by('-name/name/?') name คือเรียงจากอะไร
    r_article = r_article.annotate(countcomment=Count('commentarticle'))

    r_masalah = masalah.order_by('-view')[:3]  # เลขจำนวนที่จะเอา order_by('-name/name/?') name คือเรียงจากอะไร
    r_masalah = r_masalah.annotate(countcomment=Count('commentmasalah'))
    context = {'category_article': category_article,
               'r_articles': r_article,
               'category_post': category_post,
               'post': r_post,
               'category_masalah': category_masalah,
               'masalah': r_masalah,
               }
    return render(request, 'index.html', context)


# masalah
def masalahPage(request, category_masalah_slug, masalah_slug):
    try:
        masalah = Masalah.objects.get(category__slug=category_masalah_slug, slug=masalah_slug)
        Masalah.objects.filter(pk=masalah.pk).update(view=F('view') + 1)
    except Exception as e:
        raise e
    is_liked = False
    if masalah.likes.filter(id=request.user.id).exists():
        is_liked = True
    commentmasalah = CommentMasalah.objects.filter(masalah=masalah, reply=None).order_by('id')
    commentmasalah_count = CommentMasalah.objects.filter(masalah=masalah)
    if request.method == 'POST':
        commentmasalahform = CommentMasalahForm(request.POST or None)
        if commentmasalahform.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = CommentMasalah.objects.get(id=reply_id)
            comment = CommentMasalah.objects.create(masalah=masalah, user=request.user, content=content,
                                                    reply=comment_qs)
            comment.save()
            # return HttpResponseRedirect(post.get_url())
    else:
        commentmasalahform = CommentMasalahForm()
    #
    totallikes = masalah.total_likes()
    context = {
        'masalah': masalah,
        'is_liked': is_liked,
        'totallikes': totallikes,
        'commentmasalah': commentmasalah,
        'commentmasalah_count': commentmasalah_count,
        'commentmasalahform': commentmasalahform
    }
    if request.is_ajax():
        html = render_to_string('commentmasalah.html', context, request=request)
        return JsonResponse({'form': html})

    return render(request, 'masalahpage.html', context)


def masalah(request):
    filter = filters.MasalahFilters(request.GET, queryset=Masalah.objects.all().filter(answered=True).order_by('?'))
    # articles = Article.objects.all().filter(available=True)
    paginator = Paginator(filter.qs, 15)
    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)
    context = {
        'page_obj': response,
        'filter': filter
    }
    return render(request, 'masalah.html', context)


def masalah_answered(request):
    masalah = Masalah.objects.all().filter(quester=request.user, answered=True)
    masalah = masalah.order_by('-updated')
    paginator = Paginator(masalah, 15)
    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)
    context = {
        'masalah': masalah,
        'page_obj': response,
    }
    return render(request, 'masalah-answered.html', context)


def masalah_noanswered(request):
    masalah = Masalah.objects.all().filter(quester=request.user, answered=False)
    masalah = masalah.order_by('-updated')
    paginator = Paginator(masalah, 15)
    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)
    context = {
        'masalah': masalah,
        'page_obj': response,
    }
    return render(request, 'masalah-noanswered.html', context)


def masalah_create(request):
    if request.method == 'POST':
        form = MasalahCreateform(request.POST)
        if form.is_valid():
            masalah = form.save(commit=False)
            masalah.quester = request.user
            masalah.save()
            messages.success(request, "ส่งคำถามเรียบร้อยแล้ว")
            return redirect('masalah-noanswered')
    else:
        form = MasalahCreateform
    context = {
        'form': form
    }
    return render(request, 'masalahcreateform.html', context)


def like_masalah(request):
    # post = get_object_or_404(Post, id=request.POST.get('post_id'))
    masalah = get_object_or_404(Masalah, id=request.POST.get('id'))
    is_liked = False

    if masalah.likes.filter(id=request.user.id).exists():
        masalah.likes.remove(request.user)
        is_liked = False
    else:
        masalah.likes.add(request.user)
        is_liked = True
        # totallikes = post.total_likes()
    context = {
        'masalah': masalah,
        'is_liked': is_liked,
        'totallikes': masalah.total_likes(),
    }
    if request.is_ajax():
        html = render_to_string('like_masalah_section.html', context, request=request)
        return JsonResponse({'form': html})
    # return HttpResponseRedirect(post.get_url())


def articlePage(request, category_article_slug, article_slug):
    try:
        article = Article.objects.get(category__slug=category_article_slug, slug=article_slug)
        Article.objects.filter(pk=article.pk).update(view=F('view') + 1)
    except Exception as e:
        raise e
    is_liked = False
    if article.likes.filter(id=request.user.id).exists():
        is_liked = True
    commentarticle = CommentArticle.objects.filter(article=article, reply=None).order_by('id')
    commentarticle_count = CommentArticle.objects.filter(article=article)
    if request.method == 'POST':
        commentarticleform = CommentArticleForm(request.POST or None)
        if commentarticleform.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = CommentArticle.objects.get(id=reply_id)
            comment = CommentArticle.objects.create(article=article, user=request.user, content=content,
                                                    reply=comment_qs)
            comment.save()
            # return HttpResponseRedirect(post.get_url())
    else:
        commentarticleform = CommentArticleForm()

    totallikes = article.total_likes()
    context = {
        'article': article,
        'is_liked': is_liked,
        'totallikes': totallikes,
        'commentarticle': commentarticle,
        'commentarticle_count': commentarticle_count,
        'commentarticleform': commentarticleform
    }
    if request.is_ajax():
        html = render_to_string('commentarticle.html', context, request=request)
        return JsonResponse({'form': html})

    return render(request, 'articlePage.html', context)


def article(request):
    filter = filters.ArticleFilters(request.GET, queryset=Article.objects.all().filter(available=True).order_by('?'))
    # articles = Article.objects.all().filter(available=True)
    paginator = Paginator(filter.qs, 15)
    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)
    context = {
        'page_obj': response,
        'filter': filter
    }
    return render(request, 'article.html', context)


def like_article(request):
    # post = get_object_or_404(Post, id=request.POST.get('post_id'))
    article = get_object_or_404(Article, id=request.POST.get('id'))
    is_liked = False

    if article.likes.filter(id=request.user.id).exists():
        article.likes.remove(request.user)
        is_liked = False
    else:
        article.likes.add(request.user)
        is_liked = True
        # totallikes = post.total_likes()
    context = {
        'article': article,
        'is_liked': is_liked,
        'totallikes': article.total_likes(),
    }
    if request.is_ajax():
        html = render_to_string('like_article_section.html', context, request=request)
        return JsonResponse({'form': html})
    # return HttpResponseRedirect(post.get_url())


def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "สร้างโพสต์/บทความรียบร้อยแล้ว")
            return redirect('blog_user')
    else:
        form = PostCreateForm
    context = {
        'form': form
    }
    return render(request, 'postcraeteform.html', context)


def post_edit(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author != request.user:
        raise Http404()
    if request.method == 'POST':
        form = PostEditForm(request.POST or None, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, '{} ถูกแก้ไขเรียบร้อยแล้ว'.format(post.title))
            return HttpResponseRedirect(post.get_url())
    else:
        form = PostEditForm(instance=post)
    context = {
        'form': form,
        'post': post
    }
    return render(request, 'post_edit.html', context)


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user != post.author:
        raise Http404()
    post.delete()
    messages.warning(request, 'ลบโพสต์/บทความ {} เรียบร้อยแล้ว'.format(post.title))
    return redirect('blog_user')


def blog(request):
    filter = filters.PostFilters(request.GET, queryset=Post.objects.all().filter(status='published').order_by('?'))
    # articles = Article.objects.all().filter(available=True)
    paginator = Paginator(filter.qs, 15)
    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)
    context = {
        'page_obj': response,
        'filter': filter
    }
    return render(request, 'blog.html', context)


def blogpage(request, category_post_slug, post_slug):
    try:
        post = Post.objects.get(category__slug=category_post_slug, slug=post_slug)
        Post.objects.filter(pk=post.pk).update(view=F('view') + 1)

    except Exception as e:
        raise e
    commentpost = CommentPost.objects.filter(post=post, reply=None).order_by('-id')
    commentpost_count = CommentPost.objects.filter(post=post)
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    if request.method == 'POST':
        commentpostform = CommentPostForm(request.POST or None)
        if commentpostform.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = CommentPost.objects.get(id=reply_id)
            comment = CommentPost.objects.create(post=post, user=request.user, content=content, reply=comment_qs)
            comment.save()
            # return HttpResponseRedirect(post.get_url())
    else:
        commentpostform = CommentPostForm()

    totallikes = post.total_likes()
    context = {
        'post': post,
        'is_liked': is_liked,
        'totallikes': totallikes,
        'commentpost': commentpost,
        'commentpost_count': commentpost_count,
        'commentpostform': commentpostform
    }
    if request.is_ajax():
        html = render_to_string('commentpost.html', context, request=request)
        return JsonResponse({'form': html})
    return render(request, 'blogpage.html', context)


def blog_user_draft(request):
    post = Post.objects.all().filter(author=request.user, status='dratf')
    post = post.order_by('-updated')
    paginator = Paginator(post, 15)
    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)
    context = {
        'post': post,
        'page_obj': response,
    }
    return render(request, 'blog_user_draft.html', context)


def blog_user(request):
    post = Post.objects.all().filter(author=request.user, status='published')
    post = post.order_by('-updated')
    paginator = Paginator(post, 15)
    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)
    context = {
        'post': post,
        'page_obj': response,
    }
    return render(request, 'blog_user.html', context)


def blog_each_user(request, user):
    userprofile = Profile.objects.all().get(user=user)
    post = Post.objects.all().filter(author=user, status='published')
    post = post.order_by('-updated')
    post = post.annotate(countcomment=Count('commentpost'))
    paginator = Paginator(post, 15)
    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)
    context = {
        'post': post,
        'user': userprofile,
        'page_obj': response,
    }
    return render(request, 'blog_each_user.html', context)


def like_post(request):
    # post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post = get_object_or_404(Post, id=request.POST.get('id'))
    is_liked = False

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
        # totallikes = post.total_likes()
    context = {
        'post': post,
        'is_liked': is_liked,
        'totallikes': post.total_likes(),
    }
    if request.is_ajax():
        html = render_to_string('like_post_section.html', context, request=request)
        return JsonResponse({'form': html})
    # return HttpResponseRedirect(post.get_url())


# def remove_post_from_readlist(request, post_id):
#     # ทำงานกับตัวลิสต์
#     readlist = ReadList.objects.get(readlist_id=readlist_id(request))
#     # ทำงานกับตัวบทความที่จะลบ
#     post = get_object_or_404(Post, id=post_id)
#     readlistitem_post = ReadList_Item_Post.objects.get(post=post, readlist=readlist)
#     # ลบรายการสินค้า จากลิสต์ และบทความ ที่มีรหัสตรงกับข้างบน
#     readlistitem_post.delete()
#     return redirect('readlistdetail')


def signupview(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            Profile.objects.create(user=new_user)
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': account_activation_token.make_token(new_user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'signupconfirm1.html')
            # บันทึกข้อมูล User
            # form.save()

            # # ดึง username จากแบบฟอร์มมาใช้
            # username = form.cleaned_data.get('username')
            # # ดึงข้อมูล User จากฐานข้อมูล
            # signupuser = User.objects.get(username=username)
            # # บันทึกเข้ากลุ่ม readerwriter
            # readwritegroup = Group.objects.get(name='readerwriter')
            # readwritegroup.user_set.add(signupuser)

    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # user = authenticate(request, username=username, password=password)
        login(request, user, backend='games.backend.EmailorUsernameAuthBackend')
        # login(request, user)
        # return redirect('home')
        return render(request, 'signupconfirm.html')
    else:
        return render(request, 'signupconnotfirm.html')


def signinview(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('blog_user')
            else:
                messages.success(request, "username/email/password ไม่ถูกต้อง โปรดตรวจสอบใหม่อีกครั้งหนึ่ง")
                return redirect('signin')
    else:
        form = UserLoginForm()
    return render(request, 'signin.html', {'form': form})


def signoutview(request):
    logout(request)
    return redirect('index')


def praytime(request):
    url = "https://aladhan.p.rapidapi.com/timingsByCity"
    city = ("Bangkok", "Narathiwat","Chiangrai","Khonkaen")
    headers = {
        'x-rapidapi-host': "aladhan.p.rapidapi.com",
        'x-rapidapi-key': "2544a08880mshd72d821fe59ae77p1e86ebjsnad28cedca983"
    }
    querystring = [{"city": i, "country": "thailand", "method": "1"} for i in city]
    response = [requests.request("GET", url, headers=headers, params=i).json() for i in querystring]
    praytime_non = {
        'city': city[0],
        'fajr': response[0]['data']['timings']['Fajr'],
        'shuruq': response[0]['data']['timings']['Sunrise'],
        'dhuri': response[0]['data']['timings']['Dhuhr'],
        'asri': response[0]['data']['timings']['Asr'],
        'maghrib': response[0]['data']['timings']['Sunset'],
        'isha': response[0]['data']['timings']['Isha'],
        'latitude': response[0]['data']['meta']['latitude'],  # 'meta': {'latitude'
        'longitude': response[0]['data']['meta']['longitude'],
    }
    praytime_nara = {
        'city': city[1],
        'fajr': response[1]['data']['timings']['Fajr'],
        'shuruq': response[1]['data']['timings']['Sunrise'],
        'dhuri': response[1]['data']['timings']['Dhuhr'],
        'asri': response[1]['data']['timings']['Asr'],
        'maghrib': response[1]['data']['timings']['Sunset'],
        'isha': response[1]['data']['timings']['Isha'],
        'latitude': response[1]['data']['meta']['latitude'],  # 'meta': {'latitude'
        'longitude': response[1]['data']['meta']['longitude'],
    }
    praytime_Chiangrai = {
        'city': city[2],
        'fajr': response[2]['data']['timings']['Fajr'],
        'shuruq': response[2]['data']['timings']['Sunrise'],
        'dhuri': response[2]['data']['timings']['Dhuhr'],
        'asri': response[2]['data']['timings']['Asr'],
        'maghrib': response[2]['data']['timings']['Sunset'],
        'isha': response[2]['data']['timings']['Isha'],
        'latitude': response[2]['data']['meta']['latitude'],  # 'meta': {'latitude'
        'longitude': response[2]['data']['meta']['longitude'],
    }
    praytime_Khonkaen = {
        'city': city[3],
        'fajr': response[3]['data']['timings']['Fajr'],
        'shuruq': response[3]['data']['timings']['Sunrise'],
        'dhuri': response[3]['data']['timings']['Dhuhr'],
        'asri': response[3]['data']['timings']['Asr'],
        'maghrib': response[3]['data']['timings']['Sunset'],
        'isha': response[3]['data']['timings']['Isha'],
        'latitude': response[3]['data']['meta']['latitude'],  # 'meta': {'latitude'
        'longitude': response[3]['data']['meta']['longitude'],
    }
    context = {
        'praytime_non': praytime_non,
        'praytime_nara': praytime_nara,
        'praytime_Chiangrai':praytime_Chiangrai,
        'praytime_Khonkaen':praytime_Khonkaen,
    }
    # print(praytime)

    return render(request, 'praytime.html', context)

def blockpraytime(request):
    url = "https://aladhan.p.rapidapi.com/timingsByCity"
    city = ("Bangkok", "Narathiwat","Chiangrai","Khonkaen")
    headers = {
        'x-rapidapi-host': "aladhan.p.rapidapi.com",
        'x-rapidapi-key': "2544a08880mshd72d821fe59ae77p1e86ebjsnad28cedca983"
    }
    querystring = [{"city": i, "country": "thailand", "method": "1"} for i in city]
    response = [requests.request("GET", url, headers=headers, params=i).json() for i in querystring]
    praytime_non = {
        'city': city[0],
        'fajr': response[0]['data']['timings']['Fajr'],
        'shuruq': response[0]['data']['timings']['Sunrise'],
        'dhuri': response[0]['data']['timings']['Dhuhr'],
        'asri': response[0]['data']['timings']['Asr'],
        'maghrib': response[0]['data']['timings']['Sunset'],
        'isha': response[0]['data']['timings']['Isha'],
        'latitude': response[0]['data']['meta']['latitude'],  # 'meta': {'latitude'
        'longitude': response[0]['data']['meta']['longitude'],
    }
    context = {
        'praytime_non': praytime_non,
    }
    # print(praytime)
    print(praytime_non)
    return render(request,'blockpraytime.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(data=request.POST or None, instance=request.user)
        profile_form = ProfileEditForm(data=request.POST or None, instance=request.user.profile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'การแก้ไขโปรไฟล์สำเร็จ')
        return redirect('blog_user')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'edit_profile_form.html', context)


def search(request):
    search = request.GET['search']
    article = Article.objects.filter(name__contains=search,available=True)
    post = Post.objects.filter(title__contains=search,status='published')
    masalah = Masalah.objects.filter(question__contains=search,answered=True)
    results=list(chain(article, post, masalah))
    # articles = Article.objects.all().filter(description__contains=search,available=True) \
    #            or Article.objects.all().filter(name__contains=search,available=True) \
    #            or Post.objects.all().filter(title__contains=search,status='published') \
    #            or Post.objects.all().filter(body__contains=search,status='published') \
    #            or Masalah.objects.all().filter(question__contains=search,answered=True) \
    #            or Masalah.objects.all().filter(answer__contains=search,answered=True)
    paginator = Paginator(results, 15)
    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)
    context = {
        'articles': results,
        'page_obj': response,
    }
    return render(request, 'search.html', context)
