from rest_framework import serializers

from Gsite.models import Post, Tags, InfoAboutRock


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = [
            'name',
            'slug',
        ]

class InfoAboutRockSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoAboutRock
        fields = [
            'rock',
            'hardness',
            'color',
            'formula',
            'category',
            'Streak',
            'Opacity',
            'Lustre',
            'SpecificGravity',
            'Cleavage',
            'Fracture',
            'CristalSystem',
        ]

class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    Infobox = InfoAboutRockSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'tags',
            'published_date',
            'thumb',
            'Infobox'
        ]
