from rest_framework.generics import ListAPIView

from Gsite.models import Post
from .serializer import PostSerializer


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all().order_by('title')
    serializer_class = PostSerializer
