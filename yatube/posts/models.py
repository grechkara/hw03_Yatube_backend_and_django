from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts'
    )
# # Post.objects.filter(author=me)

# start_date = datetime.date(1890, 1, 1)
# end_date = datetime.date(1895, 3, 31)
# Post.objects.filter(text__contains='oops')
# .filter(pub_date__range=(start_date, end_date))

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-pub_date']
