from rest_framework import serializers

from Gsite.models import Post, Tags


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = [
            'name',
            'slug',
        ]


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'tags',
            'published_date',
        ]
