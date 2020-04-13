from pagesite.models import Category, ReadList, ReadList_Item
from pagesite.views import readlist_id


def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)


def readlistcount(request):
    itemcount = 0

    if 'admin' in request.path:
        return {}
    else:
        try:
            # query readlist
            readlist = ReadList.objects.filter(readlist_id=readlist_id(request))  # ดึงตัวลิสต์มา
            # query readlist item
            readlistitem = ReadList_Item.objects.all().filter(readlist=readlist[:1])
            for item in readlistitem:
                itemcount += item.quantity
        except ReadList.DoesNotExist:
            itemcount = 0
    return dict(itemcount=itemcount)
