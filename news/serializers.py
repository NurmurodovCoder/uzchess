from rest_framework import serializers
from .models import News


class NewsSerializers(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = [
            'id',
            'title',
            'short_title',
            'text',
            'img',
            'view_count',
            'create_at',
            'upload_to'
        ]
