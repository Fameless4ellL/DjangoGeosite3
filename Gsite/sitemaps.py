from django.contrib.sitemaps import Sitemap

from Gsite.models import Post


class PostSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def lastmod(self, obj):
        return obj.published_date

    def items(self):
        return Post.objects.all()