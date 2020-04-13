from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'หมวดหมู่บทความ'
        verbose_name_plural = 'ประเภทบทความ'

    def get_url(self):
        return reverse('article_by_category', args=[self.slug])


class Article(models.Model):
    objects = None
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = RichTextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="articlepic", blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    view = models.PositiveIntegerField(default=0)
    like = 0
    comment = 0

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'บทความ'
        verbose_name_plural = 'เนื้อหาบทความ'

    def get_url(self):
        return reverse('article_detail', args=[self.category.slug, self.slug])


class ReadList(models.Model):
    objects = None
    DoesNotExist = None
    readlist_id = models.CharField(max_length=255, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.readlist_id

    class Meta:
        db_table = 'readlist'
        ordering = ('date_added',)
        verbose_name_plural = 'กล่อง readlist'


class ReadList_Item(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    readlist = models.ForeignKey(ReadList, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'บทความในคลัง'
        ordering = ('article',)
        verbose_name_plural = 'บทความในกล่อง readlist'

    def sub_total(self):
        return self.quantity

    def __str__(self):
        return self.article.name


class city(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'เมือง'
