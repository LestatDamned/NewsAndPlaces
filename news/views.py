from rest_framework import viewsets

from .models import News
from .serializers import NewsSerializer


class NewsViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с новостями"""
    queryset = News.objects.all()
    serializer_class = NewsSerializer
