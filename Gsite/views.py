import random
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Tags
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