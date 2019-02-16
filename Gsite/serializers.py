from rest_framework.serializers import HyperlinkedModelSerializer

from Gsite.models import Post


class PostSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'text', 'tags', 'published_date')
