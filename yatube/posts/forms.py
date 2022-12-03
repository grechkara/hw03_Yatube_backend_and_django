from django.forms import ModelForm
from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        help_text = {'text': 'Текст поста',
                     'group': 'Группа'
                     }
        text_muted = {'text': 'Текст нового поста',
                      'group': 'Группа, к которой будет относиться пост'
                      }
