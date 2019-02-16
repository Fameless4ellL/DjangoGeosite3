from django.conf.urls import url
from django.urls import include

from Gsite.views import FacetedSearchView
from . import views


urlpatterns = [
    url(r'^$', views.post_list, name='encyclopaedia'),
    url(r'^tag/(?P<tag_slug>[\w-]+)/$', views.post_by_tag, name='post_by_tag'),
    url(r'^$', views.home, name='home'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^feedback/$', views.Feedback, name='Feedback'),
    url(r'^', include('haystack.urls')),
]