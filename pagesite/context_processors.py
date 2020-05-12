from pagesite.models import Category, CategoryPost,CategoryMasalah,Article,Post,Masalah
import requests
from django.shortcuts import render

def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)


def menu_links_post(request):
    linkspost = CategoryPost.objects.all()
    return dict(linkspost=linkspost)

def menu_links_masalah(request):
    linksmasalah = CategoryMasalah.objects.all()
    return dict(linksmasalah=linksmasalah)

def blockpraytime(request):
    url = "https://aladhan.p.rapidapi.com/timingsByCity"
    city = ("Bangkok", "Narathiwat","Chiangrai","Khonkaen")
    headers = {
        'x-rapidapi-host': "aladhan.p.rapidapi.com",
        'x-rapidapi-key': "2544a08880mshd72d821fe59ae77p1e86ebjsnad28cedca983"
    }
    querystring = [{"city": i, "country": "thailand", "method": "1"} for i in city]
    response = [requests.request("GET", url, headers=headers, params=i).json() for i in querystring]
    block_praytime_non = {
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
        'block_praytime_non': block_praytime_non,
    }
    return context

def blockarticle(request):
    article = Article.objects.all().filter(available=True)
    article = article.order_by('?')[:3]
    context = {
        'articleblock': article,
    }
    return context

def blockpost(request):
    post = Post.objects.all().filter(status='published')
    post = post.order_by('?')[:3]
    context = {
        'postblock': post,
    }
    return context

def blockmasalah(request):
    masalah = Masalah.objects.all().filter(answered=True)
    masalah = masalah.order_by('?')[:3]
    context = {
        'masalahblock': masalah,
    }
    return context
# def readlistcount(request):
#     itemcount_article = 0
#     itemcount_post = 0
#     total_itemcount = 0
#
#     if 'admin' in request.path:
#         return {}
#     else:
#         try:
#             # query readlist
#             readlist = ReadList.objects.filter(readlist_id=readlist_id(request))  # ดึงตัวลิสต์มา
#             # query readlist item
#             readlistitem_article = ReadList_Item.objects.all().filter(readlist=readlist[:1])
#             for item in readlistitem_article:
#                 itemcount_article += item.quantity
#         except ReadList.DoesNotExist:
#             itemcount_article = 0
#
#         try:
#             # query readlist
#             readlist = ReadList.objects.filter(readlist_id=readlist_id(request))  # ดึงตัวลิสต์มา
#             # query readlist item
#             readlistitem_post = ReadList_Item_Post.objects.all().filter(readlist=readlist[:1])
#             for item in readlistitem_post:
#                 itemcount_post += item.quantity
#         except ReadList.DoesNotExist:
#             itemcount_post = 0
#
#     total_itemcount = itemcount_article + itemcount_post
#     return dict(itemcount_article=itemcount_article, itemcount_post=itemcount_post, total_itemcount=total_itemcount)
