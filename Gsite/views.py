import random

from django.core.paginator import Paginator, InvalidPage, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template.context_processors import csrf
from django.utils import timezone
from haystack.forms import ModelSearchForm, HighlightedModelSearchForm, FacetedSearchForm
from haystack.query import SearchQuerySet, EmptySearchQuerySet
from haystack.views import RESULTS_PER_PAGE

from Gsite.form import FeedbackForm
from .filters import ProductFilter
from .models import Post, Tags


class SearchView(object):
    template = 'encyclopaedia.html'
    extra_context = {}
    query = ''
    results = EmptySearchQuerySet()
    request = None
    form = None
    results_per_page = RESULTS_PER_PAGE

    def __init__(self, template=None, load_all=True, form_class=None, searchqueryset=None, results_per_page=None):
        self.load_all = load_all
        self.form_class = form_class
        self.searchqueryset = searchqueryset

        if form_class is None:
            self.form_class = ModelSearchForm

        if not results_per_page is None:
            self.results_per_page = results_per_page

        if template:
            self.template = template

    def __call__(self, request):
        """
        Generates the actual response to the search.

        Relies on internal, overridable methods to construct the response.
        """
        self.request = request

        self.form = self.build_form()
        self.query = self.get_query()
        self.results = self.get_results()

        return self.create_response()

    def build_form(self, form_kwargs=None):
        """
        Instantiates the form the class should use to process the search query.
        """
        data = None
        kwargs = {
            'load_all': self.load_all,
        }
        if form_kwargs:
            kwargs.update(form_kwargs)

        if len(self.request.GET):
            data = self.request.GET

        if self.searchqueryset is not None:
            kwargs['searchqueryset'] = self.searchqueryset

        return self.form_class(data, **kwargs)

    def get_query(self):
        """
        Returns the query provided by the user.

        Returns an empty string if the query is invalid.
        """
        if self.form.is_valid():
            return self.form.cleaned_data['q']

        return ''

    def get_results(self):
        """
        Fetches the results via the form.

        Returns an empty list if there's no query to search with.
        """
        return self.form.search()

    def build_page(self):
        """
        Paginates the results appropriately.

        In case someone does not want to use Django's built-in pagination, it
        should be a simple matter to override this method to do what they would
        like.
        """
        try:
            page_no = int(self.request.GET.get('page', 1))
        except (TypeError, ValueError):
            raise Http404("Not a valid number for page.")

        if page_no < 1:
            raise Http404("Pages should be 1 or greater.")

        start_offset = (page_no - 1) * self.results_per_page
        self.results[start_offset:start_offset + self.results_per_page]

        paginator = Paginator(self.results, self.results_per_page)

        try:
            page = paginator.page(page_no)
        except InvalidPage:
            raise Http404("No such page!")

        return (paginator, page)

    def extra_context(self):
        """
        Allows the addition of more context variables as needed.

        Must return a dictionary.
        """
        return {}

    def get_context(self):
        (paginator, page) = self.build_page()

        context = {
            'query': self.query,
            'form': self.form,
            'page': page,
            'paginator': paginator,
            'suggestion': None,
        }

        if hasattr(self.results, 'query') and self.results.query.backend.include_spelling:
            context['suggestion'] = self.form.get_suggestion()

        context.update(self.extra_context())

        return context

    def create_response(self):
        """
        Generates the actual HttpResponse to send back to the user.
        """

        context = self.get_context()

        return render(self.request, self.template, context)


def search_view_factory(view_class=SearchView, *args, **kwargs):
    def search_view(request):
        return view_class(*args, **kwargs)(request)

    return search_view


