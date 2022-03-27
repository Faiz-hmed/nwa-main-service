from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
import datetime

from .models import Article, Article_Images
from .serializers import ArticleSerializer
# Create your views here.

class ArticleViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    date_criteria = datetime.date.today()-datetime.timedelta(days=7)

    queryset = Article.objects.filter(time_written__gte=date_criteria).prefetch_related('images')
    serializer_class = ArticleSerializer