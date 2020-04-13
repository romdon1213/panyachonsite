from django.contrib import admin
from pagesite.models import Category,Article,city,ReadList,ReadList_Item
# Register your models here.
admin.site.register(Category)
admin.site.register(Article)
admin.site.register(ReadList)
admin.site.register(ReadList_Item)
admin.site.register(city)