from django.forms import ModelForm, Textarea, EmailInput
from django.utils.translation import gettext_lazy as _

from .models import Feedback


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['email', 'title', 'comment']
        labels = {
            'email': _('Email'),
            'title': _('Тема'),
            'comment': _('Описание')
        }
        widgets = {
            'email': EmailInput(attrs={'class': 'form-control col-sm-12', 'placeholder': 'info@example.com'}),
            'title': EmailInput(attrs={'class': 'form-control col-sm-12', 'autocomplete': 'off'}),
            'comment': Textarea(attrs={'class': 'form-control col-sm-12'}, ),
        }
        help_texts = {
            'email': _('Мы никогда не будем делиться вашей электронной почтой с кем-либо еще.'),
            'comment': _('Напишите здесь свое сообщение.')
        }
