import django_filters
from django import forms

from .models import Post, Tags


class ProductFilter(django_filters.FilterSet, ):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label="")
    tags = django_filters.ModelMultipleChoiceFilter(label="Категории ", queryset=Tags.objects.all(),
                                                    widget=forms.CheckboxSelectMultiple())
    text = django_filters.CharFilter(field_name='text', lookup_expr='icontains', label="Ключевое слово")
    published_date = django_filters.DateTimeFilter(field_name="published_date", label="Дата публикации статьи")

    class Meta:
        model = Post
        fields = ['title', 'tags', 'text', 'published_date']
