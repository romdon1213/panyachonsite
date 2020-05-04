from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.utils.text import slugify



# Create your models here.
#masalah
class CategoryMasalah(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'หมวดหมู่ masalah'
        verbose_name_plural = 'ประเภท masalah'
    #
    def get_url(self):
        return reverse('masalah_by_category', args=[self.slug])

class Masalah(models.Model):
    objects = None
    question = models.TextField(max_length=1000, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    answer = RichTextField(config_name='default', blank=True)
    category = models.ForeignKey(CategoryMasalah, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    view = models.PositiveIntegerField(default=0)
    likes=models.ManyToManyField(User,related_name='likes_masalah',blank=True)
    comment = 0

    def __str__(self):
        return self.question

    class Meta:
        ordering = ('question',)
        verbose_name = 'masalah'
        verbose_name_plural = 'เนื้อหา masalah'
    #
    def get_url(self):
        return reverse('masalah_detail', args=[self.category.slug, self.slug])
    #
    def total_likes(self):
        return self.likes.count()
    #
    def get_num_comment(self):
        return CommentMasalah.objects.filter(masalah=self).count()

class CommentMasalah(models.Model):
    masalah=models.ForeignKey(Masalah,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    reply = models.ForeignKey('CommentMasalah', null=True, related_name='replies', on_delete=models.CASCADE)
    content=RichTextField(config_name='awesome', blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.masalah.question, str(self.user.username))

#endmasalah

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
    description = RichTextField(config_name='default', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="articlepic", blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    view = models.PositiveIntegerField(default=0)
    likes=models.ManyToManyField(User,related_name='likes_article',blank=True)
    comment = 0

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'บทความ'
        verbose_name_plural = 'เนื้อหาบทความ'

    def get_url(self):
        return reverse('article_detail', args=[self.category.slug, self.slug])
    def total_likes(self):
        return self.likes.count()

    def get_num_comment(self):
        return CommentArticle.objects.filter(article=self).count()

class CommentArticle(models.Model):
    article=models.ForeignKey(Article,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    reply = models.ForeignKey('CommentArticle', null=True, related_name='replies', on_delete=models.CASCADE)
    content=RichTextField(config_name='awesome', blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.article.name, str(self.user.username))

class CategoryPost(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    def get_url(self):
        return reverse('post_by_category', args=[self.slug])


class Post(models.Model):
    STATUS_CHOICES=(
        ('dratf','สร้างดราฟต์'),
        ('published','เผยแพร่')
    )
    title=models.CharField(max_length=300)
    slug=models.SlugField(max_length=120,allow_unicode=True)
    author=models.ForeignKey(User,related_name='blog_post',on_delete=models.CASCADE)
    body=RichTextField(config_name='awesome', blank=True)
    likes=models.ManyToManyField(User,related_name='likes_post',blank=True)
    # savelist=models.ManyToManyField(User,related_name='save_post',blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    category = models.ForeignKey(CategoryPost, on_delete=models.CASCADE)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='published')
    view = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.title)
            if not self.slug:
                self.slug = thai_slugify(self.title) + "-" + str(self.id)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def get_url(self):
        return reverse('blog_detail', args=[self.category.slug, self.slug])


def thai_slugify(str):
    str = str.replace(" ", "-")
    str = str.replace(",", "-")
    str = str.replace("(", "-")
    str = str.replace(")", "")
    str = str.replace("؟", "")
    return str

class CommentPost(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    reply = models.ForeignKey('CommentPost', null=True, related_name='replies', on_delete=models.CASCADE)
    content=RichTextField(config_name='awesome', blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.post.title, str(self.user.username))


# @receiver(pre_save,sender=Post)
# def pre_save_slug(sender,**kwargs):
#     slug=slugify(kwargs['instance'].title)
#     kwargs['instance'].slug=slug

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    dob=models.DateField(null=True,blank=True)
    photo=models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.user.username
    def get_url(self):
        return reverse('blog_each_user', args=[self.user.id])

class city(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'เมือง'

