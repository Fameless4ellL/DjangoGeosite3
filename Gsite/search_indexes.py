from haystack import indexes

from Gsite.models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    tags = indexes.MultiValueField()
    infobox = indexes.MultiValueField()
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr="title")
    published_date = indexes.DateTimeField(model_attr='published_date')
    author = indexes.CharField(model_attr='author')

    def get_model(self):
        return Post

    def prepare_tags(self, object):
        return [Tags.name for Tags in object.tags.all()]

    # def prepare_infobox(self, object):
    #     return [Tags.name for Tags in object.tags.all()]

    def index_queryset(self, using=None):
        """используется когда весь индекс модели обновлен"""
        return self.get_model().objects.all()
