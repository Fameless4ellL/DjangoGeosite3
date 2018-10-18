import django_filters
from .models import Post, Tags
from django import forms


class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label="", )
    tags = django_filters.ModelMultipleChoiceFilter(label="Категории ", queryset=Tags.objects.all(),
                                                    widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Post
        fields = ['title', 'tags']