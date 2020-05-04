from pagesite.models import Category, CategoryPost,CategoryMasalah



def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)


def menu_links_post(request):
    linkspost = CategoryPost.objects.all()
    return dict(linkspost=linkspost)

def menu_links_masalah(request):
    linksmasalah = CategoryMasalah.objects.all()
    return dict(linksmasalah=linksmasalah)

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
