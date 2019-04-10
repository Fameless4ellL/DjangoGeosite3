from rest_framework import filters
from rest_framework.generics import ListAPIView

from Gsite.models import Post
from .serializer import PostSerializer


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all().order_by('title')
    serializer_class = PostSerializer
    paginate_by = 10
    lookup_fields = ('title', 'tags', 'text', 'infobox')
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'text', 'tags__name', 'Infobox__rock',  )