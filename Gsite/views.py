from django.contrib.admin.templatetags.admin_list import pagination
import random
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Tags
from random import sample
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .filters import ProductFilter
from .form import FeedbackForm

# Create your views here.
def post_list(request):
    global context
    num_post = Post.objects.all()
    tag = Tags.objects.all()
    updating = Post.objects.order_by("-created_date")[:5] # обновленные посты
    count = Post.objects.all().count()
    slice = random.random() * (count )
    random_post = Post.objects.all()[slice: slice + 5] # рандомные посты
    rand_ids = Post.objects.all().order_by('?')[:5]
    f = ProductFilter(request.GET, queryset=Post.objects.all())
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    paginator = Paginator(f.qs, 16)  # Показывает 16 постов за стр

    page = request.GET.get('page', 1)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
            'rand_ids':rand_ids,
            'num_post':num_post,
            'random_post':random_post,
            'updating':updating,
            'tag': tag,
            'filter': f,
            'count': count,
            'posts': posts,
            "posts": queryset,
            "title":"List",
        }
    return  render(request, 'encyclopaedia.html', context)

def home(request):
    return render(request, 'base.html', {})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})

def post_by_tag(request, tag_slug):
    tags = Tags.objects.get(slug=tag_slug)
    posts = Post.objects.filter(tags__exact=tags)
    context = {
        'tag': tags,
        'posts': posts
    }
    return render(request, 'post_by_category.html', context )

def Feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feed = form.save(commit=False)
            feed.created = timezone.now()
            feed.save()
    else:
        form = FeedbackForm()
    return render(request, 'Feedback.html', {'form': form})