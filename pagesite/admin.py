from django.contrib import admin
from pagesite.models import Category,Article,city,CategoryPost,Post,Profile,CommentPost,CommentArticle,CategoryMasalah,Masalah,CommentMasalah
# egister your models here.
admin.site.register(Category)
admin.site.register(city)
admin.site.register(CategoryPost)

class MasalahAdmin(admin.ModelAdmin):
    list_display = ('question','slug','category','updated','view')
    list_editable=('category',)
admin.site.register(Masalah,MasalahAdmin)
admin.site.register(CommentMasalah)
admin.site.register(CategoryMasalah)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name','slug','category','updated','view')
    list_editable=('category',)
admin.site.register(Article,ArticleAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug','author','status')
    list_filter = ('status','created','updated')
    search_fields = ('author__username','title')
    prepopulated_fields = {'slug':('title',)}
    list_editable = ('status',)
    date_hierarchy = ('created')

admin.site.register(Post,PostAdmin)
admin.site.register(CommentArticle)
admin.site.register(CommentPost)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','dob','photo')
admin.site.register(Profile,ProfileAdmin)
