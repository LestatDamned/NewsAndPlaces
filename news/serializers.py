from rest_framework import serializers

from .models import News


class NewsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели новостей"""
    class Meta:
        model = News
        fields = ['id', 'title', 'main_image', 'preview_image', 'text', 'publication_date']
        read_only_fields = ['preview_image', 'publication_date']