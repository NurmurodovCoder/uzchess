from django.db import models


class News(models.Model):
    title = models.CharField(max_length=255)
    short_title = models.CharField(max_length=255)
    text = models.TextField()  # RichTexField
    img = models.ImageField(upload_to='news/')

    view_count = models.IntegerField(default=0)

    create_at = models.DateTimeField(auto_now_add=True)
    upload_to = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
