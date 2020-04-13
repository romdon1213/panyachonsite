import requests
from django.db.models import F
from django.shortcuts import render, get_object_or_404, redirect
from pagesite.models import Article, Category, ReadList, ReadList_Item
from pagesite.form import SignupForm
from django.contrib.auth.models import Group,User

# Create your views here.


def index(request, category_article_slug=None):
    category_article = None
    if category_article_slug != None:
        category_article = get_object_or_404(Category, slug=category_article_slug)
        articles = Article.objects.all().filter(category=category_article, available=True)
    else:
        articles = Article.objects.all().filter(available=True)

    r_article = articles.order_by('?')[:4]  # เลขจำนวนที่จะเอา order_by('-name/name/?') name คือเรียงจากอะไร

    return render(request, 'index.html', {'articles': articles, 'category': category_article, 'r_article': r_article})


def articlePage(request, category_article_slug, article_slug):
    try:
        article = Article.objects.get(category__slug=category_article_slug, slug=article_slug)
        Article.objects.filter(pk=article.pk).update(view=F('view') + 1)
    except Exception as e:
        raise e
    return render(request, 'articlePage.html', {'article': article})


def article(request):
    articles = Article.objects.all().filter(available=True)
    articles = articles.order_by('?')
    sortarticle = request.POST.get('sortarticle', None)
    sortcate = request.POST.get('sortcate', 'all')

    if sortcate == "all":
        articles = articles.order_by('?')
        if sortarticle == "date":
            articles = articles.order_by('-updated')
        if sortarticle == "pop":
            articles = articles.order_by('-view')
        if sortarticle == "namear":
            articles = articles.order_by('name')
    if sortcate == "/category/tasoawuf":
        articles = Article.objects.all().filter(category="1")
        articles = articles.order_by('?')
        if sortarticle == "date":
            articles = articles.order_by('-updated')
        if sortarticle == "pop":
            articles = articles.order_by('-view')
        if sortarticle == "namear":
            articles = articles.order_by('name')
    if sortcate == "/category/fiqh":
        articles = Article.objects.all().filter(category="2")
        articles = articles.order_by('?')
        if sortarticle == "date":
            articles = articles.order_by('-updated')
        if sortarticle == "pop":
            articles = articles.order_by('-view')
        if sortarticle == "namear":
            articles = articles.order_by('name')
    if sortcate == "/category/aqidah":
        articles = Article.objects.all().filter(category="3")
        articles = articles.order_by('?')
        if sortarticle == "date":
            articles = articles.order_by('-updated')
        if sortarticle == "pop":
            articles = articles.order_by('-view')
        if sortarticle == "namear":
            articles = articles.order_by('name')
    if sortcate == "/category/other":
        articles = Article.objects.all().filter(category="4")
        articles = articles.order_by('?')
        if sortarticle == "date":
            articles = articles.order_by('-updated')
        if sortarticle == "pop":
            articles = articles.order_by('-view')
        if sortarticle == "namear":
            articles = articles.order_by('name')
    if sortcate == "/category/social":
        articles = Article.objects.all().filter(category="5")
        articles = articles.order_by('?')
        if sortarticle == "date":
            articles = articles.order_by('-updated')
        if sortarticle == "pop":
            articles = articles.order_by('-view')
        if sortarticle == "namear":
            articles = articles.order_by('name')

    return render(request, 'article.html', {'articles': articles, })


def blog(request):
    return render(request, 'blog.html')


def blogpage(request):
    return render(request, 'blogpage.html')


def readlist_id(request):  # สร้าง session key เพื่อบันทึกข้อมูลในหน้าเว็บไม่ให้หายไป
    readlist = request.session.session_key
    if not readlist:
        readlist = request.session.create()
    return readlist


def add_to_readlist(request, article_id):
    # ดึงบทความตามรหัสที่ส่งมา
    article = Article.objects.get(id=article_id)
    message = "มีแล้วนะ"
    # สร้างลิสต์
    try:
        readlist = ReadList.objects.get(readlist_id=readlist_id(request))
    except ReadList.DoesNotExist:
        readlist = ReadList.objects.create(readlist_id=readlist_id(request))
        readlist.save()

    try:
        # มีร่ายการบทความความซ้ำ
        readlist_item = ReadList_Item.objects.get(article=article, readlist=readlist)
        # หากเพิ่มบทความซ้ำ ก็เพิ่มจำนวน
        # readlist_item.quantity+=1
        # readlist_item.save()
    # เพิ่มรายการบทความครั้งแรก จากนั้นบันทึกลงฐานข้อมูล
    except ReadList_Item.DoesNotExist:
        readlist_item = ReadList_Item.objects.create(
            article=article,
            readlist=readlist,
            quantity=1
        )
        readlist_item.save()
    return redirect('/')

def remove_from_readlist(request, article_id):
    #ทำงานกับตัวลิสต์
    readlist=ReadList.objects.get(readlist_id=readlist_id(request))
    #ทำงานกับตัวบทความที่จะลบ
    article=get_object_or_404(Article,id=article_id)
    readlistitem=ReadList_Item.objects.get(article=article,readlist=readlist)
    #ลบรายการสินค้า จากลิสต์ และบทความ ที่มีรหัสตรงกับข้างบน
    readlistitem.delete()
    return redirect('readlistdetail')


def readlistdetail(request):
    total=0
    readlist_items=None
    try:
        readlist = ReadList.objects.get(readlist_id=readlist_id(request))#ดึงตะกร้าสินค้า ที่อ้างอิงเลขไอดีฌซสชั่น
        readlist_items = ReadList_Item.objects.filter(readlist=readlist,active=True)#ดึงสินค้าในตะกร้านั้นๆ
        for item in readlist_items:
            total+=item.quantity
    except Exception as e :
        pass
    return render(request,'readlistdetail.html',{'readlist_items':readlist_items,'total':total})


def signupview(request):
    if request.method=='POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            #บันทึกข้อมูล User
            form.save()

            #ดึง username จากแบบฟอร์มมาใช้
            username=form.cleaned_data.get('username')
            #ดึงข้อมูล User จากฐานข้อมูล
            signupuser=User.objects.get(username=username)
            # บันทึกเข้ากลุ่ม readerwriter
            readwritegroup=Group.objects.get(name='readerwriter')
            readwritegroup.user_set.add(signupuser)

    else:
        form=SignupForm()

    return render(request,'signup.html',{'form':form})

def test(request):
    url = "https://aladhan.p.rapidapi.com/timingsByCity"

    querystring = {"city": "Tarim", "country": "Yemen"}

    headers = {
        'x-rapidapi-host': "aladhan.p.rapidapi.com",
        'x-rapidapi-key': "2544a08880mshd72d821fe59ae77p1e86ebjsnad28cedca983"
    }
    response = requests.request("GET", url, headers=headers, params=querystring).json()
    # pray_time={
    #     'city':querystring['address'],
    #     'time':response['data']['timings']
    # }
    print(response)

    return render(request, 'praytime.html')
