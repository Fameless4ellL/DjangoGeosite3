from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.six import text_type


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


STREAK_CHOICES = (
    ('Белый', 'Белый'),
    ('Черный', 'Черный'),
)


class InfoAboutRock(models.Model):
    rock = models.CharField(verbose_name=u'Порода или минерал', max_length=200, help_text="Enter a rock ", blank=True)
    hardness = models.IntegerRangeField(verbose_name=u'Твердость', min_value=0, max_value=10, null=True, blank=True)
    color = models.CharField(verbose_name=u'Цвет', max_length=50, null=True, blank=True)
    formula = models.TextField(verbose_name=u"Формула", null=True, blank=True, )
    category = models.CharField(verbose_name=u'Категория', max_length=40, null=True, blank=True)
    Streak = models.CharField(verbose_name=u'полоса, жилка', choices=STREAK_CHOICES, max_length=30, null=True,
                              blank=True)
    Opacity = models.CharField(verbose_name=u'Прозрачность', max_length=50, null=True, blank=True)
    Lustre = models.CharField(verbose_name=u'Блеск', max_length=50, null=True, blank=True)
    SpecificGravity = models.IntegerRangeField(verbose_name=u'Удельный вес', min_value=0, max_value=100, null=True,
                                               blank=True)
    Cleavage = models.CharField(verbose_name=u'Спайность', max_length=50, null=True, blank=True)
    Fracture = models.CharField(verbose_name=u'Трещиноватость', max_length=50, null=True, blank=True)
    CristalSystem = models.CharField(verbose_name=u'Кристаллография', max_length=50, null=True, blank=True)

    def __str__(self):
        return self.rock

    def __get_label(self, field):
        return text_type(self._meta.get_field(field).verbose_name)

    @property
    def name_label(self):
        return self.__get_label('formula')

    @property
    def category_label(self):
        return self.__get_label('category')

    @property
    def Streak_label(self):
        return self.__get_label('Streak')

    @property
    def Opacity_label(self):
        return self.__get_label('Opacity')

    @property
    def Lustre_label(self):
        return self.__get_label('Lustre')

    @property
    def SpecificGravity_label(self):
        return self.__get_label('SpecificGravity')

    @property
    def Cleavage_label(self):
        return self.__get_label('Cleavage')

    @property
    def Fracture_label(self):
        return self.__get_label('Fracture')

    @property
    def CristalSystem_label(self):
        return self.__get_label('CristalSystem')

    @property
    def hardness_label(self):
        return self.__get_label('hardness')

    @property
    def color_label(self):
        return self.__get_label('color')

    class Meta:
        ordering = ('rock',)  # сортировка по алфавиту


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField('Заголовок', max_length=200)
    text = models.TextField()
    thumb = models.ImageField(upload_to='post_image', blank=True, null=True)
    Infobox = models.ManyToManyField(InfoAboutRock, help_text="заполнение формы для пород и минералов", blank=True)
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
    email = models.EmailField(max_length=254, blank=True, null=True, )
    title = models.CharField(('Тема'), max_length=200)
    comment = models.TextField(('Описание'))
    created = models.DateTimeField(('Creation date'), auto_now_add=True)
