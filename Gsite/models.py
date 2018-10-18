from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Tags(models.Model):
    name = models.CharField(max_length=200,
                            help_text="Enter a tag ")
    slug = models.SlugField(max_length=100, unique=True)

    def get_absolute_url(self):
        return reverse('post_by_category', args=[self.slug])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)  # сортировка по алфавиту


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    thumb = models.FileField(upload_to='post_image', blank=True, null=True)
    tags = models.ManyToManyField(Tags, help_text="Select a tag for this post")
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)


class Feedback(models.Model):
    email = models.EmailField(max_length=254, blank=True, null=True)
    title = models.CharField(('Тема'), max_length=200)
    comment = models.TextField(('Описание'))
    created = models.DateTimeField(('Creation date'), auto_now_add=True)