class FacetedSearchView(SearchView):
    def __init__(self, *args, **kwargs):
        # Needed to switch out the default form class.
        if kwargs.get('form_class') is None:
            kwargs['form_class'] = FacetedSearchForm

        super(FacetedSearchView, self).__init__(*args, **kwargs)

    def build_form(self, form_kwargs=None):
        if form_kwargs is None:
            form_kwargs = {}

        # This way the form can always receive a list containing zero or more
        # facet expressions:
        form_kwargs['selected_facets'] = self.request.GET.getlist("selected_facets")

        return super(FacetedSearchView, self).build_form(form_kwargs)

    def extra_context(self):
        extra = super(FacetedSearchView, self).extra_context()
        extra['request'] = self.request
        extra['facets'] = self.results.facet_counts()
        return extra


def post_list(request, load_all=True, form_class=HighlightedModelSearchForm, searchqueryset=None, extra_context=None,
              results_per_page=None):
    global context
    num_post = Post.objects.all()
    tag = Tags.objects.all()
    updating = Post.objects.order_by("-created_date")[:5]  # обновленные посты
    count = Post.objects.all().count()
    slice = random.random() * (count)
    random_post = Post.objects.all()[slice: slice + 5]  # рандомные посты
    rand_ids = Post.objects.all().order_by('?')[:5]
    f = ProductFilter(request.GET, queryset=Post.objects.all())
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    # paginator = Paginator(f.qs, 16)  # Показывает 16 постов за стр

    # page = request.GET.get('page', 1)
    # try:
    #     queryset = paginator.page(page)
    # except PageNotAnInteger:
    #     queryset = paginator.page(1)
    # except EmptyPage:
    #     queryset = paginator.page(paginator.num_pages)
    query = ''
    results = SearchQuerySet().filter(published_date__lte=timezone.now()).order_by('published_date').exclude(
        content='thisshouldnotmatchanything')
    if request.GET.get('q'):
        form = form_class(request.GET, searchqueryset=searchqueryset, load_all=load_all)

        if form.is_valid():
            query = form.cleaned_data['q']
            results = form.search()
    else:
        form = form_class(searchqueryset=searchqueryset, load_all=load_all)

    paginator = Paginator(results, 16)

    try:
        page = request.GET.get('page', 1)
        try:
            query = paginator.page(page)
        except PageNotAnInteger:
            query = paginator.page(1)
        except EmptyPage:
            query = paginator.page(paginator.num_pages)
    except InvalidPage:
        raise Http404("No such page of results!")

    context = {
        'rand_ids': rand_ids,
        'num_post': num_post,
        'random_post': random_post,
        'updating': updating,
        'tag': tag,
        'form': form,
        'page': page,
        'paginator': paginator,
        'suggestion': None,
        'filter': f,
        'count': count,
        'posts': posts,
        "posts": query,
        "title": "List",
    }
    context.update(csrf(request))
    if results.query.backend.include_spelling:
        context['suggestion'] = form.get_suggestion()

    if extra_context:
        context.update(extra_context)
    return render(request, 'encyclopaedia.html', context)


def home(request):
    return render(request, 'base.html', {})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    mapVisible = post.place.all()

    context = {
        'mapVisible': mapVisible,
        'post': post,
    }
    return render(request, 'post_detail.html', context)


def post_by_tag(request, tag_slug):
    tags = Tags.objects.get(slug=tag_slug)
    posts = Post.objects.filter(tags__exact=tags)
    context = {
        'tag': tags,
        'posts': posts,
    }
    return render(request, 'post_by_category.html', context)


def Feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feed = form.save(commit=False)
            feed.created = timezone.now()
            feed.save()
            html = "<html><body><h1 style='text-align: center'>Сообщение отправлено.<h1><style>body {background: steelblue;}" \
                   ".wrapper {" \
                   "width: 100%;" \
                   "height: 100%;" \
                   "transform-style: preserve-3d;" \
                   "perspective: 1000px;" \
                   "perspective-origin: 50% 50%;" \
                   "margin: auto auto;" \
                   "animation: Scales linear 1.5s 1;" \
                   "transform-origin: 50% 100%;" \
                   "}" \
                   ".diamond-base {" \
                   "transform-style: preserve-3d;" \
                   "animation: Rotation linear 2s infinite;" \
                   "}" \
                   ".diamond {" \
                   "width: 200px;" \
                   "height: 200px;" \
                   "margin: auto auto;" \
                   "transform-style: preserve-3d;" \
                   "transform-origin: 50% 50%;" \
                   "transform: rotateX(90deg) rotateZ(90deg);" \
                   "}" \
                   ".diamond svg {" \
                   "width: 200px;" \
                   "height: 200px;" \
                   "position: absolute;" \
                   "}" \
                   ".diamond svg polygon {" \
                   "stroke: #fff;" \
                   "animation: ColorDuration linear 3s 1;" \
                   "fill: #D81B60;" \
                   "}" \
                   ".diamond svg.top {" \
                   "transform: translate(40px, 48px);" \
                   "backface-visibility: hidden;" \
                   "}" \
                   ".diamond .top-triangle {" \
                   "transform-style: preserve-3d;" \
                   "transform-origin: 100px 100px;" \
                   "position: absolute;" \
                   "backface-visibility: hidden;" \
                   "}" \
                   ".diamond .top-triangle svg {" \
                   "transform: rotateX(-45deg);" \
                   "transform-origin: 50% 0%;" \
                   "}" \
                   ".diamond .top-triangle-1 {" \
                   "transform: rotateZ(0deg) translate(70px, 152px);" \
                   "}" \
                   ".diamond .top-triangle-2 {" \
                   "transform: rotateZ(60deg) translate(70px, 152px);" \
                   "}" \
                   ".diamond .top-triangle-3 {" \
                   "transform: rotateZ(120deg) translate(70px, 152px);" \
                   "}" \
                   ".diamond .top-triangle-4 {" \
                   "transform: rotateZ(180deg) translate(70px, 152px);" \
                   "}" \
                   ".diamond .top-triangle-5 {" \
                   "transform: rotateZ(240deg) translate(70px, 152px);" \
                   "}" \
                   ".diamond .top-triangle-6 {transform: rotateZ(300deg) translate(70px, 152px);" \
                   "}" \
                   ".diamond .lower-part {" \
                   "transform-style: preserve-3d;" \
                   "transform-origin: 100px 100px;" \
                   "position: absolute;" \
                   "backface-visibility: hidden;" \
                   "}" \
                   ".diamond .lower-part .triangles {" \
                   "transform-style: preserve-3d;" \
                   "transform: rotateZ(-30deg) translate3d(-14px, 51px, -48px);" \
                   "transform-origin: 50% 50%;" \
                   "position: absolute;" \
                   "}" \
                   ".diamond .lower-part .triangles .up-triangle, .diamond .lower-part .triangles .down-triangle {" \
                   "transform-origin: 0% 0%;position: absolute;" \
                   "}" \
                   ".diamond .lower-part .triangles .up-triangle {" \
                   "transform: rotateX(61.03deg);" \
                   "}" \
                   ".diamond .lower-part .triangles .down-triangle {" \
                   "transform: rotateX(-45deg);" \
                   "}" \
                   ".diamond .lower-part-1 {" \
                   "transform: rotateZ(0deg);" \
                   "}" \
                   ".diamond .lower-part-2 {" \
                   "transform: rotateZ(60deg);" \
                   "}" \
                   ".diamond .lower-part-3 {" \
                   "transform: rotateZ(120deg);" \
                   "}" \
                   ".diamond .lower-part-4 {" \
                   "transform: rotateZ(180deg);" \
                   "}" \
                   ".diamond .lower-part-5 {" \
                   "transform: rotateZ(240deg);" \
                   "}" \
                   ".diamond .lower-part-6 {" \
                   "transform: rotateZ(300deg);" \
                   "}" \
                   "@keyframes Rotation {" \
                   "0% {" \
                   "transform: rotateY(0deg);" \
                   "}" \
                   "50% {" \
                   "transform: rotateY(120deg);" \
                   "}" \
                   "100% {" \
                   "transform: rotateY(240deg);" \
                   "}" \
                   "}" \
                   "@keyframes Scales {" \
                   "0% {" \
                   "transform: scale(0);" \
                   "}" \
                   "50% {" \
                   "transform: scale(0.5);" \
                   "}" \
                   "95% {" \
                   "transform: scale(1.1);" \
                   "}" \
                   "100% {" \
                   "transform: scale(1);" \
                   "}" \
                   "}" \
                   "@keyframes ColorDuration{" \
                   "0%{" \
                   "fill: #b54183;" \
                   "}" \
                   "33%{" \
                   "fill: #ff4ac2;" \
                   "}" \
                   "66%{" \
                   "fill: #dd57aa;" \
                   "}" \
                   "100%{" \
                   "fill: #e966c1;" \
                   "}" \
                   "}" \
                   "</style><div class='wrapper'><div class='diamond-base'><div class='diamond'><svg class='top' viewBox='0 0 200 200'><polygon points='30,0 90,0 120,51.96 90,103.92 30,103.92, 0,51.96'></polygon></svg><div class='top-triangle top-triangle-1'><svg class='' viewBox='0 0 200 200'><polygon points='0,0 60,0 30,67.92'></polygon></svg></div><div class='top-triangle top-triangle-2'><svg class='' viewBox='0 0 200 200'><polygon points='0,0 60,0 30,67.92'></polygon></svg></div><div class='top-triangle top-triangle-3'><svg class='' viewBox='0 0 200 200'><polygon points='0,0 60,0 30,67.92'></polygon></svg></div><div class='top-triangle top-triangle-4'><svg class='' viewBox='0 0 200 200'><polygon points='0,0 60,0 30,67.92'></polygon></svg></div><div class='top-triangle top-triangle-5'><svg class='' viewBox='0 0 200 200'><polygon points='0,0 60,0 30,67.92'></polygon></svg></div><div class='top-triangle top-triangle-6'><svg class='' viewBox='0 0 200 200'><polygon points='0,0 60,0 30,67.92'></polygon></svg></div><div class='lower-part lower-part-1'><div class='triangles'><svg class='up-triangle'><polygon points='0,0 100,0 50,54.91'></polygon></svg><svg class='down-triangle'><polygon points='0,0 100,0 50,120'></polygon></svg></div></div><div class='lower-part lower-part-2'><div class='triangles'><svg class='up-triangl'><polygon points='0,0 100,0 50,54.91'></polygon></svg><svg class='down-triangle'><polygon points='0,0 100,0 50,120'></polygon></svg></div></div><div class='lower-part lower-part-3'><div class='triangles'><svg class='up-triangle'><polygon points='0,0 100,0 50,54.91'></polygon></svg><svg class='down-triangle'><polygon points='0,0 100,0 50,120'></polygon></svg></div></div><div class='lower-part lower-part-4'><div class='triangles'><svg class='up-triangle'><polygon points='0,0 100,0 50,54.91'></polygon></svg><svg class='down-triangle'><polygon points='0,0 100,0 50,120'></polygon></svg></div></div><div class='lower-part lower-part-5'><div class='triangles'><svg class='up-triangle'><polygon points='0,0 100,0 50,54.91'></polygon></svg><svg class='down-triangle'><polygon points='0,0 100,0 50,120'></polygon></svg></div></div><div class='lower-part lower-part-6'><div class='triangles'><svg class='up-triangle'><polygon points='0,0 100,0 50,54.91'></polygon></svg><svg class='down-triangle'><polygon points='0,0 100,0 50,120'></polygon></svg></div></div></div></div></div></body></html>"
            return HttpResponse(html)

    else:
        form = FeedbackForm()
    return render(request, 'Feedback.html', {'form': form})


def post(request, post_id=id):

    item = get_object_or_404(Post, id=post_id)

    return render(request,'Post.html', {'post': item})