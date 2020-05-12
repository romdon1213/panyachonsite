import django_filters
from pagesite.models import Article, Category,CategoryMasalah,Post,CategoryPost,Masalah


class ArticleFilters(django_filters.FilterSet):
    CHOICES = (
        ('view', 'ความนิยม'),
        ('newest', 'ล่าสุด'),
        ('lastest', 'เก่าสุด'),
        ('name', 'ชื่อบทความ'),
    )
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),label='หมวดหมู่บทความ'
    )
    ordering = django_filters.ChoiceFilter(label='เรียงตาม', choices=CHOICES, method='filter_by_order')

    class Meta:
        model = Article
        fields = ('category',)

    def filter_by_order(self, queryset, name, value):
        if value == 'view':
            expression = '-view'
        if value == 'lastest':
            expression = 'updated'
        if value == 'newest':
            expression = '-updated'
        if value == 'name':
            expression = 'name'
        return queryset.order_by(expression)

class MasalahFilters(django_filters.FilterSet):
    CHOICES = (
        ('view', 'ความนิยม'),
        ('newest', 'ล่าสุด'),
        ('lastest', 'เก่าสุด'),
        ('name', 'ชื่อบทความ'),
    )
    category = django_filters.ModelChoiceFilter(
        queryset=CategoryMasalah.objects.all(),label='หมวดหมู่มัสอะละห์'
    )
    ordering = django_filters.ChoiceFilter(label='เรียงตาม', choices=CHOICES, method='filter_by_order')

    class Meta:
        model = Masalah
        fields = ('category',)

    def filter_by_order(self, queryset, name, value):
        if value == 'view':
            expression = '-view'
        if value == 'lastest':
            expression = 'updated'
        if value == 'newest':
            expression = '-updated'
        if value == 'name':
            expression = 'name'
        return queryset.order_by(expression)

class PostFilters(django_filters.FilterSet):
    CHOICES = (
        ('view', 'ความนิยม'),
        ('newest', 'ล่าสุด'),
        ('lastest', 'เก่าสุด'),
        ('name', 'ชื่อบทความ'),
    )
    category = django_filters.ModelChoiceFilter(
        queryset=CategoryPost.objects.all(),label='หมวดหมู่โพสต์'
    )
    ordering = django_filters.ChoiceFilter(label='เรียงตาม', choices=CHOICES, method='filter_by_order')

    class Meta:
        model = Post
        fields = ('category',)

    def filter_by_order(self, queryset, name, value):
        if value == 'view':
            expression = '-view'
        if value == 'lastest':
            expression = 'updated'
        if value == 'newest':
            expression = '-updated'
        if value == 'name':
            expression = 'name'
        return queryset.order_by(expression)