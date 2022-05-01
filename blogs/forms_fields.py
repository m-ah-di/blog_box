from django import forms
from taggit.forms import TagWidget

from .models import Article

visibility_status = (
    ("private", "Only I can read this article"),
    ("public", "Anyone can read this article"),
)


class EditorForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['thumbnail_url', 'title', 'text', 'article_tags', 'visibility']
        labels = {'thumbnail_url': '',
                  'title': '',
                  'text': '',
                  'article_tags': '',
                  'visibility': ''
                  }
        help_texts = {
            'thumbnail_url': 'To use your image, upload the image to '
                             'any cloud and paste the link on this field.',
            'visibility': 'Choose visibility as you need.'
        }

        error_messages = {'text':
            {
                'required': 'Please write something and try posting again...',
            },
            'title':
                {
                    'required': 'Please add a title to differentiate it from other articles.'
                },
            'thumbnail_url':
                {
                    'invalid': 'Please enter a valid URL (with https://)'
                }
        }

        widgets = {
            'thumbnail_url': forms.URLInput(attrs={'type': "url",
                                                   'id': "typeURL",
                                                   'class': "form-control form-control-sm",
                                                   'placeholder': 'Featured Image URL '
                                                                  '(eg. https://eg.com/featured.jpg)'}),
            'title': forms.TextInput(attrs={'class': 'form-control form-control-lg',
                                            'placeholder': 'Title'}),
            'text': forms.Textarea,
            'article_tags': TagWidget(attrs={'class': 'form-control',
                                             'placeholder': 'Tags (eg. Tech, Mobile, iPhone)'}),
            'visibility': forms.Select(choices=visibility_status,
                                       attrs={
                                           'class': 'form-select form-select-lg'
                                       })
        }